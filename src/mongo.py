import os
from pymongo import MongoClient
from pymongo import ASCENDING, DESCENDING
from dotenv import load_dotenv

MONGO_HOST = os.getenv('MONGO_HOST', "0.0.0.0")
MONGO_PORT = os.getenv('MONGO_PORT', 27017)
MONGO_DATABASE = os.getenv('MONGO_DATABASE', 'colormatch')
MONGO_TABLE = os.getenv('MONGO_TABLE', 'images')
MONGO_USER = os.getenv('MONGO_USER', 'root')
MONGO_PWD = os.getenv('MONGO_PWD', 'example')

def init_db():
    """Initialization of the mongo Databse

    Returns:
        collection: the desired collection
    """

    #Get a client
    client = MongoClient(f"mongodb://{MONGO_USER}:{MONGO_PWD}@{MONGO_HOST}:{MONGO_PORT}/")

    #Load the DB
    mongo_database = client[MONGO_DATABASE]

    #Get the collection and return it
    mongo_collection = mongo_database[MONGO_TABLE]

    return mongo_database, mongo_collection