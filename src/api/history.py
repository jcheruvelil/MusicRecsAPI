from fastapi import HTTPException, status, APIRouter, Depends, Request
from pydantic import BaseModel
from typing import List
from src.api import auth

import sqlalchemy
from src import database as db

router = APIRouter(
    prefix="/history",
    tags=["history"],
    dependencies=[Depends(auth.get_api_key)],
)

class SearchItem(BaseModel):
    query: str

class RecommendationItem(BaseModel):
    input_track_id: str

@router.get("/search", response_model=List[SearchItem])
def get_search_history(user_id: int):
    with db.engine.begin() as connection:
        result = connection.execute(sqlalchemy.text(
            """
            SELECT query, created_at
            FROM search_history
            WHERE user_id = :user_id
            ORDER BY created_at DESC
            """), {"user_id": user_id}
        ).fetchall()
        
        if not result:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="Search history not found"
            )
        
        search_history = [SearchItem(query=row.query) for row in result]
        
    return search_history

@router.get("/recommendation", response_model=List[RecommendationItem])
def get_recommendation_history(user_id: int):
    with db.engine.begin() as connection:
        result = connection.execute(sqlalchemy.text(
            """
            SELECT id, user_id, query, created_at
            FROM recommendation_history
            WHERE user_id = :user_id
            ORDER BY created_at DESC
            """), {"user_id": user_id}
        ).fetchall()
        
        if not result:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="Recommendation history not found"
            )
        
        recommendation_history = [RecommendationItem(input_track_id=row.query) for row in result]
        
    return recommendation_history

@router.delete("/search/clear")
def clear_search_history(user_id: int):
    with db.engine.begin() as connection:
        result = connection.execute(sqlalchemy.text(
            """
            DELETE FROM search_history
            WHERE user_id = :user_id
            """), {"user_id": user_id}
        )
        
        if result.rowcount == 0:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="No search history to clear"
            )
        
    return {"message": "Search history cleared"}

@router.delete("/recommendation/clear")
def clear_recommendation_history(user_id: int):
    with db.engine.begin() as connection:
        result = connection.execute(sqlalchemy.text(
            """
            DELETE FROM recommendation_history
            WHERE user_id = :user_id
            """), {"user_id": user_id}
        )
        
        if result.rowcount == 0:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="No recommendation history to clear"
            )
        
    return {"message": "Recommendation history cleared"}