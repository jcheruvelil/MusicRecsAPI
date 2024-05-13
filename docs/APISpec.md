# API Specification for Music Recommendation System

## User

### 1.1 Add User `/user/` (POST)

### 1.2 Login `/user/login/` (POST)

### 1.3 Get user library `/user/{user_id}/library` (GET)

## Recommendation

### 2.1 Get song recommendation `/recommendation/song` (GET)

**Request**:

```json

[
  {
    "song": "string",
    "artist": "string",
    "album": "string",
    "year": "integer"
  },
  {
    ...
  }
]
```

**Response**:

```json
{
  "song": "string",
  "artist": "string",
  "album": "string",
  "year": "integer"
}
```

### 2.2 `/recommendation/artist` (GET)

**Request**:

````json
[
  {
    "artist": "string"
  },
  {
    ...
  }
]


**Response**:
```json
{
    "artist": "string"
}
````

### 2.3 `/recommendation/album` (GET)

**Request**:

```json
[
  {
    "artist": "string",
    "album": "string",
    "year": "integer"
  },
  {
    ...
  }
]

```

**Response**:

```json

{
    "artist": "string",
    "album": "string",
    "year": "integer"
  },

```

## Rating

### 3.1 `/song/{song_id}/rating` (POST)

### 3.2 `/album/{album_id}/rating` (POST)

**Request**:

```json
[
  {
    "rating": "integer"
  }
]
```

**Response**:

```json
[
  {
    "confirmed": "success"
  }
]
```

## Search

### 4.1 `/search`

**Request**:

```json

[
  {
    "song": "string",
    "artist": "string",
    "album": "string",
    "year": "integer"
  },
  {
    ...
  }
]
```

**Response**:

```json

{
    "song_id”: "integer"
}
```

## History

### 5.1 Get Recommendation History - `/recommendation/history` (GET)

**Response**:

```json

[
  {
    "type": "string",
    "artist": "string",
    "album": "string",
    "year": "integer"
  },
  {
    ...
  }
]
```

### 5.2 Get Search History - `/search/history` (GET)

**Response**:

```json

[
  {
    "type": "string",
    "artist": "string",
    "album": "string",
    "year": "integer"
  },
  {
    ...
  }
]
```

### 5.3 Clear Recommendation History `/history/clear/`

**Response**:

```json
{
  "success": "boolean"
}
```

### 5.4 Clear Search History `/history/clear/`

**Response**:

```json
{
  "success": "boolean"
}
```

## Playlists

### 6.1 Get playlist `/playlists/{playlist_id}` (GET)

**Response**:

```json

[
  {
    "type": "string",
    "artist": "string",
    "album": "string",
    "year": "integer"
  },
  {
    ...
  }
]
```

### 6.2 Add song to playlist `/playlists/{playlist_id}` (PUT)

**Response**:

```json
{
  "success": "boolean"
}
```
