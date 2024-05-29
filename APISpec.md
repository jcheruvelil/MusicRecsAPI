# API Specification for Music Recommendation System

## 1. User

### 1.1 Create User

Given a username, creates a user, returning their userID. 

**Request**:

```json
{
    "username": "string"
}
```
**Response**:

```json
{
    "user_id": "integer"
}
```

## 2. Searching

### 2.6. Search Music System Library - `/search` (GET)
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

## 3. Playlists 

### 3.1 Create playlist - `/playlist/{user_id}/` (POST)

Creates a playlist, returning the id of a playlist to use. Playlists are created by passing in your user id. 

**Request**:

```json
{
  "user_id": "integer"
}
```

**Response**:

```json
{
    "playlist_id": "integer"
}
```

### 3.2 Add track to playlist - `/playlist/{playlist_id}/add/{track_id}` (POST)

Adds track with track_id to playlist with playlist_id.

### 3.3 Remove track from playlist - `/playlist/{playlist_id}/remove/{track_id}` (POST)

Removes track with track_id from playlist with playlist_id.

## 4. Recommendations

### 4.1 Get Song Recommendation from Another Song - `/recs` - (GET)
Returns list of 10 similar songs that user may enjoy based on inputted track.

**Query Parameters**:

- `track_id` : The unique track_id of the track.

**Response**:

The API returns a JSON object with the following structure:

- `recommendations`: An array of objects, each representing a track. Each track object has the following properties:
    - `track_id` : The unique track_id of the track.
    - `track`   : The name of the track.
    - `album`   : The name of the album.
    - `artist`  : The name of the artist.

## 5. Ratings

### 5.1 Update Rating - `/rating/{user_id}/{track_id}` (POST)

**Request**:

```json
{
  "value": "integer",
}
```

## 6. History

### 6.1 Get Search History - `/history/search` (GET)

### 6.2 Get Recommendation History - `/history/recommendation` (GET)

### 6.3 Clear Search History - `/history/search/clear` (DELETE)

### 6.4 Clear Search History - `/history/recommendation/clear` (DELETE)

