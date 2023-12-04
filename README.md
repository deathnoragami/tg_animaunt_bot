# tg_animaunt_bot

python run_api.py - запуск веб интерфейса по адресу http://127.0.0.1:8000/docs

docker-compose up -d - для подъёма контейнера с редис

pg_dump -U animauntuser -d animaunt_db > dump.sql - дамп бд

psql -U animauntuser -d animaunt_db < /dump/dump.sql

streamlit run api_ui_main.py