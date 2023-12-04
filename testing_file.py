from pyrogram import Client
import paramiko
import threading
import os
from config import USERNAME_SFTP, PASSWORD_SFTP, ADRESS_SFTP, API_HASH
from bs4 import BeautifulSoup
import requests
import base64
import re
from database.request import AnimeDB
import asyncio
from string import ascii_letters
from parse.server_parser import ServerParser
from parse.tasks import update_parser


async def upload_tg_channel(directory, title_id: int, number: int):
    api_id = 22207760
    api_hash = API_HASH
    client = Client("my_account", api_id, api_hash)
    chat_id = 1002020583106
    await client.start()
    # image = "C:\\Users\\Reidenshi\\Pictures\\test.jpg"
    msg = await client.send_video(chat_id=-chat_id, video=directory, width=1280, height=720)
    print(msg.id)  # Message ID
    print(f"Загружен в тг {directory}")
    os.remove(directory)
    await client.stop()
    kwargs = {
        'title_id': title_id,
        'number': number,
        'video_msg_id': msg.id
    }
    await AnimeDB.add_episode(**kwargs)


async def download_video_with_sftp(title_id: int):
    hostname = ADRESS_SFTP
    port = 22
    username = USERNAME_SFTP
    password = PASSWORD_SFTP
    remote_path = '/home/video/mp4/Знак! | Cue!'
    local_path = 'video'
    os.makedirs(local_path, exist_ok=True)
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh.connect(hostname, port, username, password)
    sftp = ssh.open_sftp()
    files_with_attributes = sftp.listdir_attr(remote_path)
    files_sorted_by_time = sorted(files_with_attributes, key=lambda x: x.st_mtime)
    for file_attr in files_sorted_by_time:
        file = file_attr.filename
        if file == 'trailer.mp4':
            continue
        remote_file_path = f'{remote_path}/{file}'
        local_file_path = f'{local_path}/{file}'
        number = int(os.path.splitext(file)[0].strip(ascii_letters))
        sftp.get(remote_file_path, local_file_path)
        print(f'{file} скачан успешно.')
        await upload_tg_channel(local_file_path, title_id, number)
    sftp.close()
    ssh.close()


def parse_maunt():
    link = "https://animaunt.org/11245-ubiyca-goblinov-2.html"
    response = requests.get(link)

    soup = BeautifulSoup(response.text, 'html.parser')
    name = soup.find("h1").text.strip() # Название релища
    image_url = "https://animaunt.org" + soup.find("img").get("src") # Ссылка на картинку
    image_data = requests.get(image_url).content
    image_base64 = base64.b64encode(image_data).decode('utf-8') # Это бинарный вид
    episodes_tag = soup.find_all('li', class_='vis-clear')
    for li_tag in episodes_tag:
        if 'Эпизоды:' in li_tag.get_text():
            episodes_text = li_tag.get_text().strip()
            numbers = re.findall(r'\d+', li_tag.get_text())
            second_number = numbers[1] # Число всего серий
            break
    episodes_tag = soup.find_all('li', class_='vis-gray')
    for li_tag in episodes_tag:
        if "Тип:" in li_tag.get_text():
            type_title = li_tag.get_text().strip().split(":")[1]
            break
    discription = soup.find('div', id='fdesc').text.strip()
    print(discription)
    return
    print(f"Название: {name}"\
        f"\nКартинка: {image_url}"\
        f"\nЭпизодов: {second_number}"\
        f"\nТип: {type_title}")
    # добавить description
    kwargs = {
        'name': name,
        'url': link,
        'image_url': image_url,
        'match_episode': second_number,

    }
    return asyncio.run(AnimeDB.add_title(**kwargs))


if __name__ == '__main__':
    parse_maunt()
    # update_parser()
    # parser = ServerParser('https://animaunt.org/10591-rukovodstvo-soten-demonov-3.html', '/home/video/mp4/Руководство сотен демонов 3 | Bai Yao Pu 3rd Season')
    # asyncio.run(parser.update_parser())