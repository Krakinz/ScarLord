from sideloader import *
from SKARSHOTS.clear_cmd_sql import get_clearcmd
from SƈαɾLσɾԃ import dispatcher
from SKARS.TURNOFF import DisableAbleCommandHandler
from ꜰᴜɴᴄᴘᴏᴅ.misc import delete

__mod_name__ = "Talk 2 Speech"
TTS = TTS =__help__ = f"""{ALKL}
This is a module made to convert any english text to speech.
Try it with funny words lol!

⚔️ •/talk | /speak | /tts | /t <text>:
    convert text to speech  
"""

US = f"""{ALKL}
Sent via :@HVScarlordBot
GitHub:@HypeVoidBot"""

def talk(update: Update, context: CallbackContext):
    args = context.args
    message = update.effective_message
    chat = update.effective_chat
    delmsg = ""

    if message.reply_to_message:
        delmsg = message.reply_to_message.text

    if args:
        delmsg = "  ".join(args).lower()
        update.message.chat.send_action(ChatAction.RECORD_AUDIO)
        lang = "ml"
        talk = gTTS(delmsg, lang)
        talk.save("HVSTTS.mp3")
        musicraw = open("HVSTTS.mp3", "rb")
        linelist = list(musicraw)
        linecount = len(linelist)
        if linecount == 1:
            update.message.chat.send_action(ChatAction.RECORD_AUDIO)
            lang = "en"
            talk = gTTS(delmsg, lang)
            talk.save("HVSTTS.mp3")
        music = open(
        "HVSTTS.mp3",
        "rb")
        delmsg = update.message.reply_voice(music, caption=US,quote=False)
        os.remove("HVSTTS.mp3")
    else:
        delmsg = message.reply_text(
        f"""{ALKL}Reply a message or give something like\n⚔️ •/talk | /speak | /tts | /t <text>:""",
        parse_mode = ParseMode.MARKDOWN)
    cleartime = get_clearcmd(chat.id, "talk")
    if cleartime:
        context.dispatcher.run_async(delete, delmsg, cleartime.time)



def talk(update: Update, context: CallbackContext):
    args = context.args
    message = update.effective_message
    chat = update.effective_chat
    delmsg = ""

    if message.reply_to_message:
        delmsg = message.reply_to_message.text

    if args:
        delmsg = "  ".join(args).lower()
        update.message.chat.send_action(ChatAction.RECORD_AUDIO)
        lang = "ml"
        talk = gTTS(delmsg, lang)
        talk.save("HVSTTS.mp3")
        musicraw = open("HVSTTS.mp3", "rb")
        linelist = list(musicraw)
        linecount = len(linelist)
        if linecount == 1:
            update.message.chat.send_action(ChatAction.RECORD_AUDIO)
            lang = "hd"
            talk = gTTS(delmsg, lang)
            talk.save("HVSTTS.mp3")
        music = open(
        "HVSTTS.mp3",
        "rb")
        delmsg = update.message.reply_voice(music, caption=US,quote=False)
        os.remove("HVSTTS.mp3")
    else:
        delmsg = message.reply_text(
        f"""{ALKL}Reply a message or give something like\n⚔️ •/talk | /speak | /tts | /t <text>:""",
        parse_mode = ParseMode.MARKDOWN)
    cleartime = get_clearcmd(chat.id, "talk")
    if cleartime:
        context.dispatcher.run_async(delete, delmsg, cleartime.time)

TTS_WORK = DisableAbleCommandHandler(["talk", "speak", "tts", "t"], talk, run_async=True)
__handlers__ = [TTS_WORK]
dispatcher.add_handler(TTS_WORK)