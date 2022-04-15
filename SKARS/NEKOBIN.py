from sideloader import *
from SƈαɾLσɾԃ import dispatcher
from SKARS.TURNOFF import DisableAbleCommandHandler

__mod_name__ = "nekobin"

def paste(update: Update, context: CallbackContext):
    args = context.args
    message = update.effective_message

    if message.reply_to_message:
        data = message.reply_to_message.text

    elif len(args) >= 1:
        data = message.text.split(None, 1)[1]

    else:
        message.reply_text("What am I supposed to do with this?")
        return

    key = (
        requests.post("https://nekobin.com/api/documents", json={"content": data})
        .json()
        .get("result")
        .get("key")
    )

    url = f"https://nekobin.com/{key}"

    reply_text = f"Nekofied to *Nekobin* : {url}"

    message.reply_text(
        reply_text, parse_mode=ParseMode.MARKDOWN, disable_web_page_preview=True
    )


PASTE_WORK = DisableAbleCommandHandler("paste", paste, run_async=True)
dispatcher.add_handler(PASTE_WORK)

__help__ = f"""{ALKL} Nekobin"""

__Hype_Scar_Var__ = "nekobin"
__command_list__ = ["paste"]
__handlers__ = [PASTE_WORK]
