# Example workflow CREATE -- USER

<Create user /user/ (POST)
{
"username": "string"
}>

# Testing results

<Repeated for each step of the workflow>
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

<Repeated for each step of the workflow>
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
"username": "string"
}>

# Testing results

<Repeated for each step of the workflow>
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

<Repeated for each step of the workflow>
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

<Repeated for each step of the workflow>
1. The curl statement called:
    curl -X 'POST' \
      'https://musicrecs.onrender.com/playlist/6/remove/2' \
      -H 'accept: application/json' \
      -H 'access_token: musicrecs' \
      -d ''
2. The response received in executing the curl statement:
    Response Body:
      "OK"

# Example workflow SET -- RATING

<Update rating /rating/{user_id}/{track_id} (PUT)
{
"value": int
}>

# Testing results

<Repeated for each step of the workflow>
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
