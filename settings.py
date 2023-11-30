from config import REDIS_HOST, REDIS_PORT

API_PREFIX = '/v1'
VIDEO_ROOT = 'video'
# для разарботки
REDIS_HOST = 'localhost'
REDIS_BROKER = f'redis://{REDIS_HOST}:{REDIS_PORT}'
REDIS_BACKEND = f'redis://{REDIS_HOST}:{REDIS_PORT}/1'
