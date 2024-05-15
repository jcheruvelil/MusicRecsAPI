# Example workflow CREATE -- USER

<Create user /user/ (POST)
{
"username": "string"
}>

# Testing results

1. The curl statement called:
    curl -X 'POST' \
      'https://musicrecs.onrender.com/user/' \
      -H 'accept: application/json' \
      -H 'access_token: musicrecs' \
      -H 'Content-Type: application/json' \
      -d '{
      "username": "asa"
    }'
2. The response received in executing the curl statement:
    Response Body:
      "OK"

# Example workflow LOGIN -- USER

<Login user /user/login (POST)
{
"username": "string"
}>

# Testing results

1. The curl statement called:
    curl -X 'POST' \
      'https://musicrecs.onrender.com/user/login' \
      -H 'accept: application/json' \
      -H 'access_token: musicrecs' \
      -H 'Content-Type: application/json' \
      -d '{
      "username": "asa"
    }'
2. The response received in executing the curl statement:
    Response Body:
      "OK"

# Example workflow CREATE -- PLAYLIST

<Create playlist /playlist/ (PUT)
{
"playlist_name": "string"
}>

# Testing results

1. The curl statement called:
    curl -X 'POST' \
      'https://musicrecs.onrender.com/playlist/2' \
      -H 'accept: application/json' \
      -H 'access_token: musicrecs' \
      -H 'Content-Type: application/json' \
      -d '{
      "playlist_name": "playlist"
    }'
2. The response received in executing the curl statement:
    Response Body:
      {
        "playlist_id": 6
      }

# Example workflow ADD SONG -- PLAYLIST

<Add playlist /{playlist_id}/add/{track_id} (PUT)
{

}>

# Testing results

1. The curl statement called:
    curl -X 'POST' \
      'https://musicrecs.onrender.com/playlist/6/add/2' \
      -H 'accept: application/json' \
      -H 'access_token: musicrecs' \
      -d ''
2. The response received in executing the curl statement:
    Response Body:
      "OK"

# Example workflow REMOVE SONG -- PLAYLIST

<Remove playlist /{playlist_id}/remove/{track_id} (PUT)
{

}>

# Testing results

1. The curl statement called:
    curl -X 'POST' \
      'https://musicrecs.onrender.com/playlist/6/remove/2' \
      -H 'accept: application/json' \
      -H 'access_token: musicrecs' \
      -d ''
2. The response received in executing the curl statement:
    Response Body:
      "OK"

# Example workflow GET User Library

<Get Asa's library /user/{user_id}/library>

# Testing results

1. The curl statement called:
  curl -X 'GET' \
  'https://musicrecs.onrender.com/user/3/library' \
  -H 'accept: application/json' \
  -H 'access_token: musicrecs'

2. The response received in executing the curl statement:
  [
  {
    "playlist_id": 6,
    "playlist_title": "playlist"
  }
]

# Example workflow SET -- RATING

<Update rating /rating/{user_id}/{track_id} (PUT)
{
"value": int
}>

# Testing results

1. The curl statement called:
    curl -X 'POST' \
      'https://musicrecs.onrender.com/rating/3/2' \
      -H 'accept: application/json' \
      -H 'access_token: musicrecs' \
      -H 'Content-Type: application/json' \
      -d '{
      "value": 10
    }'
2. The response received in executing the curl statement:
    Response Body:
      "OK"


# Example workflow GET -- RECOMMENDATION
<GET recommendations from song All Star by Smash Mouth songid=3cfOd4CMv2snFaKAnMdnvK>

# Testing Results
1. The curl statement called:
  curl -X 'GET' \
  'https://musicrecs.onrender.com/recs/?track_id=3cfOd4CMv2snFaKAnMdnvK' \
  -H 'accept: application/json' \
  -H 'access_token: musicrecs'
2. The response received in executing the curl statement:
{
  "recommendations": [
    {
      "id": "1FvDJ9KGxcqwv1utyPL3JZ",
      "track": "This Charming Man - 2011 Remaster",
      "album": "The Smiths",
      "artist": "The Smiths"
    },
    {
      "id": "7CQhZA3qNDZBoTKWqjD7gR",
      "track": "Give Me Your TMI",
      "album": "MAXIDENT",
      "artist": "Stray Kids"
    },
    {
      "id": "2LxdNADWier3MKTei8FbOY",
      "track": "I Was Made For Lovin' You (feat. Nile Rodgers & House Gospel Choir)",
      "album": "I Was Made For Lovin' You (feat. Nile Rodgers & House Gospel Choir)",
      "artist": "Oliver Heldens;Nile Rodgers;House Gospel Choir"
    },
    {
      "id": "2Cd9iWfcOpGDHLz6tVA3G4",
      "track": "Waka Waka (This Time for Africa) [The Official 2010 FIFA World Cup (TM) Song] (feat. Freshlyground)",
      "album": "Waka Waka (This Time for Africa) [The Official 2010 FIFA World Cup (TM) Song] (feat. Freshlyground)",
      "artist": "Shakira;Freshlyground"
    },
    {
      "id": "0Be7sopyKMv8Y8npsUkax2",
      "track": "Tacones Rojos",
      "album": "Tacones Rojos",
      "artist": "Sebastian Yatra"
    },
    {
      "id": "0Gbp9aWNohZ4Kwdi75ntzT",
      "track": "Love You Better",
      "album": "Made For You",
      "artist": "John De Sohn;Rasmus Hagen"
    },
    {
      "id": "21aOLk12MksET8AsbU0SI6",
      "track": "LO$ER=LO♡ER",
      "album": "The Chaos Chapter: FIGHT OR ESCAPE",
      "artist": "TOMORROW X TOGETHER"
    },
    {
      "id": "2kWowW0k4oFymhkr7LmvzO",
      "track": "Come with Me Now",
      "album": "Lunatic",
      "artist": "KONGOS"
    },
    {
      "id": "6ylDpki1VpIsc525KC1ojF",
      "track": "Tacones Rojos",
      "album": "Dharma",
      "artist": "Sebastian Yatra"
    },
    {
      "id": "4UuGBDjt8gLXsANZqZxMBz",
      "track": "Love You Better",
      "album": "Love You Better",
      "artist": "John De Sohn;Rasmus Hagen"
    }
  ]
}


