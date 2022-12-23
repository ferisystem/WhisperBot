from whisperbot.keyboards_func import *
from whisperbot.lateral_func import *
from whisperbot.main_func import *
from config_bot import *
from core_file import *


async def chosen_inline_process(msg: types.ChosenInlineResult):
    user_id = msg.from_user.id
    user_name = msg.from_user.first_name
    result_id = msg.result_id
    input = msg.query
    saveUsername(msg, mode="inline")
    setupUserSteps(msg, user_id)
    langU = lang[lang_user(user_id)]
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
            uSer = najva["users"][0]
            if DataBase.sismember(f"blocks2:{uSer}", user_id):
                uSer = f"<a href=\"tg://user?id={uSer}\">{uSer}</a>"
                del user_steps[user_id]["najva"]
                return await editText(
                    inline_msg_id=msg.inline_message_id,
                    text=langU["najva_user_blocked_you"].format(uSer),
                    parse_mode="html",
                    reply_markup=None,
                )
            DataBase.hset(
                "najva:{}:{}".format(user_id, najva["time"]),
                "users",
                najva["users"][0],
            )
            if str(najva["users"][0]).isdigit():
                DataBase.sadd(f"najva_recent:{user_id}", najva["users"][0])
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
                    lang[lang_user(i)]["you_recv_najva"].format(
                        '<a href="tg://user?id={}">{}</a>'.format(
                            user_id, user_name
                        )
                    ),
                    "html",
                )
        DataBase.set(
            f"najvas_sent:{user_id}:{najva['time']}",
            msg.inline_message_id,
        )
        DataBase.incr("stat_najva")
        # for i in najva["users"]:
            # if str(i).isdigit() and not DataBase.get(f"userProfs:{i}"):
                # DataBase.setex(f"userProfs:{i}", 604800, 1)
                # profiles = await getUserProfilePhotos(i)
                # if profiles[0] and profiles[1].total_count > 0:
                    # DataBase.hset(
                        # "userProfs", i, profiles[1].photos[0][-1].file_id
                    # )
                    # have_prof = profiles[1].photos[0][1].file_id
                    # await downloadFileByID(have_prof, f"docs/profiles/{i}.jpg")
                # await asyncio.sleep(0.5)
        del user_steps[user_id]["najva"]
    if (
        re.match(r"^najvaA\d*:(\d+)$", result_id)
        and "najva" in user_steps[user_id]
    ):
        ap = re_matches(r"^najvaA\d*:(\d+)$", result_id)
        najva = user_steps[user_id]["najva"]
        DataBase.hset(
            "najva:{}:{}".format(user_id, najva["time"]), "text", najva["text"]
        )
        DataBase.hset(
            "najva:{}:{}".format(user_id, najva["time"]), "users", "all"
        )
        DataBase.set(
            f"najvas_sent:{user_id}:{najva['time']}",
            msg.inline_message_id,
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
        DataBase.set(
            f"najvas_sent:{user_id}:{najva['time']}",
            msg.inline_message_id,
        )
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
        uSer = najva["users"]
        if DataBase.sismember(f"blocks2:{uSer}", user_id):
            uSer = f"<a href=\"tg://user?id={uSer}\">{uSer}</a>"
            del user_steps[user_id]["najva"]
            return await editText(
                inline_msg_id=msg.inline_message_id,
                text=langU["najva_user_blocked_you"].format(uSer),
                parse_mode="html",
                reply_markup=None,
            )
        DataBase.set(
            f"najvas_sent:{user_id}:{najva['time']}",
            msg.inline_message_id,
        )
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
        msg_ = await sendText(
            user_id, 0, 1, langU["send_special_najva"], "html", inlineKeys
        )
        if not msg_[0] is False:
            DataBase.set("pre_msgbot:{}".format(user_id), msg_[1].message_id)
        # if str(najva["users"]).isdigit():
            # i = najva["users"]
            # if not DataBase.get(f"userProfs:{i}"):
                # DataBase.setex(f"userProfs:{i}", 604800, 1)
                # profiles = await getUserProfilePhotos(i)
                # if profiles[0] and profiles[1].total_count > 0:
                    # DataBase.hset(
                        # "userProfs", i, profiles[1].photos[0][-1].file_id
                    # )
                    # have_prof = profiles[1].photos[0][1].file_id
                    # await downloadFileByID(have_prof, f"docs/profiles/{i}.jpg")
    if (
        re.match(r"^najvaS:(\d+):(\d+)$", result_id)
        and "najva" in user_steps[user_id]
    ):
        ap = re_matches(r"^najvaS:(\d+):(\d+)$", result_id)
        najva = user_steps[user_id]["najva"]
        najva["users"] = ap[2]
        if DataBase.sismember(f"blocks2:{ap[2]}", user_id):
            uSer = f"<a href=\"tg://user?id={ap[2]}\">{ap[2]}</a>"
            del user_steps[user_id]["najva"]
            return await editText(
                inline_msg_id=msg.inline_message_id,
                text=langU["najva_user_blocked_you"].format(uSer),
                parse_mode="html",
                reply_markup=None,
            )
        DataBase.set(
            f"najvas_sent:{user_id}:{najva['time']}",
            msg.inline_message_id,
        )
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
        msg_ = await sendText(
            user_id, 0, 1, langU["send_special_najva"], "html", inlineKeys
        )
        if not msg_[0] is False:
            DataBase.set("pre_msgbot:{}".format(user_id), msg_[1].message_id)
        # if str(najva["users"]).isdigit():
            # i = najva["users"]
            # if not DataBase.get(f"userProfs:{i}"):
                # DataBase.setex(f"userProfs:{i}", 604800, 1)
                # profiles = await getUserProfilePhotos(i)
                # if profiles[0] and profiles[1].total_count > 0:
                    # DataBase.hset(
                        # "userProfs", i, profiles[1].photos[0][-1].file_id
                    # )
                    # have_prof = profiles[1].photos[0][1].file_id
                    # await downloadFileByID(have_prof, f"docs/profiles/{i}.jpg")
