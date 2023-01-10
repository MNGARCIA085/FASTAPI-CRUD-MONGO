
from fastapi import APIRouter, Body, Request, Response, HTTPException, status
from fastapi.encoders import jsonable_encoder
from typing import List
from .db_operations import add_movie,list_movies,find_movie
from .models import Movie,MovieUpdate,Review,MovieOut



#https://www.mongodb.com/languages/python/pymongo-tutorial

router = APIRouter(
    prefix="/movies",
    responses={404: {"description": "Not found"}},
    tags=['movies'],
)

@router.post("/", response_description="Create a new book", 
                status_code=status.HTTP_201_CREATED,
                response_model=MovieOut)
def create_movie(request: Request, movie: Movie = Body(...)):
    movie = jsonable_encoder(movie)
    new_movie = request.app.database["movies"].insert_one(movie)
    created_movie = request.app.database["movies"].find_one(
        {"_id": new_movie.inserted_id}
    )
    return created_movie





#https://stackoverflow.com/questions/30289071/calculate-the-average-of-fields-in-embedded-documents-array


@router.get("/", response_description="List all movies", response_model=List[MovieOut])
async def list_movies(request: Request, some: str | None = None): # acá van a estar los filtros
    
    return list(request.app.database['movies'].find(limit=100))



@router.get("/{id}", response_description="Get a single book by id", response_model=MovieOut)
async def find_movie(id: str, request: Request):

    from bson import ObjectId
    id = ObjectId(id)

    if (movie := request.app.database["movies"].find_one({"_id": id})) is not None:
        return movie
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Movie with ID {id} not found")




@router.put("/{id}", response_description="Update a movie", response_model=Movie)
def update_movie(id: str, request: Request, movie: MovieUpdate = Body(...)):
    movie = {k: v for k, v in movie.dict().items() if v is not None}

    if len(movie) >= 1:
        update_result = request.app.database["movies"].update_one(
            {"_id": id}, {"$set": movie}
        )

        if update_result.modified_count == 0:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Movie with ID {id} not found")

    if (
        existing_movie := request.app.database["movies"].find_one({"_id": id})
    ) is not None:
        return existing_movie

    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Movie with ID {id} not found")



@router.delete("/{id}", response_description="Delete a movie")
def delete_movie(id: str, request: Request, response: Response):
    delete_result = request.app.database["movies"].delete_one({"_id": id})

    if delete_result.deleted_count == 1:
        response.status_code = status.HTTP_204_NO_CONTENT
        return response

    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Movie with ID {id} not found")



"""

REVIEWS, we need to add it to a movie; see the reviews for a movie....

"""


@router.post("/{id}/reviews/", response_description="Add a review to a movie")
async def add_review(id: str, request: Request, review: Review = Body(...)):

    # que el usuario exista


    # que el usuario pueda ingresar una única review

    review = jsonable_encoder(review)
    update_result = request.app.database["movies"].update_one(
            {"_id": id}, {"$push": {'reviews':review}}
        )
    return {'Estado':'ok'}





# datos de las películas
# promedio de puntajes de todas las películas













"""

QUERIES AND AGGREGATE FOR LIST MOVIES


if some:
        return list(request.app.database['movies'].find({'title':some}))
    # other filters
    #return list(request.app.database['movies'].find({'reviews.score' : {"$gt":27}}))
    #return list(request.app.database['movies'].find({'genres' : {"$in":['drama']}}))
    #suma = request.app.database['movies'].aggregate([{'$group':{'_id' : '$title', 'totaldocs' : { '$sum' : 1 }}}])
    promedio = request.app.database['movies'].aggregate([
            {
                "$unwind":"$reviews"
            },
            {
                "$group": {
                    "_id": {
                        "_id": "$_id",
                        "title": "$title"
                        },
                    "reviews":{
                        "$push": "$reviews.score"
                    },
                    "reviews_average": {
                        "$avg": "$reviews.score"
                    }
                }
            },
            {
                "$project":{
                    "_id": 0,
                    "title": "$_id.title",
                    "reviews_average": 1,
                    "reviews": 1
                }
            }
    ])
    for p in promedio:
        print(p)




"""