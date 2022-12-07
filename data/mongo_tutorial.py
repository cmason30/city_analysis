import pymongo
from pymongo import MongoClient
import json
import datetime

# with open("interim/test1.json", "r") as f:
#     data = json.load(f)
class MongoDBConn:

    def __init__(self, host: str, port: int, database: str):#user: str, password: str):

        self.host = host
        self.port = port
        #self.user = user
        #self.password = password
        self.database = database

        self._client = pymongo.MongoClient(self.host, self.port)
        self._db = self._client[self.database]
        self._collection = self._db.sample_collection

    def close(self):
        self._client.close()

    def insert_one(self, dict_):
        self._collection.insert_one(dict_)


# def insert_day(json_file, connection="localhost", port=27017):
#
#     client = MongoClient(connection, port)
#
#     mydb = client['test_city']
#
#     mycol = mydb["SubredditData"] # table
#
#     mycol.insert_one(json_file)

if __name__ == "__main__":
    pass

