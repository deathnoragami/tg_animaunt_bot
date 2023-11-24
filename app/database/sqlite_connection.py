from sqlalchemy import create_engine
from config import DATABASE

ENGINE = create_engine(DATABASE, echo=True)


if __name__ == '__main__':
    pass
