from fastapi import FastAPI, HTTPException
app = FastAPI()

users = {
    1:{
    "name":"Sudheer",
    "orders":{
        101 : {"item" : "Pen", "amount" : 345},
        102 : {"item" : "Bun", "amount" : 800}
     }},
    2:{
        "name": "Navya",
        "orders":{
        101 : {"item" : "Pen", "amount" : 345},
        102 : {"item" : "Bun", "amount" : 800}
     }}
    }

@app.get("/getUser/{userId}/orders/{order_id}")
def get_user(userId: int, order_id: int):
    if userId not in(users):
        raise HTTPException(status_code = 404, detail = "UserId Not Found" )
    return{"userName" : users[userId]['orders'][order_id]}