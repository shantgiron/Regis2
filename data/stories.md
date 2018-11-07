## Greet
* greet
    - utter_greet

## bye
* bye
    - utter_bye

## thank
* thank
    - utter_thank

##affirm
* affirm
    - utter_happy

##deny
* deny
    - utter_bye

## Bienvenida
* start
    -utter_greet

## consultar evento ambiguo
* query_event{"event": "prematricula"}
    - slot{"event": "prematricula"}
    - action_look_event
    - slot{"matching_events": ["Inicio de prematricula", "Per\u00edodo de modificaci\u00f3n de prematr\u00edcula (presencial).", "Per\u00edodo de modificaci\u00f3n de prematr\u00edcula (presencial).", "Retirar prematr\u00edcula el 3-2017-2018.", "Per\u00edodo de prematr\u00edcula para el 3-2017-2018.", "b) Retirar prematr\u00edcula del 1-2018-2019.", "Per\u00edodo de Prematr\u00edcula Estudiantes Ciclo Estudios Generales."]}
    - action_suggest

## consultar evento
* query_event{"event": "Inicio de prematricula"}
    - slot{"event": "Inicio de prematricula"}
    - action_look_event
    - action_ack_eventdate


## consultar evento sin nombre
* query_event
    - utter_event_not_found


## preguntar por dias importantes
* query_importantes
    - action_look_important
    - utter_another_question

## preguntar por cantidad de dias importantes
* count_importante
    - action_count_important
    - utter_ack_number_importantes

## preguntar por dias asuetos
* query_asueto
    - action_look_asuetos
    - utter_did_that_help
    - utter_another_question

## preguntar cantidad dia asueto
* count_asueto
    - action_count_asuetos
    - utter_another_question

## Generated Story 6319266707024298916
* descripcion_proceso{"proceso": "bajas por prerrequisitos"}
    - slot{"proceso": "bajas por prerrequisitos"}
    - action_process_descripcion

## Generated Story 2421517452637475804
##* query_indice
##    - action_login_form

## default
* None
    - utter_default

## Generated Story -5112669426839210494
* what_should_i_ask
    - utter_you_should_ask

## Generated Story -5085138796122233298
* query_indice
    - utter_cual_indice
* indice_acumulado
    - utter_ask_matricula
    - slot{"requested_slot": "matricula"}
* informar{"matricula": "20121917"}
    - utter_indice_acumulado

## Generated Story 3741297509561492559
##* query_indice
##    - action_login_form
##    - slot{"requested_slot": "matricula"}
##* informar{"matricula": "20121917"}
##    - action_login_form
##    - slot{"matricula": "20121917"}
##    - slot{"requested_slot": "password"}
##* informar{"password": "123456"}
##    - action_login_form


## Generated Story -3767670091850773124
* mi_indice
    - utter_cual_indice
* indice_del_periodo
    - utter_ask_matricula
    - slot{"requested_slot": "matricula"}
* informar{"matricula": "20121917"}
    - utter_indice_periodo

## Generated Story -1130115263992449069
* cuando_graduacion
    - utter_cual_graduacion
* graduacion_sti
    - utter_graduacion_sti_fecha

## Generated Story 2442879605525322738
* cuando_graduacion
    - utter_cual_graduacion
* graduacion_sta
    - utter_graduacion_sta_fecha

## Generated Story -320681638175667493
* bye
    - utter_bye

## Generated Story 7261267099767182670
* thank
    - utter_thank

## Generated Story 6319266707024298916
* descripcion_proceso{"proceso": "bajas por prerrequisitos"}
    - slot{"proceso": "bajas por prerrequisitos"}
    - action_process_descripcion

## Generated Story -4629031046991902444
* cuando_graduacion
    - utter_cual_graduacion
* graduacion_sta
    - utter_graduacion_sta_fecha

## Generated Story 7784656647794306512
* condicion_academica
    - action_condicion_academica


## Generated Story -4009139781606905978
* cuando_retiro
    - utter_cual_retiro
* retiro_parcial
    - utter_retiro_parcial_fecha

## Generated Story 1684676155798266593
* cuando_retiro
    - utter_cual_retiro
* retiro_total
    - utter_retiro_total_fecha

## Generated Story 6516674712220716356
* requisitos_pendientes
    - action_requisitos_pendientes

## Generated Story -5112669426839210494
* what_should_i_ask
    - utter_you_should_ask

## Generated Story 6070435417377167289
* creditos_acumulados
    - action_creditos_acumulados

## Generated Story 7184186336441010786
* procedimiento_proceso{"proceso": "graduacion"}
    - slot{"proceso": "graduacion"}
    - action_process_procedimiento

## Generated Story -5821021971457789825
* query_asueto
    - action_look_asuetos
    - slot{"asueto_count": 1}

## Generated Story 9192142771012463284
* query_importantes
    - action_look_important
    - slot{"importantes_count": 11}

## Generated Story -189469721235285774
* nonsense
    - action_default_fallback

## Generated Story -806123001115259216
* requisitos_cursados
> login
    - action_requisitos_cursados

## Generated Story 5102960786421612016
* cuantas_calificacion{"calificacion": "A"}
    - slot{"calificacion": "A"}
> login
    - action_ack_calificacion

## Generated Story -2157983280237184028
* cuantas_calificacion{"calificacion": "B"}
    - slot{"calificacion": "B"}
> login
    - action_ack_calificacion

## Generated Story -3177612128008345689
> login
* Login
    - action_login_form
    - slot{"requested_slot": "matricula"}
* informar{"matricula": "20121917"}
    - slot{"matricula": "20121917"}
* informar{"password": "321"}
    - slot{"password": "321"}
    - action_login_form
    - slot{"password": "321"}
    - slot{"username": "Leonardo"}

