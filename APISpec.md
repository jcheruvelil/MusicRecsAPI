# API Specification for Music Recommendation System

## 1. Searching

### 1.6. Search Music System Library - `/search/` (GET)
Searches for tracks based on specified query parameters.

**Query Parameters**:

- `track` : The name of the track.
- `album` (optional): The name of the album.
- `artist` (optional): The name of the artist.

**Response**:

The API returns a JSON object with the following structure:

- `results`: An array of objects, each representing a track. Each track object has the following properties:
    - `track_id` : The unique track_id of the track.
    - `track`   : The name of the track.
    - `album`   : The name of the album.
    - `artist`  : The name of the artist.


## 2. Recommendations

### 2.1 Get Song Recommendation from Another Song
Returns list of 10 similar songs that user may enjoy based on inputted track.

**Query Parameters**:

- `track_id` : The unique track_id of the track.

**Response**:

The API returns a JSON object with the following structure:

- `results`: An array of objects, each representing a track. Each track object has the following properties:
    - `track_id` : The unique track_id of the track.
    - `track`   : The name of the track.
    - `album`   : The name of the album.
    - `artist`  : The name of the artist.