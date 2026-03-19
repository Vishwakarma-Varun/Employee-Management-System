from sqlalchemy.orm import Session
from fastapi import HTTPException
from models.attendance import Attendance
from models.employee import Employee
from schemas.attendance import AttendanceCreate, AttendanceUpdate, PaginatedAttendance
from datetime import date, datetime
import math

def get_attendances(db: Session, page: int = 1, per_page: int = 10, employee_id: int = None, record_date: date = None):
    query = db.query(Attendance)
    
    if employee_id:
        query = query.filter(Attendance.employee_id == employee_id)
    if record_date:
        query = query.filter(Attendance.date == record_date)

    total = query.count()
    if total == 0:
        return PaginatedAttendance(total=0, page=page, per_page=per_page, total_pages=0, records=[])

    total_pages = math.ceil(total / per_page)
    offset = (page - 1) * per_page
    records = query.order_by(Attendance.date.desc()).offset(offset).limit(per_page).all()

    return PaginatedAttendance(total=total, page=page, per_page=per_page, total_pages=total_pages, records=records)

def create_attendance(db: Session, data: AttendanceCreate):
    record = Attendance(**data.model_dump())
    db.add(record)
    db.commit()
    db.refresh(record)
    return record

def punch_in(db: Session, employee_id: int):
    today = date.today()
    record = db.query(Attendance).filter(Attendance.employee_id == employee_id, Attendance.date == today).first()
    
    if record:
        if record.check_in_time:
            raise HTTPException(status_code=400, detail="Already punched in today")
        # If record exists but no check-in (maybe created manually by HR)
        record.check_in_time = datetime.utcnow()
        db.commit()
        db.refresh(record)
        return record

    new_record = Attendance(
        employee_id=employee_id,
        date=today,
        status="Present",
        check_in_time=datetime.utcnow()
    )
    db.add(new_record)
    db.commit()
    db.refresh(new_record)
    return new_record

def punch_out(db: Session, employee_id: int):
    today = date.today()
    record = db.query(Attendance).filter(Attendance.employee_id == employee_id, Attendance.date == today).first()
    
    if not record or not record.check_in_time:
        raise HTTPException(status_code=400, detail="Not punched in today")
    
    if record.check_out_time:
        raise HTTPException(status_code=400, detail="Already punched out today")

    record.check_out_time = datetime.utcnow()
    db.commit()
    db.refresh(record)
    return record

def update_attendance(db: Session, record_id: int, data: AttendanceUpdate):
    record = db.query(Attendance).filter(Attendance.id == record_id).first()
    if not record:
        raise HTTPException(status_code=404, detail="Attendance record not found")

    update_data = data.model_dump(exclude_unset=True)
    for k, v in update_data.items():
        setattr(record, k, v)
        
    db.commit()
    db.refresh(record)
    return record

def delete_attendance(db: Session, record_id: int):
    record = db.query(Attendance).filter(Attendance.id == record_id).first()
    if not record:
        raise HTTPException(status_code=404, detail="Attendance record not found")
        
    db.delete(record)
    db.commit()
    return {"message": "Record deleted"}
