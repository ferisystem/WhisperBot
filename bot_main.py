# coding: utf8
from aiogram.types import (
    ReplyKeyboardMarkup,
    ReplyKeyboardRemove,
    KeyboardButton,
    InputMediaPhoto,
    InputTextMessageContent,
    InlineQueryResultArticle,
    InlineQueryResultCachedPhoto,
    InlineQueryResultCachedGif,
    InlineQueryResultCachedSticker,
    InlineQueryResultCachedVideo,
    InlineQueryResultCachedVoice,
    InputMediaVideo,
    InlineKeyboardMarkup as iMarkup,
    InlineKeyboardButton as iButtun,
    InlineQueryResultPhoto,
)
from aiogram.dispatcher.webhook import (
    AnswerCallbackQuery,
    get_new_configured_app,
)
from config_bot import *
from Files.main_func import *
from Files.lateral_func import *
from Files.keyboards_func import *

# -------------------------------------------------------------------------------- #

class DataBase:
    def get(hash):
        hash = "{}.{}".format(db, hash)
        return rds.get(hash)

    def delete(hash, *hash2):
        hash3 = []
        hash3.append("{}.{}".format(db, hash))
        for i in hash2:
            hash3.append("{}.{}".format(db, i))
        return rds.delete(*hash3)

    def set(hash, value):
        hash = "{}.{}".format(db, hash)
        return rds.set(hash, value)

    def mset(hash):
        hash2 = {}
        for i in hash:
            k = "{}.{}".format(db, i)
            hash2.update({k: hash[i]})
        return rds.mset(hash2)

    def setex(hash, time, value):
        hash = "{}.{}".format(db, hash)
        return rds.setex(hash, time, value)

    def incr(hash):
        hash = "{}.{}".format(db, hash)
        return rds.incr(hash)

    def incrby(hash, value):
        hash = "{}.{}".format(db, hash)
        return rds.incrby(hash, value)

    def decr(hash):
        hash = "{}.{}".format(db, hash)
        return rds.decr(hash)

    def decrby(hash, value):
        hash = "{}.{}".format(db, hash)
        return rds.decrby(hash, value)

    def ttl(hash):
        hash = "{}.{}".format(db, hash)
        return rds.ttl(hash)

    def hget(hash, value):
        hash = "{}.{}".format(db, hash)
        return rds.hget(hash, value)

    def hset(hash, value, field):
        hash = "{}.{}".format(db, hash)
        return rds.hset(hash, value, field)

    def hdel(hash, value):
        hash = "{}.{}".format(db, hash)
        return rds.hdel(hash, value)

    def sadd(hash, member):
        hash = "{}.{}".format(db, hash)
        return rds.sadd(hash, member)

    def srem(hash, member):
        hash = "{}.{}".format(db, hash)
        return rds.srem(hash, member)

    def sismember(hash, member):
        hash = "{}.{}".format(db, hash)
        return rds.sismember(hash, member)

    def smembers(hash):
        hash = "{}.{}".format(db, hash)
        return rds.smembers(hash)

    def scard(hash):
        hash = "{}.{}".format(db, hash)
        return rds.scard(hash)

    def keys(hash):
        hash = "{}.{}".format(db, hash)
        return rds.keys(hash)


class GlobalValues:  # Global Values
    def __init__(self):
        self.ipAdd = server_datas["ip"]
        self.ipAdD = "http://{}:{}".format(
            self.ipAdd, server_datas["port_server"]
        )
        self.WEBHOOK_URL_PATH = "/{}".format(telegram_datas["botToken"])
        self.port = server_datas["port_tg"]
        self.WEBHOOK_URL = "https://{}:{}{}".format(
            self.ipAdd, self.port, self.WEBHOOK_URL_PATH
        )
        self.WEBHOOK_SSL_CERT = "webhook_cert.pem"
        self.WEBHOOK_SSL_PRIV = "webhook_pkey.pem"
        self.botID = int(rds.hget(db, "id") or bot_id)
        self.botName = rds.hget(db, "name") or "None"
        self.botUser = rds.hget(db, "user") or "None"
        self.sudoID = int(DataBase.hget("sudo", "id") or sudo_id)
        self.supchat = int(rds.hget(db, "supchat") or self.sudoID)
        self.spychat = int(rds.hget(db, "spychat") or self.sudoID)
        self.linkyCH = rds.hget(db, "linkyCH") or "None"
        self.sudoUser = DataBase.hget("sudo", "user") or "None"
        self.sudo_users = (self.sudoID, self.botID) + sudo_users
        self.chLink = IDs_datas["chLink"]


def isBlock(UserID):
    if DataBase.get("isBan:{}".format(UserID)):
        return True
    else:
        return False


async def newUser(msg):
    DataBase.sadd("allUsers", msg.from_user.id)
    await sendText(
        GlobalValues().sudoID,
        0,
        1,
        "#NewUser\n{} > `{}`\nType: {}\nStatus: Active✅".format(
            menMD(msg), msg.from_user.id, msg.text
        ),
        "md",
        blockKeys(msg.from_user.id),
    )


async def memberCommands(msg, input, gp_id, is_super, is_fwd):
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
    langU = lang[user_steps[user_id]["lang"]]
    if "reply_to_message" in msg:
        reply_msg = msg.reply_to_message
        reply_id = reply_msg.message_id
    else:
        reply_msg = None
        reply_id = 0
    etebar = int(DataBase.get("user.etebar:{}".format(user_id)) or "0")
    if is_super:
        pass
    else:
        if isBlock(user_id):
            if not DataBase.get("user.alertBlocked:{}".format(user_id)):
                DataBase.setex(
                    "user.alertBlocked:{}".format(user_id), 120, "True"
                )
                await sendText(chat_id, 0, 1, langU["u_are_blocked"])
            return False
        if user_steps[user_id]["action"] == "support":
            inlineKeys = iMarkup()
            inlineKeys.add(
                iButtun(
                    langU["buttuns"]["disconnect"],
                    callback_data="backstart:@{}".format(user_id),
                )
            )
            inlineKeys2 = iMarkup()
            inlineKeys2.add(
                iButtun(
                    langU["buttuns"]["notice"],
                    callback_data=f"from_who:{user_id}:{msg_id}",
                )
            )
            msg_ = None
            if "text" in msg:
                if msg.entities and msg.entities[0].type == "bot_command":
                    user_steps[user_id].update({"action": "nothing"})
                else:
                    await copyMessage(
                        GlobalValues().sudoID, chat_id, msg_id, reply_markup=inlineKeys2
                    )
                    await sendText(
                        chat_id, msg, 1, langU["sent_wait"], None, inlineKeys
                    )
            else:
                await copyMessage(
                    GlobalValues().sudoID, chat_id, msg_id, reply_markup=inlineKeys2
                )
                await sendText(
                    chat_id, msg, 1, langU["sent_wait"], None, inlineKeys
                )
        if (
            DataBase.get("who_conneted:{}".format(user_id))
            and not "/start" in msg.text
        ):
            which_user = DataBase.get("who_conneted:{}".format(user_id))
            DataBase.delete("who_conneted:{}".format(user_id))
            # if not msg.text:
            # msg_ = await copyMessage(which_user, chat_id, msg_id, caption = msg.caption,\
            # caption_entities = msg.caption_entities, reply_msg = None,\
            # reply_markup = anonymous_new_message_keys(which_user, user_id, msg_id))
            # else:
            # msg_ = await copyMessage(which_user, chat_id, msg_id, reply_msg = None,
            # reply_markup = anonymous_new_message_keys(which_user, user_id, msg_id))
            msg_ = await msg.forward(GlobalValues().supchat)
            await sendText(
                chat_id,
                msg,
                1,
                langU["your_msg_sent"],
                "md",
                anonymous_send_again_keys(user_id, which_user),
            )
            # DataBase.setex('msg_from:{}'.format(msg_id), 86400*30, user_id)
            DataBase.sadd(
                "inbox_user:{}".format(which_user),
                f"{msg_.message_id}:{user_id}:{msg_id}:0:{int(time())}:no",
            )
            DataBase.setex("is_stater:{}".format(user_id), 86400 * 7, "True")
            await sendText(
                which_user, 0, 1, langU["new_message"].format(msg_.message_id)
            )
        if reply_msg:
            if "reply_markup" in reply_msg:
                input_ = reply_msg.reply_markup.inline_keyboard[0][
                    0
                ].callback_data
                if "anon:blo" in input_:
                    ap = re_matches(
                        r"^anon:blo:(\d+):(\d+):(\d+):@(\d+)$", input_
                    )
                    which_user = int(ap[1])
                    DataBase.incr("stat_anon")
                    if DataBase.sismember(
                        "blocks:{}".format(which_user), user_id
                    ):
                        await sendText(
                            chat_id,
                            msg,
                            1,
                            langU["yare_blocked_anon"],
                            "md",
                            anonymous_back_keys(user_id),
                        )
                        return False
                    if not msg.text:
                        msg_ = await msg.forward(GlobalValues().supchat)
                    elif not "/start" in msg.text:
                        msg_ = await msg.forward(GlobalValues().supchat)
                    await sendText(
                        chat_id,
                        msg,
                        1,
                        langU["your_msg_sent"],
                        "md",
                        anonymous_back_keys(user_id),
                    )
                    # DataBase.setex('msg_from:{}'.format(msg_id), 86400*30, user_id)
                    if DataBase.get("is_stater:{}".format(which_user)):
                        DataBase.sadd(
                            "inbox_user:{}".format(which_user),
                            f"{msg_.message_id}:{user_id}:{msg_id}:{ap[2]}:{int(time())}:yes",
                        )
                    else:
                        DataBase.sadd(
                            "inbox_user:{}".format(which_user),
                            f"{msg_.message_id}:{user_id}:{msg_id}:{ap[2]}:{int(time())}:no",
                        )
                    await sendText(
                        which_user,
                        0,
                        1,
                        langU["new_message"].format(msg_.message_id),
                    )
                if "from_who" in input_:
                    ap = re_matches(r"^from_who:(\d+):(\d+)$", input_)
                    which_user = int(ap[1])
                    msgID = int(ap[2])
                    sendM = await copyMessage(
                        which_user, chat_id, msg_id, reply_msg=msgID
                    )
                    if sendM[0] is True:
                        await sendText(chat_id, msg, 1, "✅‌")
                    else:
                        await sendText(chat_id, msg, 1, "❌‌\n{}".format(sendM))
        if DataBase.get("ready_to_recv_special:{}".format(user_id)):
            if (
                msg.text
                and (
                    re.match(r"^این$", msg.text)
                    or re.match(r"^this$", msg.text)
                )
                and reply_msg
            ):
                data_msg = reply_msg
            else:
                data_msg = msg
            if (
                data_msg.text
                or data_msg.photo
                or data_msg.voice
                or data_msg.video
            ):
                allow = True
            elif data_msg.animation or data_msg.audio or data_msg.sticker:
                allow = True
            elif data_msg.video_note or data_msg.document or data_msg.contact:
                allow = True
            elif data_msg.venue or data_msg.location:
                allow = True
            if allow:
                time_data = DataBase.hget(
                    "najva_special:{}".format(user_id), "time"
                )
                users_data = DataBase.hget(
                    "najva:{}:{}".format(user_id, time_data), "users"
                )
                if "@" in users_data:
                    name_user = await userIds(users_data)
                else:
                    name_user = users_data
                name_user = await userInfos(name_user, info="name")
                await sendText(
                    chat_id,
                    data_msg,
                    1,
                    langU["register_special"].format(name_user),
                    "html",
                    register_special_keys(user_id),
                )
            else:
                await sendText(chat_id, 0, 1, langU["now_allow_type"])
        if "text" in msg:
            input = msg.text.lower()
            if (
                DataBase.get("ready_to_change_link:{}".format(user_id))
                and not "/start" in input
            ):
                if 12 < len(msg.text) < 3 or not msg.text.isalnum():
                    await sendText(
                        chat_id,
                        msg,
                        1,
                        langU["rules_cus_link_anon"],
                        "md",
                        anonymous_cus_link_keys(user_id),
                    )
                elif DataBase.sismember("links_anon", msg.text):
                    await sendText(
                        chat_id,
                        msg,
                        1,
                        langU["rules_cus_link_anon2"],
                        "md",
                        anonymous_cus_link_keys(user_id),
                    )
                else:
                    link_previous = DataBase.get(
                        "link_anon:{}".format(user_id)
                    )
                    DataBase.delete("link_anon:{}".format(link_previous))
                    DataBase.srem("links_anon", link_previous)
                    DataBase.set("link_anon:{}".format(user_id), msg.text)
                    DataBase.set("link_anon:{}".format(msg.text), user_id)
                    DataBase.sadd("links_anon", msg.text)
                    DataBase.delete("ready_to_change_link:{}".format(user_id))
                    await bot.delete_message(
                        chat_id, DataBase.get("pre_msgbot:{}".format(user_id))
                    )
                    await sendText(
                        chat_id,
                        msg,
                        1,
                        "{}\nt.me/{}?start={}".format(
                            langU["customize_link_anon2"],
                            GlobalValues().botUser,
                            DataBase.get("link_anon:{}".format(user_id)),
                        ),
                        "md",
                        anonymous_cus_link_keys(user_id),
                    )
            if (
                DataBase.get("ready_to_change_name:{}".format(user_id))
                and not "/start" in input
            ):
                if 21 < len(msg.text):
                    await sendText(
                        chat_id, msg, 1, langU["rules_cus_name_anon"], "md"
                    )
                else:
                    DataBase.set("name_anon:{}".format(user_id), msg.text)
                    DataBase.delete("ready_to_change_name:{}".format(user_id))
                    await bot.delete_message(
                        chat_id, DataBase.get("pre_msgbot:{}".format(user_id))
                    )
                    await sendText(
                        chat_id,
                        msg,
                        1,
                        langU["changed_name_anon"],
                        "md",
                        anonymous_cus_name_keys(user_id),
                    )
            if (
                DataBase.get("ready_to_enter_id:{}".format(user_id))
                and not "/start" in input
            ):
                if re.match(r"^(\d+)$", input):
                    ap = re_matches(r"^(\d+)$", input)
                    DataBase.delete("ready_to_enter_id:{}".format(user_id))
                    await bot.delete_message(
                        chat_id, DataBase.get("pre_msgbot:{}".format(user_id))
                    )
                    if DataBase.sismember("allUsers", ap[1]):
                        if int(ap[1]) == int(user_id):
                            await sendText(
                                chat_id,
                                msg,
                                1,
                                "{}\n{}".format(
                                    langU["cant_send_self"],
                                    langU["enter_id_for_send"],
                                ),
                                "md",
                                anonymous_back_keys(user_id),
                            )
                        elif DataBase.sismember(
                            "blocks:{}".format(ap[1]), user_id
                        ):
                            await sendText(
                                chat_id,
                                msg,
                                1,
                                langU["yare_blocked_anon"],
                                "md",
                                anonymous_back_keys(user_id),
                            )
                        else:
                            hash = ":@{}".format(user_id)
                            langU = lang[user_steps[user_id]["lang"]]
                            buttuns = langU["buttuns"]
                            inlineKeys = iMarkup()
                            inlineKeys.add(
                                iButtun(
                                    buttuns["cancel"],
                                    callback_data="backstart{}".format(hash),
                                )
                            )
                            DataBase.set(
                                "who_conneted:{}".format(user_id), ap[1]
                            )
                            await sendText(
                                chat_id,
                                msg,
                                1,
                                langU["user_connect_4send"].format(
                                    DataBase.get("name_anon2:{}".format(ap[1]))
                                ),
                                "md",
                                inlineKeys,
                            )
                    else:
                        await sendText(
                            chat_id,
                            msg,
                            1,
                            langU["user_404_4send"],
                            "md",
                            anonymous_back_keys(user_id),
                        )
                elif re.match(r"^(@\w+)$", input):
                    ap = re_matches(r"^(@\w+)$", input)
                    DataBase.delete("ready_to_enter_id:{}".format(user_id))
                    await bot.delete_message(
                        chat_id, DataBase.get("pre_msgbot:{}".format(user_id))
                    )
                    userID = await userIds(ap[1])
                    if not str(userID).isdigit():
                        return await sendText(
                            chat_id,
                            msg,
                            1,
                            langU["user_404_4send"],
                            "md",
                            anonymous_back_keys(user_id),
                        )
                    if DataBase.sismember("allUsers", userID):
                        if int(userID) == int(user_id):
                            await sendText(
                                chat_id,
                                msg,
                                1,
                                "{}\n{}".format(
                                    langU["cant_send_self"],
                                    langU["enter_id_for_send"],
                                ),
                                "md",
                                anonymous_back_keys(user_id),
                            )
                        elif DataBase.sismember(
                            "blocks:{}".format(userID), user_id
                        ):
                            await sendText(
                                chat_id,
                                msg,
                                1,
                                langU["yare_blocked_anon"],
                                "md",
                                anonymous_back_keys(user_id),
                            )
                        else:
                            hash = ":@{}".format(user_id)
                            langU = lang[user_steps[user_id]["lang"]]
                            buttuns = langU["buttuns"]
                            inlineKeys = iMarkup()
                            inlineKeys.add(
                                iButtun(
                                    buttuns["cancel"],
                                    callback_data="backstart{}".format(hash),
                                )
                            )
                            DataBase.set(
                                "who_conneted:{}".format(user_id), userID
                            )
                            await sendText(
                                chat_id,
                                msg,
                                1,
                                langU["user_connect_4send"].format(
                                    DataBase.get(
                                        "name_anon2:{}".format(userID)
                                    )
                                ),
                                "md",
                                inlineKeys,
                            )
                    else:
                        await sendText(
                            chat_id,
                            msg,
                            1,
                            langU["user_404_4send"],
                            "md",
                            anonymous_back_keys(user_id),
                        )
                else:
                    DataBase.delete("ready_to_enter_id:{}".format(user_id))
                    await bot.delete_message(
                        chat_id, DataBase.get("pre_msgbot:{}".format(user_id))
                    )
                    await sendText(
                        chat_id,
                        msg,
                        1,
                        langU["user_404_4send"],
                        "md",
                        anonymous_back_keys(user_id),
                    )
            if re.match(r"/inbox$", input):
                if DataBase.scard("inbox_user:{}".format(user_id)) > 0:
                    your_messages = DataBase.smembers(
                        "inbox_user:{}".format(user_id)
                    )
                    for i in your_messages:
                        ap = re_matches(
                            r"^(\d+):(\d+):(\d+):(\d+):(\d+):(yes|no)$", i
                        )
                        if ap[6] == "yes":
                            show_sender = int(ap[2])
                        else:
                            show_sender = None
                        await asyncio.sleep(0.5)
                        await copyMessage(
                            user_id,
                            GlobalValues().supchat,
                            int(ap[1]),
                            reply_msg=int(ap[4]),
                            protect_content=False,
                            reply_markup=anonymous_new_message_keys(
                                user_id, ap[2], ap[3], show_sender, ap[5]
                            ),
                        )
                        if DataBase.get("is_stater:{}".format(ap[2])):
                            DataBase.setex(
                                "is_stater:{}".format(ap[2]), 86400 * 7, "True"
                            )
                            user_name = DataBase.get(
                                "name_anon2:{}".format(user_id)
                            )
                        else:
                            user_name = langU["anonymous"]
                        await sendText(
                            ap[2],
                            ap[3],
                            1,
                            langU["your_msg_seen"].format(user_name),
                        )
                        DataBase.srem("inbox_user:{}".format(user_id), i)
                else:
                    await sendText(chat_id, msg, 1, langU["inbox_empty"])
            if re.match(r"^ping$", input):
                await sendText(chat_id, msg, 1, "*PONG*", "md")
            if re.search(r"^/start (.*)$", input):
                ap = re_matches(r"^/start (.*)$", msg.text)
                if ap[1] == "set":
                    await sendText(
                        chat_id,
                        msg,
                        1,
                        langU["najva_settings"].format(GlobalValues().botName),
                        "html",
                        najva_settings_keys(user_id),
                    )
                elif ap[1] == "help":
                    await sendText(
                        chat_id,
                        msg,
                        1,
                        langU["najva_help"],
                        None,
                        najva_help_keys(user_id),
                    )
                elif re.match(r"^(\d+)_(\d+)_(\d+)$", ap[1]):
                    ap = re_matches(r"^(\d+)_(\d+)_(\d+)$", ap[1])
                    from_user = ap[1]
                    time_data = float(f"{ap[2]}.{ap[3]}")
                    DataBase.set(
                        "najva_seen_time:{}:{}".format(from_user, time_data),
                        int(time()),
                    )
                    DataBase.incr(
                        "najva_seen_count:{}:{}".format(from_user, time_data)
                    )
                    DataBase.sadd(
                        "najva_seened:{}:{}".format(from_user, time_data),
                        user_id,
                    )
                    special_msgID = DataBase.hget(
                        "najva_special:{}".format(from_user), "id"
                    )
                    users_data = DataBase.hget(
                        "najva:{}:{}".format(from_user, time_data), "users"
                    )
                    file_id = DataBase.hget(
                        "najva:{}:{}".format(from_user, time_data), "file_id"
                    )
                    file_type = DataBase.hget(
                        "najva:{}:{}".format(from_user, time_data), "file_type"
                    )
                    source_id = DataBase.hget(
                        "najva:{}:{}".format(from_user, time_data), "source_id"
                    )
                    msgid = DataBase.hget(
                        "najva:{}:{}".format(from_user, time_data), "msg_id"
                    )
                    inlineKeys = await show_speical_najva_keys(
                        user_id, from_user
                    )
                    msg_ = await copyMessage(
                        chat_id,
                        GlobalValues().supchat,
                        msgid,
                        protect_content=False,
                        reply_markup=inlineKeys,
                    )
                    if DataBase.hget(f"setting_najva:{from_user}", "seen"):
                        await sendText(
                            from_user,
                            source_id,
                            1,
                            langU["speical_najva_seen"].format(
                                msg.from_user.first_name
                            ),
                        )
                    await editText(
                        inline_msg_id=special_msgID,
                        text=langU["speical_najva_seen2"].format(
                            msg.from_user.first_name
                        ),
                        parse_mode="html",
                        reply_markup=najva_seen3_keys(from_user, time_data),
                    )
                    if DataBase.hget(f"setting_najva:{from_user}", "dispo"):
                        DataBase.delete(
                            "najva:{}:{}".format(from_user, time_data)
                        )
                        DataBase.delete("najva_special:{}".format(from_user))
                        DataBase.srem(
                            "najva_autodel",
                            f"{from_user}:{time_data}:{special_msgID}",
                        )
                    DataBase.hset(
                        "najva:{}:{}".format(from_user, time_data),
                        "seen_id",
                        f"{chat_id}:{msg_[1].message_id}",
                    )
                else:
                    we_have = DataBase.get("link_anon:{}".format(ap[1]))
                    if we_have:
                        DataBase.incr("stat_anon")
                        if int(we_have) == int(user_id):
                            await sendText(
                                chat_id,
                                msg,
                                1,
                                "{}\n{}".format(
                                    langU["cant_send_self"],
                                    langU["enter_id_for_send"],
                                ),
                                "md",
                                anonymous_back_keys(user_id),
                            )
                        elif DataBase.sismember(
                            "blocks:{}".format(we_have), user_id
                        ):
                            await sendText(
                                chat_id,
                                msg,
                                1,
                                langU["yare_blocked_anon"],
                                "md",
                                anonymous_back_keys(user_id),
                            )
                        else:
                            hash = ":@{}".format(user_id)
                            langU = lang[user_steps[user_id]["lang"]]
                            buttuns = langU["buttuns"]
                            inlineKeys = iMarkup()
                            inlineKeys.add(
                                iButtun(
                                    buttuns["cancel"],
                                    callback_data="backstart{}".format(hash),
                                )
                            )
                            DataBase.set(
                                "who_conneted:{}".format(user_id), we_have
                            )
                            DataBase.incr("user.stats_anon:{}".format(we_have))
                            await sendText(
                                chat_id,
                                msg,
                                1,
                                langU["user_connect_4send"].format(
                                    DataBase.get(
                                        "name_anon2:{}".format(we_have)
                                    )
                                ),
                                "md",
                                inlineKeys,
                            )
                    else:
                        await sendText(
                            chat_id, msg, 1, langU["link_expire_anon"], "md"
                        )
            if not re.search(r"^/start p(\d+)$", input):
                if not DataBase.sismember("allUsers", user_id):
                    await newUser(msg)
            if not isSudo(user_id):
                hash = "user.flood:{}:{}:num".format(user_id, chat_id)
                msgs = int(rds.get(hash) or 0)
                if msgs > (5 - 1):
                    name = user_name.replace("[ < >]", "")
                    await sendText(
                        chat_id,
                        msg,
                        1,
                        langU["ban_flood"].format(
                            name,
                            user_id,
                            GlobalValues().botName,
                            GlobalValues().botUser,
                            GlobalValues().sudoUser,
                        ),
                        "html",
                    )
                    DataBase.setex("isBan:{}".format(user_id), 900, "True")
                rds.setex(hash, 3, msgs + 1)
            if int(user_id) != GlobalValues().botID and not await is_Channel_Member(
                "@{}".format(IDs_datas["chUsername"]), user_id
            ):
                await sendText(
                    chat_id,
                    msg,
                    1,
                    langU["join_channel"].format(IDs_datas["chUsername"]),
                    "md",
                )
                return False
            if not re.search(
                r"^[!/#]start", input
            ) and not await is_Channel_Member(
                "@{}".format(IDs_datas["chUsername"]), user_id
            ):
                inlineKeys = iMarkup()
                inlineKeys.add(
                    iButtun(
                        langU["buttuns"]["join"],
                        url="https://t.me/{}".format(IDs_datas["chUsername"]),
                    ),  # GlobalValues().chLink),
                    iButtun(
                        langU["buttuns"]["joined"],
                        callback_data="backstart:@{}".format(user_id),
                    ),
                )
                await sendText(
                    chat_id,
                    msg,
                    1,
                    langU["force_join"].format(IDs_datas["chUsername"]),
                    "md",
                    inlineKeys,
                )
                return False
            if re.match(r"^/najva$", input):
                await sendText(
                    chat_id,
                    msg,
                    1,
                    langU["najva_help"],
                    None,
                    najva_help_keys(user_id),
                )
            if re.match(r"^/nashenas$", input):
                await sendText(
                    chat_id,
                    msg,
                    1,
                    langU["anon"].format(GlobalValues().botName),
                    "html",
                    anonymous_keys(user_id),
                )
            if re.match(r"^/help$", input):
                await sendText(
                    chat_id,
                    msg,
                    1,
                    langU["najva_help"],
                    None,
                    najva_help_keys(user_id),
                )
            if re.match(r"^/settings$", input):
                await sendText(
                    chat_id,
                    msg,
                    1,
                    langU["najva_settings"].format(GlobalValues().botName),
                    "html",
                    najva_settings_keys(user_id),
                )
            if re.match(r"^/free$", input):
                await sendText(chat_id, msg, 1, langU["adsfree"], None)
            if re.match(r"^/lang$", input):
                await sendText(
                    chat_id,
                    msg,
                    1,
                    langU["language"],
                    None,
                    settings_keys(user_id),
                )
            if re.match(r"^/support$", input):
                await sendText(
                    chat_id,
                    msg,
                    1,
                    langU["support"],
                    None,
                    support_keys(user_id),
                )
            if re.match(r"^/start$", input) or re.match(
                r"^{}$".format(langU["buttuns"]["back_menu"]), input
            ):
                user_steps[user_id].update({"action": "nothing"})
                sendM = await sendText(chat_id, msg, 1, ".", None, ())
                try:
                    await sendM[1].delete()
                except:
                    pass
                DataBase.delete("sup:{}".format(user_id))
                await sendText(
                    chat_id,
                    msg,
                    1,
                    langU["start"].format(GlobalValues().botName),
                    "html",
                    start_keys(user_id),
                )
            if (
                re.match(r"^قطع ارتباط$", input)
                or re.match(r"^disconnect$", input)
                or re.match(r"^قطع الاتصال$", input)
            ):
                if DataBase.get("sup:{}".format(user_id)):
                    DataBase.delete("sup:{}".format(user_id))
                    text = langU["disconnect"]
                else:
                    text = langU["not_connect"]
                await sendText(
                    chat_id, msg, 1, text, "md", start_keys(user_id)
                )
            if isSudo(user_id):
                if re.match(r"/block (\d+)$", input):
                    ap = re_matches("/block (\d+)$", input)
                    if DataBase.get("isBan:{}".format(ap[1])):
                        alerttext = langU["usblocked"]
                    else:
                        DataBase.set("isBan:{}".format(ap[1]), "True")
                        alerttext = langU["usblock"]
                    await sendText(chat_id, msg, 1, alerttext)
                if re.match(r"/unblock (\d+)$", input):
                    ap = re_matches("/unblock (\d+)$", input)
                    if DataBase.get("isBan:{}".format(ap[1])):
                        DataBase.delete("isBan:{}".format(ap[1]))
                        alerttext = langU["usunblocked"]
                    else:
                        alerttext = langU["usunblock"]
                    await sendText(chat_id, msg, 1, alerttext)
                if re.match(r"^/send2all$", input):
                    if reply_msg:
                        if (
                            reply_msg.forward_from
                            or reply_msg.forward_from_chat
                        ):
                            LIST = DataBase.smembers("allUsers")
                            sendM = await sendText(
                                chat_id,
                                msg,
                                1,
                                langU["fwd_to_all"].format(len(LIST)),
                            )
                            n = 0
                            for i in LIST:
                                await asyncio.sleep(0.1)
                                try:
                                    await reply_msg.forward(i)
                                    n += 1
                                except:
                                    pass
                            await editText(
                                chat_id,
                                sendM[1].message_id,
                                0,
                                langU["fwdd_to_all"].format(len(LIST), n),
                            )
                        elif reply_msg:
                            LIST = DataBase.smembers("allUsers")
                            sendM = await sendText(
                                chat_id,
                                msg,
                                1,
                                langU["send_to_all"].format(len(LIST)),
                            )
                            n = 0
                            for i in LIST:
                                await asyncio.sleep(0.1)
                                # sendM2 = await sendText(i, 0, 1, reply_msg.text)
                                sendM2 = await copyMessage(
                                    i, chat_id, reply_id, protect_content=False
                                )
                                if sendM2[0] is True:
                                    n += 1
                            await editText(
                                chat_id,
                                sendM[1].message_id,
                                0,
                                langU["sent_to_all"].format(len(LIST), n),
                            )
                    else:
                        await sendText(chat_id, msg, 1, langU["just_reply"])


def find_media_id(msg):
    can_hide = False
    if msg.photo:
        file_id = msg.photo[-1].file_id
        file_type = "photo"
        can_hide = True
    elif msg.video:
        file_id = msg.video.file_id
        file_type = "video"
        can_hide = True
    elif msg.sticker:
        file_id = msg.sticker.file_id
        file_type = "sticker"
        can_hide = True
    elif msg.animation:
        file_id = msg.animation.file_id
        file_type = "animation"
        can_hide = True
    elif msg.voice:
        file_id = msg.voice.file_id
        file_type = "voice"
        can_hide = True
    elif msg.audio:
        file_id = msg.audio.file_id
        file_type = "audio"
    elif msg.document:
        file_id = msg.document.file_id
        file_type = "document"
    elif msg.video_note:
        file_id = msg.video_note.file_id
        file_type = "video_note"
    elif msg.text:
        file_id = msg.message_id
        file_type = "text"
    elif msg.contact:
        file_id = msg.message_id
        file_type = "contact"
    elif msg.venue:
        file_id = msg.message_id
        file_type = "venue"
    return file_id, file_type, can_hide


def isUserSteps(user_id):
    if user_id in user_steps and "action" in user_steps[user_id]:
        return True
    else:
        return False


def setupUserSteps(msg, user_id):
    if user_id in user_steps and "action" in user_steps[user_id]:
        action = user_steps[user_id]["action"]
    else:
        action = "nothing"
    try:
        if not DataBase.get("link_anon:{}".format(user_id)):
            DataBase.hset(f"setting_najva:{user_id}", "seen", 1)
            DataBase.hset(f"setting_najva:{user_id}", "recv", 1)
            text = generate_link()
            while True:
                if not DataBase.sismember("links_anon", text):
                    DataBase.set("link_anon:{}".format(user_id), text)
                    DataBase.set("link_anon:{}".format(text), user_id)
                    DataBase.sadd("links_anon", text)
                    break
                text = generate_link()
        name_anon2 = DataBase.get("name_anon2:{}".format(user_id))
        user_name = msg.from_user.first_name
        if not name_anon2:
            DataBase.set("name_anon2:{}".format(user_id), user_name)
        elif name_anon2 != user_name:
            DataBase.set("name_anon2:{}".format(user_id), user_name)
        user_steps[user_id].update(
            {
                "action": action,
                "lang": (
                    DataBase.get("user.lang:{}".format(user_id))
                    or echoLangCode(msg.from_user)
                ),
            }
        )
    except:
        user_steps.update(
            {
                user_id: {
                    "action": action,
                    "lang": (
                        DataBase.get("user.lang:{}".format(user_id))
                        or echoLangCode(msg.from_user)
                    ),
                }
            }
        )


def echoLangCode(from_user):
    if "language_code" in from_user:
        from_user = from_user.language_code
        if re.search("^fa", from_user):
            return "fa"
        elif re.search("^en", from_user):
            return "en"
        else:
            return "en"
    else:
        return "en"


def deletePreviousData(user_id):
    if "deezer" in user_steps[user_id]:
        del user_steps[user_id]["deezer"]
    if "spotify" in user_steps[user_id]:
        del user_steps[user_id]["spotify"]
    if "sound_cloud" in user_steps[user_id]:
        del user_steps[user_id]["sound_cloud"]
    if "youtube" in user_steps[user_id]:
        del user_steps[user_id]["youtube"]
    if "dl" in user_steps[user_id]:
        del user_steps[user_id]["dl"]
    if "in_wait_dl" in user_steps[user_id]:
        del user_steps[user_id]["in_wait_dl"]
    if "what_do" in user_steps[user_id]:
        del user_steps[user_id]["what_do"]


def generate_link():
    # alphabets = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'n', 'm', 'l', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z']
    # numbers = [1, 2, 3, 4, 5, 6, 7, 8, 9, 0]
    # letters = (alphabets, numbers, alphabets, alphabets, numbers)
    # text = ''
    # for i in range(0, 12):
    # which_one = random.choice(letters)
    # which_key = random.choice(which_one)
    # text = "{}{}".format(text, which_key)
    text = "".join(random.choices(string.ascii_letters + string.digits, k=12))
    return text


def generate_uniqid():
    text = "".join(random.choices(string.ascii_letters + string.digits, k=29))
    while True:
        if not DataBase.sismember("file_ids", text):
            DataBase.sadd("file_ids", text)
            break
        text = "".join(
            random.choices(string.ascii_letters + string.digits, k=29)
        )
    return text


async def message_process(msg: types.Message):
    if int(msg.date.timestamp()) < (int(time()) - 60):
        cPrint("{} Old Message Skipped".format(msg.date), 2, textColor="cyan")
        return False
    data = CheckMsg(msg)
    chat_id = int(msg.chat.id)
    content = data.content
    user_id = int(msg.from_user.id)
    msg_id = msg.message_id
    setupUserSteps(msg, user_id)
    langU = lang[user_steps[user_id]["lang"]]
    print(colored("Message >", "cyan"))
    print(colored("userID", "yellow"), colored(user_id, "white"))
    print(colored("Type", "yellow"), colored(content, "white"))
    print(colored("msgID", "yellow"), colored(msg_id, "white"))
    print()
    if "reply_to_message" in msg:
        reply_msg = msg.reply_to_message
        reply_id = reply_msg.message_id
    else:
        reply_msg = None
        reply_id = 0
    if "forward_from" in msg and msg.forward_from.id:
        saveUsername(msg)
    else:
        saveUsername(msg)
    if not DataBase.get("checkBotInfo"):
        try:
            b = await bot.get_me()
            DataBase.hset(db, "user", b.username)
            DataBase.hset(db, "id", b.id)
            DataBase.hset(db, "name", b.first_name)
            DataBase.hset(db, "token", telegram_datas["botToken"])
            getC = await bot.get_chat(sudo_id)
            DataBase.hset("sudo", "user", getC.id)
            if getC.username:
                DataBase.hset("sudo", "user", getC.username)
            DataBase.setex("checkBotInfo", 86400, "True")
        except:
            print("Sudo or Channel Not Found!!!")
            pass
    if isPv(msg):
        setupUserSteps(msg, user_id)
        await memberCommands(msg, "input", chat_id, False, False)
    if isSuper(msg):
        if chat_id == GlobalValues().supchat:
            if isSudo(user_id):
                IF = reply_msg and reply_msg.from_user.id == GlobalValues().botID
                if IF and reply_msg.text and "text" in msg:
                    IF2 = reply_msg.text.split(" | ")
                    sendM = await sendText(IF2[1], 0, 1, msg.text, "html")
                    if sendM[0] is True:
                        await sendText(chat_id, msg, 1, "✅")
                    else:
                        await sendText(chat_id, msg, 1, "❌\n{}".format(sendM))
        else:
            # await bot.leave_chat(chat_id)
            if (
                msg.via_bot
                and msg.via_bot.username == GlobalValues().botUser
                and msg.reply_markup
            ):
                time_data = msg.reply_markup.inline_keyboard[0][0]
                if (
                    time_data.callback_data
                    and "showN2" in time_data.callback_data
                ):
                    time_data = time_data.callback_data.split(":")[2]
                    if reply_msg:
                        Uid = reply_msg.from_user.id
                        Uname = reply_msg.from_user.first_name
                        DataBase.hset(
                            "najva:{}:{}".format(user_id, time_data),
                            "users",
                            Uid,
                        )
                        await editText(
                            chat_id,
                            msg_id,
                            0,
                            langU["inline"]["text"]["najva_person"].format(
                                Uname
                            ),
                            "HTML",
                            msg.reply_markup,
                        )
                        if DataBase.hget(f"setting_najva:{Uid}", "recv"):
                            await sendText(
                                Uid,
                                0,
                                1,
                                '<a href="t.me/c/{}/{}">{}</a>'.format(
                                    str(chat_id).replace("-100", ""),
                                    msg_id,
                                    langU["new_najva"],
                                ),
                                "html",
                            )
                    else:
                        if (
                            DataBase.hget(
                                "najva:{}:{}".format(user_id, time_data),
                                "users",
                            )
                            == "reply"
                        ):
                            await editText(
                                chat_id,
                                msg_id,
                                0,
                                langU["didnt_enter_user"],
                                "HTML",
                            )
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
    saveUsername(msg, mode="callback")
    user_id = msg.from_user.id
    if msg.from_user.username:
        username = msg.from_user.username
    else:
        username = ""
    input = msg.data.lower()
    setupUserSteps(msg, user_id)
    langU = lang[user_steps[user_id]["lang"]]
    if "message" in msg:
        msg_id = msg.message.message_id
    else:
        msg_id = 0
    if "message" in msg and "reply_to_message" in msg.message:
        reply_msg = msg.message.reply_to_message
        reply_id = reply_msg.message_id
    else:
        reply_msg = None
        reply_id = 0
    print(colored("Callback >", "cyan"))
    print(colored("userID", "yellow"), colored(user_id, "white"))
    print(colored("Query", "yellow"), colored(input, "white"))
    print(colored("queryID", "yellow"), colored(msg.id, "white"))
    print()
    # if re.search(r"@(\d+)", input):
    # ap = re_matches("@(\d+)", input, 's')
    # if int(ap[1]) != user_id:
    # if not DataBase.get('user.alertinline:{}:{}'.format(user_id, msg_id)):
    # DataBase.setex('user.alertinline:{}:{}'.format(user_id, msg_id), 3600, "True")
    # return AnswerCallbackQuery(msg.id, langU['isNot4u'], True, None, 3600)
    # return False
    # if int(ap[1]) == user_id and not DataBase.get('user.alertNotMemberChannel:{}'.format(user_id)):
    # if not re.search(r'insgp(.*)', input) and not re.search(r'ib(.*)', input) and not await is_Channel_Member("@{}".format(IDs_datas['chUsername']), user_id):
    # DataBase.set('user.alertNotMemberChannel2:{}'.format(user_id), "True")
    # await answerCallbackQuery(msg, langU['uNotJoined'].format(IDs_datas['chUsername']), True)
    # inlineKeys = iMarkup()
    # inlineKeys.add = (
    # iButtun(langU['buttuns']['join'], url = 'https://t.me/{}'.format(IDs_datas['chUsername'])),
    # iButtun(langU['buttuns']['joined'], callback_data = input)
    # )
    # await editText(chat_id, msg_id, 1, langU['join_channel'].format(IDs_datas['chUsername']), 'md', inlineKeys)
    # return False
    # if DataBase.get('user.alertNotMemberChannel2:{}'.format(user_id)):
    # DataBase.delete('user.alertNotMemberChannel2:{}'.format(user_id))
    # await answerCallbackQuery(msg, langU['you_accepted'])
    # DataBase.setex('user.alertNotMemberChannel:{}'.format(user_id), 3600, "True")
    if "message" in msg:
        DataBase.incr("amarBot.callmsg")
        _ = msg.message
        msg_id = _.message_id
        chat_id = _.chat.id
        chat_name = _.chat.title
        if not rds.get(input):
            rds.psetex(input, 500, 1)
        else:
            return False
        if int(_.date.timestamp()) < (int(time()) - 86400):
            cPrint(
                "{} Old Callback Skipped".format(_.date), 2, textColor="cyan"
            )
            try:
                await _.edit_reply_markup()
            except:
                pass
            return AnswerCallbackQuery(
                msg.id,
                "این پنل قدیمی است دوباره پنل مربوطه را دریافت کنید!\nاگر پنل پرداختی است نگران نباشید :D",
                True,
            )
        if re.match(r"^backstart:@(\d+)$", input):
            DataBase.delete("sup:{}".format(user_id))
            DataBase.delete("ready_to_change_link:{}".format(user_id))
            DataBase.delete("ready_to_change_name:{}".format(user_id))
            DataBase.delete("ready_to_enter_id:{}".format(user_id))
            DataBase.delete("ready_to_recv_special:{}".format(user_id))
            DataBase.delete("who_conneted:{}".format(user_id))
            user_steps[user_id].update({"action": "nothing"})
            deletePreviousData(user_id)
            await editText(
                chat_id,
                msg_id,
                0,
                langU["start"].format(GlobalValues().botName),
                "html",
                start_keys(user_id),
            )
        if re.match(r"^supp:@(\d+)$", input):
            await editText(
                chat_id,
                msg_id,
                0,
                langU["support2"],
                "html",
                support_keys(user_id),
            )
        if re.match(r"^support:@(\d+)$", input):
            user_steps[user_id].update({"action": "support"})
            await sendText(
                GlobalValues().sudoID,
                0,
                1,
                langU["connected_support"].format(menMD(msg)),
                "md",
            )
            inlineKeys = iMarkup()
            inlineKeys.add(
                iButtun(
                    langU["buttuns"]["disconnect"],
                    callback_data="backstart:@{}".format(user_id),
                )
            )
            await editText(
                chat_id, msg_id, 0, langU["support"], "html", inlineKeys
            )
        if re.match(r"^from_who:(\d+):(\d+)$", input):
            ap = re_matches(r"^from_who:(\d+):(\d+)$", input)
            name_user = await userInfos(ap[1], "name")
            await answerCallbackQuery(
                msg,
                langU["message_from"].format(name_user),
                show_alert=True,
                cache_time=86400,
            )
        if re.match(r"^language:@(\d+)$", input):
            await editText(
                chat_id,
                msg_id,
                0,
                langU["language"],
                None,
                settings_keys(user_id),
            )
        if re.match(r"^adsfree:@(\d+)$", input):
            await editText(
                chat_id,
                msg_id,
                0,
                langU["adsfree"].format(GlobalValues().linkyCH),
                "html",
                back_keys(user_id),
            )
        if re.match(r"^set_(.*)_(.*):@(\d+)$", input):
            ap = re_matches("^set_(.*)_(.*):@(\d+)$", input)
            if ap[1] == "lang":
                DataBase.set("user.lang:{}".format(user_id), ap[2])
                try:
                    await editText(
                        chat_id,
                        msg_id,
                        0,
                        lang[ap[2]]["settings"],
                        None,
                        settings_keys(user_id, ap[2]),
                    )
                except:
                    await _.edit_reply_markup(settings_keys(user_id, ap[2]))
                return AnswerCallbackQuery(
                    msg.id, lang["set_{}".format(ap[2])], True, None, 0
                )
        if re.match(r"^notice_1:@(\d+)$", input):
            return AnswerCallbackQuery(
                msg.id, langU["notice_change_file"], True, None, 86400
            )
        if re.match(r"^start_again:@(\d+)$", input):
            DataBase.delete("sup:{}".format(user_id))
            user_steps[user_id].update({"action": "nothing"})
            deletePreviousData(user_id)
            try:
                await _.edit_reply_markup()
            except:
                pass
            await sendText(
                chat_id, 0, 1, langU["start"], None, start_keys(user_id)
            )
        if re.match(r"^blockuser:(\d+)$", input):
            ap = re_matches("^blockuser:(\d+)$", input)
            if DataBase.get("isBan:{}".format(ap[1])):
                alerttext = langU["usblocked"]
            else:
                DataBase.set("isBan:{}".format(ap[1]), "True")
                alerttext = langU["usblock"]
                keyboard = blockKeys(ap[1])
                try:
                    getC = await bot.get_chat(ap[1])
                    await editText(
                        chat_id,
                        msg_id,
                        0,
                        "#NewUser\nName: [{0}](tg://user?id={1})\nID: `{1}`\nStatus: Deactive🚫".format(
                            getC.first_name, ap[1]
                        ),
                        "md",
                        keyboard,
                    )
                except:
                    await editText(
                        chat_id,
                        msg_id,
                        0,
                        "#NewUser\nName: [{0}](tg://user?id={0})\nID: `{0}`\nStatus: Deactive🚫".format(
                            ap[1]
                        ),
                        "md",
                        keyboard,
                    )
            await answerCallbackQuery(msg, alerttext)
        if re.match(r"^unblockuser:(\d+)$", input):
            ap = re_matches("^unblockuser:(\d+)$", input)
            if DataBase.get("isBan:{}".format(ap[1])):
                DataBase.delete("isBan:{}".format(ap[1]))
                alerttext = langU["usunblocked"]
                keyboard = blockKeys(ap[1])
                try:
                    getC = getChat(ap[1])
                    await editText(
                        chat_id,
                        msg_id,
                        0,
                        "#NewUser\nName: [{0}](tg://user?id={1})\nID: `{1}`\nStatus: Active✅".format(
                            getC.first_name, ap[1]
                        ),
                        "md",
                        keyboard,
                    )
                except:
                    await editText(
                        chat_id,
                        msg_id,
                        0,
                        "#NewUser\nName: [{0}](tg://user?id={0})\nID: `{0}`\nStatus: Active✅".format(
                            ap[1]
                        ),
                        "md",
                        keyboard,
                    )
            else:
                alerttext = langU["usunblock"]
            await answerCallbackQuery(msg, alerttext)
        if re.match(r"^list:(.*):(\d+):@(\d+)$", input):
            ap = re_matches("^list:(.*):(\d+):@(\d+)$", input)
            inlineKeys = iMarkup()
            if ap[1] == "block":
                await editText(chat_id, msg_id, 0, langU["wait"])
                text = langU["list_block"]
                keys = DataBase.smembers("isBanned")
                n = int(ap[2])
                for i in keys:
                    n += 1
                    # userID = i.split(':')[-1]
                    userID = i
                    text = "{}{}- {} | {}\n".format(
                        text,
                        n,
                        await userInfos(userID),
                        userID,
                    )
                with open(
                    "Files/list_block.txt", mode="a", encoding="utf-8"
                ) as file:
                    file.write(text)
                await sendDocument(
                    chat_id, open("Files/list_block.txt", encoding="utf-8")
                )
                inlineKeys.add(
                    iButtun(
                        langU["buttuns"]["back"],
                        callback_data="backstart:@{}".format(user_id),
                    ),
                )
                await editText(
                    chat_id,
                    msg_id,
                    0,
                    langU["blocklist_sent"],
                    None,
                    inlineKeys,
                )
                os.system("rm Files/list_block.txt")
            elif ap[1] == "stats":
                stat_users = DataBase.scard("allUsers")
                stat_block = DataBase.scard("isBanned")
                stat_najva = DataBase.get("stat_najva")
                stat_anon = DataBase.get("stat_anon")
                await editText(
                    chat_id,
                    msg_id,
                    0,
                    langU["stats"]
                    .format(
                        stat_users,
                        stat_block,
                        stat_najva,
                        stat_anon,
                    )
                    .replace("None", "0"),
                    "html",
                    back_keys(user_id),
                )
        if re.match(r"^anon:@(\d+)$", input):
            DataBase.delete("ready_to_change_link:{}".format(user_id))
            DataBase.delete("ready_to_change_name:{}".format(user_id))
            DataBase.delete("ready_to_enter_id:{}".format(user_id))
            DataBase.delete("ready_to_recv_special:{}".format(user_id))
            DataBase.delete("who_conneted:{}".format(user_id))
            await editText(
                chat_id,
                msg_id,
                0,
                langU["anon"],
                None,
                anonymous_keys(user_id),
            )
        if re.match(r"^anon:link:@(\d+)$", input):
            DataBase.delete("ready_to_change_link:{}".format(user_id))
            await editText(
                chat_id,
                msg_id,
                0,
                langU["my_link_anon"].format(
                    GlobalValues().botName,
                    GlobalValues().botUser,
                    DataBase.get("link_anon:{}".format(user_id)),
                ),
                "html",
                anonymous_my_link_keys(user_id),
            )
        if re.match(r"^anon:cus:@(\d+)$", input):
            DataBase.setex(
                "ready_to_change_link:{}".format(user_id), 3600, "True"
            )
            DataBase.set(
                "pre_msgbot:{}".format(user_id), msg.message.message_id
            )
            await editText(
                chat_id,
                msg_id,
                0,
                "{}t.me/{}?start={}".format(
                    langU["customize_link_anon"],
                    GlobalValues().botUser,
                    DataBase.get("link_anon:{}".format(user_id)),
                ),
                None,
                anonymous_cus_link_keys(user_id),
            )
        if re.match(r"^anon:change:@(\d+)$", input):
            link_previous = DataBase.get("link_anon:{}".format(user_id))
            DataBase.delete("link_anon:{}".format(link_previous))
            DataBase.srem("links_anon", link_previous)
            text = generate_link()
            while True:
                if not DataBase.sismember("links_anon", text):
                    DataBase.set("link_anon:{}".format(user_id), text)
                    DataBase.set("link_anon:{}".format(text), user_id)
                    DataBase.sadd("links_anon", text)
                    break
                text = generate_link()
            await editText(
                chat_id,
                msg_id,
                0,
                "{}t.me/{}?start={}".format(
                    langU["customize_link_anon"],
                    GlobalValues().botUser,
                    DataBase.get("link_anon:{}".format(user_id)),
                ),
                None,
                anonymous_cus_link_keys(user_id),
            )
        if re.match(r"^anon:telg:@(\d+)$", input):
            await editText(
                chat_id,
                msg_id,
                0,
                "{}\n<code>https://t.me/{}?start={}</code>".format(
                    langU["telg_link_anon"],
                    GlobalValues().botUser,
                    DataBase.get("link_anon:{}".format(user_id)),
                ),
                "html",
                anonymous_insta_link_keys(user_id),
            )
        if re.match(r"^anon:insta:@(\d+)$", input):
            link_picture = '<a href="https://s6.uupload.ir/files/photo_2022-09-01_18-03-08_s3qf.jpg">مشاهده عکس آموزشی</a>'
            await editText(
                chat_id,
                msg_id,
                0,
                langU["insta_link_anon"].format(
                    GlobalValues().botUser, DataBase.get("link_anon:{}".format(user_id))
                ),
                parse_mode="html",
                reply_markup=anonymous_insta_link_keys(user_id),
            )
        if re.match(r"^anon:help:@(\d+)$", input):
            await editText(
                chat_id,
                msg_id,
                0,
                langU["help_anon"],
                None,
                anonymous_help_keys(user_id),
            )
        if re.match(r"^anon:help(\d+):@(\d+)$", input):
            ap = re_matches(r"^anon:help(\d+):@(\d+)$", input)
            hash = ":@{}".format(user_id)
            langU = lang[user_steps[user_id]["lang"]]
            buttuns = langU["buttuns"]
            inlineKeys = iMarkup()
            inlineKeys.add(
                iButtun(
                    buttuns["back_help_anon"],
                    callback_data="anon:help{}".format(hash),
                )
            )
            await editText(
                chat_id,
                msg_id,
                0,
                langU["help{}_anon".format(ap[1])].format(GlobalValues().botName),
                None,
                inlineKeys,
            )
        if re.match(r"^anon:stats:@(\d+)$", input):
            await answerCallbackQuery(
                msg,
                langU["stats_anon"].format(
                    int(
                        DataBase.get("user.stats_anon:{}".format(user_id)) or 0
                    )
                ),
                show_alert=True,
                cache_time=90,
            )
        if re.match(r"^anon:name:@(\d+)$", input):
            DataBase.delete("ready_to_change_name:{}".format(user_id))
            await editText(
                chat_id,
                msg_id,
                0,
                langU["name_anon"].format(
                    DataBase.get("name_anon:{}".format(user_id))
                    or msg.from_user.first_name
                ),
                None,
                anonymous_name_keys(user_id),
            )
        if re.match(r"^anon:cus_name:@(\d+)$", input):
            DataBase.setex(
                "ready_to_change_name:{}".format(user_id), 3600, "True"
            )
            DataBase.set(
                "pre_msgbot:{}".format(user_id), msg.message.message_id
            )
            await editText(
                chat_id,
                msg_id,
                0,
                langU["help_cus_name_anon"],
                None,
                anonymous_cus_name_keys(user_id),
            )
        if re.match(r"^anon:default_name:@(\d+)$", input):
            DataBase.delete("name_anon:{}".format(user_id))
            await answerCallbackQuery(
                msg, langU["changed_name_anon"], show_alert=True, cache_time=90
            )
            await editText(
                chat_id,
                msg_id,
                0,
                langU["name_anon"].format(
                    DataBase.get("name_anon:{}".format(user_id))
                    or msg.from_user.first_name
                ),
                None,
                anonymous_name_keys(user_id),
            )
        if re.match(r"^anon:send:@(\d+)$", input):
            DataBase.setex(
                "ready_to_enter_id:{}".format(user_id), 3600, "True"
            )
            DataBase.set(
                "pre_msgbot:{}".format(user_id), msg.message.message_id
            )
            await editText(
                chat_id,
                msg_id,
                0,
                langU["enter_id_for_send"],
                None,
                anonymous_back_keys(user_id),
            )
        if re.match(r"^anon:blo:(\d+):(\d+):(\d+):@(\d+)$", input):
            ap = re_matches(r"^anon:blo:(\d+):(\d+):(\d+):@(\d+)$", input)
            if DataBase.sismember("blocks:{}".format(user_id), ap[1]):
                DataBase.srem("blocks:{}".format(user_id), ap[1])
                text = langU["user_unblocked"]
            else:
                DataBase.sadd("blocks:{}".format(user_id), ap[1])
                text = langU["user_blocked"]
            input_ = _.reply_markup.inline_keyboard[1][0].callback_data
            SHOW_SENDER = False
            if input_ == "none:yes":
                SHOW_SENDER = ap[1]
            await answerCallbackQuery(msg, text, show_alert=True, cache_time=2)
            await bot.edit_message_reply_markup(
                chat_id,
                msg_id,
                reply_markup=anonymous_new_message_keys(
                    user_id, ap[1], ap[2], SHOW_SENDER, ap[3]
                ),
            )
        if re.match(r"^anon:rep:(\d+):(\d+):(\d+):@(\d+)$", input):
            ap = re_matches(r"^anon:rep:(\d+):(\d+):(\d+):@(\d+)$", input)
            await answerCallbackQuery(
                msg, langU["help_reply_anon"], show_alert=True, cache_time=3600
            )
        if re.match(r"^anon:stime:(\d+):(\d+):(\d+):@(\d+)$", input):
            ap = re_matches(r"^anon:stime:(\d+):(\d+):(\d+):@(\d+)$", input)
            ti_me = datetime.fromtimestamp(int(ap[3]))
            ti_me = ti_me.strftime("%Y-%m-%d %H:%M:%S")
            ti_me = re_matches(r"(\d+)-(\d+)-(\d+) (\d+):(\d+):(\d+)", ti_me)
            if user_steps[user_id]["lang"] == "fa":
                ti_me2 = gregorian_to_jalali(
                    int(ti_me[1]), int(ti_me[2]), int(ti_me[3])
                )
                sent_time = "{:04d}/{}/{:02d} - {:02d}:{:02d}:{:02d}".format(
                    ti_me2[0],
                    echoMonth(ti_me2[1], True),
                    ti_me2[2],
                    int(ti_me[4]),
                    int(ti_me[5]),
                    int(ti_me[6]),
                )
            else:
                sent_time = "{:04d}/{}/{:02d} - {:02d}:{:02d}:{:02d}".format(
                    int(ti_me[1]),
                    echoMonth(ti_me[2], False),
                    int(ti_me[3]),
                    int(ti_me[4]),
                    int(ti_me[5]),
                    int(ti_me[6]),
                )
            await answerCallbackQuery(
                msg, sent_time, show_alert=True, cache_time=180
            )
        if re.match(r"^anon:receive:@(\d+)$", input):
            ap = re_matches(r"^anon:receive:@(\d+)$", input)
            if DataBase.get("dont_receive_anon:{}".format(user_id)):
                DataBase.delete("dont_receive_anon:{}".format(user_id))
                text = langU["receive_anon_active"]
            else:
                DataBase.set("dont_receive_anon:{}".format(user_id), "True")
                text = langU["receive_anon_deactive"]
            await answerCallbackQuery(msg, text, show_alert=True, cache_time=2)
            await bot.edit_message_reply_markup(
                chat_id, msg_id, reply_markup=anonymous_keys(user_id)
            )
        if re.match(r"^anon:myblock:@(\d+)$", input):
            if DataBase.scard("blocks:{}".format(user_id)) > 0:
                await editText(
                    chat_id,
                    msg_id,
                    0,
                    langU["besure_del_all_blocks"],
                    None,
                    anonymous_delete_blocks_keys(user_id),
                )
            else:
                await answerCallbackQuery(
                    msg,
                    langU["blocks_empty_anon"],
                    show_alert=True,
                    cache_time=10,
                )
        if re.match(r"^anon:delblocks:@(\d+)$", input):
            DataBase.delete("blocks:{}".format(user_id))
            await answerCallbackQuery(
                msg, langU["blocks_clear_anon"], show_alert=True, cache_time=2
            )
            await editText(
                chat_id,
                msg_id,
                0,
                langU["anon"],
                None,
                anonymous_keys(user_id),
            )
        if re.match(r"^anon:sendmore:(\d+):@(\d+)$", input):
            ap = re_matches(r"^anon:sendmore:(\d+):@(\d+)$", input)
            hash = ":@{}".format(user_id)
            langU = lang[user_steps[user_id]["lang"]]
            buttuns = langU["buttuns"]
            inlineKeys = iMarkup()
            inlineKeys.add(
                iButtun(
                    buttuns["cancel"], callback_data="backstart{}".format(hash)
                )
            )
            DataBase.set("who_conneted:{}".format(user_id), ap[1])
            await _.edit_reply_markup()
            await sendText(
                chat_id,
                0,
                1,
                langU["user_connect_4send"].format(
                    DataBase.get("name_anon2:{}".format(ap[1]))
                ),
                "md",
                inlineKeys,
            )
        if re.match(r"^najva:@(\d+)$", input):
            await editText(
                chat_id,
                msg_id,
                0,
                langU["najva"].format(GlobalValues().botUser, GlobalValues().botName),
                "html",
                najva_keys(user_id),
            )
        if re.match(r"^najva:settings:@(\d+)$", input):
            await editText(
                chat_id,
                msg_id,
                0,
                langU["najva_settings"].format(GlobalValues().botName),
                "html",
                najva_settings_keys(user_id),
            )
        if re.match(r"^najva:settings:(.*):@(\d+)$", input):
            ap = re_matches(r"^najva:settings:(.*):@(\d+)$", input)
            if ap[1] == "recents":
                recent = DataBase.smembers("najva_recent:{}".format(user_id))
                recent2 = DataBase.smembers("najva_recent2:{}".format(user_id))
                if len(recent) > 0 or len(recent2) > 0:
                    text = langU["recent_list"].format(
                        len(recent) + len(recent2)
                    )
                    inlineKeys = iMarkup()
                    count = 0
                    for i in recent:
                        name_user = await userInfos(i, "name")
                        if "Deleted" in name_user:
                            DataBase.srem(f"najva_recent:{user_id}", i)
                            DataBase.srem(f"najva_recent2:{user_id}", i)
                        else:
                            count += 1
                            inlineKeys.add(
                                iButtun(
                                    f"{count}- {name_user}",
                                    callback_data=f"recent:{i}:@{user_id}",
                                ),
                            )
                            if count > 22:
                                break
                    for i in recent2:
                        name_user = await userInfos(i, "name")
                        if "Deleted" in name_user:
                            DataBase.srem(f"najva_recent:{user_id}", i)
                            DataBase.srem(f"najva_recent2:{user_id}", i)
                        else:
                            count += 1
                            inlineKeys.add(
                                iButtun(
                                    f"{count}- {name_user}",
                                    callback_data=f"recent:{i}:@{user_id}",
                                ),
                            )
                            if count > 22:
                                break
                    inlineKeys.add(
                        iButtun(
                            langU["buttuns"]["back_nset"],
                            callback_data=f"najva:settings:@{user_id}",
                        ),
                        iButtun(
                            langU["buttuns"]["delall"],
                            callback_data=f"recent:all:@{user_id}",
                        ),
                    )
                    await editText(chat_id, msg_id, 0, text, None, inlineKeys)
                else:
                    await answerCallbackQuery(
                        msg,
                        langU["recent_empty"],
                        show_alert=True,
                        cache_time=10,
                    )
            elif ap[1] == "blocks":
                blocks2 = DataBase.smembers("blocks2:{}".format(user_id))
                if len(blocks2) > 0:
                    text = langU["blocks2_list"].format(len(blocks2))
                    inlineKeys = iMarkup()
                    count = 0
                    for i in blocks2:
                        name_user = await userInfos(i, "name")
                        if "Deleted" in name_user:
                            DataBase.srem(f"blocks2:{user_id}", i)
                        else:
                            count += 1
                            inlineKeys.add(
                                iButtun(
                                    f"{count}- {name_user}",
                                    callback_data=f"blocks2:{i}:@{user_id}",
                                ),
                            )
                            if count > 22:
                                break
                    inlineKeys.add(
                        iButtun(
                            langU["buttuns"]["back_nset"],
                            callback_data=f"najva:settings:@{user_id}",
                        ),
                        iButtun(
                            langU["buttuns"]["delall"],
                            callback_data=f"blocks2:all:@{user_id}",
                        ),
                    )
                    await editText(chat_id, msg_id, 0, text, None, inlineKeys)
                else:
                    await answerCallbackQuery(
                        msg,
                        langU["blocks2_empty"],
                        show_alert=True,
                        cache_time=10,
                    )
            elif ap[1] == "delall":
                await answerCallbackQuery(
                    msg, langU["delall"], show_alert=True, cache_time=3600
                )
        if re.match(r"^blocks2:all:@(\d+)$", input):
            inlineKeys = iMarkup()
            inlineKeys.add(
                iButtun(
                    langU["buttuns"]["no"],
                    callback_data=f"najva:settings:blocks:@{user_id}",
                ),
                iButtun(
                    langU["buttuns"]["yes"],
                    callback_data=f"blocks2:all:y:@{user_id}",
                ),
            )
            await editText(
                chat_id, msg_id, 0, langU["sure_del_blocks2"], None, inlineKeys
            )
        if re.match(r"^blocks2:all:y:@(\d+)$", input):
            DataBase.delete(f"blocks2:{user_id}")
            await answerCallbackQuery(msg, langU["delall_y"], show_alert=True)
            await editText(
                chat_id,
                msg_id,
                0,
                langU["najva_settings"].format(GlobalValues().botName),
                "html",
                najva_settings_keys(user_id),
            )
        if re.match(r"^blocks2:(\d+):@(\d+)$", input):
            ap = re_matches(r"^blocks2:(\d+):@(\d+)$", input)
            inlineKeys = iMarkup()
            uname_user = await userInfos(int(ap[1]), info="username")
            name_user = await userInfos(int(ap[1]), info="name")
            if uname_user:
                call_url = "https://t.me/{}".format(uname_user)
            else:
                call_url = "https://t.me?openmessage?user_id={}".format(ap[1])
            inlineKeys.add(
                iButtun(name_user, call_url),
            )
            inlineKeys.add(
                iButtun(
                    langU["buttuns"]["no"],
                    callback_data=f"najva:settings:blocks:@{user_id}",
                ),
                iButtun(
                    langU["buttuns"]["yes"],
                    callback_data=f"blocks2:{ap[1]}:y:@{user_id}",
                ),
            )
            await editText(
                chat_id,
                msg_id,
                0,
                langU["blocks2_info"].format(ap[1]),
                "md",
                inlineKeys,
            )
        if re.match(r"^blocks2:(\d+):y:@(\d+)$", input):
            ap = re_matches(r"^blocks2:(\d+):y:@(\d+)$", input)
            DataBase.srem(f"blocks2:{user_id}", ap[1])
            await answerCallbackQuery(
                msg, langU["blocks2_user_del"], show_alert=True
            )
            await editText(
                chat_id,
                msg_id,
                0,
                langU["najva_settings"].format(GlobalValues().botName),
                "html",
                najva_settings_keys(user_id),
            )
        if re.match(r"^recent:all:@(\d+)$", input):
            inlineKeys = iMarkup()
            inlineKeys.add(
                iButtun(
                    langU["buttuns"]["no"],
                    callback_data=f"najva:settings:recents:@{user_id}",
                ),
                iButtun(
                    langU["buttuns"]["yes"],
                    callback_data=f"recent:all:y:@{user_id}",
                ),
            )
            await editText(
                chat_id, msg_id, 0, langU["sure_del_recent"], None, inlineKeys
            )
        if re.match(r"^recent:all:y:@(\d+)$", input):
            DataBase.delete(f"najva_recent:{user_id}")
            DataBase.delete(f"najva_recent2:{user_id}")
            await answerCallbackQuery(
                msg, langU["delall_recent"], show_alert=True
            )
            await editText(
                chat_id,
                msg_id,
                0,
                langU["najva_settings"].format(GlobalValues().botName),
                "html",
                najva_settings_keys(user_id),
            )
        if re.match(r"^recent:(\d+):@(\d+)$", input):
            ap = re_matches(r"^recent:(\d+):@(\d+)$", input)
            inlineKeys = iMarkup()
            uname_user = await userInfos(int(ap[1]), info="username")
            name_user = await userInfos(int(ap[1]), info="name")
            if uname_user:
                call_url = "https://t.me/{}".format(uname_user)
            else:
                call_url = "https://t.me?openmessage?user_id={}".format(ap[1])
            inlineKeys.add(
                iButtun(name_user, call_url),
            )
            inlineKeys.add(
                iButtun(
                    langU["buttuns"]["block"],
                    callback_data=f"recent:{ap[1]}:b:@{user_id}",
                ),
            )
            inlineKeys.add(
                iButtun(
                    langU["buttuns"]["delete"],
                    callback_data=f"recent:{ap[1]}:y:@{user_id}",
                ),
            )
            inlineKeys.add(
                iButtun(
                    langU["buttuns"]["back_nrec"],
                    callback_data=f"najva:settings:recents:@{user_id}",
                ),
            )
            await editText(
                chat_id,
                msg_id,
                0,
                langU["recent_info"].format(ap[1]),
                "md",
                inlineKeys,
            )
        if re.match(r"^recent:(\d+):y:@(\d+)$", input):
            ap = re_matches(r"^recent:(\d+):y:@(\d+)$", input)
            DataBase.srem(f"najva_recent:{user_id}", ap[1])
            DataBase.srem(f"najva_recent2:{user_id}", ap[1])
            await answerCallbackQuery(
                msg, langU["recent_user_del"], show_alert=True
            )
            await editText(
                chat_id,
                msg_id,
                0,
                langU["najva_settings"].format(GlobalValues().botName),
                "html",
                najva_settings_keys(user_id),
            )
        if re.match(r"^recent:(\d+):b:@(\d+)$", input):
            ap = re_matches(r"^recent:(\d+):b:@(\d+)$", input)
            await answerCallbackQuery(
                msg, langU["block_recent"], show_alert=True, cache_time=3600
            )
        if re.match(r"^najva:help:@(\d+)$", input):
            try:
                await _.delete()
            except:
                pass
            await sendText(
                chat_id,
                _.reply_to_message,
                1,
                langU["najva_help"],
                "html",
                najva_help_keys(user_id),
            )
        if re.match(r"^najva:settings1:(.*):@(\d+)$", input):
            ap = re_matches(r"^najva:settings1:(.*):@(\d+)$", input)
            if ap[1] == "autodel":
                if DataBase.hget(
                    "setting_najva:{}".format(user_id), "autodel"
                ):
                    await editText(
                        chat_id,
                        msg_id,
                        0,
                        langU["autodel"],
                        None,
                        najva_autodel2_keys(user_id),
                    )
                else:
                    await editText(
                        chat_id,
                        msg_id,
                        0,
                        langU["autodel"],
                        None,
                        najva_autodel_keys(user_id),
                    )
            else:
                if DataBase.hget("setting_najva:{}".format(user_id), ap[1]):
                    DataBase.hdel("setting_najva:{}".format(user_id), ap[1])
                    text = langU["najva_setoff_{}".format(ap[1])]
                else:
                    DataBase.hset("setting_najva:{}".format(user_id), ap[1], 1)
                    text = langU["najva_seton_{}".format(ap[1])]
                await answerCallbackQuery(
                    msg, text, show_alert=True, cache_time=2
                )
                await bot.edit_message_reply_markup(
                    chat_id, msg_id, reply_markup=najva_settings_keys(user_id)
                )
        if re.match(r"^najva:autodel:@(\d+)$", input):
            ap = re_matches(r"^najva:autodel:@(\d+)$", input)
            if DataBase.hget("setting_najva:{}".format(user_id), "autodel"):
                DataBase.hdel("setting_najva:{}".format(user_id), "autodel")
                text = langU["najva_setoff_autodel"]
                await answerCallbackQuery(msg, text, cache_time=2)
                await bot.edit_message_reply_markup(
                    chat_id, msg_id, reply_markup=najva_autodel_keys(user_id)
                )
            else:
                if not DataBase.get("autodel_time:{}".format(user_id)):
                    DataBase.set("autodel_time:{}".format(user_id), 10)
                text = langU["najva_seton_autodel"]
                DataBase.hset("setting_najva:{}".format(user_id), "autodel", 1)
                await answerCallbackQuery(msg, text, cache_time=2)
                await bot.edit_message_reply_markup(
                    chat_id, msg_id, reply_markup=najva_autodel2_keys(user_id)
                )
        if re.match(r"^najva:help:(.*):@(\d+)$", input):
            ap = re_matches(r"^najva:help:(.*):@(\d+)$", input)
            try:
                await _.delete()
            except:
                pass
            if ap[1] == "send":
                file = "Files/helps/help_media.jpg"
                with open(file, "rb") as file:
                    await sendPhoto(
                        chat_id,
                        file,
                        langU["najva_help_send"].format(GlobalValues().botUser),
                        "html",
                        _.reply_to_message,
                        reply_markup=najva_help1_keys(user_id),
                    )
            elif ap[1] == "media":
                file = "Files/helps/help_media.jpg"
                with open(file, "rb") as file:
                    await sendPhoto(
                        chat_id,
                        file,
                        langU["najva_help_media"].format(GlobalValues().botUser),
                        "html",
                        _.reply_to_message,
                        reply_markup=najva_help2_keys(user_id),
                    )
            elif ap[1] == "group":
                file = "Files/helps/help_group.jpg"
                with open(file, "rb") as file:
                    await sendPhoto(
                        chat_id,
                        file,
                        langU["najva_help_group"].format(GlobalValues().botUser),
                        "html",
                        _.reply_to_message,
                        reply_markup=najva_help3_keys(user_id),
                    )
            elif ap[1] == "bd":
                file = "Files/helps/help_bd.jpg"
                with open(file, "rb") as file:
                    await sendPhoto(
                        chat_id,
                        file,
                        langU["najva_help_bd"].format(GlobalValues().botUser),
                        "html",
                        _.reply_to_message,
                        reply_markup=najva_help4_keys(user_id),
                    )
            elif ap[1] == "noid":
                file = "Files/helps/help_noid.mp4"
                with open(file, "rb") as file:
                    await sendVideo(
                        chat_id,
                        _.reply_to_message,
                        file,
                        langU["najva_help_noid"].format(GlobalValues().botUser),
                        "html",
                        supports_streaming=True,
                        reply_markup=najva_help5_keys(user_id),
                    )
            elif ap[1] == "shset":
                file = "Files/helps/help_shset.jpg"
                with open(file, "rb") as file:
                    await sendPhoto(
                        chat_id,
                        file,
                        langU["najva_help_shset"].format(GlobalValues().botUser),
                        "html",
                        _.reply_to_message,
                        reply_markup=najva_help6_keys(user_id),
                    )
            elif ap[1] == "prob":
                file = "Files/helps/help_prob.mp4"
                with open(file, "rb") as file:
                    await sendVideo(
                        chat_id,
                        _.reply_to_message,
                        file,
                        langU["najva_help_prob"].format(GlobalValues().botUser),
                        "html",
                        supports_streaming=True,
                        reply_markup=najva_help7_keys(user_id),
                    )
            elif ap[1] == "examp":
                await sendText(
                    chat_id,
                    _.reply_to_message,
                    1,
                    langU["najva_help_examp"],
                    "html",
                    najva_help8_keys(user_id),
                )
        if re.match(r"^najva:vid:(\d+):@(\d+)$", input):
            ap = re_matches(r"^najva:vid:(\d+):@(\d+)$", input)
            try:
                await _.delete()
            except:
                pass
            keyboard = najva_help7_keys(user_id)
            if ap[1] == "5":
                keyboard = najva_help9_keys(user_id)
            elif ap[1] == "6":
                keyboard = najva_help5_keys(user_id)
            file = f"Files/helps/vid-{ap[1]}.mp4"
            with open(file, "rb") as file:
                await sendVideo(
                    chat_id,
                    _.reply_to_message,
                    file,
                    langU[f"najva_vid-{ap[1]}"].format(GlobalValues().botUser),
                    "html",
                    supports_streaming=True,
                    reply_markup=keyboard,
                )
        if re.match(r"^autodel:(.*):@(\d+)$", input):
            ap = re_matches(r"^autodel:(.*):@(\d+)$", input)
            old_autodel_time = DataBase.get("autodel_time:{}".format(user_id))
            if int(old_autodel_time) + int(ap[1]) > 0:
                DataBase.set(
                    "autodel_time:{}".format(user_id),
                    int(old_autodel_time) + int(ap[1]),
                )
                await bot.edit_message_reply_markup(
                    chat_id, msg_id, reply_markup=najva_autodel2_keys(user_id)
                )
            else:
                await answerCallbackQuery(
                    msg, langU["autodel_must_1"], cache_time=2
                )
        if re.match(r"^special:cancel:@(\d+)", input):
            time_data = DataBase.hget(
                "najva_special:{}".format(user_id), "time"
            )
            special_msgID = DataBase.hget(
                "najva_special:{}".format(user_id), "id"
            )
            DataBase.delete("najva:{}:{}".format(user_id, time_data))
            DataBase.delete("najva_special:{}".format(user_id))
            DataBase.delete("ready_to_recv_special:{}".format(user_id))
            DataBase.srem(
                "najva_autodel", f"{user_id}:{time_data}:{special_msgID}"
            )
            await editText(
                inline_msg_id=special_msgID, text=langU["special_najva_cancel"]
            )
            try:
                await _.delete()
            except:
                pass
            await answerCallbackQuery(msg, langU["canceled"], cache_time=3600)
        if re.match(r"^special:antisave:@(\d+)", input):
            await answerCallbackQuery(
                msg, langU["anti_save"], show_alert=True, cache_time=3600
            )
        if re.match(r"^special:reg1:@(\d+)", input):
            try:
                msg_ = await reply_msg.forward(GlobalValues().supchat)
                find_ID, find_type, can_hide = find_media_id(msg_)
                time_data = DataBase.hget(
                    "najva_special:{}".format(user_id), "time"
                )
                special_msgID = DataBase.hget(
                    "najva_special:{}".format(user_id), "id"
                )
                DataBase.delete("ready_to_recv_special:{}".format(user_id))
                DataBase.hset(
                    "najva:{}:{}".format(user_id, time_data),
                    "file_id",
                    find_ID,
                )
                DataBase.hset(
                    "najva:{}:{}".format(user_id, time_data),
                    "file_type",
                    find_type,
                )
                DataBase.hset(
                    "najva:{}:{}".format(user_id, time_data),
                    "source_id",
                    reply_id,
                )
                DataBase.hset(
                    "najva:{}:{}".format(user_id, time_data),
                    "msg_id",
                    msg_.message_id,
                )
                if DataBase.hget(f"setting_najva:{user_id}", "autodel"):
                    DataBase.sadd(
                        "najva_autodel",
                        f"{user_id}:{time_data}:{special_msgID}",
                    )
                inlineKeys = iMarkup()
                inlineKeys.add(
                    iButtun(
                        langU["buttuns"]["show_najva"],
                        callback_data="shown:{}:{}".format(user_id, time_data),
                    )
                )
                users_data = DataBase.hget(
                    "najva:{}:{}".format(user_id, time_data), "users"
                )
                if "@" in users_data:
                    name_user = await userIds(users_data)
                else:
                    name_user = users_data
                name_user2 = None
                if DataBase.hget(f"setting_najva:{name_user}", "noname"):
                    name_user2 = langU["no_name"]
                name_user = await userInfos(name_user, info="name")
                await editText(
                    inline_msg_id=special_msgID,
                    text=langU["special_najva_registered"].format(
                        name_user2 or name_user
                    ),
                    parse_mode="html",
                    reply_markup=inlineKeys,
                )
                await editText(chat_id, msg_id, 0, langU["reg_najva"])
            except Exception as e:
                await editText(chat_id, msg_id, 0, langU["error_reg_najva"])
        if re.match(r"^special:reg2:@(\d+)", input):
            try:
                find_ID, find_type, can_hide = find_media_id(reply_msg)
                if not can_hide:
                    return await answerCallbackQuery(
                        msg,
                        langU["cant_hide"],
                        show_alert=True,
                        cache_time=3600,
                    )
                msg_ = await reply_msg.forward(GlobalValues().supchat)
                find_ID, find_type, can_hide = find_media_id(msg_)
                time_data = DataBase.hget(
                    "najva_special:{}".format(user_id), "time"
                )
                special_msgID = DataBase.hget(
                    "najva_special:{}".format(user_id), "id"
                )
                DataBase.delete("ready_to_recv_special:{}".format(user_id))
                DataBase.hset(
                    "najva:{}:{}".format(user_id, time_data),
                    "file_id",
                    find_ID,
                )
                DataBase.hset(
                    "najva:{}:{}".format(user_id, time_data),
                    "file_type",
                    find_type,
                )
                DataBase.hset(
                    "najva:{}:{}".format(user_id, time_data),
                    "source_id",
                    reply_id,
                )
                DataBase.hset(
                    "najva:{}:{}".format(user_id, time_data),
                    "msg_id",
                    msg_.message_id,
                )
                if DataBase.hget(f"setting_najva:{user_id}", "autodel"):
                    DataBase.sadd(
                        "najva_autodel",
                        f"{user_id}:{time_data}:{special_msgID}",
                    )
                inlineKeys = iMarkup()
                inlineKeys.add(
                    iButtun(
                        langU["buttuns"]["show_najva"],
                        switch_inline_query_current_chat="sp{}.{}".format(
                            user_id, time_data
                        ),
                    )
                )
                users_data = DataBase.hget(
                    "najva:{}:{}".format(user_id, time_data), "users"
                )
                if "@" in users_data:
                    name_user = await userIds(users_data)
                else:
                    name_user = users_data
                name_user2 = None
                if DataBase.hget(f"setting_najva:{name_user}", "noname"):
                    name_user2 = langU["no_name"]
                name_user = await userInfos(name_user, info="name")
                await editText(
                    inline_msg_id=special_msgID,
                    text=langU["special_najva_registered"].format(
                        name_user2 or name_user
                    ),
                    parse_mode="html",
                    reply_markup=inlineKeys,
                )
                await editText(chat_id, msg_id, 0, langU["reg2_najva"])
            except Exception as e:
                await editText(chat_id, msg_id, 0, langU["error_reg_najva"])
        if re.match(r"^special:sendpv:@(\d+)", input):
            try:
                msg_ = await reply_msg.forward(GlobalValues().supchat)
                find_ID, find_type, can_hide = find_media_id(msg_)
                time_data = DataBase.hget(
                    "najva_special:{}".format(user_id), "time"
                )
                special_msgID = DataBase.hget(
                    "najva_special:{}".format(user_id), "id"
                )
                DataBase.hset(
                    "najva:{}:{}".format(user_id, time_data),
                    "file_id",
                    find_ID,
                )
                DataBase.hset(
                    "najva:{}:{}".format(user_id, time_data),
                    "file_type",
                    find_type,
                )
                DataBase.hset(
                    "najva:{}:{}".format(user_id, time_data),
                    "source_id",
                    reply_id,
                )
                DataBase.hset(
                    "najva:{}:{}".format(user_id, time_data),
                    "msg_id",
                    msg_.message_id,
                )
                if DataBase.hget(f"setting_najva:{user_id}", "autodel"):
                    DataBase.sadd(
                        "najva_autodel",
                        f"{user_id}:{time_data}:{special_msgID}",
                    )
                inlineKeys = iMarkup()
                inlineKeys.add(
                    iButtun(
                        langU["buttuns"]["show_najva"],
                        callback_data="showpv:{}:{}".format(
                            user_id, time_data
                        ),
                    )
                )
                users_data = DataBase.hget(
                    "najva:{}:{}".format(user_id, time_data), "users"
                )
                if "@" in users_data:
                    id_user = await userIds(users_data)
                else:
                    id_user = users_data
                if not id_user:
                    return await answerCallbackQuery(
                        msg,
                        langU["cant_sent_najva_pv"],
                        show_alert=True,
                        cache_time=3600,
                    )
                DataBase.delete("ready_to_recv_special:{}".format(user_id))
                name_user2 = None
                if DataBase.hget(f"setting_najva:{id_user}", "noname"):
                    name_user2 = langU["no_name"]
                name_user = await userInfos(id_user, info="name")
                await editText(
                    inline_msg_id=special_msgID,
                    text=langU["special_najva_registered"].format(
                        name_user2 or name_user
                    ),
                    parse_mode="html",
                )
                await sendText(
                    id_user,
                    0,
                    1,
                    langU["receive_new_najva_pv"].format(
                        msg.from_user.first_name
                    ),
                    "html",
                    inlineKeys,
                )
                await editText(
                    chat_id,
                    msg_id,
                    0,
                    langU["sent_najva_pv"].format(
                        '<a href="tg://user?id={}">{}</a>'.format(
                            id_user, name_user
                        )
                    ),
                    "html",
                )
            except Exception as e:
                await editText(chat_id, msg_id, 0, langU["error_reg_najva"])
        if re.match(r"^showpv:(\d+):([-+]?\d*\.\d+|\d+)$", input):
            ap = re_matches(r"^showpv:(\d+):([-+]?\d*\.\d+|\d+)$", input)
            try:
                await _.delete()
            except:
                pass
            from_user = ap[1]
            time_data = ap[2]
            DataBase.set(
                "najva_seen_time:{}:{}".format(from_user, time_data),
                int(time()),
            )
            DataBase.incr(
                "najva_seen_count:{}:{}".format(from_user, time_data)
            )
            DataBase.sadd(
                "najva_seened:{}:{}".format(from_user, time_data), user_id
            )
            special_msgID = DataBase.hget(
                "najva_special:{}".format(from_user), "id"
            )
            users_data = DataBase.hget(
                "najva:{}:{}".format(from_user, time_data), "users"
            )
            file_id = DataBase.hget(
                "najva:{}:{}".format(from_user, time_data), "file_id"
            )
            file_type = DataBase.hget(
                "najva:{}:{}".format(from_user, time_data), "file_type"
            )
            source_id = DataBase.hget(
                "najva:{}:{}".format(from_user, time_data), "source_id"
            )
            msgid = DataBase.hget(
                "najva:{}:{}".format(from_user, time_data), "msg_id"
            )
            inlineKeys = await show_speical_najva_keys(user_id, from_user)
            msg_ = await copyMessage(
                chat_id,
                GlobalValues().supchat,
                msgid,
                protect_content=False,
                reply_markup=inlineKeys,
            )
            if DataBase.hget(f"setting_najva:{from_user}", "seen"):
                await sendText(
                    from_user,
                    source_id,
                    1,
                    langU["speical_najva_seen"].format(
                        msg.from_user.first_name
                    ),
                )
            await editText(
                inline_msg_id=special_msgID,
                text=langU["speical_najva_seen2"].format(
                    msg.from_user.first_name
                ),
                parse_mode="html",
                reply_markup=najva_seen3_keys(from_user, time_data),
            )
            if DataBase.hget(f"setting_najva:{from_user}", "dispo"):
                special_msgID = DataBase.hget(
                    "najva_special:{}".format(from_user), "id"
                )
                DataBase.srem(
                    "najva_autodel", f"{from_user}:{time_data}:{special_msgID}"
                )
                DataBase.delete("najva:{}:{}".format(from_user, time_data))
                DataBase.delete("najva_special:{}".format(from_user))
            DataBase.hset(
                "najva:{}:{}".format(from_user, time_data),
                "seen_id",
                f"{chat_id}:{msg_[1].message_id}",
            )
        if re.match(r"^special:block:(\d+):@(\d+)$", input):
            ap = re_matches(r"^special:block:(\d+):@(\d+)$", input)
            if DataBase.sismember("blocks2:{}".format(user_id), ap[1]):
                DataBase.srem("blocks2:{}".format(user_id), ap[1])
                text = langU["user_unblocked"]
            else:
                DataBase.sadd("blocks2:{}".format(user_id), ap[1])
                text = langU["user_blocked"]
            await answerCallbackQuery(msg, text, show_alert=True, cache_time=2)
            inlineKeys = await show_speical_najva_keys(user_id, ap[1])
            await bot.edit_message_reply_markup(
                chat_id, msg_id, reply_markup=inlineKeys
            )
        if re.match(r"^special:report:(\d+):@(\d+)$", input):
            ap = re_matches(r"^special:report:(\d+):@(\d+)$", input)
            await sendText(
                chat_id,
                _,
                1,
                langU["report_special_najva"],
                "html",
                report_najva_keys(user_id, ap[1], msg_id),
            )
        if re.match(r"^report:cancel:(\d+)@(\d+)$", input):
            ap = re_matches(r"^report:cancel:(\d+)@(\d+)$", input)
            try:
                await _.delete()
            except:
                pass
            await answerCallbackQuery(msg, langU["canceled"], cache_time=3600)
        if re.match(r"^special:report2:(\d+):(\d+):@(\d+)$", input):
            ap = re_matches(r"^special:report2:(\d+):(\d+):@(\d+)$", input)
            from_user = ap[1]
            msg_ID = ap[2]
            msg_ = await copyMessage(
                GlobalValues().sudoID, chat_id, msg_ID, protect_content=False
            )
            name_user = await userInfos(from_user, info="name")
            text = langU["reported_this_user"].format(
                msg.from_user.first_name, name_user
            )
            await sendText(
                GlobalValues().sudoID,
                msg_[1].message_id,
                1,
                text,
                "html",
                ban_user_keys(from_user, GlobalValues().sudoID),
            )
            await editText(chat_id, msg_id, 0, langU["reported_special_najva"])
            await _.reply_to_message.delete()
        if re.match(r"^banuser:(\d+)$", input):
            ap = re_matches(r"^banuser:(\d+)$", input)
            if DataBase.sismember("isBanned", ap[1]):
                DataBase.srem("isBanned", ap[1])
                text = langU["user_unbanned"]
            else:
                DataBase.sadd("isBanned", ap[1])
                text = langU["user_banned"]
            await answerCallbackQuery(msg, text, show_alert=True, cache_time=2)
            inlineKeys = ban_user_keys(ap[1], chat_id)
            await bot.edit_message_reply_markup(
                chat_id, msg_id, reply_markup=inlineKeys
            )
    else:
        # {
        # "id": "601066437221691493",
        # "from": {
        # "id": 139946685, "is_bot": false, "first_name": "Alireza 🏴🏳",
        # "username": "ferisystem", "language_code": "de"},
        # "inline_message_id": "BAAAACcAAABRsQ-ZJkZtztRsZ9I", "chat_instance": "8145064389776335333", "data": "showN:139946685:1666127436.399383"
        # }
        msgID = msg.id
        msg_id = msg.inline_message_id
        if re.match(r"^shown:(\d+):([-+]?\d*\.\d+|\d+)$", input):
            ap = re_matches(r"^shown:(\d+):([-+]?\d*\.\d+|\d+)$", input)
            from_user = ap[1]
            time_data = ap[2]
            text_data = DataBase.hget(
                "najva:{}:{}".format(from_user, time_data), "text"
            )
            users_data = DataBase.hget(
                "najva:{}:{}".format(from_user, time_data), "users"
            )
            is_allow = (username != "" and username in users_data) or str(
                user_id
            ) in users_data
            if is_allow or str(user_id) in from_user or users_data == "all":
                file_id = DataBase.hget(
                    "najva:{}:{}".format(user_id, time_data), "file_id"
                )
                if file_id:
                    return await answerCallbackQuery(
                        msg,
                        url_web="t.me/{}?start={}_{}".format(
                            GlobalValues().botUser,
                            from_user,
                            time_data.replace(".", "_"),
                        ),
                    )
                await answerCallbackQuery(
                    msg, text_data, show_alert=True, cache_time=3600
                )
                # if not str(user_id) in from_user and DataBase.scard('najva_seened:{}:{}'.format(from_user, time_data)) == 0
                if (
                    DataBase.scard(
                        "najva_seened:{}:{}".format(from_user, time_data)
                    )
                    == 0
                    and is_allow
                ):
                    if (
                        DataBase.hget(f"setting_najva:{from_user}", "seen")
                        and users_data != "all"
                    ):
                        await sendText(
                            from_user,
                            0,
                            1,
                            langU["najva_seened"].format(
                                msg.from_user.first_name
                            ),
                        )
                    if users_data != "all":
                        if len(users_data) == 1:
                            await bot.edit_message_reply_markup(
                                inline_message_id=msg_id,
                                reply_markup=najva_seen_keys(
                                    user_id, from_user, time_data
                                ),
                            )
                        else:
                            await editText(
                                inline_msg_id=msg_id,
                                text=langU["najva_seened"].format(
                                    '<a href="tg://user?id={}">{}</a>'.format(
                                        user_id, msg.from_user.first_name
                                    )
                                ),
                                parse_mode="html",
                                reply_markup=najva_seen_keys(
                                    user_id, from_user, time_data
                                ),
                            )
                        DataBase.sadd(
                            "najva_seened:{}:{}".format(from_user, time_data),
                            user_id,
                        )
                    if str(users_data).isdigit() and not DataBase.get(
                        "najva_seen_time:{}:{}".format(from_user, time_data)
                    ):
                        DataBase.set(
                            "najva_seen_time:{}:{}".format(
                                from_user, time_data
                            ),
                            int(time()),
                        )
                # if not str(user_id) in from_user:
                DataBase.incr(
                    "najva_seen_count:{}:{}".format(from_user, time_data)
                )
            else:
                DataBase.sadd(
                    "najva_nosy:{}:{}".format(from_user, time_data), user_id
                )
                await answerCallbackQuery(
                    msg,
                    langU["najva_not_for_you"],
                    show_alert=True,
                    cache_time=3600,
                )
        if re.match(r"^delnajva:(\d+):([-+]?\d*\.\d+|\d+)$", input):
            ap = re_matches(r"^delnajva:(\d+):([-+]?\d*\.\d+|\d+)$", input)
            if user_id == int(ap[1]):
                seen_id = DataBase.hget(
                    "najva:{}:{}".format(ap[1], ap[2]), "seen_id"
                )
                if seen_id:
                    seen_id = seen_id.split(":")
                    await bot.delete_message(seen_id[0], seen_id)
                special_msgID = DataBase.hget(
                    "najva_special:{}".format(ap[1]), "id"
                )
                DataBase.srem(
                    "najva_autodel", f"{ap[1]}:{ap[2]}:{special_msgID}"
                )
                DataBase.delete("najva:{}:{}".format(ap[1], ap[2]))
                DataBase.delete("najva_special:{}".format(ap[1]))
                await answerCallbackQuery(msg, langU["najva_deleted"])
                await bot.edit_message_reply_markup(
                    inline_message_id=msg_id,
                    reply_markup=najva_seen2_keys(user_id, ap[1], ap[2]),
                )
            else:
                await answerCallbackQuery(
                    msg, langU["must_be_owner_najva"], cache_time=3600
                )
        if re.match(r"^shows:(\d+):([-+]?\d*\.\d+|\d+)$", input):
            ap = re_matches(r"^shows:(\d+):([-+]?\d*\.\d+|\d+)$", input)
            from_user, time_data = ap[1], ap[2]
            if user_id != int(from_user):
                await answerCallbackQuery(
                    msg,
                    langU["must_be_owner_najva"],
                    show_alert=True,
                    cache_time=3600,
                )
                return False
            seen_time = DataBase.get(
                "najva_seen_time:{}:{}".format(from_user, time_data)
            )
            seen_count = DataBase.get(
                "najva_seen_count:{}:{}".format(from_user, time_data)
            )
            seened_users = DataBase.smembers(
                "najva_seened:{}:{}".format(from_user, time_data)
            )
            nosy_users = DataBase.smembers(
                "najva_nosy:{}:{}".format(from_user, time_data)
            )
            if len(nosy_users) > 0:
                nosy_users_text = ""
                for i in nosy_users:
                    name_user = await userInfos(i, info="name")
                    nosy_users_text = "{}\n{}".format(
                        name_user, nosy_users_text
                    )
            else:
                nosy_users_text = langU["nobody_nosy"]
            if not seen_count:
                await answerCallbackQuery(
                    msg, langU["no_one_seen"], show_alert=True, cache_time=3
                )
            else:
                if seen_time:
                    ti_me = datetime.fromtimestamp(int(seen_time))
                    ti_me = ti_me.strftime("%Y-%m-%d %H:%M:%S")
                    ti_me = re_matches(
                        r"(\d+)-(\d+)-(\d+) (\d+):(\d+):(\d+)", ti_me
                    )
                    if user_steps[user_id]["lang"] == "fa":
                        ti_me2 = gregorian_to_jalali(
                            int(ti_me[1]), int(ti_me[2]), int(ti_me[3])
                        )
                        seen_time = (
                            "{:04d}/{}/{:02d} - {:02d}:{:02d}:{:02d}".format(
                                ti_me2[0],
                                echoMonth(ti_me2[1], True),
                                ti_me2[2],
                                int(ti_me[4]),
                                int(ti_me[5]),
                                int(ti_me[6]),
                            )
                        )
                    else:
                        seen_time = (
                            "{:04d}/{}/{:02d} - {:02d}:{:02d}:{:02d}".format(
                                int(ti_me[1]),
                                echoMonth(ti_me[2], False),
                                int(ti_me[3]),
                                int(ti_me[4]),
                                int(ti_me[5]),
                                int(ti_me[6]),
                            )
                        )
                    name_user = list(
                        DataBase.smembers(
                            "najva_seened:{}:{}".format(from_user, time_data)
                        )
                    )[0]
                    name_user = await userInfos(name_user, info="name")
                    await answerCallbackQuery(
                        msg,
                        langU["seen_najva_person"].format(
                            seen_time,
                            seen_count,
                            name_user,
                            langU["nosies"].format(nosy_users_text),
                        ),
                        show_alert=True,
                        cache_time=3,
                    )
                else:
                    if len(seened_users) > 0:
                        seened_users_text = ""
                        for i in seened_users:
                            name_user = await userInfos(i, info="name")
                            seened_users_text = "{}\n{}".format(
                                name_user, seened_users_text
                            )
                        await answerCallbackQuery(
                            msg,
                            langU["seen_najva_group"].format(
                                seen_count,
                                len(seened_users),
                                seened_users_text,
                                langU["nosies"].format(nosy_users_text),
                            ),
                            show_alert=True,
                            cache_time=3,
                        )
                    else:
                        await answerCallbackQuery(
                            msg,
                            langU["seen_najva_all"].format(seen_count),
                            show_alert=True,
                            cache_time=3,
                        )


async def inline_query_process(msg: types.InlineQuery):
    # {
    # "id": "601066437965102448",
    # "from": {
    # "id": 139946685, "is_bot": false, "first_name": "Alireza 🏴🏳",
    # "username": "ferisystem", "language_code": "de"},
    # "chat_type": "sender/private/group/supergroup/channel",
    # "query": "text", "offset": ""
    # }
    msg_id = msg.id
    user_id = msg.from_user.id
    if msg.from_user.username:
        username = f"@{msg.from_user.username}"
    else:
        username = user_id
    user_name = msg.from_user.first_name
    chat_type = msg.chat_type
    input = msg.query
    saveUsername(msg, mode="inline")
    setupUserSteps(msg, user_id)
    langU = lang[user_steps[user_id]["lang"]]
    buttuns = langU["buttuns"]
    print(colored("Inline >", "cyan"))
    print(colored("userID", "yellow"), colored(user_id, "white"))
    print(colored("Query", "yellow"), colored(input, "white"))
    print(colored("inlineID", "yellow"), colored(msg_id, "white"))
    print()
    if input == "":
        input_content = InputTextMessageContent(
            message_text=langU["inline"]["text"]["help_send"]
        )
        inlineKeys = iMarkup()
        inlineKeys.add(
            iButtun(
                buttuns["help_comp"],
                url="t.me/{}?start=help".format(GlobalValues().botUser),
            )
        )
        item1 = InlineQueryResultArticle(
            id=f"help:{user_id}",
            title=langU["inline"]["title"]["help_send"],
            description=langU["inline"]["desc"]["help_send"],
            thumb_url=pic_question,
            thumb_width=512,
            thumb_height=512,
            input_message_content=input_content,
            reply_markup=inlineKeys,
        )
        input_content = InputTextMessageContent(
            message_text=langU["inline"]["text"]["my_id"].format(user_id)
        )
        inlineKeys = iMarkup()
        inlineKeys.add(
            iButtun(
                buttuns["najva_to"].format(user_name),
                switch_inline_query_current_chat="{} {}".format(
                    username, buttuns["example"]
                ),
            )
        )
        item2 = InlineQueryResultArticle(
            id=f"myid:{user_id}",
            title=langU["inline"]["title"]["my_id"],
            description=langU["inline"]["desc"]["my_id"].format(user_id),
            thumb_url=pic_atsign,
            thumb_width=512,
            thumb_height=512,
            input_message_content=input_content,
            reply_markup=inlineKeys,
        )
        await answerInlineQuery(msg_id, results=[item1, item2], cache_time=1)
    if not re.findall(r"@all ", input.lower()) and (
        re.search(r"(?:(?<!\d)\d{6,10}(?!\d)) (.*)$", input)
        or re.search(r"(@[a-zA-Z0-9_]*) (.*)$", input)
    ):
        ap = re.findall(r"(@[a-zA-Z0-9_]*)", input)
        ap2 = re.findall(r"(?:(?<!\d)\d{6,10}(?!\d))", input)
        text = input
        users = set()
        for i in ap:
            text = text.replace(f"{i} ", "").replace(f"{i}", "")
            users.add(i)
        for i in ap2:
            text = text.replace(f"{i} ", "").replace(f"{i}", "")
            users.add(i)
        users = list(users)
        ti_me = time()
        inlineKeys = iMarkup()
        inlineKeys.add(
            iButtun(
                buttuns["show_najva"],
                callback_data="showN:{}:{}".format(user_id, ti_me),
            )
        )
        ads = DataBase.get("have_ads")
        if ads:
            inlineKeys.add(
                iButtun(
                    DataBase.hget("info_ads", "buttuns"),
                    url=DataBase.hget("info_ads", "url"),
                )
            )
        if text == "":
            input_content = InputTextMessageContent(
                message_text=langU["inline"]["text"]["najva_havn_text"],
                parse_mode="HTML",
                disable_web_page_preview=True,
            )
            item1 = InlineQueryResultArticle(
                id="null",
                title=langU["inline"]["title"]["najva_havn_text"],
                description=langU["inline"]["desc"]["najva_havn_text"],
                thumb_url=pic_cross,
                thumb_width=512,
                thumb_height=512,
                input_message_content=input_content,
            )
            return await answerInlineQuery(
                msg_id,
                results=[
                    item1,
                ],
                cache_time=1,
            )
        if len(users) > 1:
            name_users = ""
            count = 0
            for i in users:
                if "@" in i:
                    k = await userIds(i)
                    if k:
                        users[count] = k
                count += 1
            for i in users:
                name_user = await userInfos(i, info="name")
                if str(i).isdigit():
                    name_users = '<a href="tg://user?id={}">{}</a>\n{}'.format(
                        i, name_user, name_users
                    )
                else:
                    name_users = "{}\n{}".format(name_user, name_users)
            input_content = InputTextMessageContent(
                message_text=langU["inline"]["text"]["najva_group"].format(
                    len(users), name_users
                ),
                parse_mode="HTML",
                disable_web_page_preview=True,
            )
            item1 = InlineQueryResultArticle(
                id=f"najvaP:{user_id}",
                title=langU["inline"]["title"]["najva_group"].format(
                    len(users)
                ),
                description=langU["inline"]["desc"]["najva_group"].format(
                    len(text)
                ),
                thumb_url=pic_group,
                thumb_width=512,
                thumb_height=512,
                input_message_content=input_content,
                reply_markup=inlineKeys,
            )
        else:
            if "@" in users[0]:
                k = await userIds(users[0])
                if k:
                    users[0] = k
            name_user2 = None
            if DataBase.hget(f"setting_najva:{users[0]}", "noname"):
                name_user2 = langU["no_name"]
            name_user = await userInfos(users[0], info="name")
            input_content = InputTextMessageContent(
                message_text=langU["inline"]["text"]["najva_person"].format(
                    name_user2 or name_user
                ),
                parse_mode="HTML",
                disable_web_page_preview=False,
            )
            item1 = InlineQueryResultArticle(
                id=f"najvaP:{user_id}",
                title=langU["inline"]["title"]["najva_person"].format(
                    name_user
                ),
                description=langU["inline"]["desc"]["najva_person"].format(
                    len(text)
                ),
                thumb_url=pic_message,
                thumb_width=512,
                thumb_height=512,
                input_message_content=input_content,
                reply_markup=inlineKeys,
            )
        user_steps[user_id].update(
            {
                "najva": {
                    "time": ti_me,
                    "text": text,
                    "users": users,
                }
            }
        )
        await answerInlineQuery(
            msg_id,
            results=[
                item1,
            ],
            cache_time=1,
        )
    if re.search(r"@[Aa][Ll][Ll] (.*)$", input) or re.search(
        r"@[Aa][Ll][Ll] (.*)$", input
    ):
        ap = re.findall(r"@[Aa][Ll][Ll] (.*)$", input)
        text = ap[0]
        ti_me = time()
        inlineKeys = iMarkup()
        inlineKeys.add(
            iButtun(
                buttuns["stats"],
                callback_data="showS:{}:{}".format(user_id, ti_me),
            ),
            iButtun(
                buttuns["show_najva"],
                callback_data="showN:{}:{}".format(user_id, ti_me),
            ),
        )
        ads = DataBase.get("have_ads")
        if ads:
            inlineKeys.add(
                iButtun(
                    DataBase.hget("info_ads", "buttuns"),
                    url=DataBase.hget("info_ads", "url"),
                )
            )
        input_content = InputTextMessageContent(
            message_text=langU["inline"]["text"]["najva_all"],
            parse_mode="HTML",
            disable_web_page_preview=False,
        )
        item1 = InlineQueryResultArticle(
            id=f"najvaA:{user_id}",
            title=langU["inline"]["title"]["najva_all"],
            description=langU["inline"]["desc"]["najva_all"].format(len(text)),
            thumb_url=pic_all,
            thumb_width=512,
            thumb_height=512,
            input_message_content=input_content,
            reply_markup=inlineKeys,
        )
        input_content = InputTextMessageContent(
            message_text=langU["inline"]["text"]["najva_all2"],
            parse_mode="HTML",
            disable_web_page_preview=False,
        )
        item2 = InlineQueryResultArticle(
            id=f"najvaA2:{user_id}",
            title=langU["inline"]["title"]["najva_all"],
            description=langU["inline"]["desc"]["najva_all2"].format(
                len(text)
            ),
            thumb_url=pic_all,
            thumb_width=512,
            thumb_height=512,
            input_message_content=input_content,
            reply_markup=inlineKeys,
        )
        user_steps[user_id].update(
            {
                "najva": {
                    "time": ti_me,
                    "text": text,
                    "users": "all",
                }
            }
        )
        await answerInlineQuery(msg_id, results=[item1, item2], cache_time=1)
    if re.search(r"set$", input.lower()):
        set_desc = langU["inline"]["desc"]
        if DataBase.hget(f"setting_najva:{user_id}", "seen"):
            seen = langU["is_power_on"]
            title1 = langU["inline"]["title"]["power_off"]
            photo1 = pic_tick
        else:
            seen = langU["is_power_off"]
            title1 = langU["inline"]["title"]["power_on"]
            photo1 = pic_cross
        seen = set_desc["najva_seen"].format(seen)
        if DataBase.hget(f"setting_najva:{user_id}", "recv"):
            recv = langU["is_power_on"]
            title2 = langU["inline"]["title"]["power_off"]
            photo2 = pic_tick
        else:
            recv = langU["is_power_off"]
            title2 = langU["inline"]["title"]["power_on"]
            photo2 = pic_cross
        recv = set_desc["najva_recv"].format(recv)
        if DataBase.hget(f"setting_najva:{user_id}", "encrypt"):
            encrypt = langU["is_power_on"]
            title3 = langU["inline"]["title"]["power_off"]
            photo3 = pic_tick
        else:
            encrypt = langU["is_power_off"]
            title3 = langU["inline"]["title"]["power_on"]
            photo3 = pic_cross
        encrypt = set_desc["najva_encrypt"].format(encrypt)
        if DataBase.hget(f"setting_najva:{user_id}", "noname"):
            noname = langU["is_power_on"]
            title4 = langU["inline"]["title"]["power_off"]
            photo4 = pic_tick
        else:
            noname = langU["is_power_off"]
            title4 = langU["inline"]["title"]["power_on"]
            photo4 = pic_cross
        noname = set_desc["najva_noname"].format(noname)
        if DataBase.hget(f"setting_najva:{user_id}", "dispo"):
            dispo = langU["is_power_on"]
            title5 = langU["inline"]["title"]["power_off"]
            photo5 = pic_tick
        else:
            dispo = langU["is_power_off"]
            title5 = langU["inline"]["title"]["power_on"]
            photo5 = pic_cross
        dispo = set_desc["najva_dispo"].format(dispo)
        inlineKeys = iMarkup()
        inlineKeys.add(
            iButtun(
                buttuns["quick_set"], switch_inline_query_current_chat="set"
            )
        )
        input_content = InputTextMessageContent(
            message_text=langU["inline"]["text"]["setting_changed"],
            parse_mode="HTML",
            disable_web_page_preview=False,
        )
        item1 = InlineQueryResultArticle(
            id=f"set:seen:{user_id}",
            title=title1,
            description=seen,
            thumb_url=photo1,
            thumb_width=512,
            thumb_height=512,
            input_message_content=input_content,
            reply_markup=inlineKeys,
        )
        item2 = InlineQueryResultArticle(
            id=f"set:recv:{user_id}",
            title=title2,
            description=recv,
            thumb_url=photo2,
            thumb_width=512,
            thumb_height=512,
            input_message_content=input_content,
            reply_markup=inlineKeys,
        )
        item3 = InlineQueryResultArticle(
            id=f"set:encrypt:{user_id}",
            title=title3,
            description=encrypt,
            thumb_url=photo3,
            thumb_width=512,
            thumb_height=512,
            input_message_content=input_content,
            reply_markup=inlineKeys,
        )
        item4 = InlineQueryResultArticle(
            id=f"set:noname:{user_id}",
            title=title4,
            description=noname,
            thumb_url=photo4,
            thumb_width=512,
            thumb_height=512,
            input_message_content=input_content,
            reply_markup=inlineKeys,
        )
        item5 = InlineQueryResultArticle(
            id=f"set:dispo:{user_id}",
            title=title5,
            description=dispo,
            thumb_url=photo5,
            thumb_width=512,
            thumb_height=512,
            input_message_content=input_content,
            reply_markup=inlineKeys,
        )
        await answerInlineQuery(
            msg_id,
            [item1, item2, item3, item4, item5],
            1,
            langU["inline"]["title"]["all_set"],
            "set",
        )
    if (
        not re.findall(r"@all ", input.lower())
        and not re.findall(r"(?:(?<!\d)\d{6,10}(?!\d))", input)
        and not re.findall(r"(@[a-zA-Z0-9_]*)", input)
        and chat_type == "supergroup"
    ):
        ap = re_matches(r"(.*)", input)
        text = ap[1]
        ti_me = time()
        inlineKeys = iMarkup()
        inlineKeys.add(
            iButtun(
                buttuns["show_najva"],
                callback_data="showN2:{}:{}".format(user_id, ti_me),
            )
        )
        ads = DataBase.get("have_ads")
        if ads:
            inlineKeys.add(
                iButtun(
                    DataBase.hget("info_ads", "buttuns"),
                    url=DataBase.hget("info_ads", "url"),
                )
            )
        input_content = InputTextMessageContent(
            message_text=langU["inline"]["text"]["najva_reply"],
            parse_mode="HTML",
            disable_web_page_preview=True,
        )
        item1 = InlineQueryResultArticle(
            id=f"najvaR:{user_id}",
            title=langU["inline"]["title"]["najva_reply"],
            description=langU["inline"]["desc"]["najva_reply"],
            thumb_url=pic_message,
            thumb_width=512,
            thumb_height=512,
            input_message_content=input_content,
            reply_markup=inlineKeys,
        )
        user_steps[user_id].update(
            {
                "najva": {
                    "time": ti_me,
                    "text": text,
                    "users": "reply",
                }
            }
        )
        await answerInlineQuery(
            msg_id,
            results=[
                item1,
            ],
            cache_time=1,
        )
    if not re.findall(r"@all ", input.lower()) and (
        re.search(r"^(?:(?<!\d)\d{6,10}(?!\d))$", input)
        or re.search(r"^(@[a-zA-Z0-9_]*)$", input)
    ):
        ap1 = re.findall(r"(@[a-zA-Z0-9_]*)", input)
        ap2 = re.findall(r"(?:(?<!\d)\d{6,10}(?!\d))", input)
        ap = ap1 or ap2
        user = ap[0]
        ti_me = time()
        inlineKeys = iMarkup()
        inlineKeys.add(
            iButtun(
                "{} - {}".format(GlobalValues().botName, GlobalValues().botUser),
                url="t.me/{}".format(GlobalValues().botUser),
            )
        )
        ads = DataBase.get("have_ads")
        if ads:
            inlineKeys.add(
                iButtun(
                    DataBase.hget("info_ads", "buttuns"),
                    url=DataBase.hget("info_ads", "url"),
                )
            )
        input_content = InputTextMessageContent(
            message_text=langU["inline"]["text"]["najva_havn_text"],
            parse_mode="HTML",
            disable_web_page_preview=True,
        )
        item2 = InlineQueryResultArticle(
            id="null",
            title=langU["inline"]["title"]["najva_havn_text"],
            description=langU["inline"]["desc"]["najva_havn_text"],
            thumb_url=pic_cross,
            thumb_width=512,
            thumb_height=512,
            input_message_content=input_content,
        )
        if "@" in user:
            name_user = await userIds(user)
            user = name_user
        else:
            name_user = user
        name_user2 = None
        if DataBase.hget(f"setting_najva:{name_user}", "noname"):
            name_user2 = langU["no_name"]
        name_user = await userInfos(name_user, info="name")
        input_content = InputTextMessageContent(
            message_text=langU["inline"]["text"]["najva_special"].format(
                name_user2 or name_user
            ),
            parse_mode="HTML",
            disable_web_page_preview=True,
        )
        item1 = InlineQueryResultArticle(
            id=f"najvaS:{user_id}",
            title=langU["inline"]["title"]["najva_special"].format(name_user),
            description=langU["inline"]["desc"]["najva_special"],
            thumb_url=pic_special,
            thumb_width=512,
            thumb_height=512,
            input_message_content=input_content,
            reply_markup=inlineKeys,
        )
        user_steps[user_id].update(
            {
                "najva": {
                    "time": ti_me,
                    "text": None,
                    "users": user,
                }
            }
        )
        await answerInlineQuery(msg_id, results=[item1, item2], cache_time=1)
    if re.match(r"sp(\d+)\.(\d+)\.(\d+)", input):
        ap = re_matches(r"sp(\d+)\.(\d+)\.(\d+)", input)
        from_user = ap[1]
        time_data = float(f"{ap[2]}.{ap[3]}")
        special_msgID = DataBase.hget(
            "najva_special:{}".format(from_user), "id"
        )
        users_data = DataBase.hget(
            "najva:{}:{}".format(from_user, time_data), "users"
        )
        if not str(user_id) in users_data and not str(username) in users_data:
            if special_msgID:
                return DataBase.sadd(
                    "najva_nosy:{}:{}".format(from_user, time_data), user_id
                )
            else:
                return False
        if not special_msgID:
            input_content = InputTextMessageContent(
                message_text=langU["inline"]["text"]["special_404"],
                parse_mode="HTML",
                disable_web_page_preview=True,
            )
            item1 = InlineQueryResultArticle(
                id="null",
                title=langU["inline"]["title"]["special_404"],
                description=langU["inline"]["desc"]["special_404"],
                thumb_url=pic_cross,
                thumb_width=512,
                thumb_height=512,
                input_message_content=input_content,
            )
            await answerInlineQuery(
                msg_id,
                results=[
                    item1,
                ],
                cache_time=3600,
            )
        file_id = DataBase.hget(
            "najva:{}:{}".format(from_user, time_data), "file_id"
        )
        file_type = DataBase.hget(
            "najva:{}:{}".format(from_user, time_data), "file_type"
        )
        source_id = DataBase.hget(
            "najva:{}:{}".format(from_user, time_data), "source_id"
        )
        msg_ID = DataBase.hget(
            "najva:{}:{}".format(from_user, time_data), "msg_id"
        )
        input_content = InputTextMessageContent(
            message_text=langU["cant_send_hide"],
            parse_mode="HTML",
            disable_web_page_preview=True,
        )
        item1 = None
        if file_type == "photo":
            item1 = InlineQueryResultCachedPhoto(
                id="null",
                photo_file_id=file_id,
                input_message_content=input_content,
            )
        elif file_type == "video":
            item1 = InlineQueryResultCachedVideo(
                id="null",
                title=" ",
                video_file_id=file_id,
                input_message_content=input_content,
            )
        elif file_type == "voice":
            item1 = InlineQueryResultCachedVoice(
                id="null",
                title=" ",
                voice_file_id=file_id,
                input_message_content=input_content,
            )
        elif file_type == "sticker":
            item1 = InlineQueryResultCachedSticker(
                id="null",
                sticker_file_id=file_id,
                input_message_content=input_content,
            )
        elif file_type == "animation":
            item1 = InlineQueryResultCachedGif(
                id="null",
                gif_file_id=file_id,
                input_message_content=input_content,
            )
        if item1:
            if DataBase.hget(
                f"setting_najva:{from_user}", "seen"
            ) and not DataBase.get(
                "notif_before:{}:{}".format(from_user, time_data)
            ):
                DataBase.set(
                    "notif_before:{}:{}".format(from_user, time_data), 1
                )
                await sendText(
                    from_user,
                    source_id,
                    1,
                    langU["speical_najva_seen"].format(
                        msg.from_user.first_name
                    ),
                )
                await editText(
                    inline_msg_id=special_msgID,
                    text=langU["speical_najva_seen2"].format(
                        msg.from_user.first_name
                    ),
                    parse_mode="html",
                    reply_markup=najva_seen3_keys(from_user, time_data),
                )
                DataBase.set(
                    "najva_seen_time:{}:{}".format(from_user, time_data),
                    int(time()),
                )
                DataBase.incr(
                    "najva_seen_count:{}:{}".format(from_user, time_data)
                )
                DataBase.sadd(
                    "najva_seened:{}:{}".format(from_user, time_data), user_id
                )
                if DataBase.hget(f"setting_najva:{from_user}", "dispo"):
                    special_msgID = DataBase.hget(
                        "najva_special:{}".format(from_user), "id"
                    )
                    DataBase.srem(
                        "najva_autodel",
                        f"{from_user}:{time_data}:{special_msgID}",
                    )
                    DataBase.delete("najva:{}:{}".format(from_user, time_data))
                    DataBase.delete("najva_special:{}".format(from_user))
            await answerInlineQuery(
                msg_id,
                results=[
                    item1,
                ],
                is_personal=True,
                cache_time=3600,
            )
    if re.match(r"^\*$", input):
        users = DataBase.smembers(f"najva_recent2:{user_id}")
        if len(users) == 0:
            return False
        users = list(users)
        ti_me = time()
        inlineKeys = iMarkup()
        inlineKeys.add(
            iButtun(
                "{} - {}".format(GlobalValues().botName, GlobalValues().botUser),
                url="t.me/{}".format(GlobalValues().botUser),
            )
        )
        ads = DataBase.get("have_ads")
        if ads:
            inlineKeys.add(
                iButtun(
                    DataBase.hget("info_ads", "buttuns"),
                    url=DataBase.hget("info_ads", "url"),
                )
            )
        items = []
        input_content = InputTextMessageContent(
            message_text=langU["inline"]["text"]["najva_havn_text"],
            parse_mode="HTML",
            disable_web_page_preview=True,
        )
        item2 = InlineQueryResultArticle(
            id="null",
            title=langU["inline"]["title"]["najva_havn_text"],
            description=langU["inline"]["desc"]["najva_havn_text"],
            thumb_url=pic_cross,
            thumb_width=512,
            thumb_height=512,
            input_message_content=input_content,
        )
        items.append(item2)
        count = 0
        for user in users:
            count += 1
            if count > 5:
                break
            name_user = user
            name_user2 = None
            if DataBase.hget(f"setting_najva:{name_user}", "noname"):
                name_user2 = langU["no_name"]
            name_user = await userInfos(name_user, info="name")
            input_content = InputTextMessageContent(
                message_text=langU["inline"]["text"]["najva_special"].format(
                    name_user2 or name_user
                ),
                parse_mode="HTML",
                disable_web_page_preview=True,
            )
            # have_prof = DataBase.hget('userProfs', user)
            # if have_prof:
            # get_file = await bot.get_file(have_prof)
            # file_path = get_file['file_path']
            # file_path = f'https://api.telegram.org/file/bot{telegram_datas["botToken"]}/{file_path}'
            # else:
            # file_path = pic_user
            file_path = pic_user
            item1 = InlineQueryResultArticle(
                id=f"najvaS:{user_id}:{user}",
                title=langU["inline"]["title"]["najva_special"].format(
                    name_user
                ),
                description=langU["inline"]["desc"]["najva_special"],
                thumb_url=file_path,
                thumb_width=512,
                thumb_height=512,
                input_message_content=input_content,
                reply_markup=inlineKeys,
            )
            items.append(item1)
        user_steps[user_id].update(
            {
                "najva": {
                    "time": ti_me,
                    "text": None,
                    "users": "x",
                }
            }
        )
        await answerInlineQuery(msg_id, results=items, cache_time=1)


async def chosen_inline_process(msg: types.ChosenInlineResult):
    # {
    # "from": {
    # "id": 139946685, "is_bot": false,
    # "first_name": "Alireza 🏴🏳",
    # "username": "ferisystem", "language_code": "de"},
    # "inline_message_id": "BAAAAKqZKQC9alcIRMLU6NZ-9PU", # if keyboard attached
    # "query": "awd", "result_id": "601066437369956078"
    # }
    user_id = msg.from_user.id
    user_name = msg.from_user.first_name
    result_id = msg.result_id
    input = msg.query
    saveUsername(msg, mode="inline")
    setupUserSteps(msg, user_id)
    langU = lang[user_steps[user_id]["lang"]]
    buttuns = langU["buttuns"]
    print(colored("Chosen_Inline >", "cyan"))
    print(colored("userID", "yellow"), colored(user_id, "white"))
    print(colored("Query", "yellow"), colored(input, "white"))
    print(colored("resultID", "yellow"), colored(result_id, "white"))
    print()
    if (
        re.match(r"^najvaP:(\d+)$", result_id)
        and "najva" in user_steps[user_id]
    ):
        ap = re_matches(r"^najvaP:(\d+)$", result_id)
        najva = user_steps[user_id]["najva"]
        DataBase.hset(
            "najva:{}:{}".format(user_id, najva["time"]), "text", najva["text"]
        )
        if len(najva["users"]) > 1:
            DataBase.hset(
                "najva:{}:{}".format(user_id, najva["time"]),
                "users",
                str(najva["users"]),
            )
            for i in najva["users"]:
                if str(i).isdigit():
                    DataBase.sadd(f"najva_recent:{user_id}", i)
        else:
            DataBase.hset(
                "najva:{}:{}".format(user_id, najva["time"]),
                "users",
                najva["users"][0],
            )
            if str(najva["users"][0]).isdigit():
                DataBase.sadd(f"najva_recent:{user_id}", najva["users"][0])
            # DataBase.hset('najva_special:{}'.format(user_id), 'time', najva['time'])
            # DataBase.hset('najva_special:{}'.format(user_id), 'id2', msg.inline_message_id)
            if DataBase.hget(f"setting_najva:{user_id}", "autodel"):
                DataBase.sadd(
                    "najva_autodel",
                    f"{user_id}:{najva['time']}:{msg.inline_message_id}",
                )
        for i in najva["users"]:
            if DataBase.hget(f"setting_najva:{i}", "recv"):
                await sendText(
                    i,
                    0,
                    1,
                    langU["you_recv_najva"].format(
                        '<a href="tg://user?id={}">{}</a>'.format(
                            user_id, user_name
                        )
                    ),
                    "html",
                )
        DataBase.incr("stat_najva")
        for i in najva["users"]:
            if str(i).isdigit() and not DataBase.get(f"userProfs:{i}"):
                DataBase.setex(f"userProfs:{i}", 604800, 1)
                profiles = await getUserProfilePhotos(i)
                if profiles[0] and profiles[1].total_count > 0:
                    DataBase.hset(
                        "userProfs", i, profiles[1].photos[0][-1].file_id
                    )
                await asyncio.sleep(0.5)
        del user_steps[user_id]["najva"]
    if (
        re.match(r"^najvaA:(\d+)$", result_id)
        and "najva" in user_steps[user_id]
    ):
        ap = re_matches(r"^najvaA:(\d+)$", result_id)
        najva = user_steps[user_id]["najva"]
        DataBase.hset(
            "najva:{}:{}".format(user_id, najva["time"]), "text", najva["text"]
        )
        DataBase.hset(
            "najva:{}:{}".format(user_id, najva["time"]), "users", "all"
        )
        DataBase.incr("stat_najva")
        del user_steps[user_id]["najva"]
    if (
        re.match(r"^najvaR:(\d+)$", result_id)
        and "najva" in user_steps[user_id]
    ):
        ap = re_matches(r"^najvaR:(\d+)$", result_id)
        najva = user_steps[user_id]["najva"]
        DataBase.hset(
            "najva:{}:{}".format(user_id, najva["time"]), "text", najva["text"]
        )
        DataBase.hset(
            "najva:{}:{}".format(user_id, najva["time"]), "users", "reply"
        )
        # DataBase.hset('najva_special:{}'.format(user_id), 'time', najva['time'])
        # DataBase.hset('najva_special:{}'.format(user_id), 'id2', msg.inline_message_id)
        if DataBase.hget(f"setting_najva:{user_id}", "autodel"):
            DataBase.sadd(
                "najva_autodel",
                f"{user_id}:{najva['time']}:{msg.inline_message_id}",
            )
        DataBase.incr("stat_najva")
        del user_steps[user_id]["najva"]
    if re.match(r"^set:(.*):(\d+)$", result_id):
        ap = re_matches(r"^set:(.*):(\d+)$", result_id)
        if DataBase.hget(f"setting_najva:{user_id}", ap[1]):
            DataBase.hdel(f"setting_najva:{user_id}", ap[1])
        else:
            DataBase.hset(f"setting_najva:{user_id}", ap[1], 1)
    if (
        re.match(r"^najvaS:(\d+)$", result_id)
        and "najva" in user_steps[user_id]
    ):
        ap = re_matches(r"^najvaS:(\d+)$", result_id)
        najva = user_steps[user_id]["najva"]
        DataBase.hset(
            "najva:{}:{}".format(user_id, najva["time"]),
            "users",
            najva["users"],
        )
        DataBase.hset(
            "najva_special:{}".format(user_id), "time", najva["time"]
        )
        DataBase.hset(
            "najva_special:{}".format(user_id), "id", msg.inline_message_id
        )
        DataBase.setex(
            "ready_to_recv_special:{}".format(user_id), 1800, "True"
        )
        if str(najva["users"]).isdigit():
            DataBase.sadd(f"najva_recent2:{user_id}", najva["users"])
        if DataBase.hget(f"setting_najva:{user_id}", "autodel"):
            DataBase.sadd(
                "najva_autodel",
                f"{user_id}:{najva['time']}:{msg.inline_message_id}",
            )
        DataBase.incr("stat_najva")
        del user_steps[user_id]["najva"]
        inlineKeys = iMarkup()
        inlineKeys.add(
            iButtun(
                buttuns["cancel"],
                callback_data="special:cancel:@{}".format(user_id),
            ),
        )
        await sendText(
            user_id, 0, 1, langU["send_special_najva"], "html", inlineKeys
        )
        if str(najva["users"]).isdigit():
            i = najva["users"]
            if not DataBase.get(f"userProfs:{i}"):
                DataBase.setex(f"userProfs:{i}", 604800, 1)
                profiles = await getUserProfilePhotos(i)
                if profiles[0] and profiles[1].total_count > 0:
                    DataBase.hset(
                        "userProfs", i, profiles[1].photos[0][-1].file_id
                    )
    if (
        re.match(r"^najvaS:(\d+):(\d+)$", result_id)
        and "najva" in user_steps[user_id]
    ):
        ap = re_matches(r"^najvaS:(\d+):(\d+)$", result_id)
        najva = user_steps[user_id]["najva"]
        najva["users"] = ap[2]
        DataBase.hset(
            "najva:{}:{}".format(user_id, najva["time"]),
            "users",
            najva["users"],
        )
        DataBase.hset(
            "najva_special:{}".format(user_id), "time", najva["time"]
        )
        DataBase.hset(
            "najva_special:{}".format(user_id), "id", msg.inline_message_id
        )
        DataBase.setex(
            "ready_to_recv_special:{}".format(user_id), 1800, "True"
        )
        if str(najva["users"]).isdigit():
            DataBase.sadd(f"najva_recent2:{user_id}", najva["users"])
        if DataBase.hget(f"setting_najva:{user_id}", "autodel"):
            DataBase.sadd(
                "najva_autodel",
                f"{user_id}:{najva['time']}:{msg.inline_message_id}",
            )
        DataBase.incr("stat_najva")
        del user_steps[user_id]["najva"]
        inlineKeys = iMarkup()
        inlineKeys.add(
            iButtun(
                buttuns["cancel"],
                callback_data="special:cancel:@{}".format(user_id),
            ),
        )
        await sendText(
            user_id, 0, 1, langU["send_special_najva"], "html", inlineKeys
        )
        if str(najva["users"]).isdigit():
            i = najva["users"]
            if not DataBase.get(f"userProfs:{i}"):
                DataBase.setex(f"userProfs:{i}", 604800, 1)
                profiles = await getUserProfilePhotos(i)
                if profiles[0] and profiles[1].total_count > 0:
                    DataBase.hset(
                        "userProfs", i, profiles[1].photos[0][-1].file_id
                    )


async def channel_post_process(msg: types.Message):
    if (msg.chat.username or "") != IDs_datas["chUsername"] and int(
        msg.chat.id
    ) != int(GlobalValues().supchat):
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
        log.debug("Message is not modified!")
        return
    if isinstance(exception, expts.MessageToDeleteNotFound):
        log.debug("Message to delete not found!")
        return
    if isinstance(exception, expts.Unauthorized):
        log.info(f"Unauthorized: {exception} !")
        return
    if isinstance(exception, expts.InvalidQueryID):
        log.exception(f"InvalidQueryID: {exception} !\nUpdate: {update}")
        return
    if isinstance(exception, expts.TelegramAPIError):
        log.exception(f"TelegramAPIError: {exception} !\nUpdate: {update}")
        return
    if isinstance(exception, expts.RestartingTelegram):
        await asyncio.sleep(5)
        # log.exception(f'TelegramAPIError: {exception} !\nUpdate: {update}')
        await sendText(
            GlobalValues().sudoID, 0, 1, "The Telegram Bot API service is restarting..."
        )
        return
    if isinstance(exception, telethonErrors.BotMethodInvalidError):
        return
    try:
        pass
    except AttributeError:
        log.exception(f"AttributeError: {exception} !\nUpdate: {update}")
        return


async def bot_off(app):
    await bot.delete_webhook()
    # await client.disconnect()
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
    # await client.start(bot_token = telegram_datas['botToken'])
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
    # await sendText(GlobalValues().sudoID, 0, 1, 'Bot has been Successfully Loaded')
    # if not rds.hget(db, 'linkyCH'):
    # status = False
    # while status != True:
    # iD = input("Enter LinkyCH Username: ")
    # if re.match(r'^(@\w+)$', iD):
    # rds.hset(db, 'linkyCH', re.match(r'^(@\w+)$', iD).group(1))
    # status = True
    # break
    # else:
    # iD = input("Enter LinkyCH Username: ")
    # status = False
    if not rds.hget(db, "supchat"):
        status = False
        while status != True:
            iD = input("Enter Supergroup ID for support: ")
            if re.match(r"^(-\d+)$", iD):
                rds.hset(db, "supchat", re.match(r"^(-\d+)$", iD).group(1))
                status = True
                break
            else:
                iD = input("Enter Channel ID for support: ")
                status = False


# کاراکتر
if __name__ == "__main__":
    app = get_new_configured_app(dispatcher=dp, path=GlobalValues().WEBHOOK_URL_PATH)
    app.on_startup.append(bot_run)
    app.on_shutdown.append(bot_off)
    context = ssl.SSLContext(ssl.PROTOCOL_TLS)
    context.load_cert_chain(GlobalValues().WEBHOOK_SSL_CERT, GlobalValues().WEBHOOK_SSL_PRIV)
    web.run_app(app, host="0.0.0.0", port=GlobalValues().port, ssl_context=context)