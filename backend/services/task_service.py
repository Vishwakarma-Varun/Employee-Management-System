from sqlalchemy.orm import Session
from sqlalchemy import or_
from fastapi import HTTPException
from models.task import Task
from models.employee import Employee
from schemas.task import TaskCreate, TaskUpdate, PaginatedTasks, TaskResponse
import math

def get_tasks(db: Session, page: int = 1, per_page: int = 10, search: str = None, status: str = None, employee_id: int = None):
    query = db.query(Task)
    
    if search:
        query = query.filter(
            or_(
                Task.title.ilike(f"%{search}%"),
                Task.description.ilike(f"%{search}%")
            )
        )
    if status:
        query = query.filter(Task.status == status)
    if employee_id:
        query = query.filter(Task.employee_id == employee_id)

    total = query.count()
    if total == 0:
        return PaginatedTasks(total=0, page=page, per_page=per_page, total_pages=0, tasks=[])

    total_pages = math.ceil(total / per_page)
    offset = (page - 1) * per_page
    tasks = query.order_by(Task.created_at.desc()).offset(offset).limit(per_page).all()

    return PaginatedTasks(
        total=total,
        page=page,
        per_page=per_page,
        total_pages=total_pages,
        tasks=tasks
    )

def create_task(db: Session, task_data: TaskCreate):
    employee = db.query(Employee).filter(Employee.id == task_data.employee_id).first()
    if not employee:
        raise HTTPException(status_code=404, detail="Employee not found")

    new_task = Task(**task_data.model_dump())
    db.add(new_task)
    db.commit()
    db.refresh(new_task)
    return new_task

def get_task(db: Session, task_id: int):
    task = db.query(Task).filter(Task.id == task_id).first()
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    return task

def update_task(db: Session, task_id: int, task_data: TaskUpdate):
    task = get_task(db, task_id)

    if task_data.employee_id is not None:
        employee = db.query(Employee).filter(Employee.id == task_data.employee_id).first()
        if not employee:
            raise HTTPException(status_code=404, detail="Employee not found")

    update_data = task_data.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(task, key, value)

    db.commit()
    db.refresh(task)
    return task

def delete_task(db: Session, task_id: int):
    task = get_task(db, task_id)
    db.delete(task)
    db.commit()
    return {"message": "Task deleted successfully"}
