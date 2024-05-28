from fastapi import APIRouter, Depends, Request
from src.api import auth
import sqlalchemy
from src import database as db


song_feature_cols = ['popularity', 'duration_ms', 'danceability',
                     'energy', 'key', 'loudness', 'speechiness', 'acousticness', 'instrumentalness',
                     'liveness', 'valence', 'tempo', 'time_signature']

router = APIRouter(
    prefix="/recs",
    tags=["recs"],
    dependencies=[Depends(auth.get_api_key)],
)

@router.get("/")
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
