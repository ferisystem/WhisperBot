from aiogram.types import (
    ReplyKeyboardMarkup,
    ReplyKeyboardRemove,
)
import aiogram.utils.exceptions as expts
from termcolor import colored, cprint
from core_file import bot, DataBase
from config_bot2 import IDs_datas


def cPrint(text, type=1, backColor="on_white", textColor="blue", modes=None):
    """
	print(colored('bold', 'red', attrs))
	# attrs = ['bold', 'dark', 'underline', \
	'blink', 'reverse', 'concealed']
	- - -
	2 >> print(colored('hello', 'red'), colored('world', 'green')) * best
	grey/red/green/yellow/blue/magenta/cyan/white/
	- - -
	1 >> cprint('Hello, World!', 'red', 'on_blue') * default in lua
	on_grey/on_red/on_green/on_yellow/on_blue/on_magenta/on_cyan/on_white
	"""
    if type == 1:
        cprint(text, textColor, backColor, attrs=modes)
    elif type == 2:
        print(colored(text, textColor, attrs=modes))


async def sendText(
    chat_id, reply_msg, dis_webpage, text, parse_mode=None, reply_markup=None
):
    dis_webpage = str(dis_webpage)
    dis_webpage = dis_webpage.replace("1", "True")
    dis_webpage = dis_webpage.replace("0", "False")
    if reply_msg is 0:
        reply_msgs = None
    elif reply_msg and str(reply_msg).isdigit():
        reply_msgs = reply_msg
    elif reply_msg and "message_id" in reply_msg:
        reply_msgs = reply_msg.message_id
    else:
        reply_msgs = None
    if parse_mode:
        parse_mode = parse_mode.replace("md", "Markdown")
        parse_mode = parse_mode.replace("html", "HTML")
    if type(reply_markup) is tuple:
        if len(reply_markup) > 0:
            markup = ReplyKeyboardMarkup(resize_keyboard=True, selective=True)
            for row in reply_markup:
                markup.row(*row)
        else:
            markup = ReplyKeyboardRemove()
    else:
        markup = reply_markup
    try:
        if DataBase.get("typing"):
            await bot.send_chat_action(chat_id, "typing")
        result = await bot.send_message(
            chat_id=chat_id,
            text=text,
            parse_mode=(parse_mode or None),
            disable_web_page_preview=bool(dis_webpage),
            disable_notification=False,
            reply_to_message_id=reply_msgs,
            reply_markup=markup,
        )
        DataBase.incr("amarBot.sendMsg")
        return True, result
    except expts.ChatNotFound as a:
        return a.args
    except expts.BotBlocked as a:
        return a.args
    except expts.RetryAfter as a:
        await asyncio.sleep(a.timeout)
        return await sendText(
            chat_id, reply_msgs, 1, text, parse_mode, reply_markup
        )
    except expts.UserDeactivated as a:
        return a.args
    except expts.TelegramAPIError as a:
        if a.args[0] == "Reply message not found":
            try:
                return True, await sendText(
                    chat_id, 0, 1, text, parse_mode, reply_markup
                )
            except:
                return a.args
        else:
            return a.args
    except expts.CantInitiateConversation as a:
        return a.args
    except expts.Unauthorized as a:
        return a.args
    except expts.BadRequest as a:
        if a.args[0] == "Reply message not found":
            try:
                return True, await sendText(
                    chat_id, 0, 1, text, parse_mode, reply_markup
                )
            except:
                return a.args
        else:
            return a.args
    except Exception as e:
        print(e)
        return False, False
        pass


async def sendPhoto(
    chat_id,
    photo,
    caption=None,
    parse_mode=None,
    reply_msg=None,
    protect_content=False,
    allow_no_reply=True,
    reply_markup=None,
):
    if reply_msg is 0:
        reply_msgs = None
    elif reply_msg and str(reply_msg).isdigit():
        reply_msgs = reply_msg
    elif reply_msg and "message_id" in reply_msg:
        reply_msgs = reply_msg.message_id
    else:
        reply_msgs = None
    if parse_mode:
        parse_mode = parse_mode.replace("md", "Markdown")
        parse_mode = parse_mode.replace("html", "HTML")
    if type(reply_markup) is tuple:
        if len(reply_markup) > 0:
            markup = ReplyKeyboardMarkup(resize_keyboard=True, selective=True)
            for row in reply_markup:
                markup.row(*row)
        else:
            markup = ReplyKeyboardRemove()
    else:
        markup = reply_markup
    if type(caption) is str and len(caption) > 1000:
        if len(caption) > 1000:
            formol = len(caption)
            formol = formol - 1024
            caption = caption[formol:]
    try:
        if DataBase.get("typing"):
            await bot.send_chat_action(chat_id, "upload_photo")
        result = await bot.send_photo(
            chat_id,
            photo,
            caption,
            parse_mode=parse_mode,
            reply_to_message_id=reply_msgs,
            protect_content=protect_content,
            allow_sending_without_reply=allow_no_reply,
            reply_markup=reply_markup,
        )
        return True, result
    except expts.ChatNotFound as a:
        return a.args
    except expts.BotBlocked as a:
        return a.args
    except expts.RetryAfter as a:
        await asyncio.sleep(a.timeout)
        return await sendPhoto(
            chat_id,
            photo,
            caption,
            parse_mode,
            reply_msg,
            protect_content,
            allow_no_reply,
            reply_markup,
        )
    except expts.UserDeactivated as a:
        return a.args
    except expts.TelegramAPIError as a:
        if a.args[0] == "Reply message not found":
            try:
                return True, await sendPhoto(
                    chat_id,
                    photo,
                    caption,
                    parse_mode,
                    0,
                    protect_content,
                    True,
                    reply_markup,
                )
            except:
                return a.args
        else:
            return a.args
    except expts.CantInitiateConversation as a:
        return a.args
    except expts.Unauthorized as a:
        return a.args
    except expts.BadRequest as a:
        if a.args[0] == "Reply message not found":
            try:
                return True, await sendPhoto(
                    chat_id,
                    photo,
                    caption,
                    parse_mode,
                    0,
                    protect_content,
                    True,
                    reply_markup,
                )
            except:
                return a.args
        else:
            return a.args
    except Exception as e:
        print(e)
        return False, False
        pass


async def sendAudio(
    chat_id,
    reply_msg,
    audio,
    caption=None,
    parse_mode=None,
    duration=None,
    performer=None,
    title=None,
    thumb=None,
    dis_notif=1,
    reply_markup=None,
):
    dis_notif = str(dis_notif)
    dis_notif = dis_notif.replace("1", "True")
    dis_notif = dis_notif.replace("0", "False")
    dis_notif = bool(dis_notif)
    if reply_msg is 0:
        reply_msgs = None
    elif reply_msg and "message_id" in reply_msg:
        reply_msgs = reply_msg.message_id
    else:
        reply_msgs = None
    if parse_mode:
        parse_mode = parse_mode.replace("md", "Markdown")
        parse_mode = parse_mode.replace("html", "HTML")
    if type(reply_markup) is tuple:
        if len(reply_markup) > 0:
            markup = ReplyKeyboardMarkup(resize_keyboard=True, selective=True)
            for row in reply_markup:
                markup.row(*row)
        else:
            markup = ReplyKeyboardRemove()
    else:
        markup = reply_markup
    try:
        if DataBase.get("typing"):
            await bot.send_chat_action(chat_id, "upload_audio")
        result = await bot.send_audio(
            chat_id,
            audio,
            caption,
            parse_mode,
            duration,
            performer,
            title,
            thumb,
            dis_notif,
            reply_msgs,
            reply_markup,
        )
        return True, result
    except expts.ChatNotFound as a:
        return a.args
    except expts.BotBlocked as a:
        return a.args
    except expts.RetryAfter as a:
        await asyncio.sleep(a.timeout)
        return await sendAudio(
            chat_id,
            audio,
            caption,
            parse_mode,
            duration,
            performer,
            title,
            thumb,
            dis_notif,
            reply_msgs,
            reply_markup,
        )
    except expts.UserDeactivated as a:
        return a.args
    except expts.TelegramAPIError as a:
        if a.args[0] == "Reply message not found":
            try:
                return True, await sendAudio(
                    chat_id,
                    audio,
                    caption,
                    parse_mode,
                    duration,
                    performer,
                    title,
                    thumb,
                    dis_notif,
                    0,
                    reply_markup,
                )
            except:
                return a.args
        else:
            return a.args
    except expts.CantInitiateConversation as a:
        return a.args
    except expts.Unauthorized as a:
        return a.args
    except expts.BadRequest as a:
        if a.args[0] == "Reply message not found":
            try:
                return True, await sendAudio(
                    chat_id,
                    audio,
                    caption,
                    parse_mode,
                    duration,
                    performer,
                    title,
                    thumb,
                    dis_notif,
                    0,
                    reply_markup,
                )
            except:
                return a.args
        else:
            return a.args
    except Exception as e:
        if "Can not serialize value type:" in str(e):
            await sendDocument(
                chat_id,
                audio,
                caption=caption,
                parse_mode=parse_mode,
                thumb=thumb,
                dis_notif=dis_notif,
                reply_msg=reply_msg,
                reply_markup=reply_markup,
            )
        else:
            print(e)
            return False, False
            pass


async def sendVoice(
    chat_id,
    reply_msg,
    voice,
    caption=None,
    parse_mode=None,
    duration=None,
    dis_notif=1,
    reply_markup=None,
):
    dis_notif = str(dis_notif)
    dis_notif = dis_notif.replace("1", "True")
    dis_notif = dis_notif.replace("0", "False")
    dis_notif = bool(dis_notif)
    if reply_msg is 0:
        reply_msgs = None
    elif reply_msg and "message_id" in reply_msg:
        reply_msgs = reply_msg.message_id
    else:
        reply_msgs = None
    if parse_mode:
        parse_mode = parse_mode.replace("md", "Markdown")
        parse_mode = parse_mode.replace("html", "HTML")
    if type(reply_markup) is tuple:
        if len(reply_markup) > 0:
            markup = ReplyKeyboardMarkup(resize_keyboard=True, selective=True)
            for row in reply_markup:
                markup.row(*row)
        else:
            markup = ReplyKeyboardRemove()
    else:
        markup = reply_markup
    try:
        if DataBase.get("typing"):
            await bot.send_chat_action(chat_id, "record_voice")
        result = await bot.send_voice(
            chat_id,
            voice,
            caption,
            parse_mode,
            duration,
            dis_notif,
            reply_msgs,
            reply_markup,
        )
        return True, result
    except expts.ChatNotFound as a:
        return a.args
    except expts.BotBlocked as a:
        return a.args
    except expts.RetryAfter as a:
        await asyncio.sleep(a.timeout)
        return await sendVoice(
            chat_id,
            voice,
            caption,
            parse_mode,
            duration,
            dis_notif,
            reply_msgs,
            reply_markup,
        )
    except expts.UserDeactivated as a:
        return a.args
    except expts.TelegramAPIError as a:
        if a.args[0] == "Reply message not found":
            try:
                return True, await sendVoice(
                    chat_id,
                    voice,
                    caption,
                    parse_mode,
                    duration,
                    dis_notif,
                    0,
                    reply_markup,
                )
            except:
                return a.args
        else:
            return a.args
    except expts.CantInitiateConversation as a:
        return a.args
    except expts.Unauthorized as a:
        return a.args
    except expts.BadRequest as a:
        if a.args[0] == "Reply message not found":
            try:
                return True, await sendVoice(
                    chat_id,
                    voice,
                    caption,
                    parse_mode,
                    duration,
                    dis_notif,
                    0,
                    reply_markup,
                )
            except:
                return a.args
        else:
            return a.args
    except Exception as e:
        print(e)
        return False, False
        pass


async def sendVideo(
    chat_id,
    reply_msg,
    video,
    caption=None,
    parse_mode=None,
    duration=None,
    thumb=None,
    width=None,
    height=None,
    supports_streaming=True,
    dis_notif=1,
    reply_markup=None,
    protect_content=False,
    allow_no_reply=True,
):
    dis_notif = str(dis_notif)
    dis_notif = dis_notif.replace("1", "True")
    dis_notif = dis_notif.replace("0", "False")
    dis_notif = bool(dis_notif)
    if reply_msg is 0:
        reply_msgs = None
    elif reply_msg and str(reply_msg).isdigit():
        reply_msgs = reply_msg
    elif reply_msg and "message_id" in reply_msg:
        reply_msgs = reply_msg.message_id
    else:
        reply_msgs = None
    if parse_mode:
        parse_mode = parse_mode.replace("md", "Markdown")
        parse_mode = parse_mode.replace("html", "HTML")
    if type(caption) is str and len(caption) > 1000:
        if len(caption) > 1000:
            formol = len(caption)
            formol = formol - 1024
            caption = caption[formol:]
    if type(reply_markup) is tuple:
        if len(reply_markup) > 0:
            markup = ReplyKeyboardMarkup(resize_keyboard=True, selective=True)
            for row in reply_markup:
                markup.row(*row)
        else:
            markup = ReplyKeyboardRemove()
    else:
        markup = reply_markup
    try:
        if DataBase.get("typing"):
            await bot.send_chat_action(chat_id, "record_video")
        result = await bot.send_video(
            chat_id,
            video,
            duration,
            width,
            height,
            thumb,
            caption,
            parse_mode,
            supports_streaming=supports_streaming,
            disable_notification=dis_notif,
            protect_content=protect_content,
            reply_to_message_id=reply_msgs,
            allow_sending_without_reply=allow_no_reply,
            reply_markup=reply_markup,
        )
        return True, result
    except expts.ChatNotFound as a:
        return a.args
    except expts.BotBlocked as a:
        return a.args
    except expts.RetryAfter as a:
        await asyncio.sleep(a.timeout)
        return await sendVideo(
            chat_id,
            reply_msg,
            video,
            caption,
            parse_mode,
            duration,
            thumb,
            width,
            height,
            supports_streaming,
            dis_notif,
            reply_markup,
            protect_content,
            allow_no_reply,
        )
    except expts.UserDeactivated as a:
        return a.args
    except expts.TelegramAPIError as a:
        if a.args[0] == "Reply message not found":
            try:
                return True, await sendVideo(
                    chat_id,
                    0,
                    video,
                    caption,
                    parse_mode,
                    duration,
                    thumb,
                    width,
                    height,
                    supports_streaming,
                    dis_notif,
                    reply_markup,
                    protect_content,
                    True,
                )
            except:
                return a.args
        else:
            return a.args
    except expts.CantInitiateConversation as a:
        return a.args
    except expts.Unauthorized as a:
        return a.args
    except expts.BadRequest as a:
        if a.args[0] == "Reply message not found":
            try:
                return True, await sendVideo(
                    chat_id,
                    0,
                    video,
                    caption,
                    parse_mode,
                    duration,
                    thumb,
                    width,
                    height,
                    supports_streaming,
                    dis_notif,
                    reply_markup,
                    protect_content,
                    True,
                )
            except:
                return a.args
        else:
            return a.args
    except Exception as e:
        print(e)
        return False, False
        pass


async def sendDocument(
    chat_id,
    document,
    caption=None,
    parse_mode=None,
    thumb=None,
    dis_notif=None,
    reply_msg=None,
    reply_markup=None,
):
    dis_notif = str(dis_notif)
    dis_notif = dis_notif.replace("1", "True")
    dis_notif = dis_notif.replace("0", "False")
    dis_notif = bool(dis_notif)
    if reply_msg is 0:
        reply_msgs = None
    elif reply_msg and "message_id" in reply_msg:
        reply_msgs = reply_msg.message_id
    else:
        reply_msgs = None
    if parse_mode:
        parse_mode = parse_mode.replace("md", "Markdown")
        parse_mode = parse_mode.replace("html", "HTML")
    if type(reply_markup) is tuple:
        if len(reply_markup) > 0:
            markup = ReplyKeyboardMarkup(resize_keyboard=True, selective=True)
            for row in reply_markup:
                markup.row(*row)
        else:
            markup = ReplyKeyboardRemove()
    else:
        markup = reply_markup
    try:
        if DataBase.get("typing"):
            await bot.send_chat_action(chat_id, "upload_document")
        result = await bot.send_document(
            chat_id,
            document,
            thumb,
            caption,
            parse_mode,
            dis_notif,
            reply_msgs,
            reply_markup,
        )
        return True, result
    except expts.ChatNotFound as a:
        return a.args
    except expts.BotBlocked as a:
        return a.args
    except expts.RetryAfter as a:
        await asyncio.sleep(a.timeout)
        return await sendDocument(
            chat_id,
            document,
            caption,
            parse_mode,
            thumb,
            dis_notif,
            reply_msgs,
            reply_markup,
        )
    except expts.UserDeactivated as a:
        return a.args
    except expts.TelegramAPIError as a:
        if a.args[0] == "Reply message not found":
            try:
                return True, await sendDocument(
                    chat_id,
                    document,
                    caption,
                    parse_mode,
                    thumb,
                    dis_notif,
                    0,
                    reply_markup,
                )
            except:
                return a.args
        else:
            return a.args
    except expts.CantInitiateConversation as a:
        return a.args
    except expts.Unauthorized as a:
        return a.args
    except expts.BadRequest as a:
        if a.args[0] == "Reply message not found":
            try:
                return True, await sendDocument(
                    chat_id,
                    document,
                    caption,
                    parse_mode,
                    thumb,
                    dis_notif,
                    0,
                    reply_markup,
                )
            except:
                return a.args
        else:
            return a.args
    except Exception as e:
        print(e)
        return False, False
        pass


async def sendMediaGroup(chat_id, reply_msg, dis_notif, media):
    dis_notif = str(dis_notif)
    dis_notif = dis_notif.replace("1", "True")
    dis_notif = dis_notif.replace("0", "False")
    dis_notif = bool(dis_notif)
    if reply_msg is 0:
        reply_msgs = None
    elif reply_msg and "message_id" in reply_msg:
        reply_msgs = reply_msg.message_id
    else:
        reply_msgs = None
    try:
        result = await bot.send_media_group(
            chat_id=chat_id,
            media=media,
            disable_notification=dis_notif,
            reply_to_message_id=reply_msgs,
            allow_sending_without_reply=True,
        )
        return True, result
    except expts.ChatNotFound as a:
        return a.args
    except expts.BotBlocked as a:
        return a.args
    except expts.RetryAfter as a:
        await asyncio.sleep(a.timeout)
        return await sendMediaGroup(chat_id, reply_msgs, dis_notif, media)
    except expts.UserDeactivated as a:
        return a.args
    except expts.TelegramAPIError as a:
        if a.args[0] == "Reply message not found":
            try:
                return True, await sendMediaGroup(chat_id, 0, dis_notif, media)
            except:
                return a.args
        else:
            return a.args
    except expts.CantInitiateConversation as a:
        return a.args
    except expts.Unauthorized as a:
        return a.args
    except expts.BadRequest as a:
        if a.args[0] == "Reply message not found":
            try:
                return True, await sendMediaGroup(chat_id, 0, dis_notif, media)
            except:
                return a.args
        else:
            return a.args
    except Exception as e:
        print(e)
        return False, False
        pass


async def copyMessage(
    chat_id,
    from_chat_id,
    message_id,
    caption=None,
    parse_mode=None,
    caption_entities=None,
    dis_notif=None,
    protect_content=True,
    reply_msg=None,
    allow_sending_without_reply=True,
    reply_markup=None,
):
    dis_notif = str(dis_notif)
    dis_notif = dis_notif.replace("1", "True")
    dis_notif = dis_notif.replace("0", "False")
    dis_notif = bool(dis_notif)
    if reply_msg is 0:
        reply_msgs = None
    elif reply_msg and str(reply_msg).isdigit():
        reply_msgs = reply_msg
    elif reply_msg and "message_id" in reply_msg:
        reply_msgs = reply_msg.message_id
    else:
        reply_msgs = None
    if parse_mode:
        parse_mode = parse_mode.replace("md", "Markdown")
        parse_mode = parse_mode.replace("html", "HTML")
    if type(reply_markup) is tuple:
        if len(reply_markup) > 0:
            markup = ReplyKeyboardMarkup(resize_keyboard=True, selective=True)
            for row in reply_markup:
                markup.row(*row)
        else:
            markup = ReplyKeyboardRemove()
    else:
        markup = reply_markup
    try:
        result = await bot.copy_message(
            chat_id,
            from_chat_id,
            message_id,
            caption,
            parse_mode=parse_mode,
            caption_entities=caption_entities,
            disable_notification=dis_notif,
            protect_content=protect_content,
            reply_to_message_id=reply_msg,
            allow_sending_without_reply=allow_sending_without_reply,
            reply_markup=reply_markup,
        )
        return True, result
    except expts.ChatNotFound as a:
        return a.args
    except expts.BotBlocked as a:
        return a.args
    except expts.RetryAfter as a:
        await asyncio.sleep(a.timeout)
        return await copyMessage(
            chat_id,
            from_chat_id,
            message_id,
            caption,
            parse_mode,
            caption_entities,
            disable_notification,
            protect_content,
            reply_to_message_id,
            allow_sending_without_reply,
            reply_markup,
        )
    except expts.UserDeactivated as a:
        return a.args
    except expts.TelegramAPIError as a:
        if a.args[0] == "Reply message not found":
            try:
                return True, await copyMessage(
                    chat_id,
                    from_chat_id,
                    message_id,
                    caption,
                    parse_mode,
                    caption_entities,
                    disable_notification,
                    protect_content,
                    0,
                    allow_sending_without_reply,
                    reply_markup,
                )
            except:
                return a.args
        else:
            return a.args
    except expts.CantInitiateConversation as a:
        return a.args
    except expts.Unauthorized as a:
        return a.args
    except expts.BadRequest as a:
        if a.args[0] == "Reply message not found":
            try:
                return True, await copyMessage(
                    chat_id,
                    from_chat_id,
                    message_id,
                    caption,
                    parse_mode,
                    caption_entities,
                    disable_notification,
                    protect_content,
                    0,
                    allow_sending_without_reply,
                    reply_markup,
                )
            except:
                return a.args
        else:
            return a.args
    except Exception as e:
        print(e)
        return False, False
        pass


async def editText(
    chat_id=None,
    msg_id=0,
    inline_msg_id=0,
    text=None,
    parse_mode=None,
    reply_markup=None,
    entities=None,
):
    if parse_mode:
        parse_mode = parse_mode.replace("md", "Markdown")
        parse_mode = parse_mode.replace("html", "HTML")
    if type(reply_markup) is tuple:
        if len(reply_markup) > 0:
            markup = ReplyKeyboardMarkup(resize_keyboard=True, selective=True)
            for row in reply_markup:
                markup.row(*row)
        else:
            markup = ReplyKeyboardRemove()
    else:
        markup = reply_markup
    try:
        if inline_msg_id and not inline_msg_id.isdigit():
            result = await bot.edit_message_text(
                text=text,
                parse_mode=(parse_mode or None),
                inline_message_id=inline_msg_id,
                reply_markup=markup,
                entities=entities,
            )
            return True, result
        elif msg_id:
            result = await bot.edit_message_text(
                chat_id=chat_id,
                text=text,
                parse_mode=(parse_mode or None),
                disable_web_page_preview=True,
                message_id=msg_id,
                reply_markup=markup,
            )
            return True, result
    except expts.BadRequest as a:
        return a.args
    except Exception as e:
        print(e)


async def editMessageMedia(
    chat_id, media, message_id=None, inline_message_id=None, reply_markup=None
):
    if type(reply_markup) is tuple:
        if len(reply_markup) > 0:
            markup = ReplyKeyboardMarkup(resize_keyboard=True, selective=True)
            for row in reply_markup:
                markup.row(*row)
        else:
            markup = ReplyKeyboardRemove()
    else:
        markup = reply_markup
    try:
        if inline_message_id > 0:
            result = await bot.edit_message_media(
                chat_id=None,
                message_id=None,
                inline_message_id=inline_message_id,
                media=media,
                reply_markup=reply_markup,
            )
            return True, result
        elif message_id > 0:
            result = await bot.edit_message_media(
                chat_id,
                message_id,
                inline_message_id=None,
                media=media,
                reply_markup=reply_markup,
            )
            return True, result
    except expts.BadRequest as a:
        return a.args
    except Exception as e:
        print(e)


async def answerCallbackQuery(
    query_id, text=None, show_alert=False, cache_time=0, url_web=None
):
    try:
        return await bot.answer_callback_query(
            query_id.id, text, show_alert, url_web, cache_time
        )
    except Exception as e:
        print(e)
        return False


async def answerInlineQuery(
    inline_msg_id,
    results,
    cache_time=1,
    switch_pm_text=None,
    switch_pm_parameter=None,
    is_personal=False,
    next_offset=None,
):
    try:
        result = await bot.answer_inline_query(
            inline_msg_id,
            results,
            cache_time,
            is_personal,
            next_offset,
            switch_pm_text,
            switch_pm_parameter,
        )
        return True, result
    except Exception as e:
        print(e)
        return False


async def getUserProfilePhotos(UserID, offset=0, limit=1):
    try:
        result = await bot.get_user_profile_photos(UserID, offset, limit)
        return True, result
    except Exception as e:
        return False


async def delete_messages(chat_id, message_id):
    try:
        await bot.delete_message(chat_id, message_id)
        return True
    except:
        return False


async def editMessageReplyMarkup(
    chat_id=None,
    message_id=None,
    inline_message_id=None,
    reply_markup=None,
):
    if type(reply_markup) is tuple:
        if len(reply_markup) > 0:
            markup = ReplyKeyboardMarkup(resize_keyboard=True, selective=True)
            for row in reply_markup:
                markup.row(*row)
        else:
            markup = ReplyKeyboardRemove()
    else:
        markup = reply_markup
    try:
        result = await bot.edit_message_reply_markup(
            chat_id=chat_id,
            message_id=message_id,
            inline_message_id=inline_message_id,
            reply_markup=markup,
        )
        return True, result
    except expts.BadRequest as a:
        return a.args
    except Exception as e:
        print(e)
