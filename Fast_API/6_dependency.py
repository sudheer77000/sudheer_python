from fastapi import FastAPI, Depends, HTTPException
i = 0

def getCount():
    global i
    i += 1
    return i

app = FastAPI()
@app.get("/Hello")
def greetings(count:  int = Depends(getCount)):
    return {"Status" : "Welcome to Fast API","totalHits":count}