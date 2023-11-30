from fastapi import APIRouter
from settings import API_PREFIX
from parse.server_parser import ServerParser
from .schemas import Title
from worker.tasks import upload_episodes

ANIME_ROUTER = APIRouter(prefix=f'{API_PREFIX}/anime', tags=['anime'])


@ANIME_ROUTER.post('/', response_model=Title)
async def add_title(url: str, remote_path: str):
    server_parser = ServerParser(url, remote_path)
    title = await server_parser.parse_maunt()
    title_id = title.id
    upload_episodes.apply_async(args=(url, remote_path, title_id))
    return title


if __name__ == '__main__':
    pass
