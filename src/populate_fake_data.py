import sqlalchemy
import os
import dotenv
from faker import Faker
import numpy as np
from sqlalchemy import create_engine
import random

import datetime


def database_connection_url():
    dotenv.load_dotenv()
    return os.environ.get("LOCAL_POSTGRES_URI")

engine = create_engine(database_connection_url(), pool_pre_ping=True)


# SETUP SCHEMA
def setup_schema():
    with engine.begin() as conn:
        conn.execute(sqlalchemy.text("""
            DROP TABLE IF EXISTS users CASCADE;
            DROP TABLE IF EXISTS playlists CASCADE;
            DROP TABLE IF EXISTS playlist_tracks;
            DROP TABLE IF EXISTS ratings;
            DROP TABLE IF EXISTS search_history;
            DROP TABLE IF EXISTS recommendation_history;
            
            CREATE TABLE
                users (
                    id bigint generated by default as identity,
                    created_at timestamp with time zone not null default now(),
                    username text not null,
                    constraint users_pkey primary key (id),
                    constraint users_username_key unique (username)
                ) tablespace pg_default;
            
            CREATE TABLE
                playlists (
                    id bigint generated by default as identity,
                    created_at timestamp with time zone not null default now(),
                    user_id bigint not null,
                    playlist_name text not null,
                    constraint playlists_pkey primary key (id),
                    constraint playlists_user_id_fkey foreign key (user_id) references users (id)
                ) tablespace pg_default;
            
            CREATE TABLE 
                playlist_tracks (
                    id bigint generated by default as identity,
                    created_at timestamp with time zone not null default now(),
                    playlist_id bigint not null,
                    track_id text not null,
                    constraint playlist_tracks_pkey primary key (id),
                    constraint playlist_tracks_playlist_id_fkey foreign key (playlist_id) references playlists (id),
                    constraint playlist_tracks_track_id_fkey foreign key (track_id) references tracks (track_id)
                ) tablespace pg_default;
                
            CREATE TABLE
                ratings (
                    id bigint generated by default as identity,
                    created_at timestamp with time zone not null default now(),
                    user_id bigint not null,
                    track_id text not null,
                    rating bigint null,
                    constraint ratings_pkey primary key (id),
                    constraint ratings_track_id_fkey foreign key (track_id) references tracks (track_id),
                    constraint ratings_user_id_fkey foreign key (user_id) references users (id)
                ) tablespace pg_default;
                
            CREATE TABLE 
                search_history (
                    id bigint generated by default as identity,
                    created_at timestamp with time zone not null default now(),
                    user_id bigint not null,
                    query text null,
                    constraint search_history1_pkey primary key (id),
                    constraint search_history1_user_id_fkey foreign key (user_id) references users (id)
                ) tablespace pg_default;
                
            CREATE TABLE
                recommendation_history (
                    id bigint generated by default as identity,
                    created_at timestamp with time zone not null default now(),
                    user_id bigint not null,
                    query text null,
                    constraint recommendation_history1_pkey primary key (id),
                    constraint recommendation_history1_user_id_fkey foreign key (user_id) references users (id)
                ) tablespace pg_default;
                
        """))
        
    
def populate_fake_data(num_users: int):
    
    # GET ALL DB SONGS (USED FOR FAKE DATA)
    songs = []
    with engine.begin() as conn:
        tracks = conn.execute(sqlalchemy.text("""
            SELECT track_id, artists, album_name, track_name FROM tracks
        """))
        
        for t in tracks:
            songs.append({
                "track_id": t.track_id,
                "artists": t.artists,
                "album_name": t.album_name,
                "track_name": t.track_name,
            })
    total_num_songs = len(songs)
            

    # GENERATE FAKE DATA
    # num_users = 200000

    fake = Faker()
    playlists_sample_distribution = np.random.default_rng().negative_binomial(n=20, p=0.5, size=num_users)
    ratings_sample_distribution = np.random.default_rng().negative_binomial(n=0.1, p=0.01, size=num_users)
    # search_sample_distribution = np.random.default_rng().negative_binomial(n=750, p=0.5, size=num_users)
    search_sample_distribution = np.random.default_rng().negative_binomial(n=0.8, p=0.001, size=num_users)
    # search_sample_distribution = np.random.default_rng().negative_binomial(n=100, p=0.5, size=num_users)
    # rec_sample_distribution = np.random.default_rng().negative_binomial(n=0.04, p=0.001, size=num_users)
    # rec_sample_distribution = np.random.default_rng().negative_binomial(n=750, p=0.5, size=num_users)
    rec_sample_distribution = np.random.default_rng().negative_binomial(0.8, 0.001, size=num_users)

    # ratings = np.random.randint(10, size=(num_users*num_rating_per_user))
    # print(ratings)
    # print(f"max rating: {max(ratings)}")
    # print(f"min rating: {min(ratings)}")


    print(playlists_sample_distribution)
    print(f"max num_playlists: {max(playlists_sample_distribution)}")
    print(f"min num_playlists: {min(playlists_sample_distribution)}")
    print(f"avg num_playlists: {sum(playlists_sample_distribution)/num_users}")
    print(ratings_sample_distribution)
    print(f"max rating: {max(ratings_sample_distribution)}")
    print(f"min rating: {min(ratings_sample_distribution)}")
    print(f"avg rating: {sum(ratings_sample_distribution)/num_users}")
    print(search_sample_distribution)
    print(f"max search: {max(search_sample_distribution)}")
    print(f"min search: {min(search_sample_distribution)}")
    print(f"avg search: {sum(search_sample_distribution)/num_users}")
    print(rec_sample_distribution)
    print(f"max rec: {max(rec_sample_distribution)}")
    print(f"min rec: {min(rec_sample_distribution)}")
    print(f"avg rec: {sum(rec_sample_distribution)/num_users}")
    
    # with engine.begin() as conn:
    print("creating fake MusicRecs users...")
    
    for user_num in range(num_users):
        username = fake.unique.user_name()
        # print(username)
        
        # Create user
        before = datetime.datetime.now()
        
        with engine.begin() as conn:
            user_id = conn.execute(
                sqlalchemy.text("""
                    INSERT INTO users (username) VALUES (:username) RETURNING id;
                """), {"username": username}).scalar_one();
            
        after = datetime.datetime.now()
        
        print(f"time to create user: {(after-before).total_seconds()}")
        
        # Create playlists
        before = datetime.datetime.now()
        num_playlists = playlists_sample_distribution[user_num]

        # Determine the number of songs that will be in each playlist
        songs_sample_distribution =  np.random.default_rng().negative_binomial(n=0.6, p=0.005, size=1000)
        
        for playlist_num in range(num_playlists):
            # playlist_name = fake.word().title()
            music_words = ['harmony', 'melody', 'rhythm', 'beat', 'note', 'chorus', 'tune', 'symphony', 'tempo', 'instrument', 
                'groove', 'bass', 'lyric', 'vibe', 'jam', 'sound', 'acoustic', 'electric', 'fusion', 'loop']
            playlist_words = ['mix', 'party', 'chill', 'vibes', 'session', 'playlist', 'journey', 'escape', 'serenade', 'anthem']
            ext_word_list = music_words + playlist_words

            playlist_name = ' '.join(fake.words(nb=2, unique=True, ext_word_list=music_words)).title()

            # print(playlist_name)
            
            with engine.begin() as conn:
                playlist_id = conn.execute(
                sqlalchemy.text("""
                    INSERT INTO playlists (user_id, playlist_name) VALUES (:user_id, :playlist_name) RETURNING id;
                """), {"user_id": user_id, "playlist_name": playlist_name}).scalar_one();
            
            num_songs = songs_sample_distribution[playlist_num]
            # print(num_songs)
            
            songs_to_add = []
            
            song_dist = np.random.randint(total_num_songs, size=(num_songs))
            for song_num in range(num_songs):
                song = songs[song_dist[song_num]]
                songs_to_add.append({"playlist_id": playlist_id, "track_id": song["track_id"]})

            if songs_to_add:
                with engine.begin() as conn:
                    conn.execute(
                        sqlalchemy.text("""
                            INSERT INTO playlist_tracks (playlist_id, track_id) 
                            VALUES (:playlist_id, :track_id);"""), 
                        songs_to_add
                    )
                    
        after = datetime.datetime.now()
        
        print(f"time to create playlists: {(after-before).total_seconds()}")
        
        # Create ratings
        before = datetime.datetime.now()
        num_ratings = ratings_sample_distribution[user_num]
        ratings = np.random.randint(10, size=(num_ratings))
        
        ratings_to_add = []
        for rating_num in range(num_ratings):
            song = songs[random.randint(0, total_num_songs)]
            rating = int(ratings[rating_num])
            # print(f"song: {song}, rating: {rating}")
            ratings_to_add.append({"user_id": user_id, "track_id": song["track_id"], "rating": rating})
        
        if ratings_to_add:
            with engine.begin() as conn:
                conn.execute(
                    sqlalchemy.text("""
                        INSERT INTO ratings (user_id, track_id, rating) 
                        VALUES (:user_id, :track_id, :rating);"""
                    ), 
                    ratings_to_add
                )
        after = datetime.datetime.now()
        
        print(f"time to create ratings: {(after-before).total_seconds()}")
            
        # Execute rec requests -> populate rec history
        before = datetime.datetime.now()
        num_recs = rec_sample_distribution[user_num]
        if num_recs:
            # print(f"executing {num_recs} recs")
            song_dist = np.random.randint(total_num_songs, size=(num_recs))
            recs = []
            for rec_num in range(num_recs):
                song = songs[song_dist[rec_num]]
                recs.append({"user_id": user_id, "input_track": song["track_name"]})
                          
            with engine.begin() as conn:
                conn.execute(sqlalchemy.text("""
                    INSERT INTO recommendation_history (user_id, query)
                    VALUES (:user_id, :input_track)"""),
                    recs)
                    
        after = datetime.datetime.now()
        
        print(f"time to execute rec requests: {(after-before).total_seconds()}")
            
        # Execute searches -> populate search history
        before = datetime.datetime.now()
        num_searches = search_sample_distribution[user_num]
        if num_searches:
                
            # print(f"executing {num_searches} searches")
            
            search_dist = np.random.randint(total_num_songs, size=(num_searches))
            songs_to_search = []
            for search_num in range(num_searches):
                song = songs[song_dist[rec_num]]
                songs_to_search.append({"user_id": user_id, "query": song["track_name"]}) 
                
            with engine.begin() as conn:
                conn.execute(sqlalchemy.text("""
                    INSERT INTO search_history (user_id, query)
                    VALUES (:user_id, :query)"""),
                    songs_to_search)
                
        after = datetime.datetime.now()
        
        print(f"time to execute searches: {(after-before).total_seconds()}")
            
            
if __name__ == "__main__":
    # setup_schema()
    populate_fake_data(10)

        
if __name__ == "__main__":
    # setup_schema()
    populate_fake_data(25)
                
                
                
        
    
    