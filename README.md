# 🏢 Employee Management System (EMS)

A production-ready, full-stack Employee Management System built with FastAPI, SQLAlchemy, and React.

---

## 📁 Project Structure

```
emp-mgmt/
├── backend/
│   ├── core/
│   │   ├── config.py          # Pydantic Settings (env vars)
│   │   └── security.py        # JWT, password hashing, RBAC
│   ├── database/
│   │   └── db.py              # SQLAlchemy engine & session
│   ├── models/
│   │   ├── user.py            # User ORM model
│   │   └── employee.py        # Employee ORM model
│   ├── schemas/
│   │   ├── user.py            # Pydantic schemas for users
│   │   └── employee.py        # Pydantic schemas for employees
│   ├── routes/
│   │   ├── auth.py            # /api/auth/* endpoints
│   │   └── employees.py       # /api/employees/* endpoints
│   ├── services/
│   │   ├── auth_service.py    # Auth business logic
│   │   └── employee_service.py# Employee business logic
│   ├── main.py                # FastAPI app entry point
│   ├── seed.py                # Database seeder
│   ├── requirements.txt
│   └── .env.example
└── frontend/
    └── index.html             # Single-file React app
```

---

## 🗄️ Database Schema

### `users` table
| Column | Type | Notes |
|--------|------|-------|
| id | INTEGER PK | Auto-increment |
| full_name | VARCHAR(100) | Required |
| email | VARCHAR(255) UNIQUE | Required |
| hashed_password | VARCHAR(255) | bcrypt |
| role | VARCHAR(20) | admin/hr/manager |
| is_active | BOOLEAN | Default true |
| created_at | DATETIME | Auto |
| updated_at | DATETIME | Auto |

### `employees` table
| Column | Type | Notes |
|--------|------|-------|
| id | INTEGER PK | Auto-increment |
| employee_id | VARCHAR(20) UNIQUE | Auto: EMP0001... |
| full_name | VARCHAR(100) | Indexed |
| email | VARCHAR(255) UNIQUE | Indexed |
| phone | VARCHAR(20) | Optional |
| department | VARCHAR(50) | Indexed |
| designation | VARCHAR(100) | |
| salary | FLOAT | Must be > 0 |
| date_of_joining | DATE | |
| performance_score | FLOAT | 0.0–10.0 |
| created_at | DATETIME | Auto |
| updated_at | DATETIME | Auto |

---

## 🚀 Quick Start

### 1. Clone & Setup Backend

```bash
cd emp-mgmt/backend

# Create virtual environment
python -m venv venv
source venv/bin/activate        # Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Copy and configure environment
cp .env.example .env
# Edit .env if needed (defaults work for local SQLite dev)

# Seed database with sample data
python seed.py

# Start server
uvicorn main:app --reload --port 8000
```

### 2. Launch Frontend

```bash
# Option A: Simple (open directly in browser)
open emp-mgmt/frontend/index.html

# Option B: Serve with Python
cd emp-mgmt/frontend
python -m http.server 3000
# Visit http://localhost:3000
```

### 3. Access Points

| Service | URL |
|---------|-----|
| Frontend | http://localhost:3000 |
| API | http://localhost:8000 |
| Swagger Docs | http://localhost:8000/docs |
| ReDoc | http://localhost:8000/redoc |

---

## 🔑 Demo Credentials

| Role | Email | Password |
|------|-------|----------|
| Admin | admin@company.com | Admin@1234 |
| HR | hr@company.com | Hr@12345 |
| Manager | manager@company.com | Manager@1 |

---

## 🌐 API Endpoints

### Authentication

| Method | Endpoint | Description | Auth |
|--------|----------|-------------|------|
| POST | `/api/auth/register` | Register new user | None |
| POST | `/api/auth/login` | Login, get JWT | None |
| GET | `/api/auth/me` | Current user profile | Any |

### Employees

| Method | Endpoint | Description | Required Role |
|--------|----------|-------------|---------------|
| GET | `/api/employees` | List (paginated + search) | Any |
| POST | `/api/employees` | Create employee | admin, hr |
| GET | `/api/employees/{id}` | Get single employee | Any |
| PUT | `/api/employees/{id}` | Update employee | admin, hr, manager |
| DELETE | `/api/employees/{id}` | Delete employee | admin |
| GET | `/api/employees/dashboard` | Analytics & stats | Any |

### Query Parameters (GET /api/employees)

| Param | Type | Default | Description |
|-------|------|---------|-------------|
| page | int | 1 | Page number |
| per_page | int | 10 | Items per page (max 100) |
| search | string | - | Search name, dept, designation |
| department | string | - | Filter by exact department |

---

## 🔐 Role-Based Access Control

| Feature | Admin | HR | Manager |
|---------|-------|----|---------|
| View employees | ✅ | ✅ | ✅ |
| Create employee | ✅ | ✅ | ❌ |
| Update employee | ✅ | ✅ | ✅ |
| Delete employee | ✅ | ❌ | ❌ |
| View dashboard | ✅ | ✅ | ✅ |

---

## 🐘 PostgreSQL (Production)

Update `.env`:

```env
DATABASE_URL=postgresql://username:password@localhost:5432/emp_management
SECRET_KEY=your-super-secure-random-key-at-least-32-characters
```

Create database:
```sql
CREATE DATABASE emp_management;
```

---

## 📊 Sample API Requests

### Login
```bash
curl -X POST http://localhost:8000/api/auth/login \
  -H "Content-Type: application/json" \
  -d '{"email":"admin@company.com","password":"Admin@1234"}'
```

### List Employees with Search
```bash
curl "http://localhost:8000/api/employees?search=john&page=1&per_page=5" \
  -H "Authorization: Bearer YOUR_TOKEN"
```

### Create Employee
```bash
curl -X POST http://localhost:8000/api/employees \
  -H "Authorization: Bearer YOUR_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "full_name": "New Employee",
    "email": "new@company.com",
    "department": "Engineering",
    "designation": "Junior Developer",
    "salary": 65000,
    "date_of_joining": "2024-01-15",
    "performance_score": 7.5
  }'
```

### Dashboard Stats
```bash
curl http://localhost:8000/api/employees/dashboard \
  -H "Authorization: Bearer YOUR_TOKEN"
```
