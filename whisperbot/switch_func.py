from whisperbot.callback_process import callback_query_process
from whisperbot.chosen_process import chosen_inline_process
from whisperbot.channel_process import channel_post_process
from whisperbot.inline_process import inline_query_process
from whisperbot.messages_process import message_process
from whisperbot.errors_process import errors_handlers
from core_file import (
    GlobalValues,
    DataBase,
    datetime,
	sudo_id,
    colored,
    types,
    bot,
    rds,
    dp,
    re
)
from whisperbot.main_func import sendText
from config_bot import *


async def bot_off(app):
    await bot.delete_webhook()
    print(
        colored("==========================", "white"),
        colored("\n= ", "white")
        + colored("Bot has been power ", "yellow")
        + colored("off", "red")
        + colored(" =", "white"),
        colored("\n==========================", "white"),
    )


async def bot_run(app):
    content_types = types.ContentType.ANY
    dp.register_message_handler(message_process, content_types=content_types)
    dp.register_channel_post_handler(
        channel_post_process, content_types=content_types
    )
    dp.register_callback_query_handler(callback_query_process)
    dp.register_inline_handler(inline_query_process)
    dp.register_chosen_inline_handler(chosen_inline_process)
    dp.register_errors_handler(errors_handlers)
    webhook = await bot.get_webhook_info()
    if webhook.url != GlobalValues().WEBHOOK_URL:
        if not webhook.url:
            await bot.delete_webhook()
        await bot.set_webhook(
            GlobalValues().WEBHOOK_URL,
            open(GlobalValues().WEBHOOK_SSL_CERT, "rb"),
            max_connections=100,
            allowed_updates=[
                "message",
                "edited_message",
                "channel_post",
                "edited_channel_post",
                "inline_query",
                "chosen_inline_result",
                "callback_query",
                "shipping_query",
                "pre_checkout_query",
                "poll",
                "poll_answer",
                "my_chat_member",
                "chat_member",
                "chat_join_request",
            ],
        )
    bt = None
    while not bt:
        bt = await bot.get_me()
    if "last_name" in bt:
        name = "{} {}".format(bt.first_name, bt.last_name)
    else:
        name = bt.first_name
    ti_me = datetime.now()
    text = "{:04d}/{:02d}/{:02d} - {:02d}:{:02d}:{:02d}".format(
        ti_me.year,
        ti_me.month,
        ti_me.day,
        ti_me.hour,
        ti_me.minute,
        ti_me.second,
    )
    a1 = 22 - (len("Name > {}".format(name)) // 2)
    aa = ""
    for i in range(-1, a1):
        aa += " "
    b1 = 22 - (len("Username > @{}".format(bt.username)) // 2)
    bb = ""
    for i in range(-1, b1):
        bb += " "
    c1 = 22 - (len("ID > {}".format(bt.id)) // 2)
    cc = ""
    for i in range(-1, c1):
        cc += " "
    d1 = 22 - (
        len("Developer > @{} [{}]".format(GlobalValues().sudoUser, GlobalValues().sudoID)) // 2
    )
    dd = ""
    for i in range(-1, d1):
        dd += " "
    e1 = 22 - (len(text) // 2)
    ee = ""
    for i in range(0, e1):
        ee += " "
    z1 = 22 - (len("#by aiogram[2.11.2]") // 2)
    zz = ""
    for i in range(-1, z1):
        zz += " "
    pW = colored("\n= ", "white")
    pW1 = colored("=================================================", "white")
    pW2 = colored("=", "white")
    print(
        pW1,
        pW
        + aa
        + colored("Name", "red")
        + colored(" > ", "white")
        + colored("{}".format(name), "cyan")
        + aa
        + pW2,
        pW
        + bb
        + colored("Username", "red")
        + colored(" > ", "white")
        + colored("@{}".format(bt.username), "cyan")
        + bb
        + pW2,
        pW
        + cc
        + colored("ID", "red")
        + colored(" > ", "white")
        + colored("{}".format(bt.id), "cyan")
        + cc
        + pW2,
        pW
        + dd
        + colored("Developer", "red")
        + colored(" > ", "white")
        + colored("@{}[{}]".format(GlobalValues().sudoUser, GlobalValues().sudoID), "cyan")
        + dd
        + pW2,
        pW + ee + colored(text, "yellow") + ee + " " + pW2,
        pW + zz + colored("#by aiogram[2.4]", "magenta") + zz + "=\n" + pW1,
    )
    rds.hset(db, "id", bt.id)
    rds.hset(db, "name", name)
    rds.hset(db, "user", bt.username)
    rds.hset(db, "token", telegram_datas["botToken"])
    try:
        bt1 = await bot.get_chat(sudo_id)
        DataBase.hset("sudo", "user", bt1.username)
        if bt1.username:
            DataBase.hset("sudo", "id", bt1.id)
    except:
        print("Sudo Not Found!!!")
    try:
        bt1 = await bot.get_chat("@{}".format(IDs_datas["chUsername"]))
        DataBase.hset("channel", "id", bt1.id)
    except:
        print("Channel Not Found!!!")
    await sendText(GlobalValues().sudoID, 0, 1, 'Bot has been Successfully Loaded')
    if not rds.hget(db, "linkyCH"):
        status = False
        while status != True:
            iD = input("Enter Channel Username for linkyCH: ")
            if re.match(r"^(@\w+)$", iD):
                rds.hset(db, "linkyCH", re.match(r"^(@\w+)$", iD).group(1))
                status = True
                break
            else:
                print("Enter Channel Username that start with @")
                break
    if not rds.hget(db, "supchat"):
        status = False
        while status != True:
            iD = input("Enter Supergroup ID for Support Messages: ")
            if re.match(r"^(-\d+)$", iD):
                rds.hset(db, "supchat", re.match(r"^(-\d+)$", iD).group(1))
                status = True
                break
            else:
                print("Enter Supergroup ID that start with -100")
                break
    if not rds.hget(db, "logchat"):
        status = False
        while status != True:
            iD = input("Enter Channel ID for Anonymous Messages & special Whispers: ")
            if re.match(r"^(-\d+)$", iD):
                rds.hset(db, "logchat", re.match(r"^(-\d+)$", iD).group(1))
                status = True
                break
            else:
                print("Enter Channel ID that start with -100")
                break
