from fastapi import HTTPException, status, APIRouter, Depends, Request
from pydantic import BaseModel
from typing import List
from src.api import auth

import sqlalchemy
from src import database as db

router_history = APIRouter(
    prefix="/history",
    tags=["history"],
    dependencies=[Depends(auth.get_api_key)],
)

class HistoryItem(BaseModel):
    id: int
    user_id: int
    query: str
    timestamp: str

@router_history.get("/search/history", response_model=List[HistoryItem])
def get_search_history(user_id: int):
    with db.engine.begin() as connection:
        result = connection.execute(sqlalchemy.text(
            """
            SELECT id, user_id, query, timestamp
            FROM search_history
            WHERE user_id = :user_id
            ORDER BY timestamp DESC
            """), {"user_id": user_id}
        ).fetchall()
        
        if not result:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="Search history not found"
            )
        
        search_history = [HistoryItem(id=row.id, user_id=row.user_id, query=row.query, timestamp=row.timestamp) for row in result]
        
    return search_history

@router_history.get("/recommendation/history", response_model=List[HistoryItem])
def get_recommendation_history(user_id: int):
    with db.engine.begin() as connection:
        result = connection.execute(sqlalchemy.text(
            """
            SELECT id, user_id, query, timestamp
            FROM recommendation_history
            WHERE user_id = :user_id
            ORDER BY timestamp DESC
            """), {"user_id": user_id}
        ).fetchall()
        
        if not result:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="Recommendation history not found"
            )
        
        recommendation_history = [HistoryItem(id=row.id, user_id=row.user_id, query=row.query, timestamp=row.timestamp) for row in result]
        
    return recommendation_history

@router_history.delete("/searchhistory/clear")
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

@router_history.delete("/recommendationhistory/clear")
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