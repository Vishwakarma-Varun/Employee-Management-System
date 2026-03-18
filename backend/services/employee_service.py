from sqlalchemy.orm import Session
from sqlalchemy import func, or_
from fastapi import HTTPException
from typing import Optional
import math

from models.employee import Employee
from schemas.employee import EmployeeCreate, EmployeeUpdate, PaginatedEmployees, DashboardStats


def _generate_employee_id(db: Session) -> str:
    count = db.query(func.count(Employee.id)).scalar()
    return f"EMP{str(count + 1).zfill(4)}"


def create_employee(db: Session, data: EmployeeCreate) -> Employee:
    if db.query(Employee).filter(Employee.email == data.email).first():
        raise HTTPException(status_code=400, detail="Employee with this email already exists")
    employee = Employee(**data.model_dump(), employee_id=_generate_employee_id(db))
    db.add(employee)
    db.commit()
    db.refresh(employee)
    return employee


def get_employee(db: Session, employee_id: int) -> Employee:
    employee = db.query(Employee).filter(Employee.id == employee_id).first()
    if not employee:
        raise HTTPException(status_code=404, detail=f"Employee with id {employee_id} not found")
    return employee


def get_employees(db, page=1, per_page=10, search=None, department=None):
    query = db.query(Employee)
    if department:
        query = query.filter(Employee.department == department)
    if search:
        term = f"%{search}%"
        query = query.filter(or_(
            Employee.full_name.ilike(term),
            Employee.department.ilike(term),
            Employee.designation.ilike(term)
        ))
    total = query.count()
    total_pages = math.ceil(total / per_page) if total > 0 else 1
    employees = query.offset((page - 1) * per_page).limit(per_page).all()
    return PaginatedEmployees(total=total, page=page, per_page=per_page, total_pages=total_pages, employees=employees)


def update_employee(db: Session, employee_id: int, data: EmployeeUpdate) -> Employee:
    employee = get_employee(db, employee_id)
    if data.email and data.email != employee.email:
        if db.query(Employee).filter(Employee.email == data.email).first():
            raise HTTPException(status_code=400, detail="Email already in use")
    for field, value in data.model_dump(exclude_unset=True).items():
        setattr(employee, field, value)
    db.commit()
    db.refresh(employee)
    return employee


def delete_employee(db: Session, employee_id: int):
    employee = get_employee(db, employee_id)
    db.delete(employee)
    db.commit()
    return {"message": f"Employee {employee.employee_id} deleted successfully"}


def get_dashboard_stats(db: Session):
    total = db.query(func.count(Employee.id)).scalar()
    avg_salary = db.query(func.avg(Employee.salary)).scalar() or 0.0
    dept_rows = db.query(Employee.department, func.count(Employee.id)).group_by(Employee.department).all()
    dept_dist = {dept: count for dept, count in dept_rows}
    top_performers = db.query(Employee).order_by(Employee.performance_score.desc()).limit(5).all()
    low_performers = db.query(Employee).filter(Employee.performance_score < 5.0).order_by(Employee.performance_score.asc()).limit(10).all()
    return DashboardStats(
        total_employees=total,
        avg_salary=round(avg_salary, 2),
        department_distribution=dept_dist,
        top_performers=top_performers,
        low_performers=low_performers
    )