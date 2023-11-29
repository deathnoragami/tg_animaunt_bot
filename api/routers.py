from fastapi import APIRouter
from config import API_PREFIX
from parse.server_parser import ServerParser

ANIME_ROUTER = APIRouter(prefix=f'{API_PREFIX}/anime', tags=['anime'])


@ANIME_ROUTER.post('/')
async def add_title(url: str, remote_path: str):
    server_parser = ServerParser(url, remote_path)
    await server_parser.parse_maunt()
    await server_parser.download_video_with_sftp()


if __name__ == '__main__':
    pass
