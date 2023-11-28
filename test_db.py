from database.sqlite_connection import ENGINE
from sqlalchemy.orm import sessionmaker
from database.models import Title, Episode
from database.request import AnimeDB
import asyncio

# with sessionmaker(ENGINE)() as session:
#     session.add(Title(name='Имя', url='url', description='блаблабла'))
#     session.commit()

async def get():
    titles = await AnimeDB.get_episode_all(title_id='1')

    print(titles)


asyncio.run(get())