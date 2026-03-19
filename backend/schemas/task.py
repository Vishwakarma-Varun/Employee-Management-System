from pydantic import BaseModel
from typing import Optional, List
from datetime import date, datetime
from .employee import EmployeeResponse

class TaskBase(BaseModel):
    title: str
    description: Optional[str] = None
    status: str = "Pending"
    employee_id: int
    due_date: Optional[date] = None

class TaskCreate(TaskBase):
    pass

class TaskUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    status: Optional[str] = None
    employee_id: Optional[int] = None
    due_date: Optional[date] = None

class TaskResponse(TaskBase):
    id: int
    created_at: datetime
    updated_at: Optional[datetime] = None
    employee: Optional[EmployeeResponse] = None

    class Config:
        from_attributes = True

class PaginatedTasks(BaseModel):
    total: int
    page: int
    per_page: int
    total_pages: int
    tasks: List[TaskResponse]
