from sideloader import *
import SƈαɾLσɾԃ
from SƈαɾLσɾԃ import dispatcher
from ꜰᴜɴᴄᴘᴏᴅ.chat_status import dev_plus


@dev_plus
def allow_groups(update: Update, context: CallbackContext):
    args = context.args
    if not args:
        state = "Lockdown is " + "on" if not SƈαɾLσɾԃ.ALLOW_CHATS else "off"
        update.effective_message.reply_text(f"Current state: {state}")
        return
    if args[0].lower() in ["off", "no"]:
        SƈαɾLσɾԃ.ALLOW_CHATS = True
    elif args[0].lower() in ["yes", "on"]:
        SƈαɾLσɾԃ.ALLOW_CHATS = False
    else:
        update.effective_message.reply_text("Format: /lockdown Yes/No or Off/On")
        return
    update.effective_message.reply_text("Done! Lockdown value toggled.")


@dev_plus
def leave(update: Update, context: CallbackContext):
    bot = context.bot
    args = context.args
    if args:
        chat_id = str(args[0])
        try:
            bot.leave_chat(int(chat_id))
        except TelegramError:
            update.effective_message.reply_text(
                "Beep boop, I could not leave that group(dunno why tho)."
            )
            return
        with suppress(Unauthorized):
            update.effective_message.reply_text("Beep boop, I left that soup!.")
    else:
        update.effective_message.reply_text("Send a valid chat ID")


LEAVE_WORK = CommandHandler("leave", leave, run_async=True)
ALLOWGROUPS_WORK = CommandHandler("lockdown", allow_groups, run_async=True)

dispatcher.add_handler(ALLOWGROUPS_WORK)
dispatcher.add_handler(LEAVE_WORK)

__Hype_Scar_Var__ = "Dev"
__handlers__ = [LEAVE_WORK, ALLOWGROUPS_WORK]
