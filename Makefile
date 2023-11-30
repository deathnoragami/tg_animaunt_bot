bot:
	python run.py
web:
	python run_api.py
migrations:
	alembic revision --autogenerate -m "migrations"
migrate:
	alembic upgrade head
up:
	docker-compose up -d
celery:
	celery -A worker.tasks:worker worker -l info --pool=solo