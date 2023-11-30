from fastapi import FastAPI
from .routers import ANIME_ROUTER


BOT_ADMIN = FastAPI()

BOT_ADMIN.include_router(ANIME_ROUTER)


if __name__ == '__main__':
    pass
