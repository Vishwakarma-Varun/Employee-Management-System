from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from typing import Optional

from database import get_db
from schemas.employee import EmployeeCreate, EmployeeUpdate, EmployeeResponse, PaginatedEmployees, DashboardStats
from services.employee_service import create_employee, get_employee, get_employees, update_employee, delete_employee, get_dashboard_stats
from core.security import get_current_user, require_roles

router = APIRouter(prefix="/api/employees", tags=["Employees"])


@router.get("/dashboard", response_model=DashboardStats)
def dashboard(db: Session = Depends(get_db), _=Depends(get_current_user)):
    return get_dashboard_stats(db)


@router.get("", response_model=PaginatedEmployees)
def list_employees(
    page: int = Query(1, ge=1),
    per_page: int = Query(10, ge=1, le=100),
    search: Optional[str] = Query(None),
    department: Optional[str] = Query(None),
    db: Session = Depends(get_db),
    _=Depends(get_current_user),
):
    return get_employees(db, page=page, per_page=per_page, search=search, department=department)


@router.post("", response_model=EmployeeResponse, status_code=201)
def create(data: EmployeeCreate, db: Session = Depends(get_db), _=Depends(require_roles("admin", "hr"))):
    return create_employee(db, data)


@router.get("/{employee_id}", response_model=EmployeeResponse)
def get_one(employee_id: int, db: Session = Depends(get_db), _=Depends(get_current_user)):
    return get_employee(db, employee_id)


@router.put("/{employee_id}", response_model=EmployeeResponse)
def update(employee_id: int, data: EmployeeUpdate, db: Session = Depends(get_db), _=Depends(require_roles("admin", "hr", "manager"))):
    return update_employee(db, employee_id, data)


@router.delete("/{employee_id}")
def delete(employee_id: int, db: Session = Depends(get_db), _=Depends(require_roles("admin"))):
    return delete_employee(db, employee_id)