from fastapi import FastAPI, HTTPException
from typing import Optional
from pydantic import BaseModel, Field,EmailStr

app = FastAPI()

user_details = {}
count_id = 1

class User(BaseModel):
    name: str = Field(...,min_length=3,max_length=10)
    phone: int
    email: EmailStr

@app.post("/create")
def create_user(user: User):
    global count_id
    user_details[count_id] = user
    response =  {"Status" : "User Succesfully Created",
            "userId" : count_id}
    count_id += 1
    return response
@app.get("/users")
def get_users():
    if not user_details:
        raise HTTPException(status_code = 404, detail = "User Details Not Found" )
    return user_details

@app.get("/users/{userId}")
def get_user(userId : int):
    if userId not in user_details:
        raise HTTPException(status_code = 404, detail = "UserId Not Found" )
    return user_details[userId]

@app.put("/users/{userId}")
def put_user(userId : int, user: User):
    if userId not in user_details:
        raise HTTPException(status_code = 404, detail = "UserId Not Found" )
    user_details[userId] = user
    response =  {"Status" : "User Succesfully Updated","userId" : userId}
    return response

@app.delete("/users/{userId}")
def put_user(userId : int):
    if userId not in user_details:
        raise HTTPException(status_code = 404, detail = "UserId Not Found" )
    delete = user_details.pop(userId)
    response =  {"Status" : "User Succesfully Deleted","userId" : userId}
    return response
