import telethon.errors.rpcerrorlist as telethonErrors
from aiogram.dispatcher import Dispatcher
from telethon.sync import TelegramClient
from aiogram import (
    executor,
    types,
    Bot
)
import aiogram.utils.exceptions as expts
from termcolor import colored, cprint
from teleredis import RedisSession
from aiogram.dispatcher.webhook import (
    AnswerCallbackQuery,
    get_new_configured_app,
)
from datetime import datetime
from aiogram.types import (
    ReplyKeyboardMarkup,
    ReplyKeyboardRemove,
    KeyboardButton,
    InputMediaPhoto,
    InputTextMessageContent,
    InlineQueryResultArticle,
    InlineQueryResultCachedPhoto,
    InlineQueryResultCachedGif,
    InlineQueryResultCachedSticker,
    InlineQueryResultCachedVideo,
    InlineQueryResultCachedVoice,
    InputMediaVideo,
    InlineKeyboardMarkup as iMarkup,
    InlineKeyboardButton as iButtun,
    InlineQueryResultPhoto,
)
from config_bot2 import (
    telegram_datas,
    server_datas,
    sudo_users,
    IDs_datas,
    db
)
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


class DataBase:
    def get(hash):
        hash = "{}.{}".format(db, hash)
        return rds.get(hash)

    def delete(hash, *hash2):
        hash3 = []
        hash3.append("{}.{}".format(db, hash))
        for i in hash2:
            hash3.append("{}.{}".format(db, i))
        return rds.delete(*hash3)

    def set(hash, value):
        hash = "{}.{}".format(db, hash)
        return rds.set(hash, value)

    def mset(hash):
        hash2 = {}
        for i in hash:
            k = "{}.{}".format(db, i)
            hash2.update({k: hash[i]})
        return rds.mset(hash2)

    def setex(hash, time, value):
        hash = "{}.{}".format(db, hash)
        return rds.setex(hash, time, value)

    def incr(hash):
        hash = "{}.{}".format(db, hash)
        return rds.incr(hash)

    def incrby(hash, value):
        hash = "{}.{}".format(db, hash)
        return rds.incrby(hash, value)

    def decr(hash):
        hash = "{}.{}".format(db, hash)
        return rds.decr(hash)

    def decrby(hash, value):
        hash = "{}.{}".format(db, hash)
        return rds.decrby(hash, value)

    def ttl(hash):
        hash = "{}.{}".format(db, hash)
        return rds.ttl(hash)

    def hget(hash, value):
        hash = "{}.{}".format(db, hash)
        return rds.hget(hash, value)

    def hset(hash, value, field):
        hash = "{}.{}".format(db, hash)
        return rds.hset(hash, value, field)

    def hdel(hash, value):
        hash = "{}.{}".format(db, hash)
        return rds.hdel(hash, value)

    def sadd(hash, member):
        hash = "{}.{}".format(db, hash)
        return rds.sadd(hash, member)

    def srem(hash, member):
        hash = "{}.{}".format(db, hash)
        return rds.srem(hash, member)

    def sismember(hash, member):
        hash = "{}.{}".format(db, hash)
        return rds.sismember(hash, member)

    def smembers(hash):
        hash = "{}.{}".format(db, hash)
        return rds.smembers(hash)

    def scard(hash):
        hash = "{}.{}".format(db, hash)
        return rds.scard(hash)

    def keys(hash):
        hash = "{}.{}".format(db, hash)
        return rds.keys(hash)


class GlobalValues:
    def __init__(self):
        self.ipAdd = server_datas["ip"]
        self.ipAdD = "http://{}:{}".format(
            self.ipAdd, server_datas["port_server"]
        )
        self.WEBHOOK_URL_PATH = "/{}".format(telegram_datas["botToken"])
        self.port = server_datas["port_tg"]
        self.WEBHOOK_URL = "https://{}:{}{}".format(
            self.ipAdd, self.port, self.WEBHOOK_URL_PATH
        )
        self.WEBHOOK_SSL_CERT = "webhook_cert.pem"
        self.WEBHOOK_SSL_PRIV = "webhook_pkey.pem"
        self.botID = int(rds.hget(db, "id") or bot_id)
        self.botName = rds.hget(db, "name") or "None"
        self.botUser = rds.hget(db, "user") or "None"
        self.sudoID = int(DataBase.hget("sudo", "id") or sudo_id)
        self.supchat = int(rds.hget(db, "supchat") or self.sudoID)
        self.spychat = int(rds.hget(db, "spychat") or self.sudoID)
        self.linkyCH = rds.hget(db, "linkyCH") or "None"
        self.sudoUser = DataBase.hget("sudo", "user") or "None"
        self.sudo_users = (self.sudoID, self.botID) + sudo_users
        self.chLink = IDs_datas["chLink"]


class CheckMsg:
    def __init__(self, msg, echoMsg=False):
        if "text" in msg:
            self.content = "Text"
        elif "audio" in msg:
            self.content = "Audio"
        elif "voice" in msg:
            self.content = "Voice"
        elif "video" in msg:
            self.content = "Video"
        elif "video_note" in msg:
            self.content = "VideoNote"
        elif "photo" in msg:
            self.content = "Photo"
        elif "document" in msg:
            self.content = "File"
        elif "animation" in msg:
            self.content = "Gif"
        elif "poll" in msg:
            self.content = "Poll"
        elif "edit_date" in msg:
            self.content = "Edited"
        elif "game" in msg:
            self.content = "Game"
        elif "sticker" in msg:
            self.content = "Sticker"
        elif "contact" in msg:
            self.content = "Contact"
        elif "venue" in msg:
            self.content = "Venue"
        elif "location" in msg:
            self.content = "Location"
        elif "new_chat_members" in msg:
            self.content = "NewChatMembers"
        elif "left_chat_member" in msg:
            self.content = "LeftChatMember"
        elif "new_chat_title" in msg:
            self.content = "NewChatTitle"
        elif "new_chat_photo" in msg:
            self.content = "NewChatPhoto"
        elif "delete_chat_photo" in msg:
            self.content = "DeleteChatPhoto"
        elif "group_chat_created" in msg:
            self.content = "GroupChatCreated"
        elif "supergroup_chat_created" in msg:
            self.content = "SupergroupChatCreated"
        elif "channel_chat_created" in msg:
            self.content = "ChannelChatCreated"
        elif "migrate_to_chat_id" in msg:
            self.content = "MigrateToChatId"
        elif "pinned_message" in msg:
            self.content = "PinnedMessage"
        elif "invoice" in msg:
            self.content = "Invoice"
        elif "successful_payment" in msg:
            self.content = "SuccessfulPayment"
        elif "connected_website" in msg:
            self.content = "ConnectedWebsite"
        elif "passport_data" in msg:
            self.content = "PassportData"
        elif "reply_markup" in msg:
            self.content = "ReplyMarkup"
        elif "caption" in msg:
            self.content = "caption"
        if "reply_to_message" in msg:
            msg = msg.reply_to_message
            if "forward_from" in msg:
                self.user = msg.forward_from
            elif "from" in msg:
                self.user = msg.from_user
        else:
            if "forward_from" in msg:
                self.user = msg.forward_from
            elif "from" in msg:
                self.user = msg.from_user