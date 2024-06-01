from pymongo import MongoClient
from os import getenv

try:
    db_client = MongoClient()
    #TODO: complete client uri
except:
    db_client = MongoClient(host=getenv('DB_HOST'), port=int(getenv('DB_PORT')))
