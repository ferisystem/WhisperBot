from Files.keyboards_func import *
from Files.lateral_func import *
from Files.main_func import *
from config_bot2 import *
from core_file import *


async def channel_post_process(msg: types.Message):
    if (msg.chat.username or "") != IDs_datas["chUsername"] and int(
        msg.chat.id
    ) != int(GlobalValues().supchat):
        await bot.leave_chat(msg.chat.id)
