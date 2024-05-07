# Example workflow

<Create user /user/ (PUT)>

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

