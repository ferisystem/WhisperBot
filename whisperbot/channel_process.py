from whisperbot.keyboards_func import *
from whisperbot.lateral_func import *
from whisperbot.main_func import *
from config_bot import *
from core_file import *


async def channel_post_process(msg: types.Message):
    if (msg.chat.username or "") != IDs_datas["chUsername"] and int(
        msg.chat.id
    ) != int(GlobalValues().logchat):
        try:
            await bot.leave_chat(msg.chat.id)
        except:
            pass
