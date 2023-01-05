from fastapi import FastAPI
from pymongo import MongoClient
from routes import router as book_router
from movies import routes as movies_routes
from settings import settings


app = FastAPI()




@app.on_event("startup")
def startup_db_client():
    app.mongodb_client = MongoClient(settings.DB_URI)
    app.database = app.mongodb_client[settings.DB_NAME]

@app.on_event("shutdown")
def shutdown_db_client():
    app.mongodb_client.close()
    



#from prueba import routes as prueba_router
#app.include_router(prueba_router.router)


app.include_router(book_router, tags=["books"], prefix="/book")


app.include_router(movies_routes.router)












