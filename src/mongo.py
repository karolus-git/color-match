from pymongo import MongoClient
from pymongo import ASCENDING, DESCENDING

from settings import MONGO_HOST
from settings import MONGO_PORT
from settings import MONGO_DATABASE
from settings import MONGO_TABLE
from settings import MONGO_USER
from settings import MONGO_PWD

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