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

<Create user /user/ (PUT)
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

# Example workflow ADD SONG -- PLAYLIST

<Create user /user/ (PUT)
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

# Example workflow REMOVE SONG -- PLAYLIST

<Create user /user/ (PUT)
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

# Example workflow SET -- RATING

<Create user /user/ (PUT)
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
