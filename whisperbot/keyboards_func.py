from aiogram.types import (
    InlineKeyboardMarkup as iMarkup,
    InlineKeyboardButton as iButtun
)
from core_file import (
	GlobalValues,
    user_steps,
    DataBase,
	lang,
    bot,
    rds,
    re
)
from config_bot import (
	IDs_datas,
	db
)
from whisperbot.lateral_func import (
    local_id_user,
    userInfos,
    lang_user,
    isSudo
)


def start_keys(UserID):
    hash = ":@{}".format(UserID)
    langU = lang[lang_user(UserID)]
    inlineKeys = iMarkup()
    inlineKeys.add(
        iButtun(
            langU["buttuns"]["whisper_section"],
            callback_data="whisper{}".format(hash),
        ),
        iButtun(
            langU["buttuns"]["anon_section"],
            callback_data="anon{}".format(hash),
        ),
    )
    inlineKeys.add(
        iButtun(
            langU["buttuns"]["support"], callback_data="supp{}".format(hash)
        ),
        iButtun(
            langU["buttuns"]["language"],
            callback_data="language{}".format(hash),
        ),
    )
    inlineKeys.add(
        iButtun(
            langU["buttuns"]["adsfree"], callback_data="adsfree{}".format(hash)
        ),
    )
    if isSudo(UserID):
        inlineKeys.add(
            iButtun(
                langU["buttuns"]["list_block"],
                callback_data="list:block:0{}".format(hash),
            ),
            iButtun(
                langU["buttuns"]["stats"],
                callback_data="list:stats:0{}".format(hash),
            ),
        )
        inlineKeys.add(
            iButtun(
                langU["buttuns"]["force_join"].format(
                    rplac_tick(DataBase.get("force_join"))
                ),
                callback_data="forcejoin",
            ),
        )
    # inlineKeys.add(
        # iButtun(
            # langU["buttuns"]["channel"],
            # url="https://t.me/{}".format(IDs_datas["chUsername"]),
        # ),
    # )
    return inlineKeys


def back_keys(UserID):
    hash = ":@{}".format(UserID)
    langU = lang[lang_user(UserID)]
    inlineKeys = iMarkup()
    inlineKeys.add(
        iButtun(
            langU["buttuns"]["back"], callback_data="backstart{}".format(hash)
        ),
    )
    return inlineKeys


def settings_keys(UserID, arg2=None):
    hash = ":@{}".format(UserID)
    langU = lang[lang_user(UserID)]
    buttuns = langU["buttuns"]
    inlineKeys = iMarkup()
    inlineKeys.add(iButtun("زبان/language/Sprache", callback_data="nil"))
    if (arg2 or user_steps[UserID]["lang"]) == "fa":
        status1 = "✅"
    else:
        status1 = ""
    if (arg2 or user_steps[UserID]["lang"]) == "en":
        status2 = "✅"
    else:
        status2 = ""
    if (arg2 or user_steps[UserID]["lang"]) == "de":
        status3 = "✅"
    else:
        status3 = ""
    inlineKeys.add(
        iButtun(
            "{}English🇺🇸".format(status2),
            callback_data="set_lang_en{}".format(hash),
        ),
        iButtun(
            "{}پارسی🇮🇷".format(status1),
            callback_data="set_lang_fa{}".format(hash),
        ),
    )
    inlineKeys.add(
        iButtun(
            "{}Deutsch🇩🇪".format(status3),
            callback_data="set_lang_de{}".format(hash),
        ),
    )
    if arg2:
        inlineKeys.add(
            iButtun(
                lang[arg2]["buttuns"]["back"],
                callback_data="backstart{}".format(hash),
            )
        )
    else:
        inlineKeys.add(
            iButtun(buttuns["back"], callback_data="backstart{}".format(hash))
        )
    return inlineKeys


def anonymous_keys(UserID):
    hash = ":@{}".format(UserID)
    langU = lang[lang_user(UserID)]
    buttuns = langU["buttuns"]
    if DataBase.get("dont_receive_anon:{}".format(UserID)):
        status_receive = "❌"
    else:
        status_receive = "✅"
    if DataBase.get("anti_save.anon:{}".format(UserID)):
        status_lock = "✅"
    else:
        status_lock = "❌"
    blocks_number = DataBase.scard("blocks:{}".format(UserID))
    inlineKeys = iMarkup()
    if status_receive == "✅":
        inlineKeys.add(
            iButtun(
                buttuns["link_my_anon"],
                callback_data="anon:link{}".format(hash),
            ),
            iButtun(
                buttuns["help_my_anon"],
                callback_data="anon:help{}".format(hash),
            ),
        )
        inlineKeys.add(
            iButtun(
                buttuns["stats_my_anon"],
                callback_data="anon:stats{}".format(hash),
            ),
            iButtun(
                buttuns["name_my_anon"],
                callback_data="anon:name{}".format(hash),
            ),
        )
        inlineKeys.add(
            iButtun(
                buttuns["send_persion_anon"],
                callback_data="anon:send{}".format(hash),
            ),
        )
        inlineKeys.add(
            iButtun(
                buttuns["anti_save"].format(status_lock),
                callback_data="anon:lock{}".format(hash),
            ),
        )
    inlineKeys.add(
        iButtun(
            buttuns["receive_my_anon"].format(status_receive),
            callback_data="anon:receive{}".format(hash),
        ),
    )
    if status_receive == "✅":
        inlineKeys.add(
            iButtun(
                buttuns["blocks_my_anon"].format(blocks_number),
                callback_data="anon:myblock{}".format(hash),
            ),
        )
    inlineKeys.add(
        iButtun(buttuns["back"], callback_data="backstart{}".format(hash))
    )
    return inlineKeys


def anonymous_my_link_keys(UserID):
    hash = ":@{}".format(UserID)
    langU = lang[lang_user(UserID)]
    buttuns = langU["buttuns"]
    share_text_anon = langU["share_text_anon"].format(GlobalValues().botName)
    link_anon = DataBase.get("link_anon:{}".format(UserID))
    inlineKeys = iMarkup()
    inlineKeys.add(
        iButtun(
            buttuns["customize_link_anon"],
            callback_data="anon:cus{}".format(hash),
        ),
        iButtun(
            buttuns["share_link_anon"],
            url=f"https://t.me/share/url?text={share_text_anon}&url=t.me/{GlobalValues().botUser}?start={link_anon}",
        ),
    )
    inlineKeys.add(
        iButtun(
            buttuns["insta_link_anon"],
            callback_data="anon:insta{}".format(hash),
        )
    )
    inlineKeys.add(
        iButtun(
            buttuns["telg_link_anon"], callback_data="anon:telg{}".format(hash)
        ),
    )
    inlineKeys.add(
        iButtun(buttuns["back_anon"], callback_data="anon{}".format(hash))
    )
    return inlineKeys


def anonymous_cus_link_keys(UserID):
    hash = ":@{}".format(UserID)
    langU = lang[lang_user(UserID)]
    buttuns = langU["buttuns"]
    inlineKeys = iMarkup()
    inlineKeys.add(
        iButtun(
            buttuns["default_link_anon"],
            callback_data="anon:change{}".format(hash),
        ),
    )
    inlineKeys.add(
        iButtun(
            buttuns["back_link_anon"], callback_data="anon:link{}".format(hash)
        )
    )
    return inlineKeys


def anonymous_insta_link_keys(UserID):
    hash = ":@{}".format(UserID)
    langU = lang[lang_user(UserID)]
    buttuns = langU["buttuns"]
    inlineKeys = iMarkup()
    inlineKeys.add(
        iButtun(
            buttuns["back_link_anon"], callback_data="anon:link{}".format(hash)
        )
    )
    return inlineKeys


def anonymous_help_keys(UserID):
    hash = ":@{}".format(UserID)
    langU = lang[lang_user(UserID)]
    buttuns = langU["buttuns"]
    inlineKeys = iMarkup()
    inlineKeys.add(
        iButtun(
            buttuns["help1_anon"], callback_data="anon:help1{}".format(hash)
        ),
    )
    inlineKeys.add(
        iButtun(
            buttuns["help2_anon"], callback_data="anon:help2{}".format(hash)
        ),
    )
    inlineKeys.add(
        iButtun(
            buttuns["help3_anon"], callback_data="anon:help3{}".format(hash)
        ),
    )
    inlineKeys.add(
        iButtun(
            buttuns["help4_anon"], callback_data="anon:help4{}".format(hash)
        ),
    )
    inlineKeys.add(
        iButtun(buttuns["back_anon"], callback_data="anon{}".format(hash))
    )
    return inlineKeys


def anonymous_back_keys(UserID):
    hash = ":@{}".format(UserID)
    langU = lang[lang_user(UserID)]
    buttuns = langU["buttuns"]
    inlineKeys = iMarkup()
    inlineKeys.add(
        iButtun(buttuns["back_anon"], callback_data="anon{}".format(hash))
    )
    return inlineKeys


def anonymous_send_again_keys(UserID, which_user):
    id_to_token = local_id_user(user_id=which_user)
    hash = ":{}:@{}".format(id_to_token, UserID)
    langU = lang[lang_user(UserID)]
    buttuns = langU["buttuns"]
    inlineKeys = iMarkup()
    inlineKeys.add(
        iButtun(
            buttuns["send_more"], callback_data="anon:sendmore{}".format(hash)
        )
    )
    return inlineKeys


def anonymous_name_keys(UserID):
    hash = ":@{}".format(UserID)
    langU = lang[lang_user(UserID)]
    buttuns = langU["buttuns"]
    inlineKeys = iMarkup()
    inlineKeys.add(
        iButtun(
            buttuns["cus_name_anon"],
            callback_data="anon:cus_name{}".format(hash),
        ),
    )
    inlineKeys.add(
        iButtun(
            buttuns["default_name_anon"],
            callback_data="anon:default_name{}".format(hash),
        ),
    )
    inlineKeys.add(
        iButtun(buttuns["back_anon"], callback_data="anon{}".format(hash))
    )
    return inlineKeys


def anonymous_cus_name_keys(UserID):
    hash = ":@{}".format(UserID)
    langU = lang[lang_user(UserID)]
    buttuns = langU["buttuns"]
    inlineKeys = iMarkup()
    inlineKeys.add(
        iButtun(buttuns["cancel"], callback_data="anon:name{}".format(hash))
    )
    return inlineKeys


def anonymous_new_message_keys(
    UserID, TO_USER, MSG_ID, SHOW_SENDER, SENT_TIME
):
    token_user = TO_USER
    token_to_id = local_id_user(uniq_id=token_user)
    hash = ":{}:{}:{}:@{}".format(TO_USER, MSG_ID, SENT_TIME, UserID)
    langU = lang[lang_user(UserID)]
    buttuns = langU["buttuns"]
    if DataBase.sismember("blocks:{}".format(UserID), token_to_id):
        buttun1 = buttuns["unblock"]
    else:
        buttun1 = buttuns["block"]
    inlineKeys = iMarkup()
    inlineKeys.add(
        iButtun(buttun1, callback_data="anon:b{}".format(hash)),
        iButtun(buttuns["reply"], callback_data="anon:r{}".format(hash)),
    )
    if SHOW_SENDER:
        inlineKeys.add(
            iButtun(
                "{} {}".format(
                    buttuns["from_who"],
                    DataBase.get("name_anon2:{}".format(SHOW_SENDER)),
                ),
                callback_data="none:yes",
            )
        )
    else:
        inlineKeys.add(iButtun(buttuns["from_who2"], callback_data="none:no"))
    inlineKeys.add(
        iButtun(
            buttuns["sent_time"], callback_data="anon:t{}".format(hash.replace(f":{TO_USER}:{MSG_ID}", ""))
        )
    )
    return inlineKeys


def anonymous_delete_blocks_keys(UserID):
    hash = ":@{}".format(UserID)
    langU = lang[lang_user(UserID)]
    buttuns = langU["buttuns"]
    inlineKeys = iMarkup()
    inlineKeys.add(
        iButtun(buttuns["yes"], callback_data="anon:delblocks{}".format(hash)),
        iButtun(buttuns["no"], callback_data="anon{}".format(hash)),
    )
    inlineKeys.add(
        iButtun(buttuns["back_anon"], callback_data="anon{}".format(hash))
    )
    return inlineKeys


def whisper_keys(UserID):
    hash = ":@{}".format(UserID)
    langU = lang[lang_user(UserID)]
    buttuns = langU["buttuns"]
    inlineKeys = iMarkup()
    inlineKeys.add(
        iButtun(
            buttuns["settings"], callback_data="whisper:settings{}".format(hash)
        ),
        iButtun(buttuns["help"], callback_data="whisper:help{}".format(hash)),
    )
    inlineKeys.add(
        iButtun(buttuns["back"], callback_data="backstart{}".format(hash))
    )
    return inlineKeys


def rplac_tick(text):
    return (
        str(text).replace("None", "❌").replace("True", "✅").replace("1", "✅")
    )


def whisper_settings_keys(UserID):
    hash = ":@{}".format(UserID)
    langU = lang[lang_user(UserID)]
    buttuns = langU["buttuns"]
    inlineKeys = iMarkup()
    inlineKeys.add(
        iButtun(
            buttuns["whisper_settings_recents"].format(
                DataBase.scard(f"whisper_recent:{UserID}")
                + DataBase.scard(f"whisper_recent2:{UserID}")
            ),
            callback_data="whisper:settings:recents{}".format(hash),
        ),
    )
    inlineKeys.add(
        iButtun(
            buttuns["whisper_settings_notif_seen"].format(
                rplac_tick(DataBase.hget(f"setting_whisper:{UserID}", "seen"))
            ),
            callback_data="whisper:settings1:seen{}".format(hash),
        ),
    )
    inlineKeys.add(
        iButtun(
            buttuns["whisper_settings_notif_recv"].format(
                rplac_tick(DataBase.hget(f"setting_whisper:{UserID}", "recv"))
            ),
            callback_data="whisper:settings1:recv{}".format(hash),
        ),
    )
    inlineKeys.add(
        iButtun(
            buttuns["whisper_settings_encrypt"].format(
                rplac_tick(DataBase.hget(f"setting_whisper:{UserID}", "encrypt"))
            ),
            callback_data="whisper:settings1:encrypt{}".format(hash),
        ),
    )
    inlineKeys.add(
        iButtun(
            buttuns["whisper_settings_no_name"].format(
                rplac_tick(DataBase.hget(f"setting_whisper:{UserID}", "noname"))
            ),
            callback_data="whisper:settings1:noname{}".format(hash),
        ),
    )
    inlineKeys.add(
        iButtun(
            buttuns["whisper_settings_disposable"].format(
                rplac_tick(DataBase.hget(f"setting_whisper:{UserID}", "dispo"))
            ),
            callback_data="whisper:settings1:dispo{}".format(hash),
        ),
    )
    inlineKeys.add(
        iButtun(
            buttuns["whisper_settings_antisave"].format(
                rplac_tick(DataBase.hget(f"setting_whisper:{UserID}", "antisave"))
            ),
            callback_data="whisper:settings1:antisave{}".format(hash),
        ),
    )
    if DataBase.hget(f"setting_whisper:{UserID}", "autodel"):
        time_del = buttuns["minute"].format(
            DataBase.get(f"autodel_time:{UserID}") or 10
        )
    else:
        time_del = rplac_tick(
            DataBase.hget(f"setting_whisper:{UserID}", "autodel")
        )
    inlineKeys.add(
        iButtun(
            buttuns["whisper_settings_auto_del"].format(time_del),
            callback_data="whisper:settings1:autodel{}".format(hash),
        ),
    )
    inlineKeys.add(
        iButtun(
            buttuns["whisper_settings_block"].format(
                DataBase.scard(f"blocks2:{UserID}")
            ),
            callback_data="whisper:settings:blocks{}".format(hash),
        ),
    )
    inlineKeys.add(
        iButtun(
            buttuns["whisper_settings_del_all"],
            callback_data="whisper:settings:delall{}".format(hash),
        ),
    )
    inlineKeys.add(
        iButtun(buttuns["back_whisper"], callback_data="whisper{}".format(hash))
    )
    return inlineKeys


def whisper_recent_user_keys(uname_user, name_user, user_ID, UserID):
    langU = lang[lang_user(UserID)]
    buttuns = langU["buttuns"]
    inlineKeys = iMarkup()
    if uname_user:
        call_url = "https://t.me/{}".format(uname_user)
    else:
        call_url = "https://t.me?openmessage?user_id={}".format(user_ID)
    if DataBase.sismember(f"blocks2:{UserID}", user_ID):
        buttun1 = buttuns["unblock"]
    else:
        buttun1 = buttuns["block"]
    inlineKeys.add(
        iButtun(name_user, call_url),
    )
    inlineKeys.add(
        iButtun(
            buttun1,
            callback_data=f"recent:{user_ID}:b:@{UserID}",
        ),
    )
    inlineKeys.add(
        iButtun(
            buttuns["delete"],
            callback_data=f"recent:{user_ID}:y:@{UserID}",
        ),
    )
    inlineKeys.add(
        iButtun(
            buttuns["back_nrec"],
            callback_data=f"whisper:settings:recents:@{UserID}",
        ),
    )
    return inlineKeys


def whisper_delall_keys(UserID):
    hash = ":@{}".format(UserID)
    langU = lang[lang_user(UserID)]
    buttuns = langU["buttuns"]
    inlineKeys = iMarkup()
    inlineKeys.add(
        iButtun(
            buttuns["yes"],
            callback_data="whisper:delall:y{}".format(hash),
        ),
        iButtun(
            buttuns["no"],
            callback_data="whisper:settings{}".format(hash),
        ),
    )
    return inlineKeys
    
def whisper_help_keys(UserID):
    hash = ":@{}".format(UserID)
    langU = lang[lang_user(UserID)]
    buttuns = langU["buttuns"]
    inlineKeys = iMarkup()
    inlineKeys.add(
        iButtun(
            buttuns["whisper_help_send"],
            callback_data="whisper:help:send{}".format(hash),
        ),
    )
    inlineKeys.add(
        iButtun(
            buttuns["whisper_help_media"],
            callback_data="whisper:help:media{}".format(hash),
        ),
    )
    inlineKeys.add(
        iButtun(
            buttuns["whisper_help_group"],
            callback_data="whisper:help:group{}".format(hash),
        ),
    )
    inlineKeys.add(
        iButtun(
            buttuns["whisper_help_broadcast"],
            callback_data="whisper:help:bd{}".format(hash),
        ),
    )
    inlineKeys.add(
        iButtun(
            buttuns["whisper_help_noid"],
            callback_data="whisper:help:noid{}".format(hash),
        ),
    )
    inlineKeys.add(
        iButtun(
            buttuns["whisper_help_short_set"],
            callback_data="whisper:help:shset{}".format(hash),
        ),
    )
    inlineKeys.add(
        iButtun(
            buttuns["whisper_help_prob"],
            callback_data="whisper:help:prob{}".format(hash),
        ),
    )
    inlineKeys.add(
        iButtun(
            buttuns["whisper_help_examp"],
            callback_data="whisper:help:examp{}".format(hash),
        ),
    )
    inlineKeys.add(
        iButtun(buttuns["back_whisper"], callback_data="whisper{}".format(hash))
    )
    return inlineKeys


def whisper_help1_keys(UserID):
    hash = ":@{}".format(UserID)
    langU = lang[lang_user(UserID)]
    buttuns = langU["buttuns"]
    inlineKeys = iMarkup()
    inlineKeys.add(
        iButtun(
            buttuns["whisper_help_noid"],
            callback_data="whisper:help:noid{}".format(hash),
        )
    )
    # inlineKeys.add(
        # iButtun(
            # buttuns["helper_video"], callback_data="whisper:vid:1{}".format(hash)
        # )
    # )
    inlineKeys.add(
        iButtun(
            buttuns["example"],
            switch_inline_query="{} {}".format(UserID, buttuns["example"]),
        )
    )
    inlineKeys.add(
        iButtun(
            buttuns["back_help_whisper"],
            callback_data="whisper:help{}".format(hash),
        )
    )
    return inlineKeys


def whisper_help2_keys(UserID):
    hash = ":@{}".format(UserID)
    langU = lang[lang_user(UserID)]
    buttuns = langU["buttuns"]
    inlineKeys = iMarkup()
    # inlineKeys.add(
        # iButtun(
            # buttuns["helper_video"], callback_data="whisper:vid:2{}".format(hash)
        # )
    # )
    inlineKeys.add(
        iButtun(buttuns["example"], switch_inline_query="{}".format(UserID))
    )
    inlineKeys.add(
        iButtun(
            buttuns["back_help_whisper"],
            callback_data="whisper:help{}".format(hash),
        )
    )
    return inlineKeys


def whisper_help3_keys(UserID):
    hash = ":@{}".format(UserID)
    langU = lang[lang_user(UserID)]
    buttuns = langU["buttuns"]
    inlineKeys = iMarkup()
    inlineKeys.add(
        iButtun(
            buttuns["example"],
            switch_inline_query="{} @user1 @user2 {}".format(
                UserID, buttuns["example"]
            ),
        )
    )
    inlineKeys.add(
        iButtun(
            buttuns["back_help_whisper"],
            callback_data="whisper:help{}".format(hash),
        )
    )
    return inlineKeys


def whisper_help4_keys(UserID):
    hash = ":@{}".format(UserID)
    langU = lang[lang_user(UserID)]
    buttuns = langU["buttuns"]
    inlineKeys = iMarkup()
    inlineKeys.add(
        iButtun(
            buttuns["example"],
            switch_inline_query="@All {}".format(buttuns["example"]),
        )
    )
    inlineKeys.add(
        iButtun(
            buttuns["back_help_whisper"],
            callback_data="whisper:help{}".format(hash),
        )
    )
    return inlineKeys


def whisper_help5_keys(UserID):
    hash = ":@{}".format(UserID)
    langU = lang[lang_user(UserID)]
    buttuns = langU["buttuns"]
    inlineKeys = iMarkup()
    inlineKeys.add(
        iButtun(
            buttuns["helper_reply"], callback_data="whisper:vid:5{}".format(hash)
        )
    )
    inlineKeys.add(
        iButtun(
            buttuns["back_help_whisper"],
            callback_data="whisper:help{}".format(hash),
        )
    )
    return inlineKeys


def whisper_help6_keys(UserID):
    hash = ":@{}".format(UserID)
    langU = lang[lang_user(UserID)]
    buttuns = langU["buttuns"]
    inlineKeys = iMarkup()
    inlineKeys.add(iButtun(buttuns["example"], switch_inline_query="set"))
    inlineKeys.add(
        iButtun(
            buttuns["back_help_whisper"],
            callback_data="whisper:help{}".format(hash),
        )
    )
    return inlineKeys


def whisper_help7_keys(UserID):
    hash = ":@{}".format(UserID)
    langU = lang[lang_user(UserID)]
    buttuns = langU["buttuns"]
    inlineKeys = iMarkup()
    inlineKeys.add(
        iButtun(
            buttuns["back_help_whisper"],
            callback_data="whisper:help{}".format(hash),
        )
    )
    return inlineKeys


def whisper_help8_keys(UserID):
    hash = ":@{}".format(UserID)
    langU = lang[lang_user(UserID)]
    buttuns = langU["buttuns"]
    inlineKeys = iMarkup()
    inlineKeys.add(
        iButtun(
            buttuns["example_whisper"],
            switch_inline_query="{} {}".format(UserID, buttuns["example"]),
        )
    )
    inlineKeys.add(
        iButtun(
            buttuns["example_group"],
            switch_inline_query="{} @user1 @user2 {}".format(
                UserID, buttuns["example"]
            ),
        )
    )
    inlineKeys.add(
        iButtun(buttuns["example_special"], switch_inline_query=UserID)
    )
    inlineKeys.add(iButtun(buttuns["example_myid"], switch_inline_query="me"))
    inlineKeys.add(
        iButtun(buttuns["example_set_shcut"], switch_inline_query="set")
    )
    inlineKeys.add(
        iButtun(
            buttuns["back_help_whisper"],
            callback_data="whisper:help{}".format(hash),
        )
    )
    return inlineKeys


def whisper_help9_keys(UserID):
    hash = ":@{}".format(UserID)
    langU = lang[lang_user(UserID)]
    buttuns = langU["buttuns"]
    inlineKeys = iMarkup()
    inlineKeys.add(
        iButtun(
            buttuns["helper_install"],
            callback_data="whisper:vid:6{}".format(hash),
        )
    )
    inlineKeys.add(
        iButtun(
            buttuns["back_help_whisper"],
            callback_data="whisper:help{}".format(hash),
        )
    )
    return inlineKeys


def whisper_autodel_keys(UserID):
    hash = ":@{}".format(UserID)
    langU = lang[lang_user(UserID)]
    buttuns = langU["buttuns"]
    inlineKeys = iMarkup()
    inlineKeys.add(
        iButtun(
            buttuns["whisper_settings_auto_del"].format(
                rplac_tick(DataBase.hget(f"setting_whisper:{UserID}", "autodel"))
            ),
            callback_data="whisper:autodel{}".format(hash),
        )
    )
    inlineKeys.add(
        iButtun(
            buttuns["back_nset"], callback_data="whisper:settings{}".format(hash)
        )
    )
    return inlineKeys


def whisper_autodel2_keys(UserID):
    hash = ":@{}".format(UserID)
    langU = lang[lang_user(UserID)]
    buttuns = langU["buttuns"]
    inlineKeys = iMarkup(row_width=6)
    inlineKeys.add(
        iButtun(
            buttuns["whisper_settings_auto_del"].format(
                rplac_tick(DataBase.hget(f"setting_whisper:{UserID}", "autodel"))
            ),
            callback_data="whisper:autodel{}".format(hash),
        )
    )
    inlineKeys.add(
        iButtun(
            buttuns["autodel_status"].format(
                DataBase.get(f"autodel_time:{UserID}")
            ),
            callback_data="none",
        )
    )
    inlineKeys.add(
        iButtun("-1", callback_data="autodel:-1{}".format(hash)),
        iButtun("-5", callback_data="autodel:-5{}".format(hash)),
        iButtun("-10", callback_data="autodel:-10{}".format(hash)),
        iButtun("+1", callback_data="autodel:+1{}".format(hash)),
        iButtun("+5", callback_data="autodel:+5{}".format(hash)),
        iButtun("+10", callback_data="autodel:+10{}".format(hash)),
    )
    inlineKeys.add(
        iButtun(
            buttuns["back_nset"], callback_data="whisper:settings{}".format(hash)
        ),
    )
    return inlineKeys


def whisper_seen_keys(UserID, from_user, time_data):
    hash = ":{}:{}".format(from_user, time_data)
    langU = lang[lang_user(from_user)]
    buttuns = langU["buttuns"]
    inlineKeys = iMarkup(row_width=3)
    inlineKeys.add(
        iButtun(buttuns["stats"], callback_data="showS{}".format(hash)),
        iButtun(buttuns["show_whisper"], callback_data="showN{}".format(hash)),
        iButtun(buttuns["delete"], callback_data="delWhisper{}".format(hash)),
    )
    return inlineKeys


def whisper_seen2_keys(UserID, from_user, time_data):
    hash = ":{}:{}".format(from_user, time_data)
    langU = lang[lang_user(UserID)]
    buttuns = langU["buttuns"]
    inlineKeys = iMarkup()
    inlineKeys.add(
        iButtun(buttuns["stats"], callback_data="showS{}".format(hash)),
    )
    return inlineKeys


def whisper_seen3_keys(from_user, time_data):
    hash = ":{}:{}".format(from_user, time_data)
    langU = lang[lang_user(from_user)]
    buttuns = langU["buttuns"]
    inlineKeys = iMarkup()
    inlineKeys.add(
        iButtun(buttuns["delete"], callback_data="delWhisper{}".format(hash)),
        iButtun(buttuns["stats"], callback_data="showS{}".format(hash)),
    )
    ads = DataBase.get("have_ads")
    if ads:
        inlineKeys.add(
            iButtun(
                DataBase.hget("info_ads", "buttuns"),
                url=DataBase.hget("info_ads", "url"),
            )
        )
    return inlineKeys


def register_special_keys(UserID):
    hash = ":@{}".format(UserID)
    langU = lang[lang_user(UserID)]
    buttuns = langU["buttuns"]
    inlineKeys = iMarkup()
    inlineKeys.add(
        iButtun(
            buttuns["anti_save"].format(
                rplac_tick(
                    DataBase.hget(f"setting_whisper:{UserID}", "antisave")
                )
            ),
            callback_data="special:antisave{}".format(hash),
        )
    )
    inlineKeys.add(
        iButtun(
            buttuns["send_pv"], callback_data="special:sendpv{}".format(hash)
        ),
    )
    inlineKeys.add(
        iButtun(
            buttuns["reg_whisper"], callback_data="special:reg1{}".format(hash)
        ),
        iButtun(
            buttuns["reg2_whisper"], callback_data="special:reg2{}".format(hash)
        ),
    )
    inlineKeys.add(
        iButtun(
            buttuns["cancel"], callback_data="special:cancel{}".format(hash)
        ),
    )
    return inlineKeys


async def show_speical_whisper_keys(UserID, from_user):
    hash2 = ":{}:@{}".format(from_user, UserID)
    langU = lang[lang_user(UserID)]
    buttuns = langU["buttuns"]
    inlineKeys = iMarkup()
    name_user = await userInfos(from_user, info="name")
    uname_user = await userInfos(from_user, info="username")
    if uname_user:
        call_url = "https://t.me/{}".format(uname_user)
    else:
        call_url = "https://t.me?openmessage?user_id={}".format(from_user)
    if DataBase.sismember("blocks2:{}".format(UserID), from_user):
        which_one = buttuns["unblock"]
    else:
        which_one = buttuns["block"]
    inlineKeys.add(
        iButtun(buttuns["special_whisper"], callback_data="none"),
        iButtun(name_user, url=call_url),
    )
    inlineKeys.add(
        iButtun(
            buttuns["report"], callback_data="special:report{}".format(hash2)
        ),
        iButtun(which_one, callback_data="special:block{}".format(hash2)),
    )
    return inlineKeys


async def show_speical_whisper2_keys(UserID, from_user):
    hash2 = ":{}:@{}".format(from_user, UserID)
    langU = lang[lang_user(UserID)]
    buttuns = langU["buttuns"]
    inlineKeys = iMarkup()
    name_user = await userInfos(from_user, info="name")
    uname_user = await userInfos(from_user, info="username")
    if uname_user:
        call_url = "https://t.me/{}".format(uname_user)
    else:
        call_url = "https://t.me?openmessage?user_id={}".format(from_user)
    if DataBase.sismember("blocks2:{}".format(UserID), from_user):
        which_one = buttuns["unblock"]
    else:
        which_one = buttuns["block"]
    inlineKeys.add(
        iButtun(buttuns["special_whisper"], callback_data="none"),
        iButtun(name_user, url=call_url),
    )
    return inlineKeys


def report_whisper_keys(UserID, from_user, reply_id):
    hash2 = ":{}:{}:@{}".format(from_user, reply_id, UserID)
    langU = lang[lang_user(UserID)]
    buttuns = langU["buttuns"]
    inlineKeys = iMarkup()
    inlineKeys.add(
        iButtun(
            buttuns["report"], callback_data="special:report2{}".format(hash2)
        ),
    )
    inlineKeys.add(
        iButtun(
            buttuns["cancel"], callback_data="report:cancel{}".format(hash2)
        ),
    )
    return inlineKeys


def ban_user_keys(UserID, user_ID):
    langU = lang[lang_user(user_ID)]
    buttuns = langU["buttuns"]
    inlineKeys = iMarkup()
    if DataBase.sismember("isBanned", UserID):
        which_one = buttuns["unban_user"]
    else:
        which_one = buttuns["ban_user"]
    inlineKeys.add(
        iButtun(which_one, callback_data="banuser:{}".format(UserID)),
    )
    return inlineKeys


def support_keys(UserID):
    hash = ":@{}".format(UserID)
    langU = lang[lang_user(UserID)]
    buttuns = langU["buttuns"]
    inlineKeys = iMarkup()
    inlineKeys.add(
        iButtun(
            buttuns["help_whisper"], callback_data="whisper:help{}".format(hash)
        )
    )
    inlineKeys.add(
        iButtun(
            buttuns["help_my_anon2"], callback_data="anon:help{}".format(hash)
        )
    )
    inlineKeys.add(
        iButtun(buttuns["support2"], callback_data="support{}".format(hash))
    )
    inlineKeys.add(
        iButtun(buttuns["back"], callback_data="backstart{}".format(hash))
    )
    return inlineKeys
