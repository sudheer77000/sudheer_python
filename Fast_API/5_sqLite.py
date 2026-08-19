from fastapi import FastAPI, Depends, HTTPException
from sqlmodel import SQLModel, create_engine, Session, select
from contextlib import asynccontextmanager
from typing import Annotated
from five_Models import User, CreateUser

DATABASE_URL = "sqlite:///./5_users.db"
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

@app.post("/createUser")
def create_user(user:CreateUser, session:SessionDep):
    new_user = User.model_validate(user)
    session.add(new_user)
    session.commit()
    session.refresh(new_user)
    return new_user

@app.get("/users", response_model = list[User])
def get_users(session:SessionDep):
    users = session.exec(select(User)).all()
    if not users:
        raise HTTPException(status_code = 404, detail = "Users Not Found" )
    return users

@app.get("/users/{userId}", response_model = User)
def get_user(userId,session:SessionDep):
    user = session.exec(select(User).where(User.id == userId)).first()
    if not user:
        raise HTTPException(status_code = 404, detail = "User Not Found" )
    return user

@app.delete("/users/{userId}", response_model=User)
def delete_user(userId: int, session: SessionDep):

    user = session.exec(
        select(User).where(User.id == userId)
    ).first()

    if not user:
        raise HTTPException(
            status_code=404,
            detail="User Not Found"
        )

    session.delete(user)
    session.commit()

    return user

@app.put("/users/{userId}", response_model=User)
def update_user(
    userId: int,
    user_data: CreateUser,
    session: SessionDep
):
    user = session.exec(
        select(User).where(User.id == userId)
    ).first()

    if not user:
        raise HTTPException(
            status_code=404,
            detail="User Not Found"
        )

    user.name = user_data.name
    user.email = user_data.email
    user.phone = user_data.phone

    session.add(user)
    session.commit()
    session.refresh(user)

    return user




