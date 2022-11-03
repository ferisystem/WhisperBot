db = 'name_database'
# - - - - - - - - - - - - - #
telegram_datas = {
"botToken": "Bot_Token",
"api_hash": "api_hash",
"api_id": api_id,
"device_model": "Linux",
"system_version": "Ubuntu 20.04",
"app_version": "1.0",
}
# - - - - - - - - - - - - - #
sudo_users = (777000, telegram_datas['botToken'].split(':')[0], 000) # PUT_YOUR_ADMINS_HERE
# - - - - - - - - - - - - - #
IDs_datas = {
"sudo_id": SUDO_ID,
"bot_id": int(telegram_datas['botToken'].split(':')[0]),
"chUsername": "YOUR_CHANNEL_USERNAME", # for force join
"chLink": "YOUR_CHANNEL_LINK",
}
# - - - - - - - - - - - - - #
server_datas = {
"ip": "YOUR_SERVER_IP",
"port_server": 10128, #optional
"port_tg": 8443, #80, 88, 443, 8443
}
# - - - - - - - - - - - - - #
sendApi = "https://api.telegram.org/bot{}/".format(telegram_datas['botToken'])
# - - - - - - - - - - - - - #
git_url = 'https://raw.githubusercontent.com/ferisystem/ferisystem/files/files'
pic_atsign = f'{git_url}/atsign.jpg'
pic_user = f'{git_url}/user.jpg'
pic_message = f'{git_url}/message.jpg'
pic_question = f'{git_url}/question.jpg'
pic_group = f'{git_url}/group.jpg'
pic_all = f'{git_url}/all.jpg'
pic_tick = f'{git_url}/tick.jpg'
pic_cross = f'{git_url}/cross.jpg'
pic_special = f'{git_url}/special.jpg'



# - - - - - - - - - - - - - - - #
# don't change lines after this #
# - - - - - - - - - - - - - - - #



import telethon.errors.rpcerrorlist as telethonErrors
from aiogram.dispatcher import Dispatcher
from telethon.sync import TelegramClient
from aiogram import Bot, executor, types
import aiogram.utils.exceptions as expts
from termcolor import colored, cprint
from teleredis import RedisSession
from datetime import datetime
from aiohttp import web
from time import time
import coloredlogs
import asyncio
import logging
import string
import random
import redis
import ssl
import re
import os
with open("Files/language.json", encoding="utf-8") as file:
    lang = eval(file.read())
coloredlogs.install()
logging.getLogger("aiohttp").setLevel(logging.WARNING)
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - [%(name)s] %(message)s",
    datefmt="%d-%b-%y %H:%M:%S",
    file="aio.log",
)
log = logging.getLogger("broadcast")
stroge = redis.Redis(
    host="localhost", port=6379, db=3, decode_responses=False, encoding="utf-8"
)
session = RedisSession(db, stroge)
client = TelegramClient(
    session,
    api_id=telegram_datas["api_id"],
    api_hash=telegram_datas["api_hash"],
    device_model = telegram_datas['device_model'],
    system_version = telegram_datas['system_version'],
    app_version = telegram_datas['app_version']
)
client.session.save_entities = False
rds = redis.Redis(
    host="localhost", port=6379, db=3, decode_responses=True, encoding="utf-8"
)
loop = asyncio.get_event_loop()
bot = Bot(token=telegram_datas["botToken"], loop=loop)
dp = Dispatcher(bot)
sudo_id = IDs_datas["sudo_id"]
bot_id = IDs_datas["bot_id"]
global user_steps
user_steps = {}