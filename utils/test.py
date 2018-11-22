import locale
from datetime import datetime
import pytz
from Database import Database
from rasa_core_sdk import Action
from rasa_core_sdk.events import SlotSet


collection = Database('kb', 'Calendarios').collection


class t:
    @classmethod
    def Events(self):
        # type: (Dispatcher, DialogueStateTracker, Domain) -> List[Event]
        projection = {}
        sort = {}
        query = dict()
        """query = {
            "$or": [
                {
                    "date": {
                        "$gte": datetime.now(tz=pytz.timezone('America/Santo_Domingo'))
                    }
                },
                {
                    "evento.finaliza": {
                        "$gte": datetime.now(tz=pytz.timezone('America/Santo_Domingo'))
                    }
                }
            ]
        }"""
        evento = 'retiro'
        query["$text"] = {
            u"$search": evento
        }
        projection = {
            "score": {u"$meta": u"textScore"},
            "evento.nombre": 1,
            "date": 1,
                      }
        sort = [('score', {'$meta': 'textScore'}), (u"date", 1)]

        docs = collection.find(query, projection=projection, sort=sort)
        matches = []
        date = str()
        hoy = datetime.now()

        if docs.count() > 0:
            if docs[0]['score'] >= 0.800:
                if docs[0]['date'] >= hoy:
                    date = docs[0]['date']
                elif docs[0]['date'] < hoy <= docs[0]['evento']['finaliza']:
                    date = docs[0]['evento']['finaliza']
                print("high")
            else:
                for doc in docs:
                    event = doc['evento']['nombre']
                    matches.append(event)
                    print(doc)

        return []

    @classmethod
    def proceso(cls):
        collection = Database('kb', 'Users').collection
        proceso = "graduacion"
        if proceso:
            query = {
                "password" : str("321"),
                "matricula" : str("20121917")
            }

            result = collection.find_one(query)
            print(result['indice'])

    @classmethod
    def reqPemdiente(cls):

        collection = Database('kb', 'ReqPendientes').collection
        matricula = 20121917
        if matricula:
            query = {
                "matricula": matricula,
                'matricula': {'$exists': True}
            }
            projection = {
                "matricula": 1,
                "codTema": 1,
                "nombre": 1,
                "creditos": 1
            }
            result = collection.find(query, projection=projection)
            requisitos = [(doc["codTema"], doc["nombre"], doc["creditos"]) for doc in result]
            print(requisitos)

        return []


    @classmethod
    def reqCursados(cls):
        collection = Database('kb', 'ReqCursados').collection
        matricula = 20121917
        if matricula:
            query = {
                "matricula": matricula,
                'matricula': {'$exists': True}
            }
            projection = {
                "matricula": 1,
                "asignatura": 1,
                "nombre": 1,
                "creditos": 1,
                "calificacion": 1
            }
            result = collection.find(query, projection=projection)
            requisitos = [(doc["asignatura"], doc["nombre"], doc["creditos"], doc["calificacion"]) for doc in result]
            print(requisitos)

    @classmethod
    def CreditosAcumulados(cls):
        collection = Database('kb', 'ReqCursados').collection
        matricula = 20121917
        if matricula:
            pipeline = [
                {
                    "$group": {
                        "_id": "$matricula",
                        "creditosAcumulados": {"$sum": '$creditos'}
                    }
                },
            ]
            result = [i for i in collection.aggregate(pipeline)][0]['creditosAcumulados']
            print(result)

    @classmethod
    def condicion(cls):
        collection = Database('kb', 'CondicionAcademica').collection
        matricula = 20121917
        if matricula:
            query = {
                "matricula": matricula,
                'matricula': {'$exists': True}
            }
            projection = {
                "condicionAcadActual": 1,

            }
            result = collection.find_one(query, projection=projection)
            print(result['condicionAcadActual'])

    @classmethod
    def califi(cls):
        collection = Database('kb', 'Calificaciones').collection
        letra = str("b").upper()
        matricula = 20121917
        if matricula and letra:
            query = {
                "matricula": matricula,
                "calificacion": letra,
            }
            projection = {
                "calificacion": 1,

            }
            result = collection.find(query, projection=projection).count()
            if result:
                print("Usted ha obtenido {0}".format(result))
            else:
                print("Usted no ha obtenido ninguna")

t.califi()
