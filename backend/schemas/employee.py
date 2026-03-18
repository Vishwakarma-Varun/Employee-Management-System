from pydantic import BaseModel, EmailStr, field_validator
from typing import Optional, List
from datetime import date, datetime


class EmployeeBase(BaseModel):
    full_name: str
    email: EmailStr
    phone: Optional[str] = None
    department: str
    designation: str
    salary: float
    date_of_joining: date
    performance_score: float = 0.0

    @field_validator("salary")
    @classmethod
    def salary_positive(cls, v):
        if v <= 0:
            raise ValueError("Salary must be positive")
        return v

    @field_validator("performance_score")
    @classmethod
    def score_range(cls, v):
        if not 0.0 <= v <= 10.0:
            raise ValueError("Performance score must be between 0 and 10")
        return v


class EmployeeCreate(EmployeeBase):
    pass


class EmployeeUpdate(BaseModel):
    full_name: Optional[str] = None
    email: Optional[EmailStr] = None
    phone: Optional[str] = None
    department: Optional[str] = None
    designation: Optional[str] = None
    salary: Optional[float] = None
    date_of_joining: Optional[date] = None
    performance_score: Optional[float] = None


class EmployeeResponse(EmployeeBase):
    id: int
    employee_id: str
    created_at: datetime
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True


class PaginatedEmployees(BaseModel):
    total: int
    page: int
    per_page: int
    total_pages: int
    employees: List[EmployeeResponse]


class DashboardStats(BaseModel):
    total_employees: int
    avg_salary: float
    department_distribution: dict
    top_performers: List[EmployeeResponse]
    low_performers: List[EmployeeResponse]