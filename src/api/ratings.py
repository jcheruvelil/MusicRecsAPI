from fastapi import HTTPException, status, APIRouter, Depends, Request
from pydantic import BaseModel
from src.api import auth

import sqlalchemy
from src import database as db

router = APIRouter(
    prefix="/rating",
    tags=["rating"],
    dependencies=[Depends(auth.get_api_key)],
)
    
class Playlist(BaseModel):
    playlist_name: str
    
class Rating(BaseModel):
    value: int

@router.post("/{user_id}/{track_id}")
def set_rating(user_id: int, track_id: int, rating: Rating):
    with db.engine.begin() as connection:
        
        # Validate input
        if rating.value > 10 or rating.value < 0:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Rating must be between 0 and 10."
            )
        
        # Check if user exists
        result = connection.execute(sqlalchemy.text(
            f"""
            SELECT COUNT(*)
            FROM users
            WHERE id = '{user_id}'
            """)
        ).scalar_one()
        
        if result < 1:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"User with username {user_id} does not exist"
            )
        
        # Check if track exists
        result = connection.execute(sqlalchemy.text(
            f"""
            SELECT COUNT(*)
            FROM tracks
            WHERE id = '{track_id}'
            """)
        ).scalar_one()
        
        if result < 1:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Track with id {track_id} does not exist"
            )
        
        # Check if rating already exists for this song
        result = connection.execute(sqlalchemy.text(
            f"""
            SELECT COUNT(*)
            FROM ratings
            JOIN users ON ratings.user_id = users.id
            WHERE 
                users.id = '{user_id}' AND
                ratings.track_id = '{track_id}'
            """)
        ).scalar_one()
        
        if result > 0:
            connection.execute(
                sqlalchemy.text(
                f"""
                UPDATE ratings
                SET rating = :rating
                WHERE 
                    user_id = '{user_id}' AND
                    track_id = '{track_id}'
                """),
                [{"rating": rating.value}]
            )
        else:
            connection.execute(
                sqlalchemy.text(f"""
                INSERT INTO ratings (user_id, track_id, rating)
                VALUES ('{user_id}', '{track_id}', :rating)"""),
                [{"rating": rating.value}]
            )
        
    return "OK"

    