from fastapi import FastAPI, Depends, HTTPException,Form
from sqlmodel import SQLModel, create_engine, Session, select
from contextlib import asynccontextmanager
from typing import Annotated
from Eight_Model import User, CreateUser, LoginUser, Token
from passlib.context import CryptContext
from jose import jwt, JWTError
from datetime import datetime, timedelta, timezone
from fastapi.security import OAuth2PasswordRequestForm, OAuth2PasswordBearer

DATABASE_URL = "sqlite:///./8_users.db"
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

oauth2_schema = OAuth2PasswordBearer(tokenUrl="login")

SECRET_KEY = "sudheer"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRY_MIN = 30

def create_access_token(data:dict, expires_delta: timedelta | None= None):
    to_encode = data.copy()
    expire = datetime.now(timezone.utc) + (expires_delta or timedelta(minutes=15))
    to_encode.update({"exp":expire})
    return jwt.encode(to_encode,SECRET_KEY,algorithm=ALGORITHM)

def verify_token(token:str):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return payload
    except JWTError:
        return None

def get_current_user(token:Annotated[str, Depends(oauth2_schema)], session: SessionDep):
    payload = verify_token(token)
    if not payload:
        raise HTTPException(status_code = 401, detail = "Invalid Token" )
    user = session.exec(select(User).where(User.email == payload.get("sub"))).first()
    if not user:
        raise HTTPException(status_code = 404, detail = "User Not Found" )
    return user
#Authorization

pwd_context = CryptContext(schemes=["bcrypt"], deprecated = "auto")

def hash_password(password:str) -> str:
    return pwd_context.hash(password)

def verify_password(plain:str, hashed:str) -> bool:
    return pwd_context.verify(plain,hashed)

@app.post("/register")
def register(session: SessionDep,
    name: str = Form(...),
    email: str = Form(...),
    password: str = Form(...)
):
    if session.exec(select(User).where(User.email == email)).first():
        raise HTTPException(status_code = 400, detail = "Email is already Registered" )
    hash_pwd = hash_password(password)
    print("HASH:", hash_pwd)  # temporary debugging
    user = User(email = email,
                name = name,
                hashed_Password = hash_pwd)
    session.add(user)
    session.commit()
    session.refresh(user)
    return user

@app.post("/login",response_model = Token)
def login(session: SessionDep, form_data : Annotated[OAuth2PasswordRequestForm, Depends()]):
    user = session.exec(select(User).where(User.email == form_data.username)).first()
    password = verify_password(form_data.password,user.hashed_Password)
    if not user or not password:
        raise HTTPException(status_code = 400, detail = "Invalid Credentials" )
    token = create_access_token(data={"sub": user.email})
    return {"access_token" : token,"token_type" : "bearer"}

@app.get("/profile")
def profile(current_user: Annotated[User, Depends(get_current_user)]):
    return {"name": current_user,"email":current_user.email}
