from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from typing import Optional

from database.db import get_db
from schemas.task import TaskCreate, TaskUpdate, TaskResponse, PaginatedTasks
from services.task_service import create_task, get_task, get_tasks, update_task, delete_task
from core.security import get_current_user, require_roles

router = APIRouter(prefix="/api/tasks", tags=["Tasks"])

@router.get("", response_model=PaginatedTasks)
def list_tasks(
    page: int = Query(1, ge=1),
    per_page: int = Query(10, ge=1, le=100),
    search: Optional[str] = Query(None),
    status: Optional[str] = Query(None),
    employee_id: Optional[int] = Query(None),
    db: Session = Depends(get_db),
    _=Depends(get_current_user),
):
    return get_tasks(db, page=page, per_page=per_page, search=search, status=status, employee_id=employee_id)

@router.post("", response_model=TaskResponse, status_code=201)
def create(data: TaskCreate, db: Session = Depends(get_db), _=Depends(get_current_user)):
    return create_task(db, data)

@router.get("/{task_id}", response_model=TaskResponse)
def get_one(task_id: int, db: Session = Depends(get_db), _=Depends(get_current_user)):
    return get_task(db, task_id)

@router.put("/{task_id}", response_model=TaskResponse)
def update(task_id: int, data: TaskUpdate, db: Session = Depends(get_db), _=Depends(get_current_user)):
    return update_task(db, task_id, data)

@router.delete("/{task_id}")
def delete(task_id: int, db: Session = Depends(get_db), _=Depends(require_roles("admin"))):
    return delete_task(db, task_id)
