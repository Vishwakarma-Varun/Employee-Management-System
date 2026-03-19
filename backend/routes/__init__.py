from .auth import router as auth_router
from .employees import router as employees_router
from .tasks import router as tasks_router
from .attendance import router as attendance_router

__all__ = ["auth_router", "employees_router", "tasks_router", "attendance_router"]
