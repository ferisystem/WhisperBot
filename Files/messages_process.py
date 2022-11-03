from Files.keyboards_func import *
from Files.lateral_func import *
from Files.main_func import *
from config_bot2 import *
from core_file import *


async def message_process(msg: types.Message):
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
        user_name = msg.from_user.first_name
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