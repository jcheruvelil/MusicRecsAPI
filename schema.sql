-- USERS
CREATE TABLE IF NOT EXISTS users (
    id SERIAL PRIMARY KEY,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    username VARCHAR(255) NOT NULL
);

-- TRACKS
CREATE TABLE IF NOT EXISTS tracks (
    id bigint NOT NULL,
    track_id text NOT NULL,
    artists text,
    album_name text NOT NULL,
    track_name text NOT NULL,
    popularity bigint NOT NULL,
    duration_ms bigint NOT NULL,
    'explicit' boolean NOT NULL,
    danceability real NOT NULL,
    energy real NOT NULL,
    'key' smallint NOT NULL,
    loudness real NOT NULL,
    mode smallint NOT NULL,
    speechiness real NOT NULL,
    acousticness real NOT NULL,
    instrumentalness double precision NOT NULL,
    liveness real NOT NULL,
    valence real NOT NULL,
    tempo real NOT NULL,
    time_signature smallint NOT NULL,
    track_genre text NOT NULL
    features_vector vector NOT NULL
)

-- PLAYLISTS
CREATE TABLE IF NOT EXISTS playlists (
    id SERIAL PRIMARY KEY,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    user_id INTEGER REFERENCES users(id),
    playlist_name VARCHAR(255)
);

-- PLAYLIST_TRACKS
CREATE TABLE IF NOT EXISTS playlist_tracks (
    id SERIAL PRIMARY KEY,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    playlist_id INTEGER REFERENCES playlists(id),
    track_id INTEGER REFERENCES tracks(id)
);

-- RATINGS
CREATE TABLE IF NOT EXISTS playlist_tracks (
    id SERIAL PRIMARY KEY,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    user_id INTEGER REFERENCES users(id),
    track_id INTEGER REFERENCES tracks(id),
    rating INTEGER REFERENCES rating(id)
);

-- SEARCH HISTORY
CREATE TABLE IF NOT EXISTS search_history (
    id SERIAL PRIMARY KEY,
    user_id INTEGER REFERENCES users(id),
    query VARCHAR(255) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
);

-- RECOMMENDATION HISTORY
CREATE TABLE IF NOT EXISTS recommendation_history (
    id SERIAL PRIMARY KEY,
    user_id INTEGER REFERENCES users(id),
    query VARCHAR(255) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
);