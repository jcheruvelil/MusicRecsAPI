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

class LibraryItem(BaseModel):
    playlist_id: int
    playlist_title: str
    

@router.post("/")
def create_user(new_user: User):
    with db.engine.begin() as connection:
        
        result = connection.execute(sqlalchemy.text(
            f"""
            SELECT COUNT(*) 
            FROM users 
            WHERE username = :username
            """),
            {"username": new_user.username}
        ).scalar_one()
        
        if result != 0:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT, detail="Username already exists"
            ) 
        
        user_id = connection.execute(sqlalchemy.text(
            f"""
            INSERT INTO users (username)
            VALUES (:username)
            RETURNING id"""),
            {"username": new_user.username}
        ).scalar_one()
        
    return {"user_id": user_id}

@router.post("/login/")
def login_user(login: Login):
    with db.engine.begin() as connection:
        try:
            user_id = connection.execute(sqlalchemy.text(
                """
                SELECT id
                FROM users 
                WHERE username = :username
                """), {"username": login.username}
            ).scalar_one()
        
        except:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid username"
            )
        
    return {"user_id": user_id}

@router.get("/{user_id}/library")
def get_user_library(user_id: int):
    with db.engine.begin() as connection:
        result = connection.execute(sqlalchemy.text(
            """
            SELECT id, playlist_name
            FROM playlists 
            WHERE user_id = :user_id
            """), 
            {"user_id": user_id}
        ).fetchall()
        
        if not result:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="User library not found"
            )
        
        library_items = [LibraryItem(playlist_id=row.id, playlist_title=row.playlist_name) for row in result]
        
    return library_items