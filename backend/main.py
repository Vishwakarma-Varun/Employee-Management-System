from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from database.db import Base, engine
import models
from routes import auth_router, employees_router, tasks_router, attendance_router

Base.metadata.create_all(bind=engine)

app = FastAPI(title="Employee Management System", version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth_router)
app.include_router(employees_router)
app.include_router(tasks_router)
app.include_router(attendance_router)


@app.get("/")
def health_check():
    return {"status": "ok", "app": "Employee Management System"}