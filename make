
#train nlu
python -m rasa_nlu.train -c nlu_config.yml --data data/nlu_data.md -o models --fixed_model_name nlu --project current --verbose

#train core
python -m rasa_core.train -d domain.yml -s data/stories.md -o models/current/dialogue --epochs 400

#run
python -m rasa_core.run -d models/current/dialogue -u models/current/nlu --endpoints endpoints.yml

#endpoint
python -m rasa_core_sdk.endpoint --actions actions

#interactive learning:
python -m rasa_core.train --online -d domain.yml -s data/stories.md -o models/current/dialogue -u models/current/nlu
python -m rasa_core.train --online -d domain.yml -s data/stories.md -o models/current/dialogue -u models/current/nlu --endpoints endpoints.yml

Activate BotProject
cd C:\Users\Leonardo\Documents\GitHub\starter-pack


python -m rasa_core.run -d models/current/dialogue -u models/current/nlu --port 5002 --credentials credentials.yml -c telegram --endpoints endpoints.yml