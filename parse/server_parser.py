from pyrogram import Client
import paramiko
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
from string import ascii_letters
from paramiko.sftp_attr import SFTPAttributes
from config import VIDEO_ROOT
from datetime import datetime as dt


class ServerParser:

    CLIENT = Client("my_account", int(API_ID), API_HASH)
    CHAT_ID = int(VIDEO_CHAT_ID)
    LOCAL_PATH = VIDEO_ROOT
    PORT = 22  # Убрать в енв
    REMOTE_DIR = '/home/video/mp4/'

    def __init__(self, url: str, remote_path: str) -> None:
        self.url = url
        self.remote_path = remote_path
        self.parsed_title_id: int = None
        os.makedirs(self.LOCAL_PATH, exist_ok=True)

    async def __ssh_connect(self):
        ssh = paramiko.SSHClient()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        ssh.connect(ADRESS_SFTP, self.PORT, USERNAME_SFTP, PASSWORD_SFTP)
        return ssh

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
        discription = soup.find('div', id='fdesc').text.strip()
        while len(discription) > 800:
            last_period_index = discription.rfind('.')
            if last_period_index == -1:
                discription = discription[:750]
            else:
                discription = discription[:last_period_index]

        kwargs = {
            'name': name,
            'url': self.url,
            'remote_path': self.remote_path,
            'image_url': image_url,
            'match_episode': second_number,
            'description': discription,
        }
        title = await AnimeDB.add_title(**kwargs)
        self.parsed_title_id = title.id
        return title

    async def upload_tg_channel(
            self, directory: str, number: int, key: str, episode_id: int = None
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
        if key == 'Add':
            await AnimeDB.add_episode(**kwargs)
        elif key == 'Update':
            await AnimeDB.update_episode(episode_id, msg.id)

    async def download_video_with_sftp(self) -> None:
        ssh = await self.__ssh_connect()
        sftp = ssh.open_sftp()
        sftp.chdir(self.REMOTE_DIR)
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
            local_file_path = f'{self.LOCAL_PATH}/{file}'
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
            await self.upload_tg_channel(local_file_path, number, 'Add')
            last_update = dt.fromtimestamp(file_attr.st_mtime)
            await AnimeDB.update_title(self.parsed_title_id, number, last_update)
        sftp.close()
        ssh.close()

    async def update_parser(self) -> None:
        ssh = await self.__ssh_connect()
        sftp = ssh.open_sftp()
        sftp.chdir(self.REMOTE_DIR)
        files_with_attributes = sftp.listdir_attr(self.remote_path)
        files_sorted_by_st_mtime = sorted(
            files_with_attributes, key=lambda x: x.st_mtime
        )
        for file_attr in files_sorted_by_st_mtime:
            file_attr: SFTPAttributes
            file = file_attr.filename
            if file.lower() == 'trailer.mp4':
                continue
            title = await AnimeDB.get_title_for_parser(self.parsed_title_id)
            last_update = dt.fromtimestamp(file_attr.st_mtime)
            uploaded_episodes = {float(i.number): i.id for i in title.episodes}
            try:
                if last_update > title.last_update:
                    remote_file_path = f'{self.remote_path}/{file}'
                    local_file_path = f'{self.LOCAL_PATH}/{file}'
                    number = float(
                        os.path.splitext(file)[0].strip(ascii_letters)
                    )
                    sftp.get(remote_file_path, local_file_path)
                    if number in uploaded_episodes:
                        key = 'Update'
                        episode_id = uploaded_episodes[number]
                        number = None
                    else:
                        key = 'Add'
                        episode_id = None
                        number = number
                    await self.upload_tg_channel(local_file_path, number, key, episode_id)
                    last_update = dt.fromtimestamp(file_attr.st_mtime)
                    await AnimeDB.update_title(self.parsed_title_id, number, last_update)
            except TypeError:
                pass
        sftp.close()
        ssh.close()
