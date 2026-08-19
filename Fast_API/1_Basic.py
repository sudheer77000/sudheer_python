from fastapi import FastAPI

app = FastAPI(
    title="My FastAPI Application",
    description="My first FastAPI application",
    version="1.0.0"
)


@app.get("/")
def root_url():
    return {"Message": "Welcome To Fast API"}


@app.get("/sub")
def sub_url():
    return {"Message": "Welcome To Fast API, Internal Page"}