from sideloader import *
from SƈαɾLσɾԃ import dispatcher
from SKARS.TURNOFF import DisableAbleCommandHandler
from ꜰᴜɴᴄᴘᴏᴅ.misc import delete
from SKARSHOTS.clear_cmd_sql import get_clearcmd

__mod_name__ = "Dictionary"

DICT = DICT = __help__ = f"""{ALKL}
Ever Found yourself in a situation where you don't know the meaning of a certain word or a phase?
This module was desigened to support you with such a situation.

⚔️ •/dict:
    The dictionary of information. Use in either groups or private.
"""


def dict(update: Update, context: CallbackContext):
    message = update.effective_message
    chat = update.effective_chat
    text = message.text[len("/dict ") :]
    results = requests.get(
        f"https://api.urbandictionary.com/v0/define?term={text}"
    ).json()
    try:
        reply_text = f'*{text}*\n\n{results["list"][0]["definition"]}\n\n_{results["list"][0]["example"]}_'
    except:
        reply_text = "No results found."
    delmsg = message.reply_text(reply_text, parse_mode=ParseMode.MARKDOWN)

    cleartime = get_clearcmd(chat.id, "dict")

    if cleartime:
        context.dispatcher.run_async(delete, delmsg, cleartime.time)


DICT_WORK = DisableAbleCommandHandler(["dict"], dict, run_async=True)

dispatcher.add_handler(DICT_WORK)

__command_list__ = ["dict"]
__handlers__ = [DICT_WORK]
