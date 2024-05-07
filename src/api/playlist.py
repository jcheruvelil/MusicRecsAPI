from fastapi import APIRouter, Depends, Request
from pydantic import BaseModel
from src.api import auth

import sqlalchemy
from src import database as db


router = APIRouter(
    prefix="/playlist",
    tags=["playlist"],
    dependencies=[Depends(auth.get_api_key)],
)

class User(BaseModel):
    username: str
    
class Playlist(BaseModel):
    playlist_name: str

@router.post("/")
def create_user(user: User, playlist: Playlist):
    with db.engine.begin() as connection:
        result = connection.execute(sqlalchemy.text(
            f"""
            SELECT id
            FROM users 
            WHERE username = '{user.username}'
            """)
        ).scalar_one()
        
        if result != 0:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT, detail="Username already exists"
            ) 
        
        result = connection.execute(sqlalchemy.text(
            f"""
            INSERT INTO playlists (playlist_name)
            VALUES ('{new_user.username}')""")
        )
        
    return "OK"
    