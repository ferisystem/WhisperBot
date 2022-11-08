from telethon.sync import TelegramClient
from docs.lang_file import lang
from config_bot import *
from time import time
import telethon
import requests
import asyncio
import redis
import re
import os


client = TelegramClient(db, telegram_datas['api_id'], telegram_datas['api_hash'])#.start(bot_token=telegram_datas['botToken'])
redis = redis.Redis(host = 'localhost', port = 6379, db = 3, decode_responses = True, encoding = 'utf-8')
loop = asyncio.get_event_loop()


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


	def hdel(hash, value):
		hash = "{}.{}".format(db, hash)
		return redis.hdel(hash, value)


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


def lang_user(UserID):
	UserID = int(UserID)
	if UserID in user_steps and 'lang' in user_steps[UserID]:
		return user_steps[UserID]['lang']
	else:
		user_steps.update({UserID: {
		"lang": (DataBase.get('user.lang:{}'.format(UserID)) or 'fa'),
		}})
		return user_steps[UserID]['lang']


async def main():
	autodels = DataBase.smembers('najva_autodel')
	for i in autodels:
		now_time = int(time())
		from_user, time_data, inline_msg_id = i.split(':')
		langU = lang[lang_user(from_user)]
		buttuns = langU['buttuns']
		time_to_del = int(DataBase.get('autodel_time:{}'.format(from_user)) or 0) * 60
		time_seen = DataBase.get('najva_seen_time:{}:{}'.format(from_user, time_data))
		seen_id = DataBase.hget('najva:{}:{}'.format(from_user, time_data), 'seen_id')
		if seen_id and time_seen:
			time_seen = int(time_seen)
			if now_time > (time_seen + time_to_del):
				chat_id, msg_id = seen_id.split(':')
				try:
                    await client.delete_messages(int(chat_id), int(msg_id))
                except:
                    pass
				DataBase.srem('najva_autodel', i)
				DataBase.delete('najva:{}:{}'.format(from_user, time_data))
				DataBase.delete('najva_special:{}'.format(from_user))
		if time_seen:
			time_seen = int(time_seen)
			if now_time > (time_seen + time_to_del):
				msg_ = requests.post(
				f'https://api.telegram.org/bot{telegram_datas["botToken"]}/editMessageReplyMarkup',
				json = {
				'inline_message_id': inline_msg_id,
				"reply_markup": {
					'inline_keyboard': [[{
						'text': buttuns['stats'],
						'callback_data': 'showS:{}:{}'.format(from_user, time_data),
						}]]}}).json()
				DataBase.srem('najva_autodel', i)
				DataBase.delete('najva:{}:{}'.format(from_user, time_data))
				DataBase.delete('najva_special:{}'.format(from_user))


with client:
	global user_steps
	user_steps = {}
	client.loop.run_until_complete(main())