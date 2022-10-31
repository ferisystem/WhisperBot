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
pic_atsign = 'https://raw.githubusercontent.com/ferisystem/ferisystem/files/files/atsign.jpg'
pic_user = 'https://raw.githubusercontent.com/ferisystem/ferisystem/files/files/user.jpg'
pic_message = 'https://raw.githubusercontent.com/ferisystem/ferisystem/files/files/message.jpg'
pic_question = 'https://raw.githubusercontent.com/ferisystem/ferisystem/files/files/question.jpg'
pic_group = 'https://raw.githubusercontent.com/ferisystem/ferisystem/files/files/group.jpg'
pic_all = 'https://raw.githubusercontent.com/ferisystem/ferisystem/files/files/all.jpg'
pic_tick = 'https://raw.githubusercontent.com/ferisystem/ferisystem/files/files/tick.jpg'
pic_cross = 'https://raw.githubusercontent.com/ferisystem/ferisystem/files/files/cross.jpg'
pic_special = 'https://raw.githubusercontent.com/ferisystem/ferisystem/files/files/special.jpg'
