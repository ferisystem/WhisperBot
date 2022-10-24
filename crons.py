from telethon.tl.functions.channels import GetFullChannelRequest
from telethon.sync import TelegramClient, events
import telethon.tl.types as types
from datetime import datetime
from config_bot import *
from time import time
import subprocess
import telethon
import requests
import asyncio
import redis
import re
import os

client = TelegramClient(db, telegram_datas['api_id'], telegram_datas['api_hash']).start(bot_token=telegram_datas['botToken'])
loop = asyncio.get_event_loop()


async def main():
	ti_me = datetime.now()
	await client.send_message(139946685, "test")


with client:
	client.loop.run_until_complete(main())