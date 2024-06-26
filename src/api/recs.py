from fastapi import APIRouter, Depends, Request
from src.api import auth
import sqlalchemy
import math
from src import database as db

from sqlalchemy import func, select, cast, text


song_feature_cols = ['popularity', 'duration_ms', 'danceability',
                     'energy', 'key', 'loudness', 'speechiness', 'acousticness', 'instrumentalness',
                     'liveness', 'valence', 'tempo', 'time_signature']

router = APIRouter(
    prefix="/recs",
    tags=["recs"],
    dependencies=[Depends(auth.get_api_key)],
)

@router.get("/{track_id}")
def get_rec(user_id: int, track_id: str):
    input_stmt = """
                SELECT features_vector
                FROM tracks
                WHERE track_id = :track_id
                """

    recs_stmt = """
        WITH input_vector AS (
            SELECT features_vector
            FROM tracks
            WHERE track_id = :track_id
        )
        SELECT
            t.track_id,
            t.track_name,
            t.album_name,
            t.artists,
            1 - (t.features_vector <=> input_vector.features_vector) AS similarity
        FROM tracks t, input_vector
        WHERE t.track_id != :track_id
        ORDER BY similarity DESC
        LIMIT 10;
    """
    
    with db.engine.begin() as connection:
        # Get the input vector
        input_vector = connection.execute(sqlalchemy.text(input_stmt), {"track_id": track_id}).fetchone()

        # If input_vector is None, it means the track_id is not found
        if input_vector is None:
            return []
        

        recs = []
        result = connection.execute(sqlalchemy.text(recs_stmt), [{"track_id": track_id}]).fetchall()

        connection.execute(sqlalchemy.text("""
                                           INSERT INTO recommendation_history (user_id, query)
                                           VALUES (:user_id, :input_track)"""),
                                           {"user_id": user_id, "input_track": track_id})

        for row in result:
            recs.append({
                    "id": row.track_id,
                    "track": row.track_name,
                    "album": row.album_name,
                    "artist": row.artists,
            })

        return{
            "recommendations": recs
        }
        
@router.get("/ratings/{user_id}")
def get_rec_from_ratings(user_id: int):
    input_stmt = """
        SELECT rating, features_vector
        FROM ratings
        JOIN tracks ON tracks.track_id = ratings.track_id
        WHERE user_id = :user_id
        """
    
    ratings_vector = [0 for i in range(13)]
    num_results = 0
    
    with db.engine.connect() as connection: 
        result = connection.execute(
            sqlalchemy.text(
                input_stmt
            ),
            {"user_id": user_id}
        )
        
        for row in result:
            num_results+=1
            features_string = row.features_vector.strip('[]')
            features_list = features_string.split(',')
            features_array = [float(i) for i in features_list]
            for i, value in enumerate(features_array):
                ratings_vector[i] += value * row.rating
    
    if num_results == 0:
        return []
    
    # Normalize the vector
    magnitude = math.sqrt(sum(v**2 for v in ratings_vector))
    
    ratings_vector = [v/magnitude for v in ratings_vector]
        
    # Get recommendations
    recs_stmt = """
        SELECT
            t.track_id,
            t.track_name,
            t.album_name,
            t.artists,
            1 - (t.features_vector <=> :ratings_vector) AS similarity
        FROM tracks t
        WHERE t.track_id NOT IN (
            SELECT track_id 
            FROM ratings
            WHERE user_id = :user_id
        )
        ORDER BY similarity DESC
        LIMIT 10;
    """
    
    with db.engine.begin() as connection:
        recs = []
        result = connection.execute(sqlalchemy.text(recs_stmt), [{"user_id": user_id, "ratings_vector": str(ratings_vector)}]).fetchall()

        for row in result:
            recs.append({
                    "id": row.track_id,
                    "track": row.track_name,
                    "album": row.album_name,
                    "artist": row.artists,
            })

        return{
            "recommendations": recs
        }
    
@router.get("/{playlist_id}")
def get_rec_from_playlist(playlist_id: int):
    input_stmt = """
        SELECT features_vector
        FROM playlist_tracks
        JOIN tracks ON tracks.track_id = playlist_tracks.track_id
        WHERE playlist_id = :playlist_id
        """
    
    playlist_vector = [0 for i in range(13)]
    num_results = 0
    
    with db.engine.connect() as connection: 
        result = connection.execute(
            sqlalchemy.text(
                input_stmt
            ),
            {"playlist_id": playlist_id}
        )
        
        for row in result:
            num_results+=1
            features_string = row.features_vector.strip('[]')
            features_list = features_string.split(',')
            features_array = [float(i) for i in features_list]
            for i, value in enumerate(features_array):
                playlist_vector[i] += value
    
    if num_results == 0:
        return []
    
    # Normalize the vector
    magnitude = math.sqrt(sum(v**2 for v in playlist_vector))
    
    print(f"magnitude: {magnitude}")
    playlist_vector = [v/magnitude for v in playlist_vector]

    # Get recommendations
    recs_stmt = """
        SELECT
            t.track_id,
            t.track_name,
            t.album_name,
            t.artists,
            1 - (t.features_vector <=> :playlist_vector) AS similarity
        FROM tracks t
        WHERE t.track_id NOT IN (
            SELECT track_id FROM playlist_tracks
            WHERE playlist_id = :playlist_id
            )
        ORDER BY similarity DESC
        LIMIT 10;
    """
    
    with db.engine.begin() as connection:
        recs = []
        result = connection.execute(sqlalchemy.text(recs_stmt), [{"playlist_id": playlist_id, "playlist_vector": str(playlist_vector)}]).fetchall()

        for row in result:
            recs.append({
                    "id": row.track_id,
                    "track": row.track_name,
                    "album": row.album_name,
                    "artist": row.artists,
            })

        return{
            "recommendations": recs
        }
    
            
        
        
    