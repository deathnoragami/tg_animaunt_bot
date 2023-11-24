from .sqlite_connection import ENGINE
from sqlalchemy.orm import sessionmaker
from .models import Episode, Title
from config import DATABASE
from sqlalchemy import func, create_engine, text


class BaseDB:

    _SESSION = sessionmaker(ENGINE)

class AnimeDB(BaseDB):



    @classmethod
    async def get_title(cls, id: int):
        with cls._SESSION() as session:
            title = session.query(Title).filter(Title.id == id).first()
            # title.episodes
            return title
        
    # @classmethod
    # async def get_episode_link(cls, id_video:int):
    #     with cls._SESSION() as session:
    #         episode = session.query(Episode).filter(
    #             Episode.id == id_video,
    #         ).first()
    #         return episode.video_link

    @classmethod
    async def search_title(cls, query: str) -> list[list, list]:
        with cls._SESSION() as session:
            result = session.query(Title).filter(Title.search_field.like(f'%{query.lower()}%')).all()[:7]
            names = [i.name for i in result]
            indexes = [str(i.id) for i in result]
            return [names, indexes]
    
    @classmethod
    async def get_episode_all(cls, title_id: int):
        with cls._SESSION() as session:
            episodes = session.query(Episode).filter(Episode.title_id == title_id).all()
            all_number = [str(i.number) for i in episodes]
            all_id = [str(i.id) for i in episodes]
            return [all_number, all_id]
        
    @classmethod
    async def get_episode(cls, get_all: bool = False, title_id: int = 1, episode_id: int = 1): # TODO: норм идея или нет?
        if get_all:
            with cls._SESSION() as session:
                episodes = session.query(Episode).filter(Episode.title_id == title_id).all()
                all_number = [str(i.number) for i in episodes]
                all_id = [str(i.id) for i in episodes]
                return [all_number, all_id]
        else:
            with cls._SESSION() as session:
                episode = session.query(Episode).filter(Episode.id == episode_id).first()
                return episode