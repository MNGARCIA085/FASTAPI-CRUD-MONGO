from fastapi import APIRouter, Body, Request, Response, HTTPException, status
from fastapi.encoders import jsonable_encoder
from typing import List
from .models import Movie,MovieUpdate


# las movies las cargo desde un script


async def add_movie(request: Request, movie: Movie = Body(...)): #async
    movie = jsonable_encoder(movie)
    new_movie = request.app.database["movies"].insert_one(movie)
    created_movie = request.app.database["movies"].find_one(
        {"_id": new_movie.inserted_id}
    )
    return created_movie


def list_movies(request:Request):
    return list(request.app.database['movies'].find(limit=100))




async def find_movie(id:str, request:Request):
    if (movie := request.app.database["movies"].find_one({"_id": id})) is not None:
        return movie
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Movie with ID {id} not found")



