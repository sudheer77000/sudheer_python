from fastapi import FastAPI
from datetime import datetime

app = FastAPI()
i = 0
@app.get("/time")
def get_current_time():
    global i
    print(f"Service Invoked Count : {i}")
    i = i + 1
    return {
        "current_time": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    }

@app.get("/name")
def get_name():
    return {
        "my_name": "Sudheer Gundra"
    }