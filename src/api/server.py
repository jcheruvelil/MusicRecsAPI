import sqlalchemy
from fastapi import FastAPI, exceptions
from fastapi.responses import JSONResponse
from pydantic import ValidationError
from src.api import search, user, recs, playlist, ratings
import json
import logging
import sys
from starlette.middleware.cors import CORSMiddleware

import sqlalchemy
from src import database as db

description = """
MusicRecs is the premier recommendation site for all your musical desires.
"""

app = FastAPI(
    title="MusicRecs API",
    description=description,
    version="0.0.1",
    terms_of_service="http://example.com/terms/",
    contact={
        "name": "Asa Grote",
        "email": "agrote@calpoly.edu",
    },
)

# origins = ["https://potion-exchange.vercel.app"]

# app.add_middleware(
#     CORSMiddleware,
#     allow_origins=origins,
#     allow_credentials=True,
#     allow_methods=["GET", "OPTIONS"],
#     allow_headers=["*"],
# )

app.include_router(search.router)
app.include_router(user.router)
app.include_router(playlist.router)
app.include_router(recs.router)
app.include_router(ratings.router)

@app.exception_handler(exceptions.RequestValidationError)
@app.exception_handler(ValidationError)
async def validation_exception_handler(request, exc):
    logging.error(f"The client sent invalid data!: {exc}")
    exc_json = json.loads(exc.json())
    response = {"message": [], "data": None}
    for error in exc_json:
        response['message'].append(f"{error['loc']}: {error['msg']}")

    return JSONResponse(response, status_code=422)

@app.get("/")
async def root():
    return {"message": "Welcome to the MusicRecs API."}
