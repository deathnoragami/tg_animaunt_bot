from database.request import AnimeDB
from parse.server_parser import ServerParser
import asyncio


def upload_episodes(url: str, remote_path: str, title_id: int):
    server_parser = ServerParser(url, remote_path)
    server_parser.parsed_title_id = title_id
    asyncio.run(server_parser.download_video_with_sftp())


def update_parser():
    loop = asyncio.get_event_loop()
    titles = loop.run_until_complete(AnimeDB.get_uncompleted())
    for title in titles:
        server_parser = ServerParser(title.url, title.remote_path)
        server_parser.parsed_title_id = title.id
        loop.run_until_complete(server_parser.update_parser())


if __name__ == '__main__':
    pass
