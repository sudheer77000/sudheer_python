from fastapi import FastAPI, Depends, HTTPException, Form, File, UploadFile
from sqlmodel import SQLModel, create_engine, Session, select
from contextlib import asynccontextmanager
from typing import Annotated
from seven_models import User, CreateUser
import os, shutil

DATABASE_URL = "sqlite:///./7_users.db"
engine = create_engine(DATABASE_URL,echo = True)

@asynccontextmanager
async def life_span(app:FastAPI):
    SQLModel.metadata.create_all(engine)
    yield

app = FastAPI(lifespan=life_span)

def get_session():
    with Session(engine) as session:
        yield session

SessionDep = Annotated[Session, Depends(get_session)]

UPLOAD_DIR = "7_Uploads"
os.makedirs(UPLOAD_DIR, exist_ok= True)

@app.post("/createUser")
def createUser(session: SessionDep,
               name: str = Form(...),
               phone: int = Form(...),
               email: str = Form(...),
               file:UploadFile = File(...)
               ):
    user_data = {"name" : name,"phone":phone,"email":email}
    validated = CreateUser.model_validate(user_data)
    file_path = os.path.join(UPLOAD_DIR,file.filename)
    with open(file_path,"wb") as f:
        shutil.copyfileobj(file.file,f)
    user = User(**validated.model_dump(), file_path = f"{UPLOAD_DIR}/{file.filename}")
    session.add(user)
    session.commit()
    session.refresh(user)
    return user