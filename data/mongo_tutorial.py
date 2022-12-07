import pymongo
from pymongo import MongoClient
import datetime
post = {"author": "Mike",
        "text": "My first blog post!",
        "tags": ["mongodb", "python", "pymongo"],
        "date": datetime.datetime.utcnow()}

client = MongoClient('localhost', 27017)

mydb = client['mydb']

mycol=mydb["people"]

data = {"name": "john", 'age':30}

mycol.insert_one(data)
