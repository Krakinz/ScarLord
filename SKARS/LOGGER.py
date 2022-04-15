from sideloader import *
from ꜰᴜɴᴄᴘᴏᴅ.misc import is_module_loaded

__mod_name__ = "📓ʟᴏɢ ᴄʜᴀɴɴᴇʟ"

FILENAME = __name__.rsplit(".", 1)[-1]
if is_module_loaded(FILENAME):
    from telegram import ParseMode, Update
    from telegram.error import BadRequest, Unauthorized
    from telegram.ext import CommandHandler, JobQueue, run_async
    from telegram.utils.helpers import escape_markdown

    from SƈαɾLσɾԃ import EVENT_LOGS, LOGGER, dispatcher
    from ꜰᴜɴᴄᴘᴏᴅ.chat_status import user_admin
    from SKARSHOTS import log_channel_sql as sql

    def loggable(func):
        @wraps(func)
        def log_action(
            update: Update,
            context: CallbackContext,
            job_queue: JobQueue = None,
            *args,
            **kwargs,
        ):
            if not job_queue:
                result = func(update, context, *args, **kwargs)
            else:
                result = func(update, context, job_queue, *args, **kwargs)

            chat = update.effective_chat
            message = update.effective_message

            if result and isinstance(result, str):
                datetime_fmt = "%H:%M - %d-%m-%Y"
                result += "\n<b>Event Stamp</b>: <code>{}</code>".format(
                    datetime.utcnow().strftime(datetime_fmt)
                )

                if message.chat.type == chat.SUPERGROUP and message.chat.username:
                    result += f'\n<b>Link:</b> <a href="https://t.me/{chat.username}/{message.message_id}">click here</a>'
                log_chat = sql.get_chat_log_channel(chat.id)
                if log_chat:
                    send_log(context, log_chat, chat.id, result)

            return result

        return log_action

    def gloggable(func):
        @wraps(func)
        def glog_action(update: Update, context: CallbackContext, *args, **kwargs):
            result = func(update, context, *args, **kwargs)
            chat = update.effective_chat
            message = update.effective_message

            if result:
                datetime_fmt = "%H:%M - %d-%m-%Y"
                result += "\n<b>Event Stamp</b>: <code>{}</code>".format(
                    datetime.utcnow().strftime(datetime_fmt)
                )

                if message.chat.type == chat.SUPERGROUP and message.chat.username:
                    result += f'\n<b>Link:</b> <a href="https://t.me/{chat.username}/{message.message_id}">click here</a>'
                log_chat = str(EVENT_LOGS)
                if log_chat:
                    send_log(context, log_chat, chat.id, result)

            return result

        return glog_action

    def send_log(
        context: CallbackContext, log_chat_id: str, orig_chat_id: str, result: str
    ):
        bot = context.bot
        try:
            bot.send_message(
                log_chat_id,
                result,
                parse_mode=ParseMode.HTML,
                disable_web_page_preview=True,
            )
        except BadRequest as excp:
            if excp.message == "Chat not found":
                bot.send_message(
                    orig_chat_id, f"{ALKL}This log channel has been deleted - unsetting."
                )
                sql.stop_chat_logging(orig_chat_id)
            else:
                LOGGER.warning(excp.message)
                LOGGER.warning(result)
                LOGGER.exception("Could not parse")

                bot.send_message(
                    log_chat_id,
                    result
                    + f"{ALKL}\n\nFormatting has been disabled due to an unexpected error.",
                )

    @user_admin
    def logging(update: Update, context: CallbackContext):
        bot = context.bot
        message = update.effective_message
        chat = update.effective_chat

        log_channel = sql.get_chat_log_channel(chat.id)
        if log_channel:
            log_channel_info = bot.get_chat(log_channel)
            message.reply_text(
                f"{ALKL}This group has all it's logs sent to:"
                f" {escape_markdown(log_channel_info.title)} (`{log_channel}`)",
                parse_mode=ParseMode.MARKDOWN,
            )

        else:
            message.reply_text(f"{ALKL}No log channel has been set for this group!")

    @user_admin
    def setlog(update: Update, context: CallbackContext):
        bot = context.bot
        message = update.effective_message
        chat = update.effective_chat
        if chat.type == chat.CHANNEL:
            message.reply_text(
                f"{ALKL}Now, forward the /setlog to the group you want to tie this channel to!"
            )

        elif message.forward_from_chat:
            sql.set_chat_log_channel(chat.id, message.forward_from_chat.id)
            try:
                message.delete()
            except BadRequest as excp:
                if excp.message == "Message to delete not found":
                    pass
                else:
                    LOGGER.exception(
                        "Error deleting message in log channel. Should work anyway though."
                    )

            try:
                bot.send_message(
                    message.forward_from_chat.id,
                    f"{ALKL}This channel has been set as the log channel for {chat.title or chat.first_name}.",
                )
            except Unauthorized as excp:
                if excp.message == "Forbidden: bot is not a member of the channel chat":
                    bot.send_message(chat.id, f"{ALKL}Successfully set log channel!")
                else:
                    LOGGER.exception("ERROR in setting the log channel.")

            bot.send_message(chat.id, "Successfully set log channel!")

        else:
            message.reply_text(
                f"{ALKL}The steps to set a log channel are:\n"
                " - add bot to the desired channel\n"
                " - send /setlog to the channel\n"
                " - forward the /setlog to the group\n"
            )

    @user_admin
    def unsetlog(update: Update, context: CallbackContext):
        bot = context.bot
        message = update.effective_message
        chat = update.effective_chat

        log_channel = sql.stop_chat_logging(chat.id)
        if log_channel:
            bot.send_message(
                log_channel, f"{ALKL}Channel has been unlinked from {chat.title}"
            )
            message.reply_text(f"{ALKL}Log channel has been un-set.")

        else:
            message.reply_text(f"{ALKL}No log channel has been set yet!")

    def __stats__():
        return f"{ALKL}• {sql.num_logchannels()} log channels set."

    def __migrate__(old_chat_id, new_chat_id):
        sql.migrate_chat(old_chat_id, new_chat_id)

    def __chat_settings__(chat_id, user_id):
        log_channel = sql.get_chat_log_channel(chat_id)
        if log_channel:
            log_channel_info = dispatcher.bot.get_chat(log_channel)
            return f"{ALKL}This group has all it's logs sent to: {escape_markdown(log_channel_info.title)} (`{log_channel}`)"
        return f"{ALKL}No log channel is set for this group!"

    __help__ = f"""{ALKL}
*Admins only*-\n
⚔️ •/logchannel-\n get log channel info
⚔️ •/setlog-\n set the log channel.
⚔️ •/unsetlog-\n unset the log channel.

Setting the log channel is done by:
⚔️ •adding the bot to the desired channel (as an admin!)
⚔️ •sending `/setlog` in the channel
⚔️ •forwarding the `/setlog` to the group
"""

    

    LOG_WORK = CommandHandler("logchannel", logging, run_async=True)
    SET_LOG_WORK = CommandHandler("setlog", setlog, run_async=True)
    UNSET_LOG_WORK = CommandHandler("unsetlog", unsetlog, run_async=True)

    dispatcher.add_handler(LOG_WORK)
    dispatcher.add_handler(SET_LOG_WORK)
    dispatcher.add_handler(UNSET_LOG_WORK)

else:
    # run anyway if module not loaded
    def loggable(func):
        return func

    def gloggable(func):
        return func
