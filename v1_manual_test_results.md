# Example workflow

<
Search
4.1 /search
Request:

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

Response:

{
"song_id”: int
},

>

# Testing results

<Repeated for each step of the workflow>
1. The curl statement called. You can find this in the /docs site for your 
API under each endpoint. For example, for my site the /catalogs/ endpoint 
curl call looks like:
curl -X 'GET' \
  'https://centralcoastcauldrons.vercel.app/catalog/' \
  -H 'accept: application/json'
2. The response you received in executing the curl statement.
