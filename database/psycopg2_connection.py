from config import POSTGRES_URL
from sqlalchemy import create_engine


DATABASE = f'postgresql+psycopg2://{POSTGRES_URL}'
ENGINE = create_engine(DATABASE, echo=True)


if __name__ == '__main__':
    pass
