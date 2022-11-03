db = 'begobot'
# - - - - - - - - - - - - - #
telegram_datas = {
"botToken": "537502140:AAHDzN2USmOMJ6iVm7S46D30aR7dUCojXR0",
"api_hash": "5146e754701a0ae922a77c940f15c803", # "a91737390f3c6f51d2b9dfef87eca954",
"api_id": 2179978, #752812,
"device_model": "Linux",
"system_version": "Ubuntu 20.04",
"app_version": "1.0",
}
# - - - - - - - - - - - - - #
sudo_users = (777000, telegram_datas['botToken'].split(':')[0], 139946685, 375029817)
# - - - - - - - - - - - - - #
IDs_datas = {
"sudo_id": 139946685,#752815712,
"bot_id": int(telegram_datas['botToken'].split(':')[0]),
"chUsername": "fereidouni",
"chLink": "https://t.me/joinchat/AAAAAFHGwAQNVhcSJSY6Qw",
}
# - - - - - - - - - - - - - #
server_datas = {
"ip": "178.63.174.231",
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
