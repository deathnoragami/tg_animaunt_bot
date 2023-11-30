from celery import Celery
from settings import REDIS_BROKER, REDIS_BACKEND
from parse.server_parser import ServerParser
import asyncio

worker = Celery('worker', broker=REDIS_BROKER, backend=REDIS_BACKEND)
worker.autodiscover_tasks()
worker.conf.event_serializer = 'json'
worker.conf.task_serializer = 'json'
worker.conf.result_serializer = 'json'
worker.conf.accept_content = ['application/json']
worker.conf.task_ignore_result = False
worker.conf.broker_connection_retry_on_startup = True
worker.conf.task_track_started = True


@worker.task
def upload_episodes(url: str, remote_path: str, title_id: int):
    server_parser = ServerParser(url, remote_path)
    server_parser.parsed_title_id = title_id
    loop = asyncio.get_event_loop()
    loop.run_until_complete(server_parser.download_video_with_sftp())


if __name__ == '__main__':
    pass
