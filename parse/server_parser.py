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

    @staticmethod
    def __trailer_check(file: str) -> bool:
        return 'trailer' in file.lower()

    @staticmethod
    def __make_number(file: str) -> tuple[float, str, str]:
        filename = os.path.splitext(file)[0]
        if 'sp' in filename:
            number = -float(filename.strip(ascii_letters))
            view_number = (
                f'сп {(int(abs(number)))}'
            )
            caption = f'Спешл {int(abs(number))}'
        elif '.' in filename:
            number = float(filename.strip(ascii_letters))
            view_number = f'{number}'
            caption = f'{number} серия'
        elif '_' in filename:
            number = float(filename.replace('_', '.').strip(ascii_letters))
            view_number = (
                f'{(str(number).split(".")[0])}. '
                f'{(str(number).split(".")[-1])}ч'
            )
            caption = (
                f'{(str(number).split(".")[0])} серия '
                f'{(str(number).split(".")[-1])} часть'
            )
        else:
            number = float(filename.strip(ascii_letters))
            view_number = f'{int(number)}'
            caption = f'{int(number)} серия'
        return number, view_number, caption

    def __special_sort(
            self,
            files_sorted_by_filename: list[SFTPAttributes]
            ) -> list[SFTPAttributes]:
        for i, file_attr in enumerate(files_sorted_by_filename):
            file_attr: SFTPAttributes
            file = file_attr.filename
            if self.__trailer_check(file):
                continue
            if '.' in os.path.splitext(file)[0].strip(ascii_letters):
                try:
                    this_file = os.path.splitext(file)[0].strip(ascii_letters)
                    next_file = os.path.splitext(
                        files_sorted_by_filename[i + 1].filename
                    )[0].strip(ascii_letters)
                    if float(this_file) > float(next_file):
                        temp = files_sorted_by_filename[i]
                        files_sorted_by_filename[i] = (
                            files_sorted_by_filename[i + 1]
                        )
                        files_sorted_by_filename[i + 1] = temp
                except (ValueError, IndexError):
                    pass
        return files_sorted_by_filename

    async def __server_connect(self):
        self.ssh = paramiko.SSHClient()
        self.ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        self.ssh.connect(ADRESS_SFTP, self.PORT, USERNAME_SFTP, PASSWORD_SFTP)
        self.sftp = self.ssh.open_sftp()
        self.sftp.chdir(self.REMOTE_DIR)

    async def __server_disconnect(self):
        self.sftp.close()
        self.ssh.close()

    async def parse_maunt(self) -> Title:
        response = requests.get(self.url)
        soup = BeautifulSoup(response.text, 'html.parser')
        name = soup.find("h1").text.strip()  # Название релища
        image_url = "https://animaunt.org" + soup.find("img").get("src")  # Ссылка на картинку
        image_data = requests.get(image_url).content
        image_base64 = base64.b64encode(image_data.encode('utf-8'))  # Это бинарный вид
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
            'image_url': image_base64,
            'match_episode': second_number,
            'description': discription,
        }
        title = await AnimeDB.add_title(**kwargs)
        self.parsed_title_id = title.id
        return title

    async def upload_tg_channel(
            self,
            directory: str,
            number: float,
            key: str,
            view_number: str = None,
            caption: str = None,
            episode_id: int = None
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
        if key == 'Add':
            kwargs = {
                'title_id': self.parsed_title_id,
                'number': number,
                'view_number': view_number,
                'caption': caption,
                'video_msg_id': msg.id,
            }
            await AnimeDB.add_episode(**kwargs)
        elif key == 'Update':
            await AnimeDB.update_episode(episode_id, msg.id)

    async def download_video_with_sftp(self) -> None:
        await self.__server_connect()
        files_with_attributes = self.sftp.listdir_attr(self.remote_path)
        files_sorted_by_filename = sorted(
            files_with_attributes, key=lambda x: x.filename
        )
        files_sorted_by_filename = self.__special_sort(
            files_sorted_by_filename
        )
        for i, file_attr in enumerate(files_sorted_by_filename):
            file_attr: SFTPAttributes
            file = file_attr.filename
            if self.__trailer_check(file):
                continue
            remote_file_path = f'{self.remote_path}/{file}'
            local_file_path = f'{self.LOCAL_PATH}/{file}'
            number, view_number, caption = self.__make_number(file)
            try:
                next_number, *_ = self.__make_number(
                    files_sorted_by_filename[i + 1].filename
                )
                if number == next_number:
                    continue
            except (ValueError, IndexError):
                pass
            self.sftp.get(remote_file_path, local_file_path)
            await self.upload_tg_channel(
                local_file_path, number, 'Add', view_number, caption
            )
            last_update = dt.fromtimestamp(file_attr.st_mtime)
            await AnimeDB.update_title(
                self.parsed_title_id, number, last_update
            )
        await self.__server_disconnect()

    async def update_parser(self) -> None:
        await self.__server_connect()
        files_with_attributes = self.sftp.listdir_attr(self.remote_path)
        files_sorted_by_st_mtime = sorted(
            files_with_attributes, key=lambda x: x.st_mtime
        )
        for file_attr in files_sorted_by_st_mtime:
            file_attr: SFTPAttributes
            file = file_attr.filename
            if self.__trailer_check(file):
                continue
            title = await AnimeDB.get_title_for_parser(self.parsed_title_id)
            last_update = dt.fromtimestamp(file_attr.st_mtime)
            uploaded_episodes = {float(i.number): i.id for i in title.episodes}
            try:
                if last_update > title.last_update:
                    remote_file_path = f'{self.remote_path}/{file}'
                    local_file_path = f'{self.LOCAL_PATH}/{file}'
                    number, view_number, caption = self.__make_number(file)
                    self.sftp.get(remote_file_path, local_file_path)
                    if number in uploaded_episodes:
                        key = 'Update'
                        episode_id = uploaded_episodes[number]
                        number = None
                        view_number = None
                        caption = None
                    else:
                        key = 'Add'
                        episode_id = None
                        number = number
                        view_number = view_number
                        caption = caption
                    await self.upload_tg_channel(
                        local_file_path,
                        number,
                        key,
                        view_number,
                        caption,
                        episode_id
                    )
                    last_update = dt.fromtimestamp(file_attr.st_mtime)
                    await AnimeDB.update_title(
                        self.parsed_title_id, number, last_update
                    )
            except (TypeError, ValueError):
                pass
        await self.__server_disconnect()
