from sideloader import *
import SKARS.FUNST as FUNST
from SƈαɾLσɾԃ import dispatcher
from SKARS.TURNOFF import DisableAbleCommandHandler
from ꜰᴜɴᴄᴘᴏᴅ.chat_status import is_user_admin
from ꜰᴜɴᴄᴘᴏᴅ.extraction import extract_user
from ꜰᴜɴᴄᴘᴏᴅ.misc import delete
from SKARSHOTS.clear_cmd_sql import get_clearcmd

GIF_ID = "CgACAgQAAx0CSVUvGgAC7KpfWxMrgGyQs-GUUJgt-TSO8cOIDgACaAgAAlZD0VHT3Zynpr5nGxsE"

__mod_name__ = "Funs"

def runs(update: Update, context: CallbackContext):
    deletion(update, context, update.effective_message.reply_text(random.choice(FUNST.RUN_STRINGS)))


def sanitize(update: Update, context: CallbackContext):
    message = update.effective_message
    name = (
        message.reply_to_message.from_user.first_name
        if message.reply_to_message
        else message.from_user.first_name
    )
    reply_animation = (
        message.reply_to_message.reply_animation
        if message.reply_to_message
        else message.reply_animation
    )
    deletion(update, context, reply_animation(random.choice(FUNST.GIFS), caption=f"*Sanitizes {name}*"))


def slap(update: Update, context: CallbackContext):
    bot, args = context.bot, context.args
    message = update.effective_message
    chat = update.effective_chat

    reply_text = (
        message.reply_to_message.reply_text
        if message.reply_to_message
        else message.reply_text
    )

    curr_user = html.escape(message.from_user.first_name)
    user_id = extract_user(message, args)

    if user_id == bot.id:
        temp = random.choice(FUNST.SLAP_SAITAMA_TEMPLATES)

        if isinstance(temp, list):
            if temp[2] == "tmute":
                if is_user_admin(chat, message.from_user.id):
                    reply_text(temp[1])
                    return

                mutetime = int(time.time() + 60)
                bot.restrict_chat_member(
                    chat.id,
                    message.from_user.id,
                    until_date=mutetime,
                    permissions=ChatPermissions(can_send_messages=False),
                )
            reply_text(temp[0])
        else:
            reply_text(temp)
        return

    if user_id:

        slapped_user = bot.get_chat(user_id)
        user1 = curr_user
        user2 = html.escape(slapped_user.first_name)

    else:
        user1 = bot.first_name
        user2 = curr_user

    temp = random.choice(FUNST.SLAP_TEMPLATES)
    item = random.choice(FUNST.ITEMS)
    hit = random.choice(FUNST.HIT)
    throw = random.choice(FUNST.THROW)

    if update.effective_user.id == 1096215023:
        temp = "@NeoTheKitty scratches {user2}"

    reply = temp.format(user1=user1, user2=user2, item=item, hits=hit, throws=throw)

    deletion(update, context, reply_text(reply, parse_mode=ParseMode.HTML))


def pat(update: Update, context: CallbackContext):
    bot = context.bot
    args = context.args
    message = update.effective_message

    reply_to = message.reply_to_message if message.reply_to_message else message

    curr_user = html.escape(message.from_user.first_name)
    user_id = extract_user(message, args)

    if user_id:
        patted_user = bot.get_chat(user_id)
        user1 = curr_user
        user2 = html.escape(patted_user.first_name)

    else:
        user1 = bot.first_name
        user2 = curr_user

    pat_type = random.choice(("Text", "Gif", "Sticker"))
    if pat_type == "Gif":
        try:
            temp = random.choice(FUNST.PAT_GIFS)
            reply_to.reply_animation(temp)
        except BadRequest:
            pat_type = "Text"

    if pat_type == "Sticker":
        try:
            temp = random.choice(FUNST.PAT_STICKERS)
            reply_to.reply_sticker(temp)
        except BadRequest:
            pat_type = "Text"

    if pat_type == "Text":
        temp = random.choice(FUNST.PAT_TEMPLATES)
        reply = temp.format(user1=user1, user2=user2)
        deletion(update, context, reply_to.reply_text(reply, parse_mode=ParseMode.HTML))


def roll(update: Update, context: CallbackContext):
    deletion(update, context, update.message.reply_text(random.choice(range(1, 7))))


def shout(update: Update, context: CallbackContext):
    args = context.args
    text = " ".join(args)
    result = []
    result.append(" ".join(list(text)))
    for pos, symbol in enumerate(text[1:]):
        result.append(symbol + " " + "  " * pos + symbol)
    result = list("\n".join(result))
    result[0] = text[0]
    result = "".join(result)
    msg = "```\n" + result + "```"
    deletion(update, context, update.effective_message.reply_text(msg, parse_mode="MARKDOWN"))


def toss(update: Update, context: CallbackContext):
    deletion(update, context, update.message.reply_text(random.choice(FUNST.TOSS)))


def shrug(update: Update, context: CallbackContext):
    msg = update.effective_message
    reply_text = (
        msg.reply_to_message.reply_text if msg.reply_to_message else msg.reply_text
    )
    deletion(update, context, reply_text(r"¯\_(ツ)_/¯"))


def bluetext(update: Update, context: CallbackContext):
    msg = update.effective_message
    reply_text = (
        msg.reply_to_message.reply_text if msg.reply_to_message else msg.reply_text
    )
    deletion(update, context, reply_text(
        "/BLUE /TEXT\n/MUST /CLICK\n/I /AM /A /STUPID /ANIMAL /THAT /IS /ATTRACTED /TO /COLORS"
    ))


def rlg(update: Update, context: CallbackContext):
    eyes = random.choice(FUNST.EYES)
    mouth = random.choice(FUNST.MOUTHS)
    ears = random.choice(FUNST.EARS)

    if len(eyes) == 2:
        repl = ears[0] + eyes[0] + mouth[0] + eyes[1] + ears[1]
    else:
        repl = ears[0] + eyes[0] + mouth[0] + eyes[0] + ears[1]
    deletion(update, context, update.message.reply_text(repl))


def decide(update: Update, context: CallbackContext):
    reply_text = (
        update.effective_message.reply_to_message.reply_text
        if update.effective_message.reply_to_message
        else update.effective_message.reply_text
    )
    deletion(update, context, reply_text(random.choice(FUNST.DECIDE)))


def eightball(update: Update, context: CallbackContext):
    reply_text = (
        update.effective_message.reply_to_message.reply_text
        if update.effective_message.reply_to_message
        else update.effective_message.reply_text
    )
    deletion(update, context, reply_text(random.choice(FUNST.EIGHTBALL)))


def table(update: Update, context: CallbackContext):
    reply_text = (
        update.effective_message.reply_to_message.reply_text
        if update.effective_message.reply_to_message
        else update.effective_message.reply_text
    )
    deletion(update, context, reply_text(random.choice(FUNST.TABLE)))


normiefont = [
    "a",
    "b",
    "c",
    "d",
    "e",
    "f",
    "g",
    "h",
    "i",
    "j",
    "k",
    "l",
    "m",
    "n",
    "o",
    "p",
    "q",
    "r",
    "s",
    "t",
    "u",
    "v",
    "w",
    "x",
    "y",
    "z",
]
weebyfont = [
    "卂",
    "乃",
    "匚",
    "刀",
    "乇",
    "下",
    "厶",
    "卄",
    "工",
    "丁",
    "长",
    "乚",
    "从",
    "𠘨",
    "口",
    "尸",
    "㔿",
    "尺",
    "丂",
    "丅",
    "凵",
    "リ",
    "山",
    "乂",
    "丫",
    "乙",
]


def weebify(update: Update, context: CallbackContext):
    args = context.args
    message = update.effective_message
    string = ""

    if message.reply_to_message:
        string = message.reply_to_message.text.lower().replace(" ", "  ")

    if args:
        string = "  ".join(args).lower()

    if not string:
        deletion(update, context, message.reply_text("Usage is `/weebify <text>`", parse_mode=ParseMode.MARKDOWN))
        return

    for normiecharacter in string:
        if normiecharacter in normiefont:
            weebycharacter = weebyfont[normiefont.index(normiecharacter)]
            string = string.replace(normiecharacter, weebycharacter)

    if message.reply_to_message:
        deletion(update, context, message.reply_to_message.reply_text(string))
    else:
        deletion(update, context, message.reply_text(string))


def deletion(update: Update, context: CallbackContext, delmsg):
    chat = update.effective_chat
    cleartime = get_clearcmd(chat.id, "fun")

    if cleartime:
        context.dispatcher.run_async(delete, delmsg, cleartime.time)



__help__ = f"""{ALKL}Fun"""

SANITIZE_WORK = DisableAbleCommandHandler("sanitize", sanitize, run_async=True)
RUNS_WORK = DisableAbleCommandHandler("runs", runs, run_async=True)
SLAP_WORK = DisableAbleCommandHandler("slap", slap, run_async=True)
PAT_WORK = DisableAbleCommandHandler("pat", pat, run_async=True)
ROLL_WORK = DisableAbleCommandHandler("roll", roll, run_async=True)
TOSS_WORK = DisableAbleCommandHandler("toss", toss, run_async=True)
SHRUG_WORK = DisableAbleCommandHandler("shrug", shrug, run_async=True)
BLUETEXT_WORK = DisableAbleCommandHandler("bluetext", bluetext, run_async=True)
RLG_WORK = DisableAbleCommandHandler("rlg", rlg, run_async=True)
DECIDE_WORK = DisableAbleCommandHandler("decide", decide, run_async=True)
EIGHTBALL_WORK = DisableAbleCommandHandler("8ball", eightball, run_async=True)
TABLE_WORK = DisableAbleCommandHandler("table", table, run_async=True)
SHOUT_WORK = DisableAbleCommandHandler("shout", shout, run_async=True)
WEEBIFY_WORK = DisableAbleCommandHandler("weebify", weebify, run_async=True)

dispatcher.add_handler(WEEBIFY_WORK)
dispatcher.add_handler(SHOUT_WORK)
dispatcher.add_handler(SANITIZE_WORK)
dispatcher.add_handler(RUNS_WORK)
dispatcher.add_handler(SLAP_WORK)
dispatcher.add_handler(PAT_WORK)
dispatcher.add_handler(ROLL_WORK)
dispatcher.add_handler(TOSS_WORK)
dispatcher.add_handler(SHRUG_WORK)
dispatcher.add_handler(BLUETEXT_WORK)
dispatcher.add_handler(RLG_WORK)
dispatcher.add_handler(DECIDE_WORK)
dispatcher.add_handler(EIGHTBALL_WORK)
dispatcher.add_handler(TABLE_WORK)

__Hype_Scar_Var__ = "Fun"
__command_list__ = [
    "runs",
    "slap",
    "roll",
    "toss",
    "shrug",
    "bluetext",
    "rlg",
    "decide",
    "table",
    "pat",
    "sanitize",
    "shout",
    "weebify",
    "8ball",
]
__handlers__ = [
    RUNS_WORK,
    SLAP_WORK,
    PAT_WORK,
    ROLL_WORK,
    TOSS_WORK,
    SHRUG_WORK,
    BLUETEXT_WORK,
    RLG_WORK,
    DECIDE_WORK,
    TABLE_WORK,
    SANITIZE_WORK,
    SHOUT_WORK,
    WEEBIFY_WORK,
    EIGHTBALL_WORK,
]
