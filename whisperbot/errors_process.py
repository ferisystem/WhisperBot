import telethon.errors.rpcerrorlist as telethonErrors
import aiogram.utils.exceptions as expts
from core_file import GlobalValues, log, asyncio
from whisperbot.main_func import sendText


async def errors_handlers(update, exception):
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
