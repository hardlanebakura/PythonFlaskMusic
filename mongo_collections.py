from pymongo import MongoClient
import os

MONGODB_CONNECTION = os.getenv('MONGODB_CONNECTION')
#MONGODB_CONNECTION = dotenv_values("mdc.env")["MONGODB_CONNECTION"]

class DatabaseAtlas(object):

    client = MongoClient(MONGODB_CONNECTION, serverSelectionTimeoutMS = 2000)
    db = client["test"]

    @staticmethod
    def insertOne(col, data):
        return DatabaseAtlas.db[col].insert_one(data)

    @staticmethod
    def insertMany(col, data):
        return DatabaseAtlas.db[col].insert_many(data)

    @staticmethod
    def find(col, query):
        return DatabaseAtlas.db[col].find_one(query, {"_id":0})

    @staticmethod
    def findAll(col, query):
        findlist = [i for i in DatabaseAtlas.db[col].find(query, {"_id":0})]
        return findlist

    @staticmethod
    def findFields(col, query, *fields):
        dict_fields = {}
        for field in fields:
            dict_fields[field] = 1
            dict_fields["_id"] = 0
        findlist = [i for i in DatabaseAtlas.db[col].find(query, dict_fields)]
        return findlist

    @staticmethod
    def dropCol(col):
        c = DatabaseAtlas.db[col].drop()
        return c

print(DatabaseAtlas.db.list_collection_names())

