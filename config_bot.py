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
sudo_users = (777000, telegram_datas['botToken'].split(':')[0], ) # PUT_YOUR_ADMINS_HERE
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
