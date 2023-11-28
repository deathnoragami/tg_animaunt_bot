bot:
	python run.py
migrations:
	alembic revision --autogenerate -m "migrations"
migrate:
	alembic upgrade head