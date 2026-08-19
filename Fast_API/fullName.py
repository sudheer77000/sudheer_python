
from fastapi import FastAPI
from datetime import datetime
from pydantic import BaseModel

class NameRequest(BaseModel):
    first_name: str
    last_name: str

app = FastAPI()
@app.post("/fullname")
def get_full_name(request: NameRequest):
    full_name = request.first_name + " " + request.last_name

    return {
        "full_name": full_name,
        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    }
