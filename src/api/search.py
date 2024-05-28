from fastapi import APIRouter, Depends, Request
from src.api import auth
from enum import Enum

from datetime import datetime


import sqlalchemy
from src import database as db


router = APIRouter(
    prefix="/search",
    tags=["search"],
    dependencies=[Depends(auth.get_api_key)],
)

@router.get("/")
def search_tracks(
    user_id: int,
    track: str = "",
    artist: str = "",
    album: str = ""
):
    results = []
    query = ""
    # Use reflection to derive table schema.
    metadata_obj = sqlalchemy.MetaData()
    tracks = sqlalchemy.Table("tracks", metadata_obj, autoload_with=db.engine)
        
    stmt = (
        sqlalchemy.select(
            tracks.c.track_id,
            tracks.c.track_name,
            tracks.c.album_name, 
            tracks.c.artists
        )
        .limit(10)
        .order_by(tracks.c.track_name)
    )
    
    if track != "":
        stmt = stmt.where(tracks.c.track_name.ilike(f"%{track}%"))
        query += f'{track} '
    
    if album != "":
        stmt = stmt.where(tracks.c.album_name.ilike(f"%{album}%"))
        query += f'{album} '
    
    if artist != "":
        stmt = stmt.where(tracks.c.artists.ilike(f"%{artist}%"))
        query += f'{artist} '
        
    with db.engine.begin() as connection:
        result = connection.execute(stmt)

        for row in result:
            results.append({
                "track_id": row.track_id,
                "track": row.track_name,
                "album": row.album_name,
                "artist": row.artists,
            })

        connection.execute(sqlalchemy.text("""
                                           INSERT INTO search_history (user_id, query)
                                           VALUES (:user_id, :query)"""),
                                           {"user_id": user_id, "query": query})
    
    return {
        "results": results,
    }
    
        
    
