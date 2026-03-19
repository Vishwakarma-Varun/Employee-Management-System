from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from typing import Optional
from datetime import date

from database.db import get_db
from schemas.attendance import AttendanceCreate, AttendanceUpdate, AttendanceResponse, PaginatedAttendance
from services.attendance_service import create_attendance, get_attendances, punch_in, punch_out, update_attendance, delete_attendance
from core.security import get_current_user, require_roles

router = APIRouter(prefix="/api/attendance", tags=["Attendance"])

@router.post("", response_model=AttendanceResponse, status_code=201)
def create_record(data: AttendanceCreate, db: Session = Depends(get_db), _=Depends(require_roles("admin", "hr", "manager"))):
    return create_attendance(db, data)

@router.get("", response_model=PaginatedAttendance)
def list_records(
    page: int = Query(1, ge=1),
    per_page: int = Query(10, ge=1, le=100),
    employee_id: Optional[int] = Query(None),
    record_date: Optional[date] = Query(None),
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user),
):
    if current_user.role == "employee":
        employee_id = current_user.id
    return get_attendances(db, page=page, per_page=per_page, employee_id=employee_id, record_date=record_date)

@router.post("/punch-in", response_model=AttendanceResponse)
def do_punch_in(db: Session = Depends(get_db), current_user=Depends(get_current_user)):
    return punch_in(db, current_user.id)

@router.post("/punch-out", response_model=AttendanceResponse)
def do_punch_out(db: Session = Depends(get_db), current_user=Depends(get_current_user)):
    return punch_out(db, current_user.id)

@router.put("/{record_id}", response_model=AttendanceResponse)
def update_record(record_id: int, data: AttendanceUpdate, db: Session = Depends(get_db), _=Depends(require_roles("admin", "hr", "manager"))):
    return update_attendance(db, record_id, data)

@router.delete("/{record_id}")
def delete_record(record_id: int, db: Session = Depends(get_db), _=Depends(require_roles("admin"))):
    return delete_attendance(db, record_id)
