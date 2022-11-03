# coding: utf8
from Files.callback_process import callback_query_process
from Files.keyboards_func import *
from Files.lateral_func import *
from Files.main_func import *
from config_bot2 import *
from core_file import *

# -------------------------------------------------------------------------------- #

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
