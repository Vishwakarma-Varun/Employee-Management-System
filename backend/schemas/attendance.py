from pydantic import BaseModel
from typing import Optional, List
from datetime import date, datetime
from .employee import EmployeeResponse

class AttendanceBase(BaseModel):
    employee_id: int
    date: date
    status: str = "Present"
    check_in_time: Optional[datetime] = None
    check_out_time: Optional[datetime] = None

class AttendanceCreate(AttendanceBase):
    pass

class AttendanceUpdate(BaseModel):
    status: Optional[str] = None
    check_in_time: Optional[datetime] = None
    check_out_time: Optional[datetime] = None

class AttendanceResponse(AttendanceBase):
    id: int
    created_at: datetime
    updated_at: Optional[datetime] = None
    employee: Optional[EmployeeResponse] = None

    class Config:
        from_attributes = True

class PaginatedAttendance(BaseModel):
    total: int
    page: int
    per_page: int
    total_pages: int
    records: List[AttendanceResponse]
