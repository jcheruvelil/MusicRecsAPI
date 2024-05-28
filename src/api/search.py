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
    track: str = "",
    artist: str = "",
    album: str = "",
):
    results = []
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
    
    if album != "":
        stmt = stmt.where(tracks.c.album_name.ilike(f"%{album}%"))
    
    if artist != "":
        stmt = stmt.where(tracks.c.artists.ilike(f"%{artist}%"))
        
    with db.engine.begin() as connection:
        result = connection.execute(stmt)

        for row in result:
            results.append({
                "track_id": row.track_id,
                "track": row.track_name,
                "album": row.album_name,
                "artist": row.artists,
            })
    
    return {
        "results": results,
    }
    
        
    
