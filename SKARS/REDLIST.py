from sideloader import *
import SKARSHOTS.blacklist_sql as sql
from SƈαɾLσɾԃ import dispatcher, LOGGER
from SKARS.TURNOFF import DisableAbleCommandHandler
from ꜰᴜɴᴄᴘᴏᴅ.chat_status import user_admin, user_not_admin
from ꜰᴜɴᴄᴘᴏᴅ.extraction import extract_text
from ꜰᴜɴᴄᴘᴏᴅ.misc import split_message
from SKARS.LOGGER import loggable
from SKARS.WARNINGS import warn
from ꜰᴜɴᴄᴘᴏᴅ.string_handling import extract_time
from SKARS.CONNECT import connected
from SKARSHOTS.approve_sql import is_approved
from ꜰᴜɴᴄᴘᴏᴅ.alternate import send_message, typing_action

__mod_name__ = "🏴‍☠️ ʙʟᴀᴄᴋʟɪꜱᴛꜱ"

BLACKLIST_GROUP = 11
@user_admin
def blacklist(update: Update, context: CallbackContext):
    chat = update.effective_chat
    user = update.effective_user
    args = context.args

    conn = connected(context.bot, update, chat, user.id, need_admin=False)
    if conn:
        chat_id = conn
        chat_name = dispatcher.bot.getChat(conn).title
    else:
        if chat.type == "private":
            return
        chat_id = update.effective_chat.id
        chat_name = chat.title

    filter_list = "{}Current blacklisted words in <b>{}</b>:\n".format(ALKL,chat_name)

    all_blacklisted = sql.get_chat_blacklist(chat_id)

    if len(args) > 0 and args[0].lower() == "copy":
        for trigger in all_blacklisted:
            filter_list += "<code>{}</code>\n".format(html.escape(trigger))
    else:
        for trigger in all_blacklisted:
            filter_list += " - <code>{}</code>\n".format(html.escape(trigger))

    # for trigger in all_blacklisted:
    #     filter_list += " - <code>{}</code>\n".format(html.escape(trigger))

    split_text = split_message(filter_list)
    for text in split_text:
        if filter_list == "{}Current blacklisted words in <b>{}</b>:\n".format(ALKL,
            html.escape(chat_name)
        ):
            send_message(
                update.effective_message,
                "{}No blacklisted words in <b>{}</b>!".format(ALKL,html.escape(chat_name)),
                parse_mode=ParseMode.HTML,
            )
            return
        send_message(update.effective_message, text, parse_mode=ParseMode.HTML)


@user_admin
def add_blacklist(update: Update, context: CallbackContext):
    msg = update.effective_message
    chat = update.effective_chat
    user = update.effective_user
    words = msg.text.split(None, 1)

    conn = connected(context.bot, update, chat, user.id)
    if conn:
        chat_id = conn
        chat_name = dispatcher.bot.getChat(conn).title
    else:
        chat_id = update.effective_chat.id
        if chat.type == "private":
            return
        else:
            chat_name = chat.title

    if len(words) > 1:
        text = words[1]
        to_blacklist = list(
            {trigger.strip() for trigger in text.split("\n") if trigger.strip()}
        )
        for trigger in to_blacklist:
            sql.add_to_blacklist(chat_id, trigger.lower())

        if len(to_blacklist) == 1:
            send_message(
                update.effective_message,
                "{}Added blacklist <code>{}</code> in chat: <b>{}</b>!".format(ALKL,
                    html.escape(to_blacklist[0]), html.escape(chat_name)
                ),
                parse_mode=ParseMode.HTML,
            )

        else:
            send_message(
                update.effective_message,
                "{}Added blacklist trigger: <code>{}</code> in <b>{}</b>!".format(ALKL,
                    len(to_blacklist), html.escape(chat_name)
                ),
                parse_mode=ParseMode.HTML,
            )

    else:
        send_message(
            update.effective_message,
            f"{ALKL}Tell me which words you would like to add in blacklist.",
        )


@user_admin
def unblacklist(update: Update, context: CallbackContext):
    msg = update.effective_message
    chat = update.effective_chat
    user = update.effective_user
    words = msg.text.split(None, 1)

    conn = connected(context.bot, update, chat, user.id)
    if conn:
        chat_id = conn
        chat_name = dispatcher.bot.getChat(conn).title
    else:
        chat_id = update.effective_chat.id
        if chat.type == "private":
            return
        else:
            chat_name = chat.title

    if len(words) > 1:
        text = words[1]
        to_unblacklist = list(
            {trigger.strip() for trigger in text.split("\n") if trigger.strip()}
        )
        successful = 0
        for trigger in to_unblacklist:
            success = sql.rm_from_blacklist(chat_id, trigger.lower())
            if success:
                successful += 1

        if len(to_unblacklist) == 1:
            if successful:
                send_message(
                    update.effective_message,
                    "{}Removed <code>{}</code> from blacklist in <b>{}</b>!".format(ALKL,
                        html.escape(to_unblacklist[0]), html.escape(chat_name)
                    ),
                    parse_mode=ParseMode.HTML,
                )
            else:
                send_message(
                    update.effective_message, f"{ALKL}This is not a blacklist trigger!"
                )

        elif successful == len(to_unblacklist):
            send_message(
                update.effective_message,
                "{}Removed <code>{}</code> from blacklist in <b>{}</b>!".format(ALKL,
                    successful, html.escape(chat_name)
                ),
                parse_mode=ParseMode.HTML,
            )

        elif not successful:
            send_message(
                update.effective_message,
                f"{ALKL}None of these triggers exist so it can't be removed.",
                parse_mode=ParseMode.HTML,
            )

        else:
            send_message(
                update.effective_message,
                "{}Removed <code>{}</code> from blacklist. {} did not exist, "
                "so were not removed.".format(ALKL,
                    successful, len(to_unblacklist) - successful
                ),
                parse_mode=ParseMode.HTML,
            )
    else:
        send_message(
            update.effective_message,
            f"{ALKL}Tell me which words you would like to remove from blacklist!",
        )


@loggable
@user_admin
def blacklist_mode(update: Update, context: CallbackContext):
    chat = update.effective_chat
    user = update.effective_user
    msg = update.effective_message
    args = context.args

    conn = connected(context.bot, update, chat, user.id, need_admin=True)
    if conn:
        chat = dispatcher.bot.getChat(conn)
        chat_id = conn
        chat_name = dispatcher.bot.getChat(conn).title
    else:
        if update.effective_message.chat.type == "private":
            send_message(
                update.effective_message,
                f"{ALKL}This command can be only used in group not in PM",
            )
            return ""
        chat = update.effective_chat
        chat_id = update.effective_chat.id
        chat_name = update.effective_message.chat.title

    if args:
        if args[0].lower() in ["off", "nothing", "no"]:
            settypeblacklist = "do nothing"
            sql.set_blacklist_strength(chat_id, 0, "0")
        elif args[0].lower() in ["del", "delete"]:
            settypeblacklist = "delete blacklisted message"
            sql.set_blacklist_strength(chat_id, 1, "0")
        elif args[0].lower() == "warn":
            settypeblacklist = "warn the sender"
            sql.set_blacklist_strength(chat_id, 2, "0")
        elif args[0].lower() == "mute":
            settypeblacklist = "mute the sender"
            sql.set_blacklist_strength(chat_id, 3, "0")
        elif args[0].lower() == "kick":
            settypeblacklist = "kick the sender"
            sql.set_blacklist_strength(chat_id, 4, "0")
        elif args[0].lower() == "ban":
            settypeblacklist = "ban the sender"
            sql.set_blacklist_strength(chat_id, 5, "0")
        elif args[0].lower() == "tban":
            if len(args) == 1:
                teks = f"""{ALKL}It looks like you tried to set time value for blacklist but you didn't specified time; Try, `/blacklistmode tban <timevalue>`.
				
Examples of time value: 4m = 4 minutes, 3h = 3 hours, 6d = 6 days, 5w = 5 weeks."""
                send_message(update.effective_message, teks, parse_mode="markdown")
                return ""
            restime = extract_time(msg, args[1])
            if not restime:
                teks = f"""{ALKL}Invalid time value!
Example of time value: 4m = 4 minutes, 3h = 3 hours, 6d = 6 days, 5w = 5 weeks."""
                send_message(update.effective_message, teks, parse_mode="markdown")
                return ""
            settypeblacklist = "{}temporarily ban for {}".format(ALKL,args[1])
            sql.set_blacklist_strength(chat_id, 6, str(args[1]))
        elif args[0].lower() == "tmute":
            if len(args) == 1:
                teks = f"""{ALKL}It looks like you tried to set time value for blacklist but you didn't specified  time; try, `/blacklistmode tmute <timevalue>`.

Examples of time value: 4m = 4 minutes, 3h = 3 hours, 6d = 6 days, 5w = 5 weeks."""
                send_message(update.effective_message, teks, parse_mode="markdown")
                return ""
            restime = extract_time(msg, args[1])
            if not restime:
                teks = f"""{ALKL}Invalid time value!
Examples of time value: 4m = 4 minutes, 3h = 3 hours, 6d = 6 days, 5w = 5 weeks."""
                send_message(update.effective_message, teks, parse_mode="markdown")
                return ""
            settypeblacklist = "{}temporarily mute for {}".format(ALKL,args[1])
            sql.set_blacklist_strength(chat_id, 7, str(args[1]))
        else:
            send_message(
                update.effective_message,
                f"{ALKL}I only understand: off/del/warn/ban/kick/mute/tban/tmute!",
            )
            return ""
        if conn:
            text = "{}Changed blacklist mode: `{}` in *{}*!".format(ALKL,
                settypeblacklist, chat_name
            )
        else:
            text = "{}Changed blacklist mode: `{}`!".format(ALKL,settypeblacklist)
        send_message(update.effective_message, text, parse_mode="markdown")
        return (
            "<b>{}:</b>\n"
            "{}<b>Admin:</b> {}\n"
            "Changed the blacklist mode. will {}.".format(
                html.escape(chat.title),
                ALKL,
                mention_html(user.id, html.escape(user.first_name)),
                settypeblacklist,
            )
        )
    else:
        getmode, getvalue = sql.get_blacklist_setting(chat.id)
        if getmode == 0:
            settypeblacklist = "do nothing"
        elif getmode == 1:
            settypeblacklist = "delete"
        elif getmode == 2:
            settypeblacklist = "warn"
        elif getmode == 3:
            settypeblacklist = "mute"
        elif getmode == 4:
            settypeblacklist = "kick"
        elif getmode == 5:
            settypeblacklist = "ban"
        elif getmode == 6:
            settypeblacklist = "temporarily ban for {}".format(getvalue)
        elif getmode == 7:
            settypeblacklist = "temporarily mute for {}".format(getvalue)
        if conn:
            text = "{}Current blacklistmode: *{}* in *{}*.".format(ALKL,
                settypeblacklist, chat_name
            )
        else:
            text = "{}Current blacklistmode: *{}*.".format(ALKL,settypeblacklist)
        send_message(update.effective_message, text, parse_mode=ParseMode.MARKDOWN)
    return ""


def findall(p, s):
    i = s.find(p)
    while i != -1:
        yield i
        i = s.find(p, i + 1)


@user_not_admin
def del_blacklist(update: Update, context: CallbackContext):
    chat = update.effective_chat
    message = update.effective_message
    user = update.effective_user
    bot = context.bot
    to_match = extract_text(message)
    if not to_match:
        return
    if is_approved(chat.id, user.id):
        return
    getmode, value = sql.get_blacklist_setting(chat.id)

    chat_filters = sql.get_chat_blacklist(chat.id)
    for trigger in chat_filters:
        pattern = r"( |^|[^\w])" + re.escape(trigger) + r"( |$|[^\w])"
        if re.search(pattern, to_match, flags=re.IGNORECASE):
            try:
                if getmode == 0:
                    return
                elif getmode == 1:
                    try:
                        message.delete()
                    except BadRequest:
                        pass
                elif getmode == 2:
                    try:
                        message.delete()
                    except BadRequest:
                        pass
                    warn(
                        update.effective_user,
                        chat,
                        ("{}Using blacklisted trigger: {}".format(ALKL,trigger)),
                        message,
                        update.effective_user,
                    )
                    return
                elif getmode == 3:
                    message.delete()
                    bot.restrict_chat_member(
                        chat.id,
                        update.effective_user.id,
                        permissions=ChatPermissions(can_send_messages=False),
                    )
                    bot.sendMessage(
                        chat.id,
                        f"{ALKL}Muted {user.first_name} for using Blacklisted word: {trigger}!",
                    )
                    return
                elif getmode == 4:
                    message.delete()
                    res = chat.unban_member(update.effective_user.id)
                    if res:
                        bot.sendMessage(
                            chat.id,
                            f"{ALKL}Kicked {user.first_name} for using Blacklisted word: {trigger}!",
                        )
                    return
                elif getmode == 5:
                    message.delete()
                    chat.kick_member(user.id)
                    bot.sendMessage(
                        chat.id,
                        f"{ALKL}Banned {user.first_name} for using Blacklisted word: {trigger}",
                    )
                    return
                elif getmode == 6:
                    message.delete()
                    bantime = extract_time(message, value)
                    chat.kick_member(user.id, until_date=bantime)
                    bot.sendMessage(
                        chat.id,
                        f"{ALKL}Banned {user.first_name} until '{value}' for using Blacklisted word: {trigger}!",
                    )
                    return
                elif getmode == 7:
                    message.delete()
                    mutetime = extract_time(message, value)
                    bot.restrict_chat_member(
                        chat.id,
                        user.id,
                        until_date=mutetime,
                        permissions=ChatPermissions(can_send_messages=False),
                    )
                    bot.sendMessage(
                        chat.id,
                        f"{ALKL}Muted {user.first_name} until '{value}' for using Blacklisted word: {trigger}!",
                    )
                    return
            except BadRequest as excp:
                if excp.message != "Message to delete not found":
                    LOGGER.exception(f"{ALKL}Error while deleting blacklist message.")
            break


def __import_data__(chat_id, data):
    # set chat blacklist
    blacklist = data.get("blacklist", {})
    for trigger in blacklist:
        sql.add_to_blacklist(chat_id, trigger)


def __migrate__(old_chat_id, new_chat_id):
    sql.migrate_chat(old_chat_id, new_chat_id)


def __chat_settings__(chat_id, user_id):
    blacklisted = sql.num_blacklist_chat_filters(chat_id)
    return "{}There are {} blacklisted words.".format(ALKL,blacklisted)


def __stats__():
    return "• {} blacklist triggers, across {} chats.".format(
        sql.num_blacklist_filters(), sql.num_blacklist_filter_chats()
    )




__help__ = f"""{ALKL}
Blacklists are used to stop certain triggers from being said in a group. Any time the trigger is mentioned, 
the message will immediately be deleted. A good combo is sometimes to pair this up with warn filters!
*NOTE*-\n Blacklists do not affect group admins.
⚔️ •/blacklist-\n View the current blacklisted words.
*Admin only*-\n
⚔️ •/addblacklist <triggers>-\n Add a trigger to the blacklist. Each line is considered one trigger, so using different lines will allow you to add multiple triggers.
⚔️ •/unblacklist <triggers>-\n Remove triggers from the blacklist. Same newline logic applies here, so you can remove multiple triggers at once.
⚔️ •/blacklistmode <off/del/warn/ban/kick/mute/tban/tmute>-\n Action to perform when someone sends blacklisted words.
Blacklist sticker is used to stop certain stickers. Whenever a sticker is sent, the message will be deleted immediately.
*NOTE*-\n Blacklist stickers do not affect the group admin
⚔️ •/blsticker-\n See current blacklisted sticker
*Only admin*-\n
⚔️ •/addblsticker <sticker link>-\n Add the sticker trigger to the black list. Can be added via reply sticker
⚔️ •/unblsticker <sticker link>-\n Remove triggers from blacklist. The same newline logic applies here, so you can delete multiple triggers at once
⚔️ •/rmblsticker <sticker link>-\n Same as above
⚔️ •/blstickermode <delete/ban/tban/mute/tmute>-\n sets up a default action on what to do if users use blacklisted stickers
Note:
⚔️ •<sticker link> can be https://t.me/addstickers/<sticker> or just <sticker> or reply to the sticker message
"""
BLACKLIST_WORK = DisableAbleCommandHandler(
    "blacklist", blacklist, admin_ok=True, run_async=True
)
ADD_BLACKLIST_WORK = CommandHandler("addblacklist", add_blacklist, run_async=True)
UNBLACKLIST_WORK = CommandHandler("unblacklist", unblacklist, run_async=True)
BLACKLISTMODE_WORK = CommandHandler("blacklistmode", blacklist_mode, run_async=True)
BLACKLIST_DEL_WORK = MessageHandler(
    (Filters.text | Filters.command | Filters.sticker | Filters.photo) & Filters.chat_type.groups,
    del_blacklist,
    run_async=True,
)

dispatcher.add_handler(BLACKLIST_WORK)
dispatcher.add_handler(ADD_BLACKLIST_WORK)
dispatcher.add_handler(UNBLACKLIST_WORK)
dispatcher.add_handler(BLACKLISTMODE_WORK)
dispatcher.add_handler(BLACKLIST_DEL_WORK, group=BLACKLIST_GROUP)

__handlers__ = [
    BLACKLIST_WORK,
    ADD_BLACKLIST_WORK,
    UNBLACKLIST_WORK,
    BLACKLISTMODE_WORK,
    (BLACKLIST_DEL_WORK, BLACKLIST_GROUP),
]
