from sideloader import *
import SKARSHOTS.rules_sql as sql
from SƈαɾLσɾԃ import dispatcher
from ꜰᴜɴᴄᴘᴏᴅ.chat_status import user_admin
from ꜰᴜɴᴄᴘᴏᴅ.string_handling import markdown_parser


__mod_name__ = "📠 ʀᴜʟᴇꜱ"
__help__ = f"""{ALKL}
⚔️ •/rules-\n get the rules for this chat.

*Admins only*-\n
⚔️ •/setrules <your rules here>-\n set the rules for this chat.
⚔️ •/clearrules-\n clear the rules for this chat.
"""

def get_rules(update: Update, context: CallbackContext):
    chat_id = update.effective_chat.id
    send_rules(update, chat_id)


# Do not async - not from a handler
def send_rules(update, chat_id, from_pm=False):
    bot = dispatcher.bot
    user = update.effective_user  # type: Optional[User]
    reply_msg = update.message.reply_to_message
    try:
        chat = bot.get_chat(chat_id)
    except BadRequest as excp:
        if excp.message == "Chat not found" and from_pm:
            bot.send_message(
                user.id,
                f"{ALKL}The rules shortcut for this chat hasn't been set properly! Ask admins to "
                "fix this.\nMaybe they forgot the hyphen in ID",
            )
            return
        else:
            raise

    rules = sql.get_rules(chat_id)
    text = f"{ALKL}The rules for *{escape_markdown(chat.title)}* are:\n\n{rules}"

    if from_pm and rules:
        bot.send_message(
            user.id, text, parse_mode=ParseMode.MARKDOWN, disable_web_page_preview=True
        )
    elif from_pm:
        bot.send_message(
            user.id,
            f"{ALKL}The group admins haven't set any rules for this chat yet. "
            "This probably doesn't mean it's lawless though...!",
        )
    elif rules and reply_msg:
        reply_msg.reply_text(
            "Please click the button below to see the rules.",
            reply_markup=InlineKeyboardMarkup(
                [
                    [
                        InlineKeyboardButton(
                            text="Rules", url=f"t.me/{bot.username}?start={chat_id}"
                        )
                    ]
                ]
            ),
        )
    elif rules:
        update.effective_message.reply_text(
            f"{ALKL}Please click the button below to see the rules.",
            reply_markup=InlineKeyboardMarkup(
                [
                    [
                        InlineKeyboardButton(
                            text="Rules", url=f"t.me/{bot.username}?start={chat_id}"
                        )
                    ]
                ]
            ),
        )
    else:
        update.effective_message.reply_text(
            f"{ALKL}The group admins haven't set any rules for this chat yet. "
            "This probably doesn't mean it's lawless though...!"
        )


@user_admin
def set_rules(update: Update, context: CallbackContext):
    chat_id = update.effective_chat.id
    msg = update.effective_message  # type: Optional[Message]
    raw_text = msg.text
    args = raw_text.split(None, 1)  # use python's maxsplit to separate cmd and args
    if len(args) == 2:
        txt = args[1]
        offset = len(txt) - len(raw_text)  # set correct offset relative to command
        markdown_rules = markdown_parser(
            txt, entities=msg.parse_entities(), offset=offset
        )

        sql.set_rules(chat_id, markdown_rules)
        update.effective_message.reply_text(f"{ALKL}Successfully set rules for this group.")


@user_admin
def clear_rules(update: Update, context: CallbackContext):
    chat_id = update.effective_chat.id
    sql.set_rules(chat_id, "")
    update.effective_message.reply_text(f"{ALKL}Successfully cleared rules!")


def __stats__():
    return f"{ALKL}• {sql.num_chats()} chats have rules set."


def __import_data__(chat_id, data):
    # set chat rules
    rules = data.get("info", {}).get("rules", "")
    sql.set_rules(chat_id, rules)


def __migrate__(old_chat_id, new_chat_id):
    sql.migrate_chat(old_chat_id, new_chat_id)


def __chat_settings__(chat_id, user_id):
    return f"{ALKL}This chat has had it's rules set: `{bool(sql.get_rules(chat_id))}`"






GET_RULES_WORK = CommandHandler("rules", get_rules, filters=Filters.chat_type.groups, run_async=True)
SET_RULES_WORK = CommandHandler("setrules", set_rules, filters=Filters.chat_type.groups, run_async=True)
RESET_RULES_WORK = CommandHandler("clearrules", clear_rules, filters=Filters.chat_type.groups, run_async=True)

dispatcher.add_handler(GET_RULES_WORK)
dispatcher.add_handler(SET_RULES_WORK)
dispatcher.add_handler(RESET_RULES_WORK)
