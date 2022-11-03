from config_bot2 import rds, sudo_users, bot, re
import aiogram.utils.exceptions as expts
from aiogram import types


async def userInfos(userID, info="name"):
    if userID:
        if rds.hget("userInfo:{}".format(userID), info):
            return rds.hget("userInfo:{}".format(userID), info)
        elif rds.get("userInfo2:{}".format(userID)):
            return rds.get("userInfo2:{}".format(userID))
        else:
            try:
                b = await client.get_entity(int(userID))
                b = b.__dict__
                if info == "name":
                    if "title" in b:
                        if re.match(r"^100(\d+)", userID):
                            rds.hset(
                                "userInfo:-{}".format(userID),
                                "name",
                                b["title"],
                            )
                        elif re.match(r"^-100(\d+)", userID):
                            rds.hset(
                                "userInfo:{}".format(userID),
                                "name",
                                b["title"],
                            )
                        else:
                            rds.hset(
                                "userInfo:{}".format(userID),
                                "name",
                                b["title"],
                            )
                        return b["title"]
                    elif "first_name" in b:
                        rds.hset(
                            "userInfo:{}".format(userID),
                            "name",
                            b["first_name"],
                        )
                        return b["first_name"]
                    elif b["first_name"] == "":
                        return "Deleted Account"
                    else:
                        return "Deleted"
                elif info == "username":
                    if "username" in b:
                        rds.hset(
                            "userInfo:{}".format(userID),
                            "username",
                            b["username"],
                        )
                        if "title" in b or "megagroup" in b:
                            if re.match(r"^100(\d+)", userID):
                                rds.hset(
                                    "UsernamesIds",
                                    b["username"].lower(),
                                    "-{}".format(userID),
                                )
                            elif re.match(r"^-100(\d+)", userID):
                                rds.hset(
                                    "UsernamesIds",
                                    b["username"].lower(),
                                    userID,
                                )
                        else:
                            rds.hset(
                                "UsernamesIds", b["username"].lower(), userID
                            )
                        return b["username"]
                    else:
                        return False
            except:
                if str(userID).isdigit():
                    rds.setex("userInfo2:{}".format(userID), 86400, userID)
                    return int(userID)
                else:
                    return userID
    else:
        return "!!!"


async def userIds(username):
    # if username:match("@"):
    username = username.replace("@", "")
    # end
    if rds.hget("UsernamesIds", username.lower()):
        return int(rds.hget("UsernamesIds", username.lower()))
    else:
        try:
            getC = await client.get_input_entity(username)
            rds.hset(
                "UsernamesIds",
                username.lower(),
                "-100{}".format(getC.channel_id),
            )
            return int("-100{}".format(getC.channel_id))
        except:
            try:
                getC = await client.get_entity(username)
                rds.hset(
                    "UsernamesIds",
                    username.lower(),
                    "-100{}".format(getC.channel_id),
                )
                return int("-100{}".format(getC.channel_id))
            except:
                try:
                    getC = await client.get_input_entity(username)
                    rds.hset("UsernamesIds", username.lower(), getC.user_id)
                    return int(getC.user_id)
                except:
                    try:
                        getC = await client.get_entity(username)
                        if getC.megagroup:
                            rds.hset(
                                "UsernamesIds",
                                username.lower(),
                                "-100{}".format(getC.id),
                            )
                            return int("-100{}".format(getC.id))
                        else:
                            rds.hset(
                                "UsernamesIds", username.lower(), getC.id
                            )
                            return int(getC.id)
                    except:
                        return False


async def getChatMember(ChatID, UserID):
    try:
        return await bot.get_chat_member(ChatID, UserID)
    except expts.BadRequest as a:
        return a.args
    except expts.Unauthorized as a:
        return a.args
    except Exception as e:
        print(e)
        return False


async def is_Channel_Member(channel, user):
    var = True
    send = await getChatMember(channel, user)
    if not type(send) is types.chat_member.ChatMember:
        var = True
    elif type(send) is types.chat_member.ChatMember and (
        send.status == "kicked" or send.status == "left"
    ):
        var = False
    return var


def isSudo(id):
    if int(id) in sudo_users:
        return True
    else:
        return False


def isSuper(msg):
    if msg.chat.type == "supergroup":
        return True
    else:
        return False


def isGroup(msg):
    if msg.chat.type == "group":
        return True
    else:
        return False


def isPv(msg):
    if msg.chat.type == "private":
        return True
    else:
        return False


def menMD(msg):
    return "[{}](tg://user?id={})".format(
        msg.from_user.first_name, msg.from_user.id
    )


def menHTML(msg):
    return '<a href="tg://user?id={}">{} </a>'.format(
        msg.from_user.id, msg.from_user.first_name
    )


def gregorian_to_jalali(gy, gm, gd):
    g_d_m = [0, 31, 59, 90, 120, 151, 181, 212, 243, 273, 304, 334]
    if gy > 1600:
        jy = 979
        gy -= 1600
    else:
        jy = 0
        gy -= 621
    if gm > 2:
        gy2 = gy + 1
    else:
        gy2 = gy
    days = (
        (365 * gy)
        + (int((gy2 + 3) / 4))
        - (int((gy2 + 99) / 100))
        + (int((gy2 + 399) / 400))
        - 80
        + gd
        + g_d_m[gm - 1]
    )
    jy += 33 * (int(days / 12053))
    days %= 12053
    jy += 4 * (int(days / 1461))
    days %= 1461
    if days > 365:
        jy += int((days - 1) / 365)
        days = (days - 1) % 365
    if days < 186:
        jm = 1 + int(days / 31)
        jd = 1 + (days % 31)
    else:
        jm = 7 + int((days - 186) / 30)
        jd = 1 + ((days - 186) % 30)
    return [jy, jm, jd]


def echoMonth(month, jalaly=False):
    month = int(month)
    if jalaly:
        if month == 1:
            text = "فروردین"
        elif month == 2:
            text = "اردیبهشت"
        elif month == 3:
            text = "خرداد"
        elif month == 4:
            text = "تیر"
        elif month == 5:
            text = "مرداد"
        elif month == 6:
            text = "شهریور"
        elif month == 7:
            text = "مهر"
        elif month == 8:
            text = "آبان"
        elif month == 9:
            text = "آذر"
        elif month == 10:
            text = "دی"
        elif month == 11:
            text = "بهمن"
        elif month == 12:
            text = "اسفند"
    else:
        if month == 1:
            text = "January"
        elif month == 2:
            text = "February"
        elif month == 3:
            text = "March"
        elif month == 4:
            text = "April"
        elif month == 5:
            text = "May"
        elif month == 6:
            text = "June"
        elif month == 7:
            text = "July"
        elif month == 8:
            text = "August"
        elif month == 9:
            text = "September"
        elif month == 10:
            text = "October"
        elif month == 11:
            text = "November"
        elif month == 12:
            text = "December"
    return text


def re_matches(match, input, type_re=None):
    if type_re == "s":
        if re.search(r"{}".format(match), input):
            ap = re.search(r"{}".format(match), input)
            ap = (ap.group(0),) + ap.groups()
            return ap
        else:
            return None
    else:
        if re.match(r"{}".format(match), input):
            ap = re.match(r"{}".format(match), input)
            ap = (ap.group(0),) + ap.groups()
            return ap
        else:
            return None


def saveUsername(msg, mode="message"):
    if mode == "message":
        u = msg.from_user
        uid = u.id
        fn = u.first_name
        rds.hset("userInfo:{}".format(u.id), "name", fn)
        us = u.username
        if us and int(rds.hget("UsernamesIds", us.lower()) or "0") != int(
            uid
        ):
            rds.hset("UsernamesIds", us.lower(), uid)
            cPrint("@{} [{}] Saved".format(us, uid), 2, None, "magenta")
    elif mode == "inline" or mode == "callback":
        u = msg.from_user
        uid = u.id
        fn = u.first_name
        rds.hset("userInfo:{}".format(u.id), "name", fn)
        us = u.username
        if us and int(rds.hget("UsernamesIds", us.lower()) or "0") != int(
            uid
        ):
            rds.hset("UsernamesIds", us.lower(), uid)
            cPrint("@{} [{}] Saved".format(us, uid), 2, None, "magenta")

