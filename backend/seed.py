"""
Seed the database with sample admin user and employees.
Run: python seed.py
"""
import sys
import os
sys.path.insert(0, os.path.dirname(__file__))

from database.db import SessionLocal, engine, Base
import models  # Ensure all models are registered
from models.user import User
from models.employee import Employee
from core.security import get_password_hash
from datetime import date

# Create all tables
Base.metadata.create_all(bind=engine)

def seed():
    db = SessionLocal()
    try:
        # ── Users ──────────────────────────────────────────────
        users = [
            User(full_name="Alice Admin", email="admin@company.com",
                 hashed_password=get_password_hash("Admin@1234"), role="admin"),
            User(full_name="Harry HR", email="hr@company.com",
                 hashed_password=get_password_hash("Hr@12345"), role="hr"),
            User(full_name="Mark Manager", email="manager@company.com",
                 hashed_password=get_password_hash("Manager@1"), role="manager"),
        ]
        for u in users:
            if not db.query(User).filter(User.email == u.email).first():
                db.add(u)

        # ── Employees ──────────────────────────────────────────
        employees_data = [
            ("EMP0001", "John Smith", "john.smith@company.com", "+1-555-0101",
             "Engineering", "Senior Developer", 95000, date(2021, 3, 15), 8.5),
            ("EMP0002", "Sarah Johnson", "sarah.j@company.com", "+1-555-0102",
             "Marketing", "Marketing Lead", 75000, date(2020, 7, 1), 9.2),
            ("EMP0003", "Michael Chen", "m.chen@company.com", "+1-555-0103",
             "Engineering", "DevOps Engineer", 88000, date(2022, 1, 10), 7.8),
            ("EMP0004", "Emily Davis", "e.davis@company.com", "+1-555-0104",
             "HR", "HR Specialist", 65000, date(2019, 11, 5), 6.5),
            ("EMP0005", "James Wilson", "j.wilson@company.com", "+1-555-0105",
             "Sales", "Sales Manager", 80000, date(2021, 8, 20), 4.2),
            ("EMP0006", "Anna Martinez", "a.martinez@company.com", "+1-555-0106",
             "Finance", "Financial Analyst", 72000, date(2020, 4, 12), 8.9),
            ("EMP0007", "Robert Taylor", "r.taylor@company.com", "+1-555-0107",
             "Engineering", "Frontend Developer", 82000, date(2022, 6, 3), 7.1),
            ("EMP0008", "Lisa Anderson", "l.anderson@company.com", "+1-555-0108",
             "Design", "UX Designer", 78000, date(2021, 2, 28), 9.5),
            ("EMP0009", "David Brown", "d.brown@company.com", "+1-555-0109",
             "Operations", "Operations Lead", 70000, date(2019, 9, 17), 3.8),
            ("EMP0010", "Jennifer Garcia", "j.garcia@company.com", "+1-555-0110",
             "Product", "Product Manager", 95000, date(2020, 12, 1), 8.0),
            ("EMP0011", "Thomas Lee", "t.lee@company.com", "+1-555-0111",
             "Engineering", "Backend Developer", 87000, date(2023, 1, 15), 7.5),
            ("EMP0012", "Patricia White", "p.white@company.com", "+1-555-0112",
             "Legal", "Legal Counsel", 105000, date(2018, 5, 22), 8.2),
            ("EMP0013", "Christopher Harris", "c.harris@company.com", "+1-555-0113",
             "Sales", "Sales Rep", 55000, date(2023, 3, 7), 2.9),
            ("EMP0014", "Jessica Clark", "j.clark@company.com", "+1-555-0114",
             "Marketing", "Content Strategist", 68000, date(2022, 9, 19), 7.3),
            ("EMP0015", "Daniel Lewis", "d.lewis@company.com", "+1-555-0115",
             "Finance", "CFO", 150000, date(2017, 3, 1), 9.8),
        ]

        for emp_data in employees_data:
            emp_id = emp_data[0]
            if not db.query(Employee).filter(Employee.employee_id == emp_id).first():
                emp = Employee(
                    employee_id=emp_data[0],
                    full_name=emp_data[1],
                    email=emp_data[2],
                    phone=emp_data[3],
                    department=emp_data[4],
                    designation=emp_data[5],
                    salary=emp_data[6],
                    date_of_joining=emp_data[7],
                    performance_score=emp_data[8],
                )
                db.add(emp)

        db.commit()
        print("✅ Database seeded successfully!")
        print("\n📋 Login credentials:")
        print("   Admin:   admin@company.com  / Admin@1234")
        print("   HR:      hr@company.com     / Hr@12345")
        print("   Manager: manager@company.com/ Manager@1")

    except Exception as e:
        db.rollback()
        print(f"❌ Seeding failed: {e}")
        raise
    finally:
        db.close()


if __name__ == "__main__":
    seed()
