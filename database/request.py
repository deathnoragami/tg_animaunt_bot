from .psycopg2_connection import ENGINE
from sqlalchemy.orm import sessionmaker, joinedload, load_only
from sqlalchemy import func
from .models import Episode, Title


class BaseDB:

    _SESSION = sessionmaker(ENGINE)


class AnimeDB(BaseDB):

    @classmethod
    async def add_title(cls, **kwargs) -> Title:
        with cls._SESSION() as session:
            title = Title(**kwargs)
            session.add(title)
            # title.update_search_field()
            session.commit()
            title = await cls.get_title(title.id)
            return title

    @classmethod
    async def get_uncompleted(cls) -> list[Title]:
        with cls._SESSION() as session:
            titles = session.query(Title).options(
                load_only(
                    Title.id,
                    Title.name,
                    Title.remote_path,
                    Title.url,
                    Title.match_episode,
                    Title.last_episode,
                )
            ).filter(Title.complete.is_(False)).all()
            return titles

    @classmethod
    async def get_title(cls, title_id: int) -> Title:
        with cls._SESSION() as session:
            title = session.query(Title).options(
                load_only(
                    Title.id,
                    Title.name,
                    Title.remote_path,
                    Title.match_episode,
                    Title.last_episode,
                    Title.last_update,
                    Title.description,
                    Title.url,
                    Title.image_url,
                )
            ).filter(Title.id == title_id).first()
            return title

    @classmethod
    async def get_title_for_parser(cls, title_id: int) -> Title:
        with cls._SESSION() as session:
            title = session.query(Title).options(
                load_only(
                    Title.id,
                    Title.match_episode,
                    Title.last_episode,
                    Title.last_update,
                    ),
                joinedload(Title.episodes).load_only(
                        Episode.id, Episode.number, Episode.video_msg_id
                    ),
                ).filter(Title.id == title_id).first()
            return title

    @classmethod
    async def update_title(cls, title_id: int, number: int, last_update) -> None:
        with cls._SESSION() as session:
            title = session.query(Title).options(
                load_only(
                    Title.id,
                    Title.match_episode,
                    Title.last_episode,
                    Title.last_update,
                    Title.complete,
                    )
                ).filter(Title.id == title_id).first()
            if number:
                title.last_episode = number
            title.last_update = last_update
            try:
                if title.last_episode >= float(title.match_episode):
                    title.complete = True
            except ValueError:
                pass
            session.commit()

    @classmethod
    async def search_title(cls, query: str) -> list[list[str], list[str]]:
        with cls._SESSION() as session:
            result = session.query(Title).options(
                load_only(Title.id, Title.name)
                ).filter(func.lower(Title.name).like(
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
            # all_number = [str(i.number) for i in episodes]
            all_id = [str(i.id) for i in episodes]
            all_view_number = [i.view_number for i in episodes]
            return [all_view_number, all_id]

    @classmethod
    async def get_episode(cls, episode_id: int) -> Episode:
        with cls._SESSION() as session:
            episode = session.query(Episode).options(
                load_only(Episode.video_msg_id, Episode.caption)
                ).filter(Episode.id == episode_id).first()
            return episode

    @classmethod
    async def add_episode(cls, **kwargs) -> None:
        with cls._SESSION() as session:
            kwargs['title'] = session.get(Title, kwargs.pop('title_id'))
            episode = Episode(**kwargs)
            session.add(episode)
            session.commit()

    @classmethod
    async def update_episode(cls, episode_id: int, video_msg_id: str) -> None:
        with cls._SESSION() as session:
            episode = session.get(Episode, episode_id)
            episode.video_msg_id = video_msg_id
            session.commit()
