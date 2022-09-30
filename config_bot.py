db = 'najvabot'
# - - - - - - - - - - - - - #
telegram_datas = {
"botToken": "",
"api_hash": "hash_key",
"api_id": api_key,
"device_model": "Linux",
"system_version": "Ubuntu 20.04",
"app_version": "1.0",
}
# - - - - - - - - - - - - - #
sudo_users = (777000, telegram_datas['botToken'].split(':')[0], your_id) # and your team, etc..
# - - - - - - - - - - - - - #
IDs_datas = {
"sudo_id": your_id,
"bot_id": int(telegram_datas['botToken'].split(':')[0]),
"chUsername": "channel_username", # a channel that you want people have to join it
"chLink": "channel_invite_link",
}
# - - - - - - - - - - - - - #
server_datas = {
"ip": "server_id",
"port_server": port_number, #optional example: 10234 (be sure it's not using by other apps)
"port_tg": port_tg, # only use: 80, 88, 443, 8443 
}
# - - - - - - - - - - - - - #
sendApi = "https://api.telegram.org/bot{}/".format(telegram_datas['botToken'])
# - - - - - - - - - - - - - #
