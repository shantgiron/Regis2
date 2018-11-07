from pymongo import MongoClient


class Database(object):
    _instance = None

    def __new__(cls, db, collection):
        if cls._instance is None:
            cls._instance = object.__new__(cls)
            # normally the db_credenials would be fetched from a config file or the enviroment
            try:
                print('connecting to database...')
                cls._instance.connection = MongoClient("mongodb://localhost:27017/")
                cls._instance.database = cls._instance.connection[db]
                # cls._instance.collection = cls._instance.database[collection]

            except Exception as error:
                print('Error: connection not established {}'.format(error))
                cls._instance = None
        else:
            print('connection established')
        return cls._instance

    def __init__(self, db, collection):
        self.collection = self.database[collection]
        print("collection is "+collection)

    def __del__(self):
        self.connection.close()
