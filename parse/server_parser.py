from pyrogram import Client
import paramiko
import threading
import os
from config import (
    USERNAME_SFTP,
    PASSWORD_SFTP,
    ADRESS_SFTP,
    API_HASH,
    API_ID,
    VIDEO_CHAT_ID
)
from bs4 import BeautifulSoup
import requests
import base64
import re
from database.request import AnimeDB
from database.models import Title
import asyncio
from string import ascii_letters
from paramiko.sftp_attr import SFTPAttributes


class ServerParser:

    CLIENT = Client("my_account", int(API_ID), API_HASH)
    CHAT_ID = int(VIDEO_CHAT_ID)

    def __init__(self, url: str, remote_path: str) -> None:
        self.url = url
        self.remote_path = remote_path
        self.parsed_title_id: int = None

    async def parse_maunt(self) -> Title:
        response = requests.get(self.url)
        soup = BeautifulSoup(response.text, 'html.parser')
        name = soup.find("h1").text.strip()  # Название релища
        image_url = "https://animaunt.org" + soup.find("img").get("src")  # Ссылка на картинку
        image_data = requests.get(image_url).content
        image_base64 = base64.b64encode(image_data).decode('utf-8') # Это бинарный вид
        episodes_tag = soup.find_all('li', class_='vis-clear')
        for li_tag in episodes_tag:
            if 'Эпизоды:' in li_tag.get_text():
                episodes_text = li_tag.get_text().strip()
                numbers = re.findall(r'\d+', li_tag.get_text())
                second_number = numbers[1]  # Число всего серий
                break
        episodes_tag = soup.find_all('li', class_='vis-gray')
        for li_tag in episodes_tag:
            if "Тип:" in li_tag.get_text():
                type_title = li_tag.get_text().strip().split(":")[1]
                break
        # добавить description
        kwargs = {
            'name': name,
            'url': self.url,
            'remote_path': self.remote_path,
            'image_url': image_url,
            'match_episode': second_number,
        }
        title = await AnimeDB.add_title(**kwargs)
        self.parsed_title_id = title.id
        return title

    async def upload_tg_channel(
            self, directory: str, number: int
            ) -> None:
        await self.CLIENT.start()
        msg = await self.CLIENT.send_video(
            chat_id=self.CHAT_ID,
            video=directory,
            width=1280,
            height=720
        )
        print(f"Загружен в тг {directory}")
        os.remove(directory)
        await self.CLIENT.stop()
        kwargs = {
            'title_id': self.parsed_title_id,
            'number': number,
            'video_msg_id': msg.id
        }
        await AnimeDB.add_episode(**kwargs)

    async def download_video_with_sftp(self) -> None:
        port = 22
        local_path = 'video'
        os.makedirs(local_path, exist_ok=True)
        ssh = paramiko.SSHClient()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        ssh.connect(ADRESS_SFTP, port, USERNAME_SFTP, PASSWORD_SFTP)
        sftp = ssh.open_sftp()
        files_with_attributes = sftp.listdir_attr(self.remote_path)
        files_sorted_by_filename = sorted(
            files_with_attributes, key=lambda x: x.filename
        )
        for i, file_attr in enumerate(files_sorted_by_filename):
            file_attr: SFTPAttributes
            file = file_attr.filename
            if file.lower() == 'trailer.mp4':
                continue
            remote_file_path = f'{self.remote_path}/{file}'
            local_file_path = f'{local_path}/{file}'
            number = float(os.path.splitext(file)[0].strip(ascii_letters))
            try:
                next_number = float(os.path.splitext(
                    files_sorted_by_filename[i + 1].filename
                )[0].strip(ascii_letters))
                if number == next_number:
                    continue
            except (ValueError, IndexError):
                pass
            sftp.get(remote_file_path, local_file_path)
            print(f'{file} скачан успешно.')
            await self.upload_tg_channel(local_file_path, number)
            await AnimeDB.update_title(self.parsed_title_id, number)
        sftp.close()
        ssh.close()
