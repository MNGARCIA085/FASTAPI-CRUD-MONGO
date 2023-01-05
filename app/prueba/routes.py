
from fastapi import APIRouter, Body, Request,status
from fastapi.encoders import jsonable_encoder
from typing import List
from .models import Prueba
from database import db



router = APIRouter(
    prefix="/prueba",
    responses={404: {"description": "Not found"}},
    tags=['prueba'],
)


@router.post("/", response_description="Create a new book", 
                status_code=status.HTTP_201_CREATED)
async def add_movie(request: Request, prueba: Prueba = Body(...)):
    movie = jsonable_encoder(prueba)
    new_movie = db["prueba"].insert_one(movie)
    created_movie = db["prueba"].find_one(
        {"_id": new_movie.inserted_id}
    )
    return created_movie

