# API Specification for Music Recommendation System

## 1. User

### 1.1 Create User `/user` (POST)

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

### 1.2 Login `/user/login/` (GET)
Given a username that is already created, returns their userID.
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

### 1.3 Get user library `/user/{user_id}/library` (GET)
Given a user_id, displays a list of all of their created playlists.
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

### 2.1. Search Music System Library - `/search` (GET)
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

**Query Parameters**:

- `playlist_id` : The unique id of the playlist to add to.
- `track_id` : The unique track_id of the track to add.

### 3.3 Remove track from playlist - `/playlist/{playlist_id}/remove/{track_id}` (DELETE)

Removes track with track_id from playlist with playlist_id.

**Query Parameters**:

- `playlist_id` : The unique id of the playlist to remove from.
- `track_id` : The unique track_id of the track to remove.

### 3.4 Get Playlist - `/playlist/{playlist_id}` (GET)

Get all songs contained in playlist with playlist_id.

**Query Parameters**:

- `playlist_id` : The unique id of the playlist.


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

### 4.2 Get Song Recommendations from User Ratings - `/recs/ratings/{user_id}` - (GET)
Returns list of 10 similar songs that user may enjoy based on a user's rated songs.

**Query Parameters**:

- `user_id` : The ID of the user for which recommendations are to be fetched.

**Response**:

The API returns a JSON object with the following structure:

- `recommendations`: An array of objects, each representing a track. Each track object has the following properties:
    - `track_id` : The unique track_id of the track.
    - `track`   : The name of the track.
    - `album`   : The name of the album.
    - `artist`  : The name of the artist.

### 4.3 Get Song Recommendations from Playlist - `/recs/{playlist_id}` - (GET)
Returns list of 10 similar songs that user may enjoy based on a user's playlist.

**Query Parameters**:

- `playlist_id` : The ID of the playlist for which recommendations are to be fetched.

**Response**:

The API returns a JSON object with the following structure:

- `recommendations`: An array of objects, each representing a track. Each track object has the following properties:
    - `track_id` : The unique track_id of the track.
    - `track`   : The name of the track.
    - `album`   : The name of the album.
    - `artist`  : The name of the artist.


## 5. Ratings

### 5.1 Update Rating - `/rating/{user_id}/{track_id}` (POST)

Set rating of a track (rating between 0 and 10)

**Request**:

```json
{
  "value": "integer",
}
```

**Response**:

    "OK"


## 6. History

### 6.1 Get Search History - `/history/search` (GET)

Get 10 last search queries.

**Query Parameters**:

- `user_id` : The unique ID of the user for which search history should be fetched.

**Response**:

```json
{
    [
        {
            "query": "string"
        },
        {
            ...
        }
    ]
}
```


### 6.2 Get Recommendation History - `/history/recommendation` (GET)

Get 10 last track_id queries for recommendations.

**Query Parameters**:

- `user_id` : The unique ID of the user for which recommendation history should be fetched.

**Response**:

```json
{
    [
        {
            "input_track_id": "string"
        },
        {
            ...
        }
    ]
}
```

### 6.3 Clear Search History - `/history/search/clear` (DELETE)

**Query Parameters**:

- `user_id` : The unique ID of the user for which search history should be cleared.

**Response**:

```json
{
  "message": "Search history cleared"
}
```


### 6.4 Clear Recommendation History - `/history/recommendation/clear` (DELETE)

**Query Parameters**:

- `user_id` : The unique ID of the user for which recommendation history should be cleared.

**Response**:

```json
{
  "message": "Recommendation history cleared"
}
```