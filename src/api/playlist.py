from fastapi import HTTPException, status, APIRouter, Depends, Request
from pydantic import BaseModel
from src.api import auth

import sqlalchemy
from src import database as db


router = APIRouter(
    prefix="/playlist",
    tags=["playlist"],
    dependencies=[Depends(auth.get_api_key)],
)
    
class Playlist(BaseModel):
    playlist_name: str

@router.get("/{playlist_id}")
def get_playlist(playlist_id: int):
    playlist_results = []

    with db.engine.begin() as connection:
        try:
            playlist_name = connection.execute(sqlalchemy.text("SELECT playlist_name FROM playlists WHERE id = :playlist_id"),
                                            {"playlist_id": playlist_id}).scalar_one()

        except:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST, 
                detail="Playlist does not exist"
            )
        
        result = connection.execute(sqlalchemy.text("""
                                                    SELECT tracks.track_id, artists, album_name, track_name
                                                    FROM playlist_tracks
                                                    JOIN tracks ON tracks.track_id = playlist_tracks.track_id
                                                    WHERE playlist_id = :playlist_id
                                                    """), {"playlist_id": playlist_id})
        
        for row in result:
            playlist_results.append({
                "track_id": row.track_id,
                "track": row.track_name,
                "album": row.album_name,
                "artist": row.artists,
            })

        return {f"{playlist_name}: ": playlist_results}

@router.post("/{user_id}")
def create_playlist(user_id: int, playlist: Playlist):
    with db.engine.begin() as connection:
        # Check if user exists
        result = connection.execute(sqlalchemy.text(
            f"""
            SELECT COUNT(*)
            FROM users
            WHERE id = :user_id
            """),
            {"user_id": user_id}
        ).scalar_one()
        
        if result < 1:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"User with id {user_id} does not exist"
            )
        
        # Check if user already has a playlist with this name
        result = connection.execute(sqlalchemy.text(
            f"""
            SELECT COUNT(*)
            FROM playlists
            JOIN users ON playlists.user_id = users.id
            WHERE 
                users.id = :user_id AND
                playlists.playlist_name = :playlist_name
            """),
            {"user_id": user_id, "playlist_name": playlist.playlist_name}
        ).scalar_one()
        
        if result != 0:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT, 
                detail=f"Playlist with name {playlist.playlist_name} already exists"
            )
        
        # Add the playlist
        playlist_id = connection.execute(
            sqlalchemy.text(
                f"""
                INSERT INTO playlists (user_id, playlist_name)
                VALUES (:user_id, :playlist_name)
                RETURNING id
                """
            ),
            {"user_id": user_id, "playlist_name": playlist.playlist_name}
        ).scalar_one()
        
    return {"playlist_id": playlist_id}

@router.post("/{playlist_id}/add/{track_id}")
def add_song_to_playlist(playlist_id: int, track_id: str):
    with db.engine.begin() as connection:
        # Check if playlist exists
        result = connection.execute(sqlalchemy.text(
            f"""
            SELECT COUNT(*)
            FROM playlists
            WHERE id = :playlist_id
            """),
            {"playlist_id": playlist_id}
        ).scalar_one()
        
        if result < 1:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST, detail="Playlist does not exist"
            )
            
        # Check if track exists
        result = connection.execute(sqlalchemy.text(
            f"""
            SELECT COUNT(*)
            FROM tracks
            WHERE track_id = :track_id
            """),
            {"track_id": track_id}
        ).scalar_one()
        
        if result != 0:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST, detail="Track does not exist"
            )
        
        # Check if playlist contains track already
        result = connection.execute(sqlalchemy.text(
            f"""
            SELECT COUNT(*)
            FROM playlist_tracks
            WHERE 
                playlist_id = :playlist_id AND
                track_id = :track_id
            """),
            {"playlist_id": playlist_id, "track_id": track_id}
        ).scalar_one()
        
        if result < 1:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST, detail="Playlist already contains this track"
            )
        
        # Add track to playlist
        connection.execute(sqlalchemy.text(
            f"""
            INSERT INTO playlist_tracks (playlist_id, track_id)
            VALUES (:playlist_id, :track_id)"""),
            {"playlist_id": playlist_id, "track_id": track_id}
        )
        
    return "OK"

@router.delete("/{playlist_id}/remove/{track_id}")
def remove_song_from_playlist(playlist_id: int, track_id: str):
    with db.engine.begin() as connection:
        result = connection.execute(sqlalchemy.text(
            f"""
            DELETE
            FROM playlist_tracks
            WHERE 
                playlist_id = :playlist_id AND
                track_id = :track_id
            """),
            {"playlist_id": playlist_id, "track_id": track_id}
        )
        
    return "OK"
    