from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()

# Request body for POST
class emp(BaseModel):
    Name: str
    Location: str | None = None

@app.post("/postEmp")
def postEmp(Employee: emp):
    return{
        "Status"  : "Post Operation Performed Successfully",
        "empName" : Employee.Name,
        "empLoc"  :  Employee.Location
    }