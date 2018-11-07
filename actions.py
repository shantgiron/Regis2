# coding=utf-8
import locale
from datetime import datetime
import pytz
from rasa_core_sdk import Action, Tracker
from rasa_core_sdk.events import SlotSet, UserUtteranceReverted
from pymongo import MongoClient
from rasa_core_sdk.forms import FormAction, EntityFormField, FormField
from Database import Database
from hunspell import hunspell


# collection = Database('kb', 'Calendarios').collection

# Actions Eventos


class ActionLogIn(FormAction):
    RANDOMIZE = False

    @staticmethod
    def required_fields():
        return [
            EntityFormField("matricula", "matricula"),
            EntityFormField("password", "password"),
        ]

    def name(self):
        return 'action_login_form'

    def submit(self, dispatcher, tracker, domain):
        collection = Database('kb', 'Users').collection
        passwd = str(tracker.get_slot("password"))
        matricula = str(tracker.get_slot("matricula"))
        query = {
            "password": passwd,
            "matricula": matricula
        }
        if passwd and matricula:
            result = collection.find_one(query)
        else:
            dispatcher.utter_message("Tengo dificultad reconociendo tu matricula, "
                                     "asegúrate de que esté sin guiones ni espacios")
            return [UserUtteranceReverted()]

        if result:
            dispatcher.utter_template("utter_welcome", tracker,
                                      username=result['nombre'])
            return [SlotSet("username", result["nombre"])]
        else:
            dispatcher.utter_message("matricula o contraseña incorrectos")
            return [UserUtteranceReverted()]
        return []


class ActionlookforEvent(Action):
    def name(self):
        # type: () -> Text
        return "action_look_event"

    def run(self, dispatcher, tracker, domain):
        # type: (Dispatcher, DialogueStateTracker, Domain) -> List[Event]
        print(tracker.latest_message.keys())
        evento = tracker.get_slot("event")
        if evento is None:
            dispatcher.utter_template("utter_event_not_found", tracker)
            return [UserUtteranceReverted()]
        query = {"$or": [
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
        ], "$text": {u"$search": evento}}

        projection = {
            "score": {u"$meta": u"textScore"},
            "evento.nombre": 1,
            "date": 1,
        }
        sort = [('score', {'$meta': 'textScore'}), (u"date", 1)]
        collection = Database('kb', 'Calendarios').collection
        docs = collection.find(query, projection=projection, sort=sort).limit(5)
        matches = []
        date = str()
        hoy = datetime.now()
        if docs.count() > 0:
            if docs[0]['score'] >= 0.800:
                if docs[0]['date'] >= hoy:
                    date = docs[0]['date']
                elif docs[0]['date'] < hoy <= docs[0]['evento']['finaliza']:
                    date = docs[0]['evento']['finaliza']
                return [SlotSet('date', date)]

            else:
                for doc in docs:
                    event = doc['evento']['nombre']
                    matches.append(event)
                return [SlotSet('matching_events', matches)]

        dispatcher.utter_template('utter_sorry', tracker)
        return []


class ActionShowEventResults(Action):
    def name(self):
        return 'action_ack_eventdate'

    def run(self, dispatcher, tracker, domain):
        match = tracker.get_slot("date")
        if match:
            date = datetime.strptime(match, '%a, %d %b %Y %H:%M:%S %Z')
            date_str = date.strftime('%d de %B del %Y')

            if date >= datetime.now():
                dispatcher.utter_template("utter_ack_eventdate", tracker,
                                          event=tracker.get_slot('event'),
                                          date=date_str)
            else:
                dispatcher.utter_template("utter_ack_prsnt_eventdate", tracker,
                                          event=tracker.get_slot('event'),
                                          date=date_str)
        return []


class ActionSuggestEventResults(Action):
    def name(self):
        return 'action_suggest'

    def run(self, dispatcher, tracker, domain):
        matches = tracker.get_slot("matching_events")

        if matches:
            dispatcher.utter_template("utter_suggestions", tracker)
            suggestions = [{'title': event, 'payload': "/query_event{\"event\": \"%s\""} for event in matches]
            dispatcher.utter_button_message("", suggestions)

        return []


class ActionLookForAsuetos(Action):
    def name(self):
        # type: () -> Text
        return "action_look_asuetos"

    def run(self, dispatcher, tracker: Tracker, domain):
        # type: (Dispatcher, DialogueStateTracker, Domain) -> List[Event]
        eventdate = tracker.get_slot('date')

        query = {
            "date": {"$gte": datetime.now(tz=pytz.timezone('America/Santo_Domingo'))}
        }
        # if eventdate:
        #    query = {"date": datetime.strptime(eventdate+"-"+str(datetime.now().year), '%B-%Y')}
        projection = dict()
        query["evento.asueto"] = "true"
        projection["evento.nombre"] = 1
        projection["date"] = 1
        matches = list()

        with MongoClient("mongodb://localhost:27017/") as client:
            database = client["kb"]
            collection = database["Calendarios"]
            docs = collection.find(query, projection=projection)

            if docs:
                for doc in docs:
                    dia = doc['date'].strftime('%d de %B del %Y')
                    matches.append(doc['evento']['nombre'] + " " + dia + '\n')

                dispatcher.utter_template('utter_ack_asuetos', tracker)
                dispatcher.utter_message(matches.__str__())
        return [SlotSet('asueto_count', docs.count())]


class ActionCountAsuetos(Action):
    def name(self):
        # type: () -> Text
        return "action_count_asuetos"

    def run(self, dispatcher, tracker, domain):
        # type: (Dispatcher, DialogueStateTracker, Domain) -> List[Event]
        counted = tracker.get_slot('asueto_count')
        if counted:
            print("the count is already done")
            return
        eventdate = tracker.get_slot('date')
        query = {
            "date": {"$gte": datetime.now(tz=pytz.timezone('America/Santo_Domingo'))}
        }
        if eventdate:
            query = {"date": datetime.strptime(eventdate + "-" + datetime.now().year, '%B-%Y')}
        projection = dict()
        query["evento.asueto"] = "true"
        projection["evento.nombre"] = 1

        with MongoClient("mongodb://localhost:27017/") as client:
            database = client["kb"]
            collection = database["Calendarios"]
            docs = collection.find(query, projection=projection)

        return [SlotSet('asueto_count', docs.count())]


class ActionLookForImportant(Action):
    def name(self):
        # type: () -> Text
        return "action_look_important"

    def run(self, dispatcher, tracker, domain):
        # type: (Dispatcher, DialogueStateTracker, Domain) -> List[Event]
        eventdate = tracker.get_slot('date')
        query = {
            "date": {
                "$gte": datetime.now(tz=pytz.timezone('America/Santo_Domingo'))
            }
        }
        # if eventdate:
        #   query = {"date": datetime.strptime(eventdate + "-" + str(datetime.now().year), '%B-%Y')}
        projection = dict()
        query["evento.importante"] = "true"
        projection["evento.nombre"] = 1
        projection["date"] = 1
        matches = list()

        with MongoClient("mongodb://localhost:27017/") as client:
            database = client["kb"]
            collection = database["Calendarios"]
            docs = collection.find(query, projection=projection)
            if docs:
                for doc in docs:
                    # date = datetime.strptime(doc['date'], '%Y-%m-%d %H:%M:%S.%f')
                    dia = doc['date'].strftime('%d de %B del %Y')
                    matches.append(doc['evento']['nombre'] + " " + dia + '\n')

                dispatcher.utter_template('utter_ack_importantes', tracker)
                dispatcher.utter_message(matches.__str__())
        return [SlotSet('importantes_count', docs.count())]


class ActionCountImportant(Action):
    def name(self):
        # type: () -> Text
        return "action_count_important"

    def run(self, dispatcher, tracker, domain):
        # type: (Dispatcher, DialogueStateTracker, Domain) -> List[Event]
        counted = tracker.get_slot('importantes_count')
        if (counted):
            print("the count is already done")
            return

        eventdate = tracker.get_slot('date')
        query = {
            "date": {
                "$gte": datetime.now(tz=pytz.timezone('America/Santo_Domingo'))
            }
        }
        # Contar los eventos de una fecha dada
        # if eventdate:
        #    query = {"date": datetime.strptime(eventdate + "-" + datetime.now().year, '%B-%Y')}
        projection = dict()
        query["evento.importante"] = "true"
        projection["evento.nombre"] = 1

        with MongoClient("mongodb://localhost:27017/") as client:
            database = client["kb"]
            collection = database["Calendarios"]
            docs = collection.find(query, projection=projection)

        return [SlotSet('importantes_count', docs.count())]


# Actions para procesos
class ActionlookforProcessDescription(Action):
    def name(self):
        # type: () -> Text
        return "action_process_descripcion"

    def run(self, dispatcher, tracker, domain):
        proceso = tracker.get_slot("proceso")
        collection = Database('kb', 'Procesos').collection
        if proceso:
            query = {
                "nombre": proceso,
                'descripcion': {'$exists': True}
            }
            projection = {
                "descripcion": 1
            }
            result = collection.find_one(query, projection=projection)
            dispatcher.utter_template("utter_descripcion_proceso", tracker,
                                      descripcion=result['descripcion'])

        return []


class ActionlookforProcessImportancia(Action):
    def name(self):
        # type: () -> Text
        return "action_process_importancia"

    def run(self, dispatcher, tracker, domain):
        proceso = tracker.get_slot("proceso")
        collection = Database('kb', 'Procesos').collection
        if proceso:
            query = {
                "nombre": proceso,
                'importancia': {'$exists': True}
            }
            projection = {
                "importancia": 1
            }
            result = collection.find_one(query, projection=projection)
            dispatcher.utter_template("utter_importancia_proceso", tracker,
                                      importancia=result['importancia'])

        return []


class ActionlookforProcessPenalidad(Action):
    def name(self):
        # type: () -> Text
        return "action_process_penalidad"

    def run(self, dispatcher, tracker, domain):
        proceso = tracker.get_slot("proceso")
        collection = Database('kb', 'Procesos').collection
        if proceso:
            query = {
                "nombre": proceso,
                'penalidad': {'$exists': True}
            }
            projection = {
                "penalidad": 1
            }
            result = collection.find_one(query, projection=projection)
            dispatcher.utter_template("utter_penalidad_proceso", tracker,
                                      penalidad=result['penalidad'])

        return []


class ActionlookforProcessAdvertencia(Action):
    def name(self):
        # type: () -> Text

        return "action_process_advertencia"

    def run(self, dispatcher, tracker, domain):
        proceso = tracker.get_slot("proceso")
        collection = Database('kb', 'Procesos').collection
        if proceso:
            query = {
                "nombre": proceso,
                'advertencia': {'$exists': True}
            }
            projection = {
                "advertencia": 1
            }
            result = collection.find_one(query, projection=projection)
            dispatcher.utter_template("utter_advertencia_proceso", tracker,
                                      advertencia=result['advertencia'])

        return []


class ActionlookforProcessProcedimiento(Action):
    def name(self):
        # type: () -> Text
        return "action_process_procedimiento"

    def run(self, dispatcher, tracker, domain):
        proceso = tracker.get_slot("proceso")
        collection = Database('kb', 'Procesos').collection
        if proceso:
            query = {
                "nombre": proceso,
                'procedimiento': {'$exists': True}
            }
            projection = {
                "procedimiento": 1
            }
            result = collection.find_one(query, projection=projection)
            dispatcher.utter_template("utter_procedimiento_proceso", tracker,
                                      procedimiento=result['procedimiento'])
        return []




# Informacion Academica
class ActionlookforRequisitosPendientes(Action):
    def name(self):
        # type: () -> Text
        return "action_requisitos_pendientes"

    def run(self, dispatcher, tracker, domain):
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
            dispatcher.utter_template("utter_requisitos_pendientes", tracker,
                                      requisitos=requisitos)
        return []


class ActionlookforRequisitosCursados(Action):
    def name(self):
        # type: () -> Text
        return "action_requisitos_cursados"

    def run(self, dispatcher, tracker, domain):
        collection = Database('kb', 'ReqCursados').collection
        matricula = int(tracker.get_slot("matricula"))
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
            dispatcher.utter_template("utter_requisitos_cursados", tracker,
                                      requisitos=requisitos)
        return []


class ActionlookforCreditosAcumulados(Action):
    def name(self):
        # type: () -> Text
        return "action_creditos_acumulados"

    def run(self, dispatcher, tracker: Tracker, domain) -> list:
        collection = Database('kb', 'ReqCursados').collection
        matricula = tracker.get_slot("matricula")
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
            dispatcher.utter_template("utter_creditos_acumulados", tracker, creditos=result)
        return []


class ActionCondicionAcademica(Action):
    def name(self):
        # type: () -> Text
        return "action_condicion_academica"

    def run(self, dispatcher, tracker, domain):
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
            if result:
                dispatcher.utter_template("utter_condicion_academica", tracker,
                                          condicion=result['condicionAcadActual'])
            else:
                dispatcher.utter_message("Error interno")

        return []


class ActionCalificacion(Action):
    def name(self):
        # type: () -> Text
        return "action_ack_calificacion"

    def run(self, dispatcher, tracker, domain):
        collection = Database('kb', 'Calificaciones').collection
        letra = str(tracker.get_slot('calificacion')).upper()
        matricula = int(tracker.get_slot('matricula'))
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
                dispatcher.utter_message("Usted ha obtenido {0}".format(result))
            else:
                dispatcher.utter_message("Usted no ha obtenido ninguna")

        return []


class ActionCalificacionMateria(Action):
    def name(self):
        # type: () -> Text
        return "action_materia_calificacion"

    def run(self, dispatcher, tracker, domain):
        collection = Database('kb', 'Calificaciones').collection
        letra = "B"
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
                dispatcher.utter_message("Usted ha obtenido {0}".format(result))
            else:
                dispatcher.utter_message("Usted no ha obtenido ninguna")

        return []
