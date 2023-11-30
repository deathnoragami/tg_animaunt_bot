# tg_animaunt_bot

python run_api.py - запуск веб интерфейса по адресу http://127.0.0.1:8000/docs

celery -A worker.tasks:worker worker -l info --pool=solo - для запуска селери

docker-compose up -d - для подъёма контейнера с редис

