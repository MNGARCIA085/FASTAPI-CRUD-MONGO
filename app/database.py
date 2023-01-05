from pymongo import mongo_client
import pymongo
from settings import settings

client = mongo_client.MongoClient(settings.DB_URI)
print('Connected to MongoDB...')

db = client[settings.DB_NAME]



#User = db.users
#Post = db.posts
#User.create_index([("email", pymongo.ASCENDING)], unique=True)
#Post.create_index([("title", pymongo.ASCENDING)], unique=True)



#https://codevoweb.com/crud-restful-api-server-with-python-fastapi-and-mongodb/