from fastapi import APIRouter, HTTPException, status, Depends, Request
from pydantic import BaseModel
from src.api import auth

import sqlalchemy
from src import database as db


router = APIRouter(
    prefix="/user",
    tags=["user"],
    dependencies=[Depends(auth.get_api_key)],
)

class User(BaseModel):
    username: str

class Login(BaseModel):
    username: str

@router.post("/")
def create_user(new_user: User):
    with db.engine.begin() as connection:
        
        result = connection.execute(sqlalchemy.text(
            f"""
            SELECT COUNT(*) 
            FROM users 
            WHERE username = '{new_user.username}'
            """)
        ).scalar_one()
        
        if result != 0:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT, detail="Username already exists"
            ) 
        
        result = connection.execute(sqlalchemy.text(
            f"""
            INSERT INTO users (username)
            VALUES ('{new_user.username}')""")
        )
        
    return "OK"

@router.post("/login/")
def login_user(login: Login):
    with db.engine.begin() as connection:
        result = connection.execute(sqlalchemy.text(
            f"""
            SELECT COUNT(*)
            FROM users 
            WHERE username = :username
            """), {"username": login.username}
        ).scalar_one()
        
        if result == 0:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid username"
            )
        
    return {"message": "Login successful"}