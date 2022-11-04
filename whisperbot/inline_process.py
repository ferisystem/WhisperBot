from whisperbot.keyboards_func import *
from whisperbot.lateral_func import *
from whisperbot.main_func import *
from config_bot import *
from core_file import *


async def inline_query_process(msg: types.InlineQuery):
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
    langU = lang[lang_user(user_id)]
    buttuns = langU["buttuns"]
    ln_in = langU["inline"]
    print(colored("Inline >", "cyan"))
    print(colored("userID", "yellow"), colored(user_id, "white"))
    print(colored("Query", "yellow"), colored(input, "white"))
    print(colored("inlineID", "yellow"), colored(msg_id, "white"))
    print()
    if input == "":
        input_content = InputTextMessageContent(
            message_text=ln_in["text"]["help_send"].format(GlobalValues().botUser),
            parse_mode="HTML",
            disable_web_page_preview=True
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
            title=ln_in["title"]["help_send"],
            description=ln_in["desc"]["help_send"],
            thumb_url=pic_question,
            thumb_width=512,
            thumb_height=512,
            input_message_content=input_content,
            reply_markup=inlineKeys,
        )
        input_content = InputTextMessageContent(
            message_text=ln_in["text"]["my_id"].format(user_id),
            parse_mode="HTML",
            disable_web_page_preview=True
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
            title=ln_in["title"]["my_id"],
            description=ln_in["desc"]["my_id"].format(user_id),
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
                message_text=ln_in["text"]["najva_havn_text"],
                parse_mode="HTML",
                disable_web_page_preview=True,
            )
            item1 = InlineQueryResultArticle(
                id="null",
                title=ln_in["title"]["najva_havn_text"],
                description=ln_in["desc"]["najva_havn_text"],
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
                message_text=ln_in["text"]["najva_group"].format(
                    len(users), name_users
                ),
                parse_mode="HTML",
                disable_web_page_preview=True,
            )
            item1 = InlineQueryResultArticle(
                id=f"najvaP:{user_id}",
                title=ln_in["title"]["najva_group"].format(
                    len(users)
                ),
                description=ln_in["desc"]["najva_group"].format(
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
                message_text=ln_in["text"]["najva_person"].format(
                    name_user2 or name_user
                ),
                parse_mode="HTML",
                disable_web_page_preview=False,
            )
            item1 = InlineQueryResultArticle(
                id=f"najvaP:{user_id}",
                title=ln_in["title"]["najva_person"].format(
                    name_user
                ),
                description=ln_in["desc"]["najva_person"].format(
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
            message_text=ln_in["text"]["najva_all"],
            parse_mode="HTML",
            disable_web_page_preview=False,
        )
        item1 = InlineQueryResultArticle(
            id=f"najvaA:{user_id}",
            title=ln_in["title"]["najva_all"],
            description=ln_in["desc"]["najva_all"].format(len(text)),
            thumb_url=pic_all,
            thumb_width=512,
            thumb_height=512,
            input_message_content=input_content,
            reply_markup=inlineKeys,
        )
        input_content = InputTextMessageContent(
            message_text=ln_in["text"]["najva_all2"],
            parse_mode="HTML",
            disable_web_page_preview=False,
        )
        item2 = InlineQueryResultArticle(
            id=f"najvaA2:{user_id}",
            title=ln_in["title"]["najva_all"],
            description=ln_in["desc"]["najva_all2"].format(
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
        set_desc = ln_in["desc"]
        if DataBase.hget(f"setting_najva:{user_id}", "seen"):
            seen = langU["is_power_on"]
            title1 = ln_in["title"]["power_off"]
            photo1 = pic_tick
        else:
            seen = langU["is_power_off"]
            title1 = ln_in["title"]["power_on"]
            photo1 = pic_cross
        seen = set_desc["najva_seen"].format(seen)
        if DataBase.hget(f"setting_najva:{user_id}", "recv"):
            recv = langU["is_power_on"]
            title2 = ln_in["title"]["power_off"]
            photo2 = pic_tick
        else:
            recv = langU["is_power_off"]
            title2 = ln_in["title"]["power_on"]
            photo2 = pic_cross
        recv = set_desc["najva_recv"].format(recv)
        if DataBase.hget(f"setting_najva:{user_id}", "encrypt"):
            encrypt = langU["is_power_on"]
            title3 = ln_in["title"]["power_off"]
            photo3 = pic_tick
        else:
            encrypt = langU["is_power_off"]
            title3 = ln_in["title"]["power_on"]
            photo3 = pic_cross
        encrypt = set_desc["najva_encrypt"].format(encrypt)
        if DataBase.hget(f"setting_najva:{user_id}", "noname"):
            noname = langU["is_power_on"]
            title4 = ln_in["title"]["power_off"]
            photo4 = pic_tick
        else:
            noname = langU["is_power_off"]
            title4 = ln_in["title"]["power_on"]
            photo4 = pic_cross
        noname = set_desc["najva_noname"].format(noname)
        if DataBase.hget(f"setting_najva:{user_id}", "dispo"):
            dispo = langU["is_power_on"]
            title5 = ln_in["title"]["power_off"]
            photo5 = pic_tick
        else:
            dispo = langU["is_power_off"]
            title5 = ln_in["title"]["power_on"]
            photo5 = pic_cross
        dispo = set_desc["najva_dispo"].format(dispo)
        inlineKeys = iMarkup()
        inlineKeys.add(
            iButtun(
                buttuns["quick_set"], switch_inline_query_current_chat="set"
            )
        )
        input_content = InputTextMessageContent(
            message_text=ln_in["text"]["setting_changed"],
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
            ln_in["title"]["all_set"],
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
            message_text=ln_in["text"]["najva_reply"],
            parse_mode="HTML",
            disable_web_page_preview=True,
        )
        item1 = InlineQueryResultArticle(
            id=f"najvaR:{user_id}",
            title=ln_in["title"]["najva_reply"],
            description=ln_in["desc"]["najva_reply"],
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
            message_text=ln_in["text"]["najva_havn_text"],
            parse_mode="HTML",
            disable_web_page_preview=True,
        )
        item2 = InlineQueryResultArticle(
            id="null",
            title=ln_in["title"]["najva_havn_text"],
            description=ln_in["desc"]["najva_havn_text"],
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
            message_text=ln_in["text"]["najva_special"].format(
                name_user2 or name_user
            ),
            parse_mode="HTML",
            disable_web_page_preview=True,
        )
        item1 = InlineQueryResultArticle(
            id=f"najvaS:{user_id}",
            title=ln_in["title"]["najva_special"].format(name_user),
            description=ln_in["desc"]["najva_special"],
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
                message_text=ln_in["text"]["special_404"],
                parse_mode="HTML",
                disable_web_page_preview=True,
            )
            item1 = InlineQueryResultArticle(
                id="null",
                title=ln_in["title"]["special_404"],
                description=ln_in["desc"]["special_404"],
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
                    lang[lang_user(from_user)]["speical_najva_seen"].format(
                        msg.from_user.first_name
                    ),
                )
                await editText(
                    inline_msg_id=special_msgID,
                    text=lang[lang_user(from_user)]["speical_najva_seen2"].format(
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
            message_text=ln_in["text"]["najva_havn_text"],
            parse_mode="HTML",
            disable_web_page_preview=True,
        )
        item2 = InlineQueryResultArticle(
            id="null",
            title=ln_in["title"]["najva_havn_text"],
            description=ln_in["desc"]["najva_havn_text"],
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
                message_text=ln_in["text"]["najva_special"].format(
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
                title=ln_in["title"]["najva_special"].format(
                    name_user
                ),
                description=ln_in["desc"]["najva_special"],
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
