from fastapi import FastAPI
from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.orm import declarative_base, sessionmaker
from pydantic import BaseModel

app = FastAPI()

# MySQL connection
DATABASE_URL = "mysql+pymysql://root:mysql@localhost/sys"
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(bind=engine)
Base = declarative_base()

# Employee table
class Employee(Base):
    __tablename__ = "employees"

    id = Column(Integer, primary_key=True)
    first_name = Column(String)
    last_name = Column(String)
    department = Column(String)

# Request body for POST
class EmployeeRequest(BaseModel):
    first_name: str
    last_name: str
    department: str



@app.get("/employees/{employee_id}")
def get_employee(employee_id: int):

    db = SessionLocal()
    employee = db.query(Employee).filter(
        Employee.id == employee_id
    ).first()
    db.close()
    if employee is None:
        return {"message": "Employee not found"}
    return {
        "id": employee.id,
        "first_name": employee.first_name,
        "last_name": employee.last_name,
        "department": employee.department
    }


# POST employee
@app.post("/employees")
def create_employee(employee: EmployeeRequest):

    db = SessionLocal()

    new_employee = Employee(
        first_name=employee.first_name,
        last_name=employee.last_name,
        department=employee.department
    )

    db.add(new_employee)
    db.commit()
    db.refresh(new_employee)
    db.close()

    return {
        "message": "Employee created successfully",
        "id": new_employee.id,
        "first_name": new_employee.first_name,
        "last_name": new_employee.last_name,
        "department": new_employee.department
    }