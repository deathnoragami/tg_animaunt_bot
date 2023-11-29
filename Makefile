bot:
	python run.py
web:
	python run_api.py
migrations:
	alembic revision --autogenerate -m "migrations"
migrate:
	alembic upgrade head