import os
os.environ['RUN_ENV'] = 'test'


from fastapi import FastAPI
from pymongo import MongoClient
from settings import settings
from movies import routes as movies_routes
import pytest




app = FastAPI()


@app.on_event("startup")
def startup_db_client():
    app.mongodb_client = MongoClient(settings.DB_URI_TEST)
    app.database = app.mongodb_client[settings.DB_NAME_TEST] # movies_test

@app.on_event("shutdown")
def shutdown_db_client():
    #pass
    app.database.drop_collection("movies")
    app.mongodb_client.close()
    


app.include_router(movies_routes.router)



"""
client = motor.motor_asyncio.AsyncIOMotorClient(os.environ["MONGODB_URL"])
db = client.college
"""






""" FXITURES """
#str(bson.Binary.from_uuid(uuid.UUID)),
import uuid,bson
# add an user to the database
@pytest.fixture(scope='function')
def add_movie():
    def _add_movie(title, genres=[]):

        new_movie = app.database["movies"].insert_one(
            {
                "_id":str(uuid.uuid4()),
                "title": title,
                "genres":genres,
            }
        )


        return new_movie
    return _add_movie
