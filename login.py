from pyrogram import Client
from config import (
    API_HASH,
    API_ID,
)
Client("my_account", int(API_ID), API_HASH).start()
