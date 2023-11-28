from .sqlite_connection import ENGINE
from sqlalchemy.orm import sessionmaker, joinedload, load_only
from .models import Episode, Title


class BaseDB:

    _SESSION = sessionmaker(ENGINE)


class AnimeDB(BaseDB):

    @classmethod
    async def get_title(cls, title_id: int) -> Title:
        with cls._SESSION() as session:
            title = session.query(Title).options(
                load_only(
                    Title.id,
                    Title.name,
                    Title.match_episode,
                    Title.description,
                    Title.url,
                    Title.image_url,
                    )
                ).filter(Title.id == title_id).first()
            return title

    @classmethod
    async def search_title(cls, query: str) -> list[list[str], list[str]]:
        with cls._SESSION() as session:
            result = session.query(Title).options(
                load_only(Title.id, Title.name)
                ).filter(Title.search_field.like(
                    f'%{query.lower()}%')
                ).all()[:7]
            names = [i.name for i in result]
            indexes = [str(i.id) for i in result]
            return [names, indexes]

    @classmethod
    async def get_episode_all(
            cls, title_id: int
            ) -> list[list[str], list[str]]:
        with cls._SESSION() as session:
            episodes = session.query(Episode).options(
                load_only(Episode.number, Episode.id)
                ).filter(Episode.title_id == title_id).all()
            all_number = [str(i.number) for i in episodes]
            all_id = [str(i.id) for i in episodes]
            return [all_number, all_id]

    @classmethod
    async def get_episode(cls, episode_id: int) -> Episode:
        with cls._SESSION() as session:
            episode = session.query(Episode).options(
                load_only(Episode.video_msg_id, Episode.number)
                ).filter(Episode.id == episode_id).first()
            return episode

    @classmethod
    async def add_title(cls, **kwargs) -> int:
        with cls._SESSION() as session:
            title = Title(**kwargs)
            session.add(title)
            session.commit()
        return title.id

    @classmethod
    async def add_episode(cls, **kwargs):
        with cls._SESSION() as session:
            kwargs['title'] = session.get(Title, kwargs.pop('title_id'))
            episode = Episode(**kwargs)
            session.add(episode)
            session.commit()
