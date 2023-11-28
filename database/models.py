from sqlalchemy import String, Integer, Text, ForeignKey, Boolean, Float
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.ext.asyncio import AsyncAttrs
from sqlalchemy.orm import mapped_column, relationship


class Base(DeclarativeBase, AsyncAttrs):
    pass


class User(Base):

    __tablename__ = 'users'

    id = mapped_column(Integer, primary_key=True)
    tg_id = mapped_column(Integer)
    is_admin = mapped_column(Boolean, default=False)

    def __str__(self) -> str:
        return self.tg_id

    def __repr__(self) -> str:
        return self.__str__()


class Episode(Base):

    __tablename__ = 'Episode'

    id = mapped_column(Integer, primary_key=True)
    number = mapped_column(Integer)  # Нужно на Float поменять
    video_msg_id = mapped_column(String(255))
    title_id = mapped_column(ForeignKey('Title.id'))
    title = relationship('Title', back_populates='episodes')

    def __str__(self) -> str:
        return self.video_msg_id

    def __repr__(self) -> str:
        return self.__str__()


class Title(Base):

    __tablename__ = 'Title'

    id = mapped_column(Integer, primary_key=True)
    name = mapped_column(String(255))
    url = mapped_column(String(255))
    episodes = relationship('Episode', back_populates='title')
    description = mapped_column(Text)
    image_url = mapped_column(Text)
    match_episode = mapped_column(String(255), nullable=True)
    search_field = mapped_column(String(255), nullable=True)
    last_episode = mapped_column(Float, nullable=True)

    def update_search_field(self):
        self.search_field = self.name.lower()

    def __str__(self) -> str:
        return self.name

    def __repr__(self) -> str:
        return self.__str__()
