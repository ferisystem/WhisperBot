# coding: utf8
from aiogram.types import ReplyKeyboardMarkup, ReplyKeyboardRemove, KeyboardButton, InputMediaPhoto, \
InputTextMessageContent, InlineQueryResultArticle, InlineQueryResultCachedPhoto, InputMediaVideo, \
InlineKeyboardMarkup as iMarkup, InlineKeyboardButton as iButtun, InlineQueryResultPhoto
from aiogram.dispatcher.webhook import AnswerCallbackQuery, get_new_configured_app
import telethon.errors.rpcerrorlist as telethonErrors
from aiogram.dispatcher import Dispatcher
from telethon.sync import TelegramClient
import aiogram.utils.exceptions as expts
from aiogram import Bot, executor, types
from termcolor import colored, cprint
from aiofile import AIOFile, Writer
from teleredis import RedisSession
from datetime import datetime
import urllib.request as ur
from pprint import pprint
from config_bot import *
from aiohttp import web
from time import time
import coloredlogs
import subprocess
import requests
import urllib3
import asyncio
import logging
import string
import redis
import json
import random
import ssl
import re
import os
stroge = redis.Redis(host = 'localhost', port = 6379, db = 3, decode_responses = False, encoding = 'utf-8')
session = RedisSession(db, stroge)
# print(session)
# print(db)
client = TelegramClient(
session, 
api_id = telegram_datas['api_id'], 
api_hash = telegram_datas['api_hash'], 
# device_model = telegram_datas['device_model'], 
# system_version = telegram_datas['system_version'], 
# app_version = telegram_datas['app_version']
)
client.session.save_entities = False
redis = redis.Redis(host = 'localhost', port = 6379, db = 3, decode_responses = True, encoding = 'utf-8')
# -------------------------------------------------------------------------------- #
coloredlogs.install()
logging.getLogger("aiohttp").setLevel(logging.WARNING)
# logging.getLogger("telethon").setLevel(logging.DEBUG)
logging.basicConfig(level = logging.INFO, \
format = '%(asctime)s - [%(name)s] %(message)s', \
datefmt = '%d-%b-%y %H:%M:%S', file = 'aio.log')
log = logging.getLogger('broadcast')
loop = asyncio.get_event_loop()
bot = Bot(token = telegram_datas['botToken'], loop = loop)
dp = Dispatcher(bot)
sudo_id = IDs_datas['sudo_id'];bot_id = IDs_datas['bot_id']
with open("Files/language.json", encoding = 'utf-8') as file:
	lang = eval(file.read())


class DataBase:
	
	def get(hash):
		hash = "{}.{}".format(db, hash)
		return redis.get(hash)


	def delete(hash, *hash2):
		hash3 = []
		hash3.append("{}.{}".format(db, hash))
		for i in hash2:
			hash3.append("{}.{}".format(db, i))
		return redis.delete(*hash3)


	def set(hash, value):
		hash = "{}.{}".format(db, hash)
		return redis.set(hash, value)


	def mset(hash):
		hash2 = {}
		for i in hash:
			k = "{}.{}".format(db, i)
			hash2.update({k:hash[i]})
		return redis.mset(hash2)


	def setex(hash, time, value):
		hash = "{}.{}".format(db, hash)
		return redis.setex(hash, time, value)


	def incr(hash):
		hash = "{}.{}".format(db, hash)
		return redis.incr(hash)

	
	def incrby(hash, value):
		hash = "{}.{}".format(db, hash)
		return redis.incrby(hash, value)


	def decr(hash):
		hash = "{}.{}".format(db, hash)
		return redis.decr(hash)


	def decrby(hash, value):
		hash = "{}.{}".format(db, hash)
		return redis.decrby(hash, value)


	def ttl(hash):
		hash = "{}.{}".format(db, hash)
		return redis.ttl(hash)


	def hget(hash, value):
		hash = "{}.{}".format(db, hash)
		return redis.hget(hash, value)


	def hset(hash, value, field):
		hash = "{}.{}".format(db, hash)
		return redis.hset(hash, value, field)


	def hmset(hash, *hash2):
		return redis.hmset(hash, *hash2)


	def hdel(hash, value, field):
		hash = "{}.{}".format(db, hash)
		return redis.hdel(hash, value, field)


	def sadd(hash, member):
		hash = "{}.{}".format(db, hash)
		return redis.sadd(hash, member)


	def srem(hash, member):
		hash = "{}.{}".format(db, hash)
		return redis.srem(hash, member)


	def sismember(hash, member):
		hash = "{}.{}".format(db, hash)
		return redis.sismember(hash, member)


	def smembers(hash):
		hash = "{}.{}".format(db, hash)
		return redis.smembers(hash)


	def scard(hash):
		hash = "{}.{}".format(db, hash)
		return redis.scard(hash)


	def keys(hash):
		hash = "{}.{}".format(db, hash)
		return redis.keys(hash)


class CheckMsg:
	
	def __init__(self, msg, echoMsg = False):
		if 'text' in msg:
			self.content = 'Text'
		elif 'audio' in msg:
			self.content = 'Audio'
		elif 'voice' in msg:
			self.content = 'Voice'
		elif 'video' in msg:
			self.content = 'Video'
		elif 'video_note' in msg:
			self.content = 'VideoNote'
		elif 'photo' in msg:
			self.content = 'Photo'
		elif 'document' in msg:
			self.content = 'File'
		elif 'animation' in msg:
			self.content = 'Gif'
		elif 'poll' in msg:
			self.content = 'Poll'
		elif 'edit_date' in msg:
			self.content = 'Edited'
		elif 'game' in msg:
			self.content = 'Game'
		elif 'sticker' in msg:
			self.content = 'Sticker'
		elif 'contact' in msg:
			self.content = 'Contact'
		elif 'venue' in msg:
			self.content = 'Venue'
		elif 'location' in msg:
			self.content = 'Location'
		elif 'new_chat_members' in msg:
			self.content = 'NewChatMembers'
		elif 'left_chat_member' in msg:
			self.content = 'LeftChatMember'
		elif 'new_chat_title' in msg:
			self.content = 'NewChatTitle'
		elif 'new_chat_photo' in msg:
			self.content = 'NewChatPhoto'
		elif 'delete_chat_photo' in msg:
			self.content = 'DeleteChatPhoto'
		elif 'group_chat_created' in msg:
			self.content = 'GroupChatCreated'
		elif 'supergroup_chat_created' in msg:
			self.content = 'SupergroupChatCreated'
		elif 'channel_chat_created' in msg:
			self.content = 'ChannelChatCreated'
		elif 'migrate_to_chat_id' in msg:
			self.content = 'MigrateToChatId'
		elif 'pinned_message' in msg:
			self.content = 'PinnedMessage'
		elif 'invoice' in msg:
			self.content = 'Invoice'
		elif 'successful_payment' in msg:
			self.content = 'SuccessfulPayment'
		elif 'connected_website' in msg:
			self.content = 'ConnectedWebsite'
		elif 'passport_data' in msg:
			self.content = 'PassportData'
		elif 'reply_markup' in msg:
			self.content = 'ReplyMarkup'
		elif 'caption' in msg:
			self.content = 'caption'
		if 'reply_to_message' in msg:
			msg = msg.reply_to_message
			if 'forward_from' in msg:
				self.user = msg.forward_from
			elif 'from' in msg:
				self.user = msg.from_user
		else:
			if 'forward_from' in msg:
				self.user = msg.forward_from
			elif 'from' in msg:
				self.user = msg.from_user


class gv: # Global Values
	
	def __init__(self):
		self.ipAdd = server_datas['ip']
		self.ipAdD = "http://{}:{}".format(self.ipAdd, server_datas['port_server'])
		self.WEBHOOK_URL_PATH = "/{}".format(telegram_datas['botToken'])
		self.port = server_datas['port_tg']
		self.WEBHOOK_URL = "https://{}:{}{}".format(self.ipAdd, self.port, self.WEBHOOK_URL_PATH)
		self.WEBHOOK_SSL_CERT = 'webhook_cert.pem'
		self.WEBHOOK_SSL_PRIV = 'webhook_pkey.pem'
		self.botID = int(redis.hget(db, 'id') or bot_id)
		self.botName = (redis.hget(db, 'name') or 'None')
		self.botUser = (redis.hget(db, 'user') or 'None')
		self.sudoID = int(DataBase.hget('sudo', 'id') or sudo_id)
		self.supchat = int(redis.hget(db, 'supchat') or self.sudoID)
		self.spychat = int(redis.hget(db, 'spychat') or self.sudoID)
		self.sudoUser = (DataBase.hget('sudo', 'user') or 'None')
		self.sudo_users = (self.sudoID, self.botID) + sudo_users
		self.chLink = IDs_datas['chLink']


def request(url, chat_id, control, langU):
	thing = False
	try:
		thing = requests.get(url)
	except:
		thing = requests.get(url)
	if control:
		try:
			if thing.json()['error']['message'] == "Quota limit exceeded":
				# sendText(chat_id, 0, 1, langU['try_request'])
				return False
		except KeyError:
			pass
		try:
			if thing.json()['error']:
				# sendText(chat_id, 0, 1, langU['not_found'])
				return False
		except KeyError:
			pass
	return thing


def cPrint(text, type = 1, backColor = "on_white", textColor = "blue", modes = None):
	"""
	print(colored('bold', 'red', attrs))
	# attrs = ['bold', 'dark', 'underline', \
	'blink', 'reverse', 'concealed']
	- - -
	2 >> print(colored('hello', 'red'), colored('world', 'green')) * best
	grey/red/green/yellow/blue/magenta/cyan/white/
	- - -
	1 >> cprint('Hello, World!', 'red', 'on_blue') * default in lua
	on_grey/on_red/on_green/on_yellow/on_blue/on_magenta/on_cyan/on_white
	"""
	if type == 1:
		cprint(text, textColor, backColor, attrs = modes)
	elif type == 2:
		print(colored(text, textColor, attrs = modes))


async def userInfos(userID, info = "name"):
	if userID:
		if redis.hget('userInfo:{}'.format(userID), info):
			return redis.hget("userInfo:{}".format(userID), info)
		elif redis.get('userInfo2:{}'.format(userID)):
			return redis.get('userInfo2:{}'.format(userID))
		else:
			try:
				b = await client.get_entity(int(userID))
				b = b.__dict__
				if info == "name":
					if 'title' in b:
						if re.match(r"^100(\d+)", userID):
							redis.hset("userInfo:-{}".format(userID), 'name', b['title'])
						elif re.match(r"^-100(\d+)", userID):
							redis.hset("userInfo:{}".format(userID), 'name', b['title'])
						else:
							redis.hset("userInfo:{}".format(userID), 'name', b['title'])
						return b['title']
					elif 'first_name' in b:
						redis.hset("userInfo:{}".format(userID), 'name', b['first_name'])
						return b['first_name']
					elif b['first_name'] == "":
						return 'Deleted Account'
					else:
						return 'Deleted'
				elif info == "username":
					if 'username' in b:
						redis.hset("userInfo:{}".format(userID), 'username', b['username'])
						if ('title' in b or 'megagroup' in b):
							if re.match(r"^100(\d+)", userID):
								redis.hset("UsernamesIds", b['username'].lower(), "-{}".format(userID))
							elif re.match(r"^-100(\d+)", userID):
								redis.hset("UsernamesIds", b['username'].lower(), userID)
						else:
							redis.hset("UsernamesIds", b['username'].lower(), userID)
						return b['username']
					else:
						return False
			except:
				redis.setex('userInfo2:{}'.format(userID), 86400, userID)
				return int(userID)
	else:
		return '!!!'


def set_stats(type_stat, hash, value = None):
	hash = "stat_{}".format(hash)
	if type_stat == "++":
		return DataBase.incrby(hash, value)
	elif type_stat == "--":
		return DataBase.decrby(hash, value)
	if type_stat == "+":
		return DataBase.incr(hash)
	elif type_stat == "-":
		return DataBase.decr(hash)


async def sendText(chat_id, reply_msg, dis_webpage, text, \
	parse_mode = None, reply_markup = None):
	dis_webpage = str(dis_webpage)
	dis_webpage = dis_webpage.replace("1", "True")
	dis_webpage = dis_webpage.replace("0", "False")
	if reply_msg is 0:
		reply_msgs = None
	elif reply_msg and str(reply_msg).isdigit():
		reply_msgs = reply_msg
	elif reply_msg and 'message_id' in reply_msg:
		reply_msgs = reply_msg.message_id
	else:
		reply_msgs = None
	if parse_mode:
		parse_mode = parse_mode.replace('md', 'Markdown')
		parse_mode = parse_mode.replace('html', 'HTML')
	if type(reply_markup) is tuple:
		if len(reply_markup)>0:
			markup = ReplyKeyboardMarkup(resize_keyboard = True, selective = True)
			for row in reply_markup:
				markup.row(*row)
		else:
			markup = ReplyKeyboardRemove()
	else:
		markup = reply_markup
	try:
		if DataBase.get('typing'):
			await bot.send_chat_action(chat_id, 'typing')
		result = await bot.send_message(chat_id = chat_id, text = text, parse_mode = (parse_mode or None), disable_web_page_preview = bool(dis_webpage), disable_notification = False, reply_to_message_id = reply_msgs, reply_markup = markup)
		DataBase.incr('amarBot.sendMsg')
		return True, result
	except expts.ChatNotFound as a:
		return a.args
	except expts.BotBlocked as a:
		#log.error(f"Target [ID:{chat_id}]: blocked by user")
		return a.args
	except expts.RetryAfter as a:
		# log.error(f"Target [ID:{chat_id}]: Flood limit is exceeded. Sleep {e.timeout} seconds.")
		await asyncio.sleep(a.timeout)
		return await sendText(chat_id, reply_msgs, 1, text, parse_mode, reply_markup)
	except expts.UserDeactivated as a:
		#log.error(f"Target [ID:{chat_id}]: user is deactivated")
		return a.args
	except expts.TelegramAPIError as a:
		if a.args[0] == "Reply message not found":
			try:
				return True, await sendText(chat_id, 0, 1, text, parse_mode, reply_markup)
			except:
				return a.args
		else:
			#log.error(f"Target [ID:{chat_id}]: failed")
			return a.args
	except expts.CantInitiateConversation as a:
		#log.error(f"Target [ID:{chat_id}]: user not started the bot")
		return a.args
	except expts.Unauthorized as a:
		#log.error(f"Target [ID:{chat_id}]: Unauthorized > {a}")
		return a.args
	except expts.BadRequest as a:
		if a.args[0] == "Reply message not found":
			try:
				return True, await sendText(chat_id, 0, 1, text, parse_mode, reply_markup)
			except:
				return a.args
		else:
			#log.error(f"Target [ID:{chat_id}]: BadRequest > {a}")
			return a.args
	except Exception as e:
		print(e)
		return False, False
		pass


async def sendPhoto(chat_id, photo, caption = None, parse_mode = None, reply_msg = None):
	if reply_msg is 0:
		reply_msgs = None
	elif reply_msg and 'message_id' in reply_msg:
		reply_msgs = reply_msg.message_id
	else:
		reply_msgs = None
	if parse_mode:
		parse_mode = parse_mode.replace('md', 'Markdown')
		parse_mode = parse_mode.replace('html', 'HTML')
	if type(caption) is str and len(caption) > 1000:
		# caption = make_short_caption(caption)
		if len(caption) > 1000:
			formol = len(caption)
			formol = formol - 1024
			caption = caption[formol:]
	try:
		if DataBase.get('typing'):
			await bot.send_chat_action(chat_id, 'upload_photo')
		result = await bot.send_photo(chat_id, photo, caption, parse_mode = parse_mode, reply_to_message_id = reply_msgs)
		return True, result
	except expts.ChatNotFound as a:
		return a.args
	except expts.BotBlocked as a:
		#log.error(f"Target [ID:{chat_id}]: blocked by user")
		return a.args
	except expts.RetryAfter as a:
		# log.error(f"Target [ID:{chat_id}]: Flood limit is exceeded. Sleep {e.timeout} seconds.")
		await asyncio.sleep(a.timeout)
		return await sendPhoto(chat_id, photo, caption, parse_mode, reply_msg)
	except expts.UserDeactivated as a:
		#log.error(f"Target [ID:{chat_id}]: user is deactivated")
		return a.args
	except expts.TelegramAPIError as a:
		if a.args[0] == "Reply message not found":
			try:
				return True, await sendPhoto(chat_id, photo, caption, parse_mode, 0)
			except:
				return a.args
		else:
			#log.error(f"Target [ID:{chat_id}]: failed")
			return a.args
	except expts.CantInitiateConversation as a:
		#log.error(f"Target [ID:{chat_id}]: user not started the bot")
		return a.args
	except expts.Unauthorized as a:
		#log.error(f"Target [ID:{chat_id}]: Unauthorized > {a}")
		return a.args
	except expts.BadRequest as a:
		if a.args[0] == "Reply message not found":
			try:
				return True, await sendPhoto(chat_id, photo, caption, parse_mode, 0)
			except:
				return a.args
		else:
			#log.error(f"Target [ID:{chat_id}]: BadRequest > {a}")
			return a.args
	except Exception as e:
		print(e)
		return False, False
		pass


async def sendAudio(chat_id, reply_msg, audio, caption = None, parse_mode = None,\
					duration = None, performer = None, title = None, thumb = None, dis_notif = 1,\
					reply_markup = None):
	dis_notif = str(dis_notif)
	dis_notif = dis_notif.replace("1", "True")
	dis_notif = dis_notif.replace("0", "False")
	dis_notif = bool(dis_notif)
	if reply_msg is 0:
		reply_msgs = None
	elif reply_msg and 'message_id' in reply_msg:
		reply_msgs = reply_msg.message_id
	else:
		reply_msgs = None
	if parse_mode:
		parse_mode = parse_mode.replace('md', 'Markdown')
		parse_mode = parse_mode.replace('html', 'HTML')
	if type(reply_markup) is tuple:
		if len(reply_markup)>0:
			markup = ReplyKeyboardMarkup(resize_keyboard = True, selective = True)
			for row in reply_markup:
				markup.row(*row)
		else:
			markup = ReplyKeyboardRemove()
	else:
		markup = reply_markup
	try:
		if DataBase.get('typing'):
			await bot.send_chat_action(chat_id, 'upload_audio')
		print(1111111111)
		result = await bot.send_audio(chat_id, audio, caption, parse_mode, duration, performer,\
		title, thumb, dis_notif, reply_msgs,\
		reply_markup)
		print(1323)
		return True, result
	except expts.ChatNotFound as a:
		return a.args
	except expts.BotBlocked as a:
		#log.error(f"Target [ID:{chat_id}]: blocked by user")
		return a.args
	except expts.RetryAfter as a:
		# log.error(f"Target [ID:{chat_id}]: Flood limit is exceeded. Sleep {e.timeout} seconds.")
		await asyncio.sleep(a.timeout)
		return await sendAudio(chat_id, audio, caption, parse_mode, duration, performer,\
		title, thumb, dis_notif, reply_msgs,\
		reply_markup)
	except expts.UserDeactivated as a:
		#log.error(f"Target [ID:{chat_id}]: user is deactivated")
		return a.args
	except expts.TelegramAPIError as a:
		if a.args[0] == "Reply message not found":
			try:
				return True, await sendAudio(chat_id, audio, caption, parse_mode, duration, performer,\
				title, thumb, dis_notif, 0,\
				reply_markup)
			except:
				return a.args
		else:
			#log.error(f"Target [ID:{chat_id}]: failed")
			return a.args
	except expts.CantInitiateConversation as a:
		#log.error(f"Target [ID:{chat_id}]: user not started the bot")
		return a.args
	except expts.Unauthorized as a:
		#log.error(f"Target [ID:{chat_id}]: Unauthorized > {a}")
		return a.args
	except expts.BadRequest as a:
		if a.args[0] == "Reply message not found":
			try:
				return True, await sendAudio(chat_id, audio, caption, parse_mode, duration, performer,\
				title, thumb, dis_notif, 0,\
				reply_markup)
			except:
				return a.args
		else:
			#log.error(f"Target [ID:{chat_id}]: BadRequest > {a}")
			return a.args
	except Exception as e:
		if 'Can not serialize value type:' in str(e):
			await sendDocument(chat_id, audio, caption = caption, parse_mode = parse_mode,\
					thumb = thumb, dis_notif = dis_notif, reply_msg = reply_msg, reply_markup = reply_markup)
		else:
			print(e)
			return False, False
			pass


async def sendVoice(chat_id, reply_msg, voice, caption = None, parse_mode = None,\
					duration = None, dis_notif = 1,\
					reply_markup = None):
	dis_notif = str(dis_notif)
	dis_notif = dis_notif.replace("1", "True")
	dis_notif = dis_notif.replace("0", "False")
	dis_notif = bool(dis_notif)
	if reply_msg is 0:
		reply_msgs = None
	elif reply_msg and 'message_id' in reply_msg:
		reply_msgs = reply_msg.message_id
	else:
		reply_msgs = None
	if parse_mode:
		parse_mode = parse_mode.replace('md', 'Markdown')
		parse_mode = parse_mode.replace('html', 'HTML')
	if type(reply_markup) is tuple:
		if len(reply_markup)>0:
			markup = ReplyKeyboardMarkup(resize_keyboard = True, selective = True)
			for row in reply_markup:
				markup.row(*row)
		else:
			markup = ReplyKeyboardRemove()
	else:
		markup = reply_markup
	try:
		if DataBase.get('typing'):
			await bot.send_chat_action(chat_id, 'record_voice')	
		result = await bot.send_voice(chat_id, voice, caption, parse_mode, duration,\
		dis_notif, reply_msgs, reply_markup)
		return True, result
	except expts.ChatNotFound as a:
		return a.args
	except expts.BotBlocked as a:
		#log.error(f"Target [ID:{chat_id}]: blocked by user")
		return a.args
	except expts.RetryAfter as a:
		# log.error(f"Target [ID:{chat_id}]: Flood limit is exceeded. Sleep {e.timeout} seconds.")
		await asyncio.sleep(a.timeout)
		return await sendVoice(chat_id, voice, caption, parse_mode, duration,\
		dis_notif, reply_msgs, reply_markup)
	except expts.UserDeactivated as a:
		#log.error(f"Target [ID:{chat_id}]: user is deactivated")
		return a.args
	except expts.TelegramAPIError as a:
		if a.args[0] == "Reply message not found":
			try:
				return True, await sendVoice(chat_id, voice, caption, parse_mode, duration,\
				dis_notif, 0, reply_markup)
			except:
				return a.args
		else:
			#log.error(f"Target [ID:{chat_id}]: failed")
			return a.args
	except expts.CantInitiateConversation as a:
		#log.error(f"Target [ID:{chat_id}]: user not started the bot")
		return a.args
	except expts.Unauthorized as a:
		#log.error(f"Target [ID:{chat_id}]: Unauthorized > {a}")
		return a.args
	except expts.BadRequest as a:
		if a.args[0] == "Reply message not found":
			try:
				return True, await sendVoice(chat_id, voice, caption, parse_mode, duration,\
		dis_notif, 0, reply_markup)
			except:
				return a.args
		else:
			#log.error(f"Target [ID:{chat_id}]: BadRequest > {a}")
			return a.args
	except Exception as e:
		print(e)
		return False, False
		pass


async def sendVideo(chat_id, reply_msg, video, caption = None, parse_mode = None,\
					duration = None, thumb = None, width = None, height = None,\
					supports_streaming = True, dis_notif = 1, reply_markup = None):
	dis_notif = str(dis_notif)
	dis_notif = dis_notif.replace("1", "True")
	dis_notif = dis_notif.replace("0", "False")
	dis_notif = bool(dis_notif)
	if reply_msg is 0:
		reply_msgs = None
	elif reply_msg and 'message_id' in reply_msg:
		reply_msgs = reply_msg.message_id
	else:
		reply_msgs = None
	if parse_mode:
		parse_mode = parse_mode.replace('md', 'Markdown')
		parse_mode = parse_mode.replace('html', 'HTML')
	if type(caption) is str and len(caption) > 1000:
		# caption = make_short_caption(caption)
		if len(caption) > 1000:
			formol = len(caption)
			formol = formol - 1024
			caption = caption[formol:]
	if type(reply_markup) is tuple:
		if len(reply_markup)>0:
			markup = ReplyKeyboardMarkup(resize_keyboard = True, selective = True)
			for row in reply_markup:
				markup.row(*row)
		else:
			markup = ReplyKeyboardRemove()
	else:
		markup = reply_markup
	try:
		if DataBase.get('typing'):
			await bot.send_chat_action(chat_id, 'upload_video')	
		result = await bot.send_video(chat_id, video, duration,\
		width, height, thumb, caption, parse_mode, supports_streaming,\
		dis_notif, reply_msgs, reply_markup)
		# print(result)
		return True, result
	except expts.ChatNotFound as a:
		return a.args
	except expts.BotBlocked as a:
		#log.error(f"Target [ID:{chat_id}]: blocked by user")
		return a.args
	except expts.RetryAfter as a:
		# log.error(f"Target [ID:{chat_id}]: Flood limit is exceeded. Sleep {e.timeout} seconds.")
		await asyncio.sleep(a.timeout)
		return await sendVideo(chat_id, reply_msgs, video, caption, parse_mode,\
				duration, thumb, width, height,\
				supports_streaming, dis_notif, reply_markup)
	except expts.UserDeactivated as a:
		#log.error(f"Target [ID:{chat_id}]: user is deactivated")
		return a.args
	except expts.TelegramAPIError as a:
		if a.args[0] == "Reply message not found":
			try:
				return True, await sendVideo(chat_id, 0, video, caption, parse_mode,\
				duration, thumb, width, height,\
				supports_streaming, dis_notif, reply_markup)
			except:
				return a.args
		else:
			#log.error(f"Target [ID:{chat_id}]: failed")
			return a.args
	except expts.CantInitiateConversation as a:
		#log.error(f"Target [ID:{chat_id}]: user not started the bot")
		return a.args
	except expts.Unauthorized as a:
		#log.error(f"Target [ID:{chat_id}]: Unauthorized > {a}")
		return a.args
	except expts.BadRequest as a:
		if a.args[0] == "Reply message not found":
			try:
				return True, await sendVideo(chat_id, 0, video, caption, parse_mode,\
				duration, thumb, width, height,\
				supports_streaming, dis_notif, reply_markup)
			except:
				return a.args
		else:
			#log.error(f"Target [ID:{chat_id}]: BadRequest > {a}")
			return a.args
	except Exception as e:
		print(e)
		return False, False
		pass


async def sendDocument(chat_id, document, caption = None, parse_mode = None,\
					thumb = None, dis_notif = None, reply_msg = None, reply_markup = None):
	dis_notif = str(dis_notif)
	dis_notif = dis_notif.replace("1", "True")
	dis_notif = dis_notif.replace("0", "False")
	dis_notif = bool(dis_notif)
	if reply_msg is 0:
		reply_msgs = None
	elif reply_msg and 'message_id' in reply_msg:
		reply_msgs = reply_msg.message_id
	else:
		reply_msgs = None
	if parse_mode:
		parse_mode = parse_mode.replace('md', 'Markdown')
		parse_mode = parse_mode.replace('html', 'HTML')
	if type(reply_markup) is tuple:
		if len(reply_markup)>0:
			markup = ReplyKeyboardMarkup(resize_keyboard = True, selective = True)
			for row in reply_markup:
				markup.row(*row)
		else:
			markup = ReplyKeyboardRemove()
	else:
		markup = reply_markup
	try:
		if DataBase.get('typing'):
			await bot.send_chat_action(chat_id, 'upload_video')	
		result = await bot.send_document(chat_id, document, thumb, caption, parse_mode,\
		dis_notif, reply_msgs, reply_markup)
		return True, result
	except expts.ChatNotFound as a:
		return a.args
	except expts.BotBlocked as a:
		#log.error(f"Target [ID:{chat_id}]: blocked by user")
		return a.args
	except expts.RetryAfter as a:
		# log.error(f"Target [ID:{chat_id}]: Flood limit is exceeded. Sleep {e.timeout} seconds.")
		await asyncio.sleep(a.timeout)
		return await sendDocument(chat_id, document, caption, parse_mode,\
		thumb, dis_notif, reply_msgs, reply_markup)
	except expts.UserDeactivated as a:
		#log.error(f"Target [ID:{chat_id}]: user is deactivated")
		return a.args
	except expts.TelegramAPIError as a:
		if a.args[0] == "Reply message not found":
			try:
				return True, await sendDocument(chat_id, document, caption, parse_mode,\
				thumb, dis_notif, 0, reply_markup)
			except:
				return a.args
		else:
			#log.error(f"Target [ID:{chat_id}]: failed")
			return a.args
	except expts.CantInitiateConversation as a:
		#log.error(f"Target [ID:{chat_id}]: user not started the bot")
		return a.args
	except expts.Unauthorized as a:
		#log.error(f"Target [ID:{chat_id}]: Unauthorized > {a}")
		return a.args
	except expts.BadRequest as a:
		if a.args[0] == "Reply message not found":
			try:
				return True, await sendDocument(chat_id, document, caption, parse_mode,\
				thumb, dis_notif, 0, reply_markup)
			except:
				return a.args
		else:
			#log.error(f"Target [ID:{chat_id}]: BadRequest > {a}")
			return a.args
	except Exception as e:
		print(e)
		return False, False
		pass


async def sendMediaGroup(chat_id, reply_msg, dis_notif, media):
	dis_notif = str(dis_notif)
	dis_notif = dis_notif.replace("1", "True")
	dis_notif = dis_notif.replace("0", "False")
	dis_notif = bool(dis_notif)
	if reply_msg is 0:
		reply_msgs = None
	elif reply_msg and 'message_id' in reply_msg:
		reply_msgs = reply_msg.message_id
	else:
		reply_msgs = None
	try:
		# print(media)
		result = await bot.send_media_group(chat_id = chat_id, media = media, disable_notification = dis_notif, reply_to_message_id = reply_msgs, allow_sending_without_reply = True)
		return True, result
	except expts.ChatNotFound as a:
		return a.args
	except expts.BotBlocked as a:
		#log.error(f"Target [ID:{chat_id}]: blocked by user")
		return a.args
	except expts.RetryAfter as a:
		# log.error(f"Target [ID:{chat_id}]: Flood limit is exceeded. Sleep {e.timeout} seconds.")
		await asyncio.sleep(a.timeout)
		return await sendMediaGroup(chat_id, reply_msgs, dis_notif, media)
	except expts.UserDeactivated as a:
		#log.error(f"Target [ID:{chat_id}]: user is deactivated")
		return a.args
	except expts.TelegramAPIError as a:
		if a.args[0] == "Reply message not found":
			try:
				return True, await sendMediaGroup(chat_id, 0, dis_notif, media)
			except:
				return a.args
		else:
			#log.error(f"Target [ID:{chat_id}]: failed")
			return a.args
	except expts.CantInitiateConversation as a:
		#log.error(f"Target [ID:{chat_id}]: user not started the bot")
		return a.args
	except expts.Unauthorized as a:
		#log.error(f"Target [ID:{chat_id}]: Unauthorized > {a}")
		return a.args
	except expts.BadRequest as a:
		if a.args[0] == "Reply message not found":
			try:
				return True, await sendMediaGroup(chat_id, 0, dis_notif, media)
			except:
				return a.args
		else:
			#log.error(f"Target [ID:{chat_id}]: BadRequest > {a}")
			return a.args
	except Exception as e:
		print(e)
		return False, False
		pass


async def copyMessage(chat_id, from_chat_id, message_id, caption = None,\
	parse_mode = None, caption_entities = None, dis_notif = None,\
	protect_content = True, reply_msg = None,\
	allow_sending_without_reply = True, reply_markup = None):
	dis_notif = str(dis_notif)
	dis_notif = dis_notif.replace("1", "True")
	dis_notif = dis_notif.replace("0", "False")
	dis_notif = bool(dis_notif)
	if reply_msg is 0:
		reply_msgs = None
	elif reply_msg and str(reply_msg).isdigit():
		reply_msgs = reply_msg
	elif reply_msg and 'message_id' in reply_msg:
		reply_msgs = reply_msg.message_id
	else:
		reply_msgs = None
	if parse_mode:
		parse_mode = parse_mode.replace('md', 'Markdown')
		parse_mode = parse_mode.replace('html', 'HTML')
	if type(reply_markup) is tuple:
		if len(reply_markup)>0:
			markup = ReplyKeyboardMarkup(resize_keyboard = True, selective = True)
			for row in reply_markup:
				markup.row(*row)
		else:
			markup = ReplyKeyboardRemove()
	else:
		markup = reply_markup
	try:
		result = await bot.copy_message(chat_id, from_chat_id, message_id, caption,\
		parse_mode = parse_mode, caption_entities = caption_entities,\
		disable_notification = dis_notif, protect_content = protect_content,\
		reply_to_message_id = reply_msg,\
		allow_sending_without_reply = allow_sending_without_reply,
		reply_markup = reply_markup)
		return True, result
	except expts.ChatNotFound as a:
		return a.args
	except expts.BotBlocked as a:
		#log.error(f"Target [ID:{chat_id}]: blocked by user")
		return a.args
	except expts.RetryAfter as a:
		# log.error(f"Target [ID:{chat_id}]: Flood limit is exceeded. Sleep {e.timeout} seconds.")
		await asyncio.sleep(a.timeout)
		return await copyMessage(chat_id, from_chat_id, message_id, caption, parse_mode,\
		caption_entities, disable_notification, protect_content, reply_to_message_id,\
		allow_sending_without_reply, reply_markup)
	except expts.UserDeactivated as a:
		#log.error(f"Target [ID:{chat_id}]: user is deactivated")
		return a.args
	except expts.TelegramAPIError as a:
		if a.args[0] == "Reply message not found":
			try:
				return True, await copyMessage(chat_id, from_chat_id, message_id, caption, parse_mode,\
				caption_entities, disable_notification, protect_content, 0,\
				allow_sending_without_reply, reply_markup)
			except:
				return a.args
		else:
			#log.error(f"Target [ID:{chat_id}]: failed")
			return a.args
	except expts.CantInitiateConversation as a:
		#log.error(f"Target [ID:{chat_id}]: user not started the bot")
		return a.args
	except expts.Unauthorized as a:
		#log.error(f"Target [ID:{chat_id}]: Unauthorized > {a}")
		return a.args
	except expts.BadRequest as a:
		if a.args[0] == "Reply message not found":
			try:
				return True, await copyMessage(chat_id, from_chat_id, message_id, caption, parse_mode,\
				caption_entities, disable_notification, protect_content, 0,\
				allow_sending_without_reply, reply_markup)
			except:
				return a.args
		else:
			#log.error(f"Target [ID:{chat_id}]: BadRequest > {a}")
			return a.args
	except Exception as e:
		print(e)
		return False, False
		pass


async def editText(chat_id, msg_id, inline_msg_id, text, parse_mode = None, reply_markup = None, entities = None):
	if msg_id>0 and inline_msg_id>0:
		print("Error in editText")
		return False
	if parse_mode:
		parse_mode = parse_mode.replace('md', 'Markdown')
		parse_mode = parse_mode.replace('html', 'HTML')
	if type(reply_markup) is tuple:
		if len(reply_markup)>0:
			markup = ReplyKeyboardMarkup(resize_keyboard = True, selective = True)
			for row in reply_markup:
				markup.row(*row)
		else:
			markup = ReplyKeyboardRemove()
	else:
		markup = reply_markup
	try:
		DataBase.incr('amarBot.editbybot')
		if inline_msg_id>0:
			result = await bot.edit_message_text(text = text, parse_mode = (parse_mode or None), inline_message_id = msg_id, reply_markup = markup, entities = entities)#, disable_web_page_preview = False)
			return True, result
		elif msg_id>0:
			result = await bot.edit_message_text(chat_id = chat_id, text = text, parse_mode = (parse_mode or None), disable_web_page_preview = True, message_id = msg_id, reply_markup = markup)
			return True, result
	except expts.BadRequest as a:
		await bot.send_message(chat_id = gv().sudoID, text = 'Chat ID: {}\nError: {}'.format(chat_id, a.args))
		return a.args
	except Exception as e:
		print(e)


async def answerCallbackQuery(query_id, text, show_alert = False, cache_time = 0, url_web = None):
	try:
		return await bot.answer_callback_query(query_id.id, text, show_alert, url_web, cache_time)
	except Exception as e:
		print(e)
		return False


async def getChatMember(ChatID, UserID):
	try:
		return await bot.get_chat_member(ChatID, UserID)
	except expts.BadRequest as a:
		return a.args
	except expts.Unauthorized as a:
		return a.args
	except Exception as e:
		print(e)
		return False


async def is_Channel_Member(channel, user):
	var = True
	send = await getChatMember(channel, user)
	if not type(send) is types.chat_member.ChatMember:
		var = True
	elif type(send) is types.chat_member.ChatMember and (send.status == "kicked" or send.status == "left"):
		var = False
	return var


def isSudo(id):
	if int(id) in sudo_users:
		return True
	else:
		return False


def isSuper(msg):
	if msg.chat.type == "supergroup":
		return True
	else:
		return False


def isGroup(msg):
	if msg.chat.type == "group":
		return True
	else:
		return False


def isPv(msg):
	if msg.chat.type == "private":
		return True
	else:
		return False


def isBlock(UserID):
	if DataBase.get('isBan:{}'.format(UserID)):
		return True
	else:
		return False


def menMD(msg):
	return '[{}](tg://user?id={})'.format(msg.from_user.first_name, msg.from_user.id)


def menHTML(msg):
	return '<a href="tg://user?id={}">{} </a>'.format(msg.from_user.id, msg.from_user.first_name)


def gregorian_to_jalali(gy,gm,gd):
	g_d_m=[0,31,59,90,120,151,181,212,243,273,304,334]
	if(gy>1600):
		jy=979
		gy-=1600
	else:
		jy=0
		gy-=621
	if(gm>2):
		gy2=gy+1
	else:
		gy2=gy
	days=(365*gy)+(int((gy2+3)/4))-(int((gy2+99)/100))+(int((gy2+399)/400))-80+gd+g_d_m[gm-1]
	jy+=33*(int(days/12053))
	days%=12053
	jy+=4*(int(days/1461))
	days%=1461
	if(days>365):
		jy+=int((days-1)/365)
		days=(days-1)%365
	if(days<186):
		jm=1+int(days/31)
		jd=1+(days%31)
	else:
		jm=7+int((days-186)/30)
		jd=1+((days-186)%30)
	return [jy,jm,jd]


def echoMonth(month,jalaly=False):
	month=int(month)
	if jalaly:
		if month==1:
			text="فروردین"
		elif month==2:
			text="اردیبهشت"
		elif month==3:
			text="خرداد"
		elif month==4:
			text="تیر"
		elif month==5:
			text="مرداد"
		elif month==6:
			text="شهریور"
		elif month==7:
			text="مهر"
		elif month==8:
			text="آبان"
		elif month==9:
			text="آذر"
		elif month==10:
			text="دی"
		elif month==11:
			text="بهمن"
		elif month==12:
			text="اسفند"
	else:
		if month==1:
			text="January"
		elif month==2:
			text="February"
		elif month==3:
			text="March"
		elif month==4:
			text="April"
		elif month==5:
			text="May"
		elif month==6:
			text="June"
		elif month==7:
			text="July"
		elif month==8:
			text="August"
		elif month==9:
			text="September"
		elif month==10:
			text="October"
		elif month==11:
			text="November"
		elif month==12:
			text="December"
	return text


def re_matches(match, input, type_re = None):
	if type_re == 's':
		if re.search(r"{}".format(match), input):
			ap = re.search(r"{}".format(match), input)
			ap = (ap.group(0),) + ap.groups()
			return ap
		else:
			return None
	else:
		if re.match(r"{}".format(match), input):
			ap = re.match(r"{}".format(match), input)
			ap = (ap.group(0),) + ap.groups()
			return ap
		else:
			return None


async def newUser(msg):
	DataBase.sadd('allUsers', msg.from_user.id)
	await sendText(gv().sudoID, 0, 1, '#NewUser\n{} > `{}`\nType: {}\nStatus: Active✅'.format(menMD(msg), msg.from_user.id, msg.text), 'md', blockKeys(msg.from_user.id))


async def memberCommands(msg, input, gp_id, is_super, is_fwd):
	# print(msg)
	# text:
	# {"message_id": 33036,
	# "from": {"id": 139946685, "is_bot": false, "first_name": "Alireza .Feri 🏴", "username": "ferisystem", "language_code": "de"},
	# "chat": {"id": 139946685, "first_name": "Alireza .Feri 🏴", "username": "ferisystem", "type": "private"},
	# "date": 1664547137, "text": "a"}
	# photo:
	# {"message_id": 33037,
	# "from": {"id": 139946685, "is_bot": false, "first_name": "Alireza .Feri 🏴", "username": "ferisystem", "language_code": "de"},
	# "chat": {"id": 139946685, "first_name": "Alireza .Feri 🏴", "username": "ferisystem", "type": "private"},
	# "date": 1664547180, "photo": [
	# {"file_id": "AgACAgQAAxkBAAKBDWM2-WwAAVBy_Xa7Ooord4Qsc5n2IgAC_LkxGwABsrlRx_tiUXUM5yIBAAMCAANzAAMqBA",
	# "file_unique_id": "AQAD_LkxGwABsrlReA",
	# "file_size": 1349, "width": 90, "height": 90},
	# {"file_id": "AgACAgQAAxkBAAKBDWM2-WwAAVBy_Xa7Ooord4Qsc5n2IgAC_LkxGwABsrlRx_tiUXUM5yIBAAMCAANtAAMqBA",
	# "file_unique_id": "AQAD_LkxGwABsrlRcg", "file_size": 11346, "width": 320, "height": 320}]
	# }
	# photo with caption:
	# {"message_id": 33038,
	# "from": {"id": 139946685, "is_bot": false, "first_name": "Alireza .Feri 🏴", "username": "ferisystem", "language_code": "de"},
	# "chat": {"id": 139946685, "first_name": "Alireza .Feri 🏴", "username": "ferisystem", "type": "private"},
	# "date": 1664547261, "photo": [
	# {"file_id": "AgACAgQAAxkBAAKBDmM2-b0OxEokHFWTT8XgywHZ9dzHAAL8uTEbAAGyuVHH-2JRdQznIgEAAwIAA3MAAyoE",
	# "file_unique_id": "AQAD_LkxGwABsrlReA", "file_size": 1349, "width": 90, "height": 90},
	# {"file_id": "AgACAgQAAxkBAAKBDmM2-b0OxEokHFWTT8XgywHZ9dzHAAL8uTEbAAGyuVHH-2JRdQznIgEAAwIAA20AAyoE",
	# "file_unique_id": "AQAD_LkxGwABsrlRcg", "file_size": 11346, "width": 320, "height": 320}],
	# "caption": "a\nb\nc", "caption_entities": [{"type": "bold", "offset": 2, "length": 2},
	# {"type": "text_link", "offset": 4, "length": 1, "url": "https://google.com/"}]
	# }
	_ = CheckMsg(msg)
	user_id = msg.from_user.id
	user_name = msg.from_user.first_name
	chat_id = msg.chat.id
	msg_id = msg.message_id
	content = _.content
	langU = lang[user_steps[user_id]['lang']]
	if 'reply_to_message' in msg:
		reply_msg = msg.reply_to_message
		reply_id = reply_msg.message_id
	else:
		reply_msg = None
		reply_id = 0
	etebar = int(DataBase.get('user.etebar:{}'.format(user_id)) or '0')
	if is_super:
		pass
	else:
		if isBlock(user_id):
			if not DataBase.get('user.alertBlocked:{}'.format(user_id)):
				DataBase.setex('user.alertBlocked:{}'.format(user_id), 120, "True")
				await sendText(chat_id, 0, 1, langU['u_are_blocked'])
			return False
		if DataBase.get('who_conneted:{}'.format(user_id)) and not '/start' in msg.text:
			which_user = DataBase.get('who_conneted:{}'.format(user_id))
			DataBase.delete('who_conneted:{}'.format(user_id))
			# if not msg.text:
				# msg_ = await copyMessage(which_user, chat_id, msg_id, caption = msg.caption,\
				# caption_entities = msg.caption_entities, reply_msg = None,\
				 # reply_markup = anonymous_new_message_keys(which_user, user_id, msg_id))
			# else:
				# msg_ = await copyMessage(which_user, chat_id, msg_id, reply_msg = None,
				# reply_markup = anonymous_new_message_keys(which_user, user_id, msg_id))
			msg_ = await msg.forward(gv().supchat)
			await sendText(chat_id, msg, 1, langU['your_msg_sent'], 'md', anonymous_back_keys(user_id))
			# DataBase.setex('msg_from:{}'.format(msg_id), 86400*30, user_id)
			DataBase.sadd('inbox_user:{}'.format(which_user), f"{msg_.message_id}:{user_id}:{msg_id}:0:{int(time())}:no")
			DataBase.setex('is_stater:{}'.format(user_id), 86400*7, 'True')
			await sendText(which_user, 0, 1, langU['new_message'].format(msg_.message_id))
		if reply_msg:
			if 'reply_markup' in reply_msg:
				input_ = reply_msg.reply_markup.inline_keyboard[0][0].callback_data
				if 'anon:blo' in input_:
					ap = re_matches(r'^anon:blo:(\d+):(\d+):@(\d+)$', input_)
					which_user = int(ap[1])
					if DataBase.sismember('blocks:{}'.format(which_user), user_id):
						await sendText(chat_id, msg, 1, langU['yare_blocked_anon'], 'md', anonymous_back_keys(user_id))
						return False
					if not msg.text:
						# msg_ = await copyMessage(which_user, chat_id, msg_id, caption = msg.caption,\
						# caption_entities = msg.caption_entities, reply_msg = None,\
						 # reply_markup = anonymous_new_message_keys(which_user, user_id, msg_id))
						msg_ = await msg.forward(gv().supchat)
					elif not '/start' in msg.text:
						# msg_ = await copyMessage(which_user, chat_id, msg_id, reply_msg = None,
						# reply_markup = anonymous_new_message_keys(which_user, user_id, msg_id))
						msg_ = await msg.forward(gv().supchat)
					await sendText(chat_id, msg, 1, langU['your_msg_sent'], 'md', anonymous_back_keys(user_id))
					# DataBase.setex('msg_from:{}'.format(msg_id), 86400*30, user_id)
					if DataBase.get('is_stater:{}'.format(which_user)):
						DataBase.sadd('inbox_user:{}'.format(which_user), f"{msg_.message_id}:{user_id}:{msg_id}:{ap[2]}:{int(time())}:yes")
					else:
						DataBase.sadd('inbox_user:{}'.format(which_user), f"{msg_.message_id}:{user_id}:{msg_id}:{ap[2]}:{int(time())}:no")
					await sendText(which_user, 0, 1, langU['new_message'].format(msg_.message_id))
		if 'text' in msg:
			input = msg.text.lower()
			if DataBase.get('ready_to_change_link:{}'.format(user_id)) and not '/start' in input:
				if 12 < len(msg.text) < 3 or not msg.text.isalnum():
					await sendText(chat_id, msg, 1, langU['rules_cus_link_anon'], 'md', anonymous_cus_link_keys(user_id))
				elif DataBase.sismember('links_anon', msg.text):
					await sendText(chat_id, msg, 1, langU['rules_cus_link_anon2'], 'md', anonymous_cus_link_keys(user_id))
				else:
					link_previous = DataBase.get('link_anon:{}'.format(user_id))
					DataBase.delete('link_anon:{}'.format(link_previous))
					DataBase.srem('links_anon', link_previous)
					DataBase.set('link_anon:{}'.format(user_id), msg.text)
					DataBase.set('link_anon:{}'.format(msg.text), user_id)
					DataBase.sadd('links_anon', msg.text)
					DataBase.delete('ready_to_change_link:{}'.format(user_id))
					await bot.delete_message(chat_id, DataBase.get('pre_msgbot:{}'.format(user_id)))
					await sendText(chat_id, msg, 1, "{}\nt.me/{}?start={}".format(langU['customize_link_anon'],
					redis.hget(db, 'user'), DataBase.get('link_anon:{}'.format(user_id))), 'md', anonymous_cus_link_keys(user_id))
			if DataBase.get('ready_to_change_name:{}'.format(user_id)) and not '/start' in input:
				if 21 < len(msg.text):
					await sendText(chat_id, msg, 1, langU['rules_cus_name_anon'], 'md')
				else:
					DataBase.set('name_anon:{}'.format(user_id), msg.text)
					DataBase.delete('ready_to_change_name:{}'.format(user_id))
					await bot.delete_message(chat_id, DataBase.get('pre_msgbot:{}'.format(user_id)))
					await sendText(chat_id, msg, 1, langU['changed_name_anon'], 'md', anonymous_cus_name_keys(user_id))
			if DataBase.get('ready_to_enter_id:{}'.format(user_id)) and not '/start' in input:
				if re.match(r'^(\d+)$', input):
					ap = re_matches(r'^(\d+)$', input)
					DataBase.delete('ready_to_enter_id:{}'.format(user_id))
					await bot.delete_message(chat_id, DataBase.get('pre_msgbot:{}'.format(user_id)))
					if DataBase.sismember('allUsers', ap[1]):
						if int(ap[1]) == int(user_id):
							await sendText(chat_id, msg, 1, "{}\n{}".format(langU['cant_send_self'],
							langU['enter_id_for_send']), 'md', anonymous_back_keys(user_id))
						elif DataBase.sismember('blocks:{}'.format(ap[1]), user_id):
							await sendText(chat_id, msg, 1, langU['yare_blocked_anon'], 'md', anonymous_back_keys(user_id))
						else:
							hash = ':@{}'.format(user_id)
							langU = lang[user_steps[user_id]['lang']]
							buttuns = langU['buttuns']
							inlineKeys = iMarkup()
							inlineKeys.add(
								iButtun(buttuns['cancel'], callback_data = 'anon{}'.format(hash))
								)
							DataBase.set('who_conneted:{}'.format(user_id), ap[1])
							await sendText(chat_id, msg, 1,
							langU['user_connect_4send'].format(DataBase.get('name_anon2:{}'.format(ap[1]))), 'md', inlineKeys)
					else:
						await sendText(chat_id, msg, 1, langU['user_404_4send'], 'md', anonymous_back_keys(user_id))
			if re.match(r"/inbox$", input):
				if DataBase.scard('inbox_user:{}'.format(user_id)) > 0:
					your_messages = DataBase.smembers('inbox_user:{}'.format(user_id))
					for i in your_messages:
						ap = re_matches(r"^(\d+):(\d+):(\d+):(\d+):(\d+):(yes|no)$", i)
						if ap[6] == 'yes':
							show_sender = int(ap[2])
						else:
							show_sender = None
						await asyncio.sleep(0.5)
						await copyMessage(user_id, gv().supchat, int(ap[1]), reply_msg = int(ap[4]),
						reply_markup = anonymous_new_message_keys(user_id, ap[2], ap[3], show_sender, ap[5]))
						if DataBase.get('is_stater:{}'.format(ap[2])):
							DataBase.setex('is_stater:{}'.format(ap[2]), 86400*7, 'True')
							user_name = DataBase.get('name_anon2:{}'.format(user_id))
						else:
							user_name = langU['anonymous']
						await sendText(ap[2], ap[3], 1, langU['your_msg_seen'].format(user_name))
						DataBase.srem('inbox_user:{}'.format(user_id), i)
				else:
					await sendText(chat_id, msg, 1, langU['inbox_empty'])
			if re.match(r"^ping$", input):
				await sendText(chat_id, msg, 1, "*PONG*", 'md')
			if re.search(r"^/start (.*)$", input):
				ap = re_matches(r"^/start (.*)$", msg.text)
				we_have = DataBase.get('link_anon:{}'.format(ap[1]))
				if we_have:
					if int(we_have) == int(user_id):
						await sendText(chat_id, msg, 1, "{}\n{}".format(langU['cant_send_self'],
						langU['enter_id_for_send']), 'md', anonymous_back_keys(user_id))
					elif DataBase.sismember('blocks:{}'.format(we_have), user_id):
						await sendText(chat_id, msg, 1, langU['yare_blocked_anon'], 'md', anonymous_back_keys(user_id))
					else:
						hash = ':@{}'.format(user_id)
						langU = lang[user_steps[user_id]['lang']]
						buttuns = langU['buttuns']
						inlineKeys = iMarkup()
						inlineKeys.add(
							iButtun(buttuns['cancel'], callback_data = 'anon{}'.format(hash))
							)
						DataBase.set('who_conneted:{}'.format(user_id), we_have)
						DataBase.incr('user.stats_anon:{}'.format(we_have))
						await sendText(chat_id, msg, 1,
						langU['user_connect_4send'].format(DataBase.get('name_anon2:{}'.format(we_have))), 'md', inlineKeys)
				else:
					await sendText(chat_id, msg, 1, langU['link_expire_anon'], 'md')
			if not re.search(r"^/start p(\d+)$", input):
				if not DataBase.sismember('allUsers', user_id):
					await newUser(msg)
			if not isSudo(user_id):
				hash = 'user.flood:{}:{}:num'.format(user_id, chat_id)
				msgs = int(redis.get(hash) or 0)
				if msgs>(5-1):
					name = user_name.replace('[ < >]', '')
					await sendText(chat_id, msg, 1, langU['ban_flood'].format(name, user_id, gv().botName, gv().botUser, gv().sudoUser), 'html')
					DataBase.setex('isBan:{}'.format(user_id), 900, "True")
				redis.setex(hash, 3, msgs+1)
			if int(user_id) != gv().botID and not await is_Channel_Member("@{}".format(IDs_datas['chUsername']), user_id):
				await sendText(chat_id, msg, 1, langU['join_channel'].format(IDs_datas['chUsername']), 'md')
				return False
			if not re.search(r"^[!/#]start", input) and not await is_Channel_Member("@{}".format(IDs_datas['chUsername']), user_id):
				inlineKeys = iMarkup()
				inlineKeys.add(
				iButtun(langU['buttuns']['join'], url = 'https://t.me/{}'.format(IDs_datas['chUsername'])),#gv().chLink), 
				iButtun(langU['buttuns']['joined'], callback_data = 'backstart:@{}'.format(user_id))
				)
				await sendText(chat_id, msg, 1, langU['force_join'].format(IDs_datas['chUsername']), 'md', inlineKeys)
				return False
			if re.match(r"^/start$", input) or re.match(r"^{}$".format(langU['buttuns']['back_menu']), input):
				user_steps[user_id].update({'action': "nothing"})
				sendM = await sendText(chat_id, msg, 1, ".", None, ())
				await sendM[1].delete()
				DataBase.delete('sup:{}'.format(user_id))
				if DataBase.get('fwdID'):
					try:
						await bot.forward_message(chat_id = chat_id, from_chat_id = int(DataBase.get('fwdChat')), message_id = int(DataBase.get('fwdID')))
					except:
						await sendText(gv().sudoID, 0, 1, "Error in FwdID2")
				await sendText(chat_id, msg, 1, langU['start'], 'md', start_keys(user_id))
			if re.match(r"^قطع ارتباط$", input) or re.match(r"^disconnect$", input) or re.match(r"^قطع الاتصال$", input):
				if DataBase.get('sup:{}'.format(user_id)):
					DataBase.delete('sup:{}'.format(user_id))
					text = langU['disconnect']
				else:
					text = langU['not_connect']
				await sendText(chat_id, msg, 1, text, 'md', start_keys(user_id))
			if isSudo(user_id):
				if re.match(r"/block (\d+)$", input):
					ap = re_matches("/block (\d+)$", input)
					if DataBase.get('isBan:{}'.format(ap[1])):
						alerttext = langU['usblocked']
					else:
						DataBase.set('isBan:{}'.format(ap[1]), "True")
						alerttext = langU['usblock']
					await sendText(chat_id, msg, 1, alerttext)
				if re.match(r"/unblock (\d+)$", input):
					ap = re_matches("/unblock (\d+)$", input)	
					if DataBase.get('isBan:{}'.format(ap[1])):
						DataBase.delete('isBan:{}'.format(ap[1]))
						alerttext = langU['usunblocked']
					else:
						alerttext = langU['usunblock']
					await sendText(chat_id, msg, 1, alerttext)
				if re.match(r"^/send2all$", input):
					if reply_msg:
						if reply_msg.forward_from or reply_msg.forward_from_chat:
							LIST = DataBase.smembers('allUsers')
							sendM = await sendText(chat_id, msg, 1, langU['fwd_to_all'].format(len(LIST)))
							n = 0
							for i in LIST:
								await asyncio.sleep(0.1)
								try:
									await reply_msg.forward(i)
									n += 1
								except:
									pass
							await editText(chat_id, sendM[1].message_id, 0, langU['fwdd_to_all'].format(len(LIST), n))
						elif reply_msg.text:
							LIST = DataBase.smembers('allUsers')
							sendM = await sendText(chat_id, msg, 1, langU['send_to_all'].format(len(LIST)))
							n = 0
							for i in LIST:
								await asyncio.sleep(0.011)
								sendM2 = await sendText(i, 0, 1, reply_msg.text)
								if sendM2[0] is True:
									n += 1
							await editText(chat_id, sendM[1].message_id, 0, langU['sent_to_all'].format(len(LIST), n))
					else:
						await sendText(chat_id, msg, 1, langU['just_reply'])
		if isUserSteps(user_id):
			pass


def saveUsername(msg, mode = "message"):
	if mode == "message":
		data = CheckMsg(msg)
		u = data.user
		uid = u.id
		fn = u.first_name
		redis.hset("userInfo:{}".format(u.id), 'name', fn)
		us = u.username
		if us and int(redis.hget("UsernamesIds", us.lower()) or "0") != int(uid):
			redis.hset("UsernamesIds", us.lower(), uid)
			cPrint("@{} [{}] Saved".format(us, uid), 2, None, "magenta")
	elif mode == "inline" or mode == "callback":
		u = msg.from_user
		uid = u.id
		fn = u.first_name
		redis.hset("userInfo:{}".format(u.id), 'name', fn)
		us = u.username
		if us and int(redis.hget("UsernamesIds", us.lower()) or "0") != int(uid):
			redis.hset("UsernamesIds", us.lower(), uid)
			cPrint("@{} [{}] Saved".format(us, uid), 2, None, "magenta")


async def answerInlineQuery(inline_msg_id, results, cache_time = 0, \
	switch_pm_text = None, switch_pm_parameter = None, is_personal = False, next_offset = None):
	try:
		a = await bot.answer_inline_query(inline_msg_id, results, cache_time = cache_time, \
		switch_pm_text = switch_pm_text, switch_pm_parameter = switch_pm_parameter, \
		is_personal = is_personal, next_offset = next_offset)
		return a
	except:
		return False


def blockKeys(UserID):
	inlineKeys = iMarkup()
	inlineKeys.add(
	iButtun('Deactive🚫', callback_data = 'blockUser:{}'.format(UserID)), 
	iButtun('Active✅', callback_data = 'unblockUser:{}'.format(UserID))
	)
	return inlineKeys


def start_keys(UserID):
	hash = ':@{}'.format(UserID)
	langU = lang[user_steps[UserID]['lang']]
	inlineKeys = iMarkup()
	inlineKeys.add(
		iButtun(langU['buttuns']['najva_section'], callback_data = 'najva{}'.format(hash)), 
		iButtun(langU['buttuns']['anon_section'], callback_data = 'anon{}'.format(hash))
		)
	inlineKeys.add(
		iButtun(langU['buttuns']['support'], callback_data = 'support{}'.format(hash)), 
		iButtun(langU['buttuns']['language'], callback_data = 'language{}'.format(hash))
		)
	inlineKeys.add(
		iButtun(langU['buttuns']['adsfree'], callback_data = 'adsfree{}'.format(hash)),
		)
	if isSudo(UserID):
		inlineKeys.add(
			iButtun(langU['buttuns']['list_block'], callback_data = 'list:block:0{}'.format(hash)),
			iButtun(langU['buttuns']['stats'], callback_data = 'list:stats:0{}'.format(hash)),
			)
	inlineKeys.add(
		iButtun(langU['buttuns']['channel'], url = 'https://t.me/{}'.format(IDs_datas['chUsername'])),
		)
	return inlineKeys


def settings_keys(UserID, arg2 = None):
	hash = ':@{}'.format(UserID)
	langU = lang[user_steps[UserID]['lang']]
	buttuns = langU['buttuns']	
	inlineKeys = iMarkup()
	inlineKeys.add(
		iButtun('زبان/language', callback_data = 'nil')
		)
	if (arg2 or user_steps[UserID]['lang']) == "fa":
		status1 = '✅'
	else:
		status1= ''
	if (arg2 or user_steps[UserID]['lang']) == "en":
		status2 = '✅'
	else:
		status2= ''
	inlineKeys.add(
		iButtun('{}English🇺🇸'.format(status2), callback_data = 'set_lang_en{}'.format(hash)),
		iButtun('{}پارسی🇮🇷'.format(status1), callback_data = 'set_lang_fa{}'.format(hash)),
		)
	if arg2:
		inlineKeys.add(
			iButtun(lang[arg2]['buttuns']['back'], callback_data = 'backstart{}'.format(hash))
			)
	else:
		inlineKeys.add(
			iButtun(buttuns['back'], callback_data = 'backstart{}'.format(hash))
			)
	return inlineKeys


def anonymous_keys(UserID):
	hash = ':@{}'.format(UserID)
	langU = lang[user_steps[UserID]['lang']]
	buttuns = langU['buttuns']
	if DataBase.get('dont_receive_anon:{}'.format(UserID)):
		status_receive = '❌'
	else:
		status_receive = '✅'
	blocks_number = DataBase.scard('blocks:{}'.format(UserID))
	# if blocks_number == 0:
		# blocks_number = buttuns['empty']
	inlineKeys = iMarkup()
	if status_receive == '✅':
		inlineKeys.add(
			iButtun(buttuns['link_my_anon'], callback_data = 'anon:link{}'.format(hash)),
			iButtun(buttuns['help_my_anon'], callback_data = 'anon:help{}'.format(hash))
			)
		inlineKeys.add(
			iButtun(buttuns['stats_my_anon'], callback_data = 'anon:stats{}'.format(hash)),
			iButtun(buttuns['name_my_anon'], callback_data = 'anon:name{}'.format(hash))
			)
		inlineKeys.add(
			iButtun(buttuns['send_persion_anon'], callback_data = 'anon:send{}'.format(hash)),
			)
	inlineKeys.add(
		iButtun(buttuns['receive_my_anon'].format(status_receive), callback_data = 'anon:receive{}'.format(hash)),
		)
	if status_receive == '✅':
		inlineKeys.add(
			iButtun(buttuns['blocks_my_anon'].format(blocks_number), callback_data = 'anon:myblock{}'.format(hash)),
			)
	inlineKeys.add(
		iButtun(buttuns['back'], callback_data = 'backstart{}'.format(hash))
		)
	return inlineKeys


def anonymous_my_link_keys(UserID):
	hash = ':@{}'.format(UserID)
	langU = lang[user_steps[UserID]['lang']]
	buttuns = langU['buttuns']
	inlineKeys = iMarkup()
	inlineKeys.add(
		iButtun(buttuns['customize_link_anon'], callback_data = 'anon:cus{}'.format(hash)),
		iButtun(buttuns['share_link_anon'],
		url = 'https://t.me/share/url?text={}&url=t.me/{}?start={}'.format(
			langU['share_text_anon'],
			redis.hget(db, 'user'),
			DataBase.get('link_anon:{}'.format(UserID))
			))
		)
	inlineKeys.add(
		iButtun(buttuns['insta_link_anon'], callback_data = 'anon:insta{}'.format(hash))
		)
	inlineKeys.add(
		iButtun(buttuns['telg_link_anon'], callback_data = 'anon:telg{}'.format(hash)),
		)
	inlineKeys.add(
		iButtun(buttuns['back_anon'], callback_data = 'anon{}'.format(hash))
		)
	return inlineKeys


def anonymous_cus_link_keys(UserID):
	hash = ':@{}'.format(UserID)
	langU = lang[user_steps[UserID]['lang']]
	buttuns = langU['buttuns']
	inlineKeys = iMarkup()
	inlineKeys.add(
		iButtun(buttuns['default_link_anon'], callback_data = 'anon:change{}'.format(hash)),
		)
	inlineKeys.add(
		iButtun(buttuns['back_link_anon'], callback_data = 'anon:link{}'.format(hash))
		)
	return inlineKeys


def anonymous_insta_link_keys(UserID):
	hash = ':@{}'.format(UserID)
	langU = lang[user_steps[UserID]['lang']]
	buttuns = langU['buttuns']
	inlineKeys = iMarkup()
	inlineKeys.add(
		iButtun(buttuns['back_link_anon'], callback_data = 'anon:link{}'.format(hash))
		)
	return inlineKeys


def anonymous_help_keys(UserID):
	hash = ':@{}'.format(UserID)
	langU = lang[user_steps[UserID]['lang']]
	buttuns = langU['buttuns']
	inlineKeys = iMarkup()
	inlineKeys.add(
		iButtun(buttuns['help1_anon'], callback_data = 'anon:help1{}'.format(hash)),
		)
	inlineKeys.add(
		iButtun(buttuns['help2_anon'], callback_data = 'anon:help2{}'.format(hash)),
		)
	inlineKeys.add(
		iButtun(buttuns['help3_anon'], callback_data = 'anon:help3{}'.format(hash)),
		)
	inlineKeys.add(
		iButtun(buttuns['help4_anon'], callback_data = 'anon:help4{}'.format(hash)),
		)
	inlineKeys.add(
		iButtun(buttuns['back_anon'], callback_data = 'anon{}'.format(hash))
		)
	return inlineKeys


def anonymous_back_keys(UserID):
	hash = ':@{}'.format(UserID)
	langU = lang[user_steps[UserID]['lang']]
	buttuns = langU['buttuns']
	inlineKeys = iMarkup()
	inlineKeys.add(
		iButtun(buttuns['back_anon'], callback_data = 'anon{}'.format(hash))
		)
	return inlineKeys


def anonymous_name_keys(UserID):
	hash = ':@{}'.format(UserID)
	langU = lang[user_steps[UserID]['lang']]
	buttuns = langU['buttuns']
	inlineKeys = iMarkup()
	inlineKeys.add(
		iButtun(buttuns['cus_name_anon'], callback_data = 'anon:cus_name{}'.format(hash)),
		)
	inlineKeys.add(
		iButtun(buttuns['default_name_anon'], callback_data = 'anon:default_name{}'.format(hash)),
		)
	inlineKeys.add(
		iButtun(buttuns['back_anon'], callback_data = 'anon{}'.format(hash))
		)
	return inlineKeys


def anonymous_cus_name_keys(UserID):
	hash = ':@{}'.format(UserID)
	langU = lang[user_steps[UserID]['lang']]
	buttuns = langU['buttuns']
	inlineKeys = iMarkup()
	inlineKeys.add(
		iButtun(buttuns['back_name_anon'], callback_data = 'anon:name{}'.format(hash))
		)
	return inlineKeys


def anonymous_new_message_keys(UserID, TO_USER, MSG_ID, SHOW_SENDER, SENT_TIME):
	hash = ':{}:{}:{}:@{}'.format(TO_USER, MSG_ID, SENT_TIME, UserID)
	try:
		langU = lang[user_steps[UserID]['lang']]
	except:
		langU = lang['fa']
	buttuns = langU['buttuns']
	if DataBase.sismember('blocks:{}'.format(UserID), TO_USER):
		buttun1 = buttuns['unblock']
	else:
		buttun1 = buttuns['block']
	inlineKeys = iMarkup()
	inlineKeys.add(
		iButtun(buttun1, callback_data = 'anon:blo{}'.format(hash)),
		iButtun(buttuns['reply'], callback_data = 'anon:rep{}'.format(hash))
		)
	if SHOW_SENDER:
		inlineKeys.add(
			iButtun("{} {}".format(buttuns['from_who'], DataBase.get('name_anon2:{}'.format(SHOW_SENDER))), callback_data = 'none')
		)
	else:
		inlineKeys.add(
			iButtun(buttuns['from_who2'], callback_data = 'none')
		)
	inlineKeys.add(
		iButtun(buttuns['sent_time'], callback_data = 'anon:stime{}'.format(hash))
		)
	return inlineKeys


def anonymous_delete_blocks_keys(UserID):
	hash = ':@{}'.format(UserID)
	langU = lang[user_steps[UserID]['lang']]
	buttuns = langU['buttuns']
	inlineKeys = iMarkup()
	inlineKeys.add(
		iButtun(buttuns['yes'], callback_data = 'anon:delblocks{}'.format(hash)),
		iButtun(buttuns['no'], callback_data = 'anon{}'.format(hash))
		)
	inlineKeys.add(
		iButtun(buttuns['back_anon'], callback_data = 'anon{}'.format(hash))
		)
	return inlineKeys


def isUserSteps(user_id):
	if user_id in user_steps and 'action' in user_steps[user_id]:
		return True
	else:
		return False


def setupUserSteps(msg, user_id):
	try:
		if not DataBase.get('link_anon:{}'.format(user_id)):
			text = generate_link()
			while True:
				if not DataBase.sismember('links_anon', text):
					DataBase.set('link_anon:{}'.format(user_id), text)
					DataBase.set('link_anon:{}'.format(text), user_id)
					DataBase.sadd('links_anon', text)
					break
				text = generate_link()
		name_anon2 = DataBase.get('name_anon2:{}'.format(user_id))
		user_name = msg.from_user.first_name
		if not name_anon2:
			DataBase.set('name_anon2:{}'.format(user_id), user_name)
		elif name_anon2 != user_name:
			DataBase.set('name_anon2:{}'.format(user_id), user_name)
		user_steps[user_id].update({
		"lang": (DataBase.get('user.lang:{}'.format(user_id)) or echoLangCode(msg.from_user)),
		})
	except:
		user_steps.update({user_id: {
		"lang": (DataBase.get('user.lang:{}'.format(user_id)) or echoLangCode(msg.from_user)),
		}})


def echoLangCode(from_user):
	if 'language_code' in from_user:
		from_user = from_user.language_code
		if re.search('^fa', from_user):
			return 'fa'
		elif re.search('^en', from_user):
			return 'en'
		else:
			return 'en'
	else:
		return 'en'


def deletePreviousData(user_id):
	if 'deezer' in user_steps[user_id]:
		del user_steps[user_id]['deezer']
	if 'spotify' in user_steps[user_id]:
		del user_steps[user_id]['spotify']
	if 'sound_cloud' in user_steps[user_id]:
		del user_steps[user_id]['sound_cloud']
	if 'youtube' in user_steps[user_id]:
		del user_steps[user_id]['youtube']
	if 'dl' in user_steps[user_id]:
		del user_steps[user_id]['dl']
	if 'in_wait_dl' in user_steps[user_id]:
		del user_steps[user_id]['in_wait_dl']
	if 'what_do' in user_steps[user_id]:
		del user_steps[user_id]['what_do']


def generate_link():
	# alphabets = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'n', 'm', 'l', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z']
	# numbers = [1, 2, 3, 4, 5, 6, 7, 8, 9, 0]
	# letters = (alphabets, numbers, alphabets, alphabets, numbers)
	# text = ''
	# for i in range(0, 12):
		# which_one = random.choice(letters)
		# which_key = random.choice(which_one)
		# text = "{}{}".format(text, which_key)
	text = ''.join(random.choices(string.ascii_letters + string.digits, k=12))
	return text


async def message_process(msg: types.Message):
	if int(msg.date.timestamp())  <  (int(time())-60):
		cPrint("{} Old Message Skipped".format(msg.date), 2, textColor = "cyan")
		return False
	data = CheckMsg(msg)
	chat_id = int(msg.chat.id)
	content = data.content
	user_id = int(msg.from_user.id)
	msg_id = msg.message_id
	setupUserSteps(msg, user_id)
	langU = lang[user_steps[user_id]['lang']]
	print(colored("Message:", "yellow"),
	colored("ID: {} | Type: {}".format(msg.from_user.id, content), "white"),
	colored("MSG_ID:", "yellow"), colored(msg_id, "white"))
	if 'reply_to_message' in msg:
		reply_msg = msg.reply_to_message
		reply_id = reply_msg.message_id
	else:
		reply_msg = None
		reply_id = 0
	if 'forward_from' in msg and msg.forward_from.id:
		saveUsername(msg)
	else:
		saveUsername(msg)
	if not DataBase.get('checkBotInfo'):
		try:
			b = await bot.get_me()
			DataBase.hmset(db, {
			'user':b.username, 
			'id':b.id, 
			'name':b.first_name, 
			'token':telegram_datas['botToken']
			})
			getC = await bot.get_chat(sudo_id)
			DataBase.hset('sudo', 'user', getC.id)
			if getC.username:
				DataBase.hset('sudo', 'user', getC.username)
			DataBase.setex('checkBotInfo', 86400, "True")
		except:
			print("Sudo or Channel Not Found!!!")
			pass
	if isPv(msg):
		setupUserSteps(msg, user_id)
		await memberCommands(msg, "input", chat_id, False, False)
	if isSuper(msg):
		if chat_id == gv().supchat:
			if isSudo(user_id):
				IF = reply_msg and reply_msg.from_user.id == gv().botID
				if IF and reply_msg.text and 'text' in msg:
					IF2 = reply_msg.text.split(' | ')
					sendM = await sendText(IF2[1], 0, 1, msg.text, 'html')
					if sendM[0] is True:
						await sendText(chat_id, msg, 1, "✅")
					else:
						await sendText(chat_id, msg, 1, "❌\n{}".format(sendM))
		else:
			await bot.leave_chat(chat_id)
	if isGroup(msg):
		await bot.leave_chat(chat_id)


async def callback_query_process(msg: types.CallbackQuery):
	# {"id": "601066438631931931",
	# "from": {"id": 139946685, "is_bot": false, "first_name": "Alireza .Feri 🏴", "username": "ferisystem", "language_code": "de"},
	# "message": {"message_id": 33021, "from": {"id": 238204510, "is_bot": true, "first_name": "TeleSeed", "username": "TeleSeedBot"},
	# "chat": {"id": 139946685, "first_name": "Alireza .Feri 🏴", "username": "ferisystem", "type": "private"},
	# "date": 1664543136, "edit_date": 1664543182,
	# "reply_to_message": {"message_id": 33019,
	# "from": {"id": 139946685, "is_bot": false, "first_name": "Alireza .Feri 🏴", "username": "ferisystem", "language_code": "de"},
	# "chat": {"id": 139946685, "first_name": "Alireza .Feri 🏴", "username": "ferisystem", "type": "private"},
	# "date": 1664543135, "text": "/start", "entities": [{"type": "bot_command", "offset": 0, "length": 6}]},
	# "text": "این متن را بعدا تغییر دهید. بخش لینک ناشناس",
	# "reply_markup": {"inline_keyboard":
	# [
	# [
	# {"text": "شخصی سازی لینک", "callback_data": "anon:cus:@139946685"},
	# {"text": "اشتراک گذاری", "url": "https://t.me/share/url?text=asdad&url=google.com"}],
	# [{"text": "لینک برای اینستاگرام", "callback_data": "anon:insta:@139946685"}],
	# [{"text": "لینک برای تلگرام", "callback_data": "anon:telg:@139946685"}],
	# [{"text": "بازگشت به بخش ناشناس", "callback_data": "anon:@139946685"}]]}},
	# "chat_instance": "1169386402171875241", "data": "anon:@139946685"}
	saveUsername(msg, mode = "callback")
	user_id = msg.from_user.id
	input = msg.data.lower()
	setupUserSteps(msg, user_id)
	langU = lang[user_steps[user_id]['lang']]
	if 'message' in msg:
		msg_id = msg.message.message_id
	else:
		msg_id = 0
	print(colored("Callback Query:", "yellow"),
	colored("ID: {} | Query: {}".format(user_id, input), "white")
	)
	if re.search(r"@(\d+)", input):
		ap = re_matches("@(\d+)", input, 's')
		if int(ap[1]) != user_id:
			if not DataBase.get('user.alertinline:{}:{}'.format(user_id, msg_id)):
				DataBase.setex('user.alertinline:{}:{}'.format(user_id, msg_id), 3600, "True")
				return AnswerCallbackQuery(msg.id, langU['isNot4u'], True, None, 3600)
			return False
		if int(ap[1]) == user_id and not DataBase.get('user.alertNotMemberChannel:{}'.format(user_id)):
			if not re.search(r'insgp(.*)', input) and not re.search(r'ib(.*)', input) and not await is_Channel_Member("@{}".format(IDs_datas['chUsername']), user_id):
				DataBase.set('user.alertNotMemberChannel2:{}'.format(user_id), "True")
				await answerCallbackQuery(msg, langU['uNotJoined'].format(IDs_datas['chUsername']), True)
				inlineKeys = iMarkup()
				inlineKeys.add = (
				iButtun(langU['buttuns']['join'], url = 'https://t.me/{}'.format(IDs_datas['chUsername'])),
				iButtun(langU['buttuns']['joined'], callback_data = input)
				)
				await editText(chat_id, msg_id, 1, langU['join_channel'].format(IDs_datas['chUsername']), 'md', inlineKeys)
				return False
			if DataBase.get('user.alertNotMemberChannel2:{}'.format(user_id)):
				DataBase.delete('user.alertNotMemberChannel2:{}'.format(user_id))
				await answerCallbackQuery(msg, langU['you_accepted'])
			DataBase.setex('user.alertNotMemberChannel:{}'.format(user_id), 3600, "True")
	if 'message' in msg:
		DataBase.incr('amarBot.callmsg')
		_ = msg.message
		msg_id = _.message_id
		chat_id = _.chat.id
		chat_name = _.chat.title
		if not redis.get(input):
			redis.psetex(input, 500, 1)
		else:
			return False
		if int(_.date.timestamp()) < (int(time())-86400):
			cPrint("{} Old Callback Skipped".format(_.date), 2, textColor = "cyan")
			try:
				await _.edit_reply_markup()
			except:
				pass
			return AnswerCallbackQuery(msg.id, "این پنل قدیمی است دوباره پنل مربوطه را دریافت کنید!\nاگر پنل پرداختی است نگران نباشید :D", True)
		if re.match(r"^backstart:@(\d+)$", input):
			DataBase.delete('sup:{}'.format(user_id))
			user_steps[user_id].update({"action": "nothing"})
			deletePreviousData(user_id)
			await editText(chat_id, msg_id, 0, langU['start'], None, start_keys(user_id))
		if re.match(r"^language:@(\d+)$", input):
			await editText(chat_id, msg_id, 0, langU['language'], None, settings_keys(user_id))
		if re.match(r"^set_(.*)_(.*):@(\d+)$", input):
			ap = re_matches("^set_(.*)_(.*):@(\d+)$", input)
			if ap[1] == 'lang':
				DataBase.set('user.lang:{}'.format(user_id),ap[2])
				try:
					await editText(chat_id, msg_id, 0, lang[ap[2]]['settings'], None, settings_keys(user_id, ap[2]))
				except:
					await _.edit_reply_markup(settings_keys(user_id, ap[2]))
				return AnswerCallbackQuery(msg.id, lang['set_{}'.format(ap[2])], True, None, 0)
		if re.match(r"^notice_1:@(\d+)$", input):
			return AnswerCallbackQuery(msg.id, langU['notice_change_file'], True, None, 86400)
		if re.match(r"^start_again:@(\d+)$", input):
			DataBase.delete('sup:{}'.format(user_id))
			user_steps[user_id].update({"action": "nothing"})
			deletePreviousData(user_id)
			try:
				await _.edit_reply_markup()
			except:
				pass
			await sendText(chat_id, 0, 1, langU['start'], None, start_keys(user_id))
		if re.match(r"^blockuser:(\d+)$",input):
			ap= re_matches("^blockuser:(\d+)$", input)
			if DataBase.get('isBan:{}'.format(ap[1])):
				alerttext = langU['usblocked']
			else:
				DataBase.set('isBan:{}'.format(ap[1]), "True")
				alerttext = langU['usblock']
				keyboard = blockKeys(ap[1])
				try:
					getC = await bot.get_chat(ap[1])
					await editText(chat_id, msg_id, 0, '#NewUser\nName: [{0}](tg://user?id={1})\nID: `{1}`\nStatus: Deactive🚫'.format(getC.first_name, ap[1]), 'md', keyboard)
				except:
					await editText(chat_id, msg_id, 0, '#NewUser\nName: [{0}](tg://user?id={0})\nID: `{0}`\nStatus: Deactive🚫'.format(ap[1]), 'md', keyboard)
			await answerCallbackQuery(msg, alerttext)
		if re.match(r"^unblockuser:(\d+)$",input):
			ap = re_matches("^unblockuser:(\d+)$", input)
			if DataBase.get('isBan:{}'.format(ap[1])):
				DataBase.delete('isBan:{}'.format(ap[1]))
				alerttext = langU['usunblocked']
				keyboard = blockKeys(ap[1])
				try:
					getC = getChat(ap[1])
					await editText(chat_id, msg_id, 0, '#NewUser\nName: [{0}](tg://user?id={1})\nID: `{1}`\nStatus: Active✅'.format(getC.first_name, ap[1]), 'md', keyboard)
				except:
					await editText(chat_id, msg_id, 0, '#NewUser\nName: [{0}](tg://user?id={0})\nID: `{0}`\nStatus: Active✅'.format(ap[1]), 'md', keyboard)
			else:
				alerttext = langU['usunblock']
			await answerCallbackQuery(msg, alerttext)
		if re.match(r"^list:(.*):(\d+):@(\d+)$", input):
			ap = re_matches("^list:(.*):(\d+):@(\d+)$", input)
			inlineKeys = iMarkup()
			if ap[1] == 'block':
				await editText(chat_id, msg_id, 0, langU['wait'])
				text = langU['list_block']
				keys = DataBase.keys("isBan:*")
				n = int(ap[2])
				for i in keys:
					n += 1
					userID = i.split(':')[-1]
					text = '{}{}- {} | {}\n'.format(
					text,
					n,
					await userInfos(userID),
					userID,
					)
				with open('Files/list_block.txt', mode = 'a', encoding = 'utf-8') as file:
					file.write(text)
				await sendDocument(chat_id, open('Files/list_block.txt', encoding = 'utf-8'))
				inlineKeys.add(
					iButtun(langU['buttuns']['back'], callback_data = 'backstart:@{}'.format(user_id)),
					)
				await editText(chat_id, msg_id, 0, langU['blocklist_sent'], None, inlineKeys) 
				os.system('rm Files/list_block.txt')
			elif ap[1] == 'stats':
				inlineKeys = iMarkup()
				inlineKeys.add(
					iButtun(langU['buttuns']['back'], callback_data = 'backstart:@{}'.format(user_id))
					)
				dl_ig_post = DataBase.get('stat_dl_ig_post')
				dl_ig_story = DataBase.get('stat_dl_ig_story')
				search_music = DataBase.get('stat_search_music')
				dl_music = DataBase.get('stat_dl_music')
				search_youtube = DataBase.get('stat_search_youtube')
				dl_youtube = DataBase.get('stat_dl_youtube')
				dl_file = DataBase.get('stat_dl_file')
				all_users = DataBase.scard('allUsers')
				await editText(chat_id, msg_id, 0, langU['stats'].format(
				dl_ig_post,
				dl_ig_story,
				search_music,
				dl_music,
				search_youtube,
				dl_youtube,
				dl_file,
				all_users,
				).replace('None', '0'), 'html', inlineKeys)
		if re.match(r"^anon:@(\d+)$", input):
			DataBase.delete('ready_to_change_link:{}'.format(user_id))
			DataBase.delete('ready_to_change_name:{}'.format(user_id))
			DataBase.delete('ready_to_enter_id:{}'.format(user_id))
			DataBase.delete('who_conneted:{}'.format(user_id))
			await editText(chat_id, msg_id, 0, langU['anon'], None, anonymous_keys(user_id))
		if re.match(r"^anon:link:@(\d+)$", input):
			DataBase.delete('ready_to_change_link:{}'.format(user_id))
			await editText(chat_id, msg_id, 0, langU['my_link_anon'], None, anonymous_my_link_keys(user_id))
		if re.match(r"^anon:cus:@(\d+)$", input):
			DataBase.setex('ready_to_change_link:{}'.format(user_id), 3600, 'True')
			DataBase.set('pre_msgbot:{}'.format(user_id), msg.message.message_id)
			await editText(chat_id, msg_id, 0, "{}t.me/{}?start={}".format(langU['customize_link_anon'], redis.hget(db, 'user'), DataBase.get('link_anon:{}'.format(user_id))), None, anonymous_cus_link_keys(user_id))
		if re.match(r"^anon:change:@(\d+)$", input):
			link_previous = DataBase.get('link_anon:{}'.format(user_id))
			DataBase.delete('link_anon:{}'.format(link_previous))
			DataBase.srem('links_anon', link_previous)
			text = generate_link()
			while True:
				if not DataBase.sismember('links_anon', text):
					DataBase.set('link_anon:{}'.format(user_id), text)
					DataBase.set('link_anon:{}'.format(text), user_id)
					DataBase.sadd('links_anon', text)
					break
				text = generate_link()
			await editText(chat_id, msg_id, 0, "{}t.me/{}?start={}".format(langU['customize_link_anon'], redis.hget(db, 'user'), DataBase.get('link_anon:{}'.format(user_id))), None, anonymous_cus_link_keys(user_id))
		if re.match(r"^anon:telg:@(\d+)$", input):
			await editText(chat_id, msg_id, 0, "{}\n<code>https://t.me/{}?start={}</code>".format(langU['telg_link_anon'],
			redis.hget(db, 'user'), DataBase.get('link_anon:{}'.format(user_id))), 'html', anonymous_insta_link_keys(user_id))
		if re.match(r"^anon:insta:@(\d+)$", input):
			link_picture = '<a href="https://s6.uupload.ir/files/photo_2022-09-01_18-03-08_s3qf.jpg">مشاهده عکس آموزشی</a>'
			await editText(chat_id, msg_id, 0,
			'{}\n{}\n<code>https://t.me/{}?start={}</code>'
			.format(link_picture, langU['insta_link_anon'], redis.hget(db, 'user'), DataBase.get('link_anon:{}'.format(user_id))),
			parse_mode = 'html', reply_markup = anonymous_insta_link_keys(user_id))
		if re.match(r"^anon:help:@(\d+)$", input):
			await editText(chat_id, msg_id, 0, langU['help_anon'], None, anonymous_help_keys(user_id))
		if re.match(r"^anon:help(\d+):@(\d+)$", input):
			ap = re_matches(r"^anon:help(\d+):@(\d+)$", input)
			hash = ':@{}'.format(user_id)
			langU = lang[user_steps[user_id]['lang']]
			buttuns = langU['buttuns']
			inlineKeys = iMarkup()
			inlineKeys.add(
				iButtun(buttuns['back_help_anon'], callback_data = 'anon:help{}'.format(hash))
				)
			await editText(chat_id, msg_id, 0, langU['help{}_anon'.format(ap[1])], None, inlineKeys)
		if re.match(r"^anon:stats:@(\d+)$", input):
			await answerCallbackQuery(msg, langU['stats_anon'].format(int(DataBase.get('user.stats_anon:{}'.format(user_id))) or 0), show_alert = True, cache_time = 90)
		if re.match(r"^anon:name:@(\d+)$", input):
			DataBase.delete('ready_to_change_name:{}'.format(user_id))
			await editText(chat_id, msg_id, 0, langU['name_anon'].format(DataBase.get('name_anon:{}'.format(user_id)) or msg.from_user.first_name), None, anonymous_name_keys(user_id))
		if re.match(r"^anon:cus_name:@(\d+)$", input):
			DataBase.setex('ready_to_change_name:{}'.format(user_id), 3600, 'True')
			DataBase.set('pre_msgbot:{}'.format(user_id), msg.message.message_id)
			await editText(chat_id, msg_id, 0, langU['help_cus_name_anon'], None, anonymous_cus_name_keys(user_id))
		if re.match(r"^anon:default_name:@(\d+)$", input):
			DataBase.delete('name_anon:{}'.format(user_id))
			await answerCallbackQuery(msg, langU['changed_name_anon'], show_alert = True, cache_time = 90)
			await editText(chat_id, msg_id, 0, langU['name_anon'].format(DataBase.get('name_anon:{}'.format(user_id)) or msg.from_user.first_name), None, anonymous_name_keys(user_id))
		if re.match(r"^anon:send:@(\d+)$", input):
			DataBase.setex('ready_to_enter_id:{}'.format(user_id), 3600, 'True')
			DataBase.set('pre_msgbot:{}'.format(user_id), msg.message.message_id)
			await editText(chat_id, msg_id, 0, langU['enter_id_for_send'], None, anonymous_back_keys(user_id))
		if re.match(r"^anon:blo:(\d+):(\d+):(\d+):@(\d+)$", input):
			ap = re_matches(r"^anon:blo:(\d+):(\d+):(\d+):@(\d+)$", input)
			if DataBase.sismember('blocks:{}'.format(user_id), ap[1]):
				DataBase.srem('blocks:{}'.format(user_id), ap[1])
				text = langU['user_unblocked']
			else:
				DataBase.sadd('blocks:{}'.format(user_id), ap[1])
				text = langU['user_blocked']
			await answerCallbackQuery(msg, text, show_alert = True, cache_time = 2)
			await bot.edit_message_reply_markup(chat_id, msg_id, reply_markup = anonymous_new_message_keys(user_id, ap[1], ap[2], ap[3]))
		if re.match(r"^anon:rep:(\d+):(\d+):(\d+):@(\d+)$", input):
			ap = re_matches(r"^anon:rep:(\d+):(\d+):(\d+):@(\d+)$", input)
			await answerCallbackQuery(msg, langU['help_reply_anon'], show_alert = True, cache_time = 3600)
		if re.match(r"^anon:stime:(\d+):(\d+):(\d+):@(\d+)$", input):
			ap = re_matches(r"^anon:stime:(\d+):(\d+):(\d+):@(\d+)$", input)
			ti_me = datetime.fromtimestamp(int(ap[3]))
			ti_me = ti_me.strftime('%Y-%m-%d %H:%M:%S')
			ti_me = re_matches(r'(\d+)-(\d+)-(\d+) (\d+):(\d+):(\d+)', ti_me)
			if user_steps[user_id]['lang'] == 'fa':
				ti_me2 = gregorian_to_jalali(int(ti_me[1]), int(ti_me[2]), int(ti_me[3]))
				sent_time = "{:04d}/{}/{:02d} - {:02d}:{:02d}:{:02d}".format(
				ti_me2[0], echoMonth(ti_me2[1], True), ti_me2[2],
				int(ti_me[4]), int(ti_me[5]), int(ti_me[6]))
			else:
				sent_time = "{:04d}/{}/{:02d} - {:02d}:{:02d}:{:02d}".format(
				int(ti_me[1]), echoMonth(ti_me[2], False), int(ti_me[3]),
				int(ti_me[4]), int(ti_me[5]), int(ti_me[6]))
			await answerCallbackQuery(msg, sent_time, show_alert = True, cache_time = 180)
		if re.match(r"^anon:receive:@(\d+)$", input):
			ap = re_matches(r"^anon:receive:@(\d+)$", input)
			if DataBase.get('dont_receive_anon:{}'.format(user_id)):
				DataBase.delete('dont_receive_anon:{}'.format(user_id))
				text = langU['receive_anon_active']
			else:
				DataBase.set('dont_receive_anon:{}'.format(user_id), 'True')
				text = langU['receive_anon_deactive']
			await answerCallbackQuery(msg, text, show_alert = True, cache_time = 2)
			await bot.edit_message_reply_markup(chat_id, msg_id, reply_markup = anonymous_keys(user_id))
		if re.match(r"^anon:myblock:@(\d+)$", input):
			if DataBase.scard('blocks:{}'.format(user_id)) > 0:
				await editText(chat_id, msg_id, 0, langU['besure_del_all_blocks'], None, anonymous_delete_blocks_keys(user_id))
			else:
				await answerCallbackQuery(msg, langU['blocks_empty_anon'], show_alert = True, cache_time = 10)
		if re.match(r"^anon:delblocks:@(\d+)$", input):
			DataBase.delete('blocks:{}'.format(user_id))
			await answerCallbackQuery(msg, langU['blocks_clear_anon'], show_alert = True, cache_time = 2)
			await editText(chat_id, msg_id, 0, langU['anon'], None, anonymous_keys(user_id))


async def channel_post_process(msg: types.Message):
	if (msg.chat.username or '') != IDs_datas['chUsername'] and int(msg.chat.id) != int(redis.hget(db, 'supchat')):
		await bot.leave_chat(msg.chat.id)


async def errors_handlers(update, exception):
	"""
	Exceptions handler. Catches all exceptions within task factory tasks.
	:param dispatcher:
	:param update:
	:param exception:
	:return: stdout logging
	"""
	if isinstance(exception, expts.CantDemoteChatCreator):
		log.debug("Can't demote chat creator!")
		return
	if isinstance(exception, expts.MessageNotModified):
		log.debug('Message is not modified!')
		return
	if isinstance(exception, expts.MessageToDeleteNotFound):
		log.debug('Message to delete not found!')
		return
	if isinstance(exception, expts.Unauthorized):
		log.info(f'Unauthorized: {exception} !')
		return
	if isinstance(exception, expts.InvalidQueryID):
		log.exception(f'InvalidQueryID: {exception} !\nUpdate: {update}')
		return
	if isinstance(exception, expts.TelegramAPIError):
		log.exception(f'TelegramAPIError: {exception} !\nUpdate: {update}')
		return
	if isinstance(exception, expts.RestartingTelegram):
		await asyncio.sleep(5)
		# log.exception(f'TelegramAPIError: {exception} !\nUpdate: {update}')
		await sendText(gv().sudoID, 0, 1, "The Telegram Bot API service is restarting...")
		return
	if isinstance(exception, telethonErrors.BotMethodInvalidError):
		return
	try:
		pass
	except AttributeError:
		log.exception(f'AttributeError: {exception} !\nUpdate: {update}')
		return


async def bot_off(app):
	await bot.delete_webhook()
	# await client.disconnect()
	print(colored("==========================", "white"), colored("\n= ", "white")+colored("Bot has been power ", "yellow")+colored("off", "red")+colored(" =", "white"), colored("\n==========================", "white"))


async def bot_run(app):
	content_types = types.ContentType.ANY
	dp.register_message_handler(message_process, content_types = content_types)
	dp.register_channel_post_handler(channel_post_process, content_types = content_types)
	dp.register_callback_query_handler(callback_query_process)
	dp.register_errors_handler(errors_handlers)
	webhook = await bot.get_webhook_info()
	if webhook.url != gv().WEBHOOK_URL:
		if not webhook.url:
			await bot.delete_webhook()
		await bot.set_webhook(gv().WEBHOOK_URL, open(gv().WEBHOOK_SSL_CERT, 'rb'), max_connections = 100, \
		allowed_updates = ['message', 'channel_post', 'callback_query'])
	# await client.start(bot_token = telegram_datas['botToken'])
	bt = None
	while not bt:
		bt = await bot.get_me()
	if 'last_name' in bt:
		name = '{} {}'.format(bt.first_name, bt.last_name)
	else:
		name = bt.first_name
	ti_me = datetime.now()
	text = "{:04d}/{:02d}/{:02d} - {:02d}:{:02d}:{:02d}".format(ti_me.year, ti_me.month, ti_me.day, ti_me.hour, ti_me.minute, ti_me.second)
	a1 = 22-(len("Name > {}".format(name)) // 2)
	aa = ""
	for i in range(-1, a1):
		aa += " "
	b1 = 22-(len("Username > @{}".format(bt.username))//2)
	bb = ""
	for i in range(-1, b1):
		bb += " "
	c1 = 22-(len("ID > {}".format(bt.id)) // 2)
	cc = ""
	for i in range(-1, c1):
		cc += " "
	d1 = 22-(len("Developer > @{} [{}]".format(gv().sudoUser, gv().sudoID)) // 2)
	dd = ""
	for i in range(-1, d1):
		dd += " "
	e1 = 22-(len(text) // 2)
	ee = ""
	for i in range(0, e1):
		ee += " "
	z1 = 22-(len("#by aiogram[2.11.2]") // 2)
	zz = ""
	for i in range(-1, z1):
		zz += " "
	pW = colored("\n= ", "white")
	pW1 = colored("=================================================", "white")
	pW2 = colored("=", "white")
	print(pW1, \
	pW+aa+colored("Name", "red")+colored(" > ", "white")+colored("{}".format(name), "cyan")+aa+pW2, \
	pW+bb+colored("Username", "red")+colored(" > ", "white")+colored("@{}".format(bt.username), "cyan")+bb+pW2, \
	pW+cc+colored("ID", "red")+colored(" > ", "white")+colored("{}".format(bt.id), "cyan")+cc+pW2, \
	pW+dd+colored("Developer", "red")+colored(" > ", "white")+colored("@{}[{}]".format(gv().sudoUser, gv().sudoID), "cyan")+dd+pW2, \
	pW+ee+colored(text, "yellow")+ee+" "+pW2, \
	pW+zz+colored("#by aiogram[2.4]", "magenta")+zz+"=\n"+pW1
	)
	redis.hmset(db, {
	'id':bt.id, 
	'name':name, 
	'user':bt.username, 
	'token':telegram_datas['botToken']
	})
	try:
		bt1 = await bot.get_chat(sudo_id)
		DataBase.hset('sudo', 'user', bt1.username)
		if bt1.username:
			DataBase.hset('sudo', 'id', bt1.id)
	except:
		print("Sudo Not Found!!!")
	# await sendText(gv().sudoID, 0, 1, 'Bot has been Successfully Loaded')
	if not redis.hget(db, 'supchat'):
		status = False
		while status != True:
			iD = input("Enter Supergroup ID for support: ")
			if re.match(r'^(-\d+)$', iD):
				redis.hset(db, 'supchat', re.match(r'^(-\d+)$', iD).group(1))
				status = True
				break
			else:
				iD = input("Enter Channel ID for support: ")
				status = False


# کاراکتر
if __name__  == '__main__':
	global user_steps
	user_steps = {}
	app = get_new_configured_app(dispatcher = dp, path = gv().WEBHOOK_URL_PATH)
	app.on_startup.append(bot_run)
	app.on_shutdown.append(bot_off)
	context = ssl.SSLContext(ssl.PROTOCOL_TLS)
	context.load_cert_chain(gv().WEBHOOK_SSL_CERT, gv().WEBHOOK_SSL_PRIV)
	web.run_app(app, host = "0.0.0.0", port = gv().port, ssl_context = context)
