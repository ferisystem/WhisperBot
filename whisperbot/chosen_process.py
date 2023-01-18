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
        re.match(r"^whisperP:(\d+)$", result_id)
        and "whisper" in user_steps[user_id]
    ):
        ap = re_matches(r"^whisperP:(\d+)$", result_id)
        whisper = user_steps[user_id]["whisper"]
        DataBase.hset(
            "whisper:{}:{}".format(user_id, whisper["time"]), "text", whisper["text"]
        )
        if len(whisper["users"]) > 1:
            DataBase.hset(
                "whisper:{}:{}".format(user_id, whisper["time"]),
                "users",
                str(whisper["users"]),
            )
            for i in whisper["users"]:
                if str(i).isdigit():
                    DataBase.sadd(f"whisper_recent:{user_id}", i)
        else:
            uSer = whisper["users"][0]
            if DataBase.sismember(f"blocks2:{uSer}", user_id):
                uSer = f"<a href=\"tg://user?id={uSer}\">{uSer}</a>"
                del user_steps[user_id]["whisper"]
                return await editText(
                    inline_msg_id=msg.inline_message_id,
                    text=langU["whisper_user_blocked_you"].format(uSer),
                    parse_mode="html",
                    reply_markup=None,
                )
            DataBase.hset(
                "whisper:{}:{}".format(user_id, whisper["time"]),
                "users",
                whisper["users"][0],
            )
            if str(whisper["users"][0]).isdigit():
                DataBase.sadd(f"whisper_recent:{user_id}", whisper["users"][0])
            if DataBase.hget(f"setting_whisper:{user_id}", "autodel"):
                DataBase.sadd(
                    "whisper_autodel",
                    f"{user_id}:{whisper['time']}:{msg.inline_message_id}",
                )
        for i in whisper["users"]:
            if DataBase.hget(f"setting_whisper:{i}", "recv"):
                await sendText(
                    i,
                    0,
                    1,
                    lang[lang_user(i)]["you_recv_whisper"].format(
                        '<a href="tg://user?id={}">{}</a>'.format(
                            user_id, user_name
                        )
                    ),
                    "html",
                )
        DataBase.set(
            f"whispers_sent:{user_id}:{whisper['time']}",
            msg.inline_message_id,
        )
        DataBase.incr("stat_whisper")
        # for i in whisper["users"]:
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
        del user_steps[user_id]["whisper"]
    if (
        re.match(r"^whisperA\d*:(\d+)$", result_id)
        and "whisper" in user_steps[user_id]
    ):
        ap = re_matches(r"^whisperA\d*:(\d+)$", result_id)
        whisper = user_steps[user_id]["whisper"]
        DataBase.hset(
            "whisper:{}:{}".format(user_id, whisper["time"]), "text", whisper["text"]
        )
        DataBase.hset(
            "whisper:{}:{}".format(user_id, whisper["time"]), "users", "all"
        )
        DataBase.set(
            f"whispers_sent:{user_id}:{whisper['time']}",
            msg.inline_message_id,
        )
        DataBase.incr("stat_whisper")
        del user_steps[user_id]["whisper"]
    if (
        re.match(r"^whisperR:(\d+)$", result_id)
        and "whisper" in user_steps[user_id]
    ):
        ap = re_matches(r"^whisperR:(\d+)$", result_id)
        whisper = user_steps[user_id]["whisper"]
        DataBase.hset(
            "whisper:{}:{}".format(user_id, whisper["time"]), "text", whisper["text"]
        )
        DataBase.set(
            f"whispers_sent:{user_id}:{whisper['time']}",
            msg.inline_message_id,
        )
        if DataBase.hget(f"setting_whisper:{user_id}", "autodel"):
            DataBase.sadd(
                "whisper_autodel",
                f"{user_id}:{whisper['time']}:{msg.inline_message_id}",
            )
        DataBase.incr("stat_whisper")
        del user_steps[user_id]["whisper"]
    if re.match(r"^set:(.*):(\d+)$", result_id):
        ap = re_matches(r"^set:(.*):(\d+)$", result_id)
        if DataBase.hget(f"setting_whisper:{user_id}", ap[1]):
            DataBase.hdel(f"setting_whisper:{user_id}", ap[1])
        else:
            DataBase.hset(f"setting_whisper:{user_id}", ap[1], 1)
    if (
        re.match(r"^whisperS:(\d+)$", result_id)
        and "whisper" in user_steps[user_id]
    ):
        ap = re_matches(r"^whisperS:(\d+)$", result_id)
        whisper = user_steps[user_id]["whisper"]
        uSer = whisper["users"]
        if DataBase.sismember(f"blocks2:{uSer}", user_id):
            uSer = f"<a href=\"tg://user?id={uSer}\">{uSer}</a>"
            del user_steps[user_id]["whisper"]
            return await editText(
                inline_msg_id=msg.inline_message_id,
                text=langU["whisper_user_blocked_you"].format(uSer),
                parse_mode="html",
                reply_markup=None,
            )
        DataBase.set(
            f"whispers_sent:{user_id}:{whisper['time']}",
            msg.inline_message_id,
        )
        DataBase.hset(
            "whisper:{}:{}".format(user_id, whisper["time"]),
            "users",
            whisper["users"],
        )
        DataBase.hset(
            "whisper_special:{}".format(user_id), "time", whisper["time"]
        )
        DataBase.hset(
            "whisper_special:{}".format(user_id), "id", msg.inline_message_id
        )
        DataBase.setex(
            "ready_to_recv_special:{}".format(user_id), 1800, "True"
        )
        if str(whisper["users"]).isdigit():
            DataBase.sadd(f"whisper_recent2:{user_id}", whisper["users"])
        if DataBase.hget(f"setting_whisper:{user_id}", "autodel"):
            DataBase.sadd(
                "whisper_autodel",
                f"{user_id}:{whisper['time']}:{msg.inline_message_id}",
            )
        DataBase.incr("stat_whisper")
        del user_steps[user_id]["whisper"]
        inlineKeys = iMarkup()
        inlineKeys.add(
            iButtun(
                buttuns["cancel"],
                callback_data="special:cancel:@{}".format(user_id),
            ),
        )
        msg_ = await sendText(
            user_id, 0, 1, langU["send_special_whisper"], "html", inlineKeys
        )
        if not msg_[0] is False:
            DataBase.set("pre_msgbot:{}".format(user_id), msg_[1].message_id)
        # if str(whisper["users"]).isdigit():
            # i = whisper["users"]
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
        re.match(r"^whisperS:(\d+):(\d+)$", result_id)
        and "whisper" in user_steps[user_id]
    ):
        ap = re_matches(r"^whisperS:(\d+):(\d+)$", result_id)
        whisper = user_steps[user_id]["whisper"]
        whisper["users"] = ap[2]
        if DataBase.sismember(f"blocks2:{ap[2]}", user_id):
            uSer = f"<a href=\"tg://user?id={ap[2]}\">{ap[2]}</a>"
            del user_steps[user_id]["whisper"]
            return await editText(
                inline_msg_id=msg.inline_message_id,
                text=langU["whisper_user_blocked_you"].format(uSer),
                parse_mode="html",
                reply_markup=None,
            )
        DataBase.set(
            f"whispers_sent:{user_id}:{whisper['time']}",
            msg.inline_message_id,
        )
        DataBase.hset(
            "whisper:{}:{}".format(user_id, whisper["time"]),
            "users",
            whisper["users"],
        )
        DataBase.hset(
            "whisper_special:{}".format(user_id), "time", whisper["time"]
        )
        DataBase.hset(
            "whisper_special:{}".format(user_id), "id", msg.inline_message_id
        )
        DataBase.setex(
            "ready_to_recv_special:{}".format(user_id), 1800, "True"
        )
        if str(whisper["users"]).isdigit():
            DataBase.sadd(f"whisper_recent2:{user_id}", whisper["users"])
        if DataBase.hget(f"setting_whisper:{user_id}", "autodel"):
            DataBase.sadd(
                "whisper_autodel",
                f"{user_id}:{whisper['time']}:{msg.inline_message_id}",
            )
        DataBase.incr("stat_whisper")
        del user_steps[user_id]["whisper"]
        inlineKeys = iMarkup()
        inlineKeys.add(
            iButtun(
                buttuns["cancel"],
                callback_data="special:cancel:@{}".format(user_id),
            ),
        )
        msg_ = await sendText(
            user_id, 0, 1, langU["send_special_whisper"], "html", inlineKeys
        )
        if not msg_[0] is False:
            DataBase.set("pre_msgbot:{}".format(user_id), msg_[1].message_id)
        # if str(whisper["users"]).isdigit():
            # i = whisper["users"]
            # if not DataBase.get(f"userProfs:{i}"):
                # DataBase.setex(f"userProfs:{i}", 604800, 1)
                # profiles = await getUserProfilePhotos(i)
                # if profiles[0] and profiles[1].total_count > 0:
                    # DataBase.hset(
                        # "userProfs", i, profiles[1].photos[0][-1].file_id
                    # )
                    # have_prof = profiles[1].photos[0][1].file_id
                    # await downloadFileByID(have_prof, f"docs/profiles/{i}.jpg")
