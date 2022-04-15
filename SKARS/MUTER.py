from sideloader import *
from SƈαɾLσɾԃ import LOGGER, dispatcher
from ꜰᴜɴᴄᴘᴏᴅ.chat_status import (
    bot_admin,
    can_restrict,
    connection_status,
    is_user_admin,
    user_admin,
)
from ꜰᴜɴᴄᴘᴏᴅ.extraction import (
    extract_user,
    extract_user_and_text,
)
from ꜰᴜɴᴄᴘᴏᴅ.string_handling import extract_time
from SKARS.LOGGER import loggable

__mod_name__ = "🔇 ᴍᴜᴛɪɴɢ"

def check_user(user_id: int, bot: Bot, chat: Chat) -> Optional[str]:
    if not user_id:
        reply = f"{ALKL}You don't seem to be referring to a user or the ID specified is incorrect.."
        return reply

    try:
        member = chat.get_member(user_id)
    except BadRequest as excp:
        if excp.message == "User not found":
            reply = f"{ALKL}I can't seem to find this user"
            return reply
        else:
            raise

    if user_id == bot.id:
        reply = f"{ALKL}I'm not gonna MUTE myself, How high are you son?"
        return reply

    if is_user_admin(chat, user_id, member):
        reply = f"{ALKL}Can't. Find someone else to mute but not this one."
        return reply

    return None


@connection_status
@bot_admin
@user_admin
@loggable
def mute(update: Update, context: CallbackContext) -> str:
    bot = context.bot
    args = context.args

    chat = update.effective_chat
    user = update.effective_user
    message = update.effective_message

    user_id, reason = extract_user_and_text(message, args)
    reply = check_user(user_id, bot, chat)

    if reply:
        message.reply_text(reply)
        return ""

    member = chat.get_member(user_id)

    log = (
        f"<b>{html.escape(chat.title)}:</b>\n"
        f"{ALKL}#MUTE\n"
        f"<b>Admin:</b> {mention_html(user.id, user.first_name)}\n"
        f"<b>User:</b> {mention_html(member.user.id, member.user.first_name)}"
    )

    if reason:
        log += f"\n<b>Reason:</b> {reason}"

    if member.can_send_messages is None or member.can_send_messages:
        chat_permissions = ChatPermissions(can_send_messages=False)
        bot.restrict_chat_member(chat.id, user_id, chat_permissions)
        reply = (
            f"{ALKL}<code>❕</code><b>Mute Event</b>\n"
            f"<code> </code><b>•  User:</b> {mention_html(member.user.id, html.escape(member.user.first_name))}\n"
            f"<code> </code><b>•  Time: no expiration date</b>"
        )
        if reason:
            reply += f"{ALKL}\n<code> </code><b>•  Reason:</b> {html.escape(reason)}"
        bot.sendMessage(chat.id, reply, parse_mode=ParseMode.HTML)
        return log

    else:
        message.reply_text(f"{ALKL}This user is already muted!")

    return ""


@connection_status
@bot_admin
@user_admin
@loggable
def unmute(update: Update, context: CallbackContext) -> str:
    bot, args = context.bot, context.args
    chat = update.effective_chat
    user = update.effective_user
    message = update.effective_message

    user_id = extract_user(message, args)
    if not user_id:
        message.reply_text(
            f"{ALKL}You'll need to either give me a username to unmute, or reply to someone to be unmuted."
        )
        return ""

    member = chat.get_member(int(user_id))

    if member.status != "kicked" and member.status != "left":
        if (
            member.can_send_messages
            and member.can_send_media_messages
            and member.can_send_other_messages
            and member.can_add_web_page_previews
        ):
            message.reply_text(f"{ALKL}This user already has the right to speak.")
        else:
            chat_permissions = ChatPermissions(
                can_send_messages=True,
                can_invite_users=True,
                can_pin_messages=True,
                can_send_polls=True,
                can_change_info=True,
                can_send_media_messages=True,
                can_send_other_messages=True,
                can_add_web_page_previews=True,
            )
            try:
                bot.restrict_chat_member(chat.id, int(user_id), chat_permissions)
            except BadRequest:
                pass
            bot.sendMessage(
                chat.id,
                f"{ALKL}I shall allow <b>{html.escape(member.user.first_name)}</b> to text!",
                parse_mode=ParseMode.HTML,
            )
            return (
                f"<b>{html.escape(chat.title)}:</b>\n"
                f"{ALKL}#UNMUTE\n"
                f"<b>Admin:</b> {mention_html(user.id, user.first_name)}\n"
                f"<b>User:</b> {mention_html(member.user.id, member.user.first_name)}"
            )
    else:
        message.reply_text(
            f"{ALKL}This user isn't even in the chat, unmuting them won't make them talk more than they "
            "already do!"
        )

    return ""


@connection_status
@bot_admin
@can_restrict
@user_admin
@loggable
def temp_mute(update: Update, context: CallbackContext) -> str:
    bot, args = context.bot, context.args
    chat = update.effective_chat
    user = update.effective_user
    message = update.effective_message

    user_id, reason = extract_user_and_text(message, args)
    reply = check_user(user_id, bot, chat)

    if reply:
        message.reply_text(reply)
        return ""

    member = chat.get_member(user_id)

    if not reason:
        message.reply_text(f"{ALKL}You haven't specified a time to mute this user for!")
        return ""

    split_reason = reason.split(None, 1)

    time_val = split_reason[0].lower()
    if len(split_reason) > 1:
        reason = split_reason[1]
    else:
        reason = ""

    mutetime = extract_time(message, time_val)

    if not mutetime:
        return ""

    log = (
        f"<b>{html.escape(chat.title)}:</b>\n"
        f"{ALKL}#TEMP MUTED\n"
        f"<b>Admin:</b> {mention_html(user.id, user.first_name)}\n"
        f"<b>User:</b> {mention_html(member.user.id, member.user.first_name)}\n"
        f"<b>Time:</b> {time_val}"
    )
    if reason:
        log += f"\n<b>Reason:</b> {reason}"

    try:
        if member.can_send_messages is None or member.can_send_messages:
            chat_permissions = ChatPermissions(can_send_messages=False)
            bot.restrict_chat_member(
                chat.id, user_id, chat_permissions, until_date=mutetime
            )
            reply = (
                f"{ALKL}<code>❕</code><b>Mute Event</b>\n"
                f"<code> </code><b>•  User:</b> {mention_html(member.user.id, html.escape(member.user.first_name))}\n"
                f"<code> </code><b>•  Time: {time_val}</b>"
            )
            if reason:
                reply += f"{ALKL}\n<code> </code><b>•  Reason:</b> {html.escape(reason)}"
            bot.sendMessage(chat.id, reply, parse_mode=ParseMode.HTML)
            return log
        else:
            message.reply_text(f"{ALKL}This user is already muted.")

    except BadRequest as excp:
        if excp.message == "Reply message not found":
            # Do not reply
            message.reply_text(f"{ALKL}Muted for {time_val}!", quote=False)
            return log
        else:
            LOGGER.warning(update)
            LOGGER.exception(
                "ERROR muting user %s in chat %s (%s) due to %s",
                user_id,
                chat.title,
                chat.id,
                excp.message,
            )
            message.reply_text(f"{ALKL}Well damn, I can't mute that user.")

    return ""


__help__ = f"""{ALKL}
*Admins only*-\n
⚔️ •/mute <userhandle> <reason>(optional)-\n silences a user. Can also be used as a reply, muting the replied to user.
⚔️ •/tmute <userhandle> x(m/h/d) <reason>(optional)-\n mutes a user for x time. (via handle, or reply). `m` = `minutes`, `h` = `hours`, `d` = `days`.
⚔️ •/unmute <userhandle>-\n unmutes a user. Can also be used as a reply, muting the replied to user.
"""

MUTE_WORK = CommandHandler("mute", mute, run_async=True)
UNMUTE_WORK = CommandHandler("unmute", unmute, run_async=True)
TEMPMUTE_WORK = CommandHandler(["tmute", "tempmute"], temp_mute, run_async=True)

dispatcher.add_handler(MUTE_WORK)
dispatcher.add_handler(UNMUTE_WORK)
dispatcher.add_handler(TEMPMUTE_WORK)


__handlers__ = [MUTE_WORK, UNMUTE_WORK, TEMPMUTE_WORK]
