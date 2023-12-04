import asyncio
from fastapi import APIRouter, BackgroundTasks, status, HTTPException
from config import API_PREFIX
from parse.server_parser import ServerParser
from .schemas import Title
from parse.tasks import upload_episodes
import traceback
from run_api import logger


ANIME_ROUTER = APIRouter(prefix=f'{API_PREFIX}/anime', tags=['anime'])


@ANIME_ROUTER.post('/', response_model=Title)
async def add_title(
        url: str,
        remote_path: str,
        background_tasks: BackgroundTasks
        ) -> Title:
    try:
        server_parser = ServerParser(url, remote_path)
        title = await server_parser.parse_maunt()
        title_id = title.id
        background_tasks.add_task(upload_episodes, url, remote_path, title_id)
        return title
    except Exception:
        logger.error(f'Ошибка: {traceback.format_exc()}')
        raise HTTPException(status.HTTP_500_INTERNAL_SERVER_ERROR, 'Что-то Сломалось')


if __name__ == '__main__':
    pass
