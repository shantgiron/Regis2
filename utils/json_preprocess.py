import datetime

import pytz
from pymongo import MongoClient

query = {}
query['year'] = {u"$exists":"true"}
projection = {}
sort = {}


with MongoClient("mongodb://localhost:27017/") as client:
    database = client["kb"]
    collection = database["Calendarios"]
    docs = collection.find({})
    #matches = []
    unset = {u"$unset": {"year": "", "month": "", "day": ""}}
    for doc in docs:
        year = 2018
        mes = int(doc['mes'])
        dia = int(doc['dia'])
        update = {}
        update["$set"] = {u'date': datetime.datetime(year, mes, dia, tzinfo=pytz.timezone('America/Santo_Domingo')
            )}
        collection.update_one(
        {'_id':doc['_id']},
        update=update,
        )




