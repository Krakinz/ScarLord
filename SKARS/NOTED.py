from sideloader import *
import SKARSHOTS.notes_sql as sql
from SKARSHOTS.clear_cmd_sql import get_clearcmd
from SƈαɾLσɾԃ import LOGGER, JOIN_LOGGER, dispatcher, KLAW_LINGS
from SKARS.TURNOFF import DisableAbleCommandHandler
from ꜰᴜɴᴄᴘᴏᴅ.handlers import MessageHandlerChecker
from ꜰᴜɴᴄᴘᴏᴅ.chat_status import user_admin, connection_status
from ꜰᴜɴᴄᴘᴏᴅ.misc import build_keyboard, revert_buttons, delete
from ꜰᴜɴᴄᴘᴏᴅ.msg_types import get_note_type
from ꜰᴜɴᴄᴘᴏᴅ.string_handling import (
    escape_invalid_curly_brackets,
)
from SKARS.private_notes import getprivatenotes


__mod_name__ = "📜 ɴᴏᴛᴇꜱ"


FILE_MATCHER = re.compile(r"^###file_id(!photo)?###:(.*?)(?:\s|$)")
STICKER_MATCHER = re.compile(r"^###sticker(!photo)?###:")
BUTTON_MATCHER = re.compile(r"^###button(!photo)?###:(.*?)(?:\s|$)")
MYFILE_MATCHER = re.compile(r"^###file(!photo)?###:")
MYPHOTO_MATCHER = re.compile(r"^###photo(!photo)?###:")
MYAUDIO_MATCHER = re.compile(r"^###audio(!photo)?###:")
MYVOICE_MATCHER = re.compile(r"^###voice(!photo)?###:")
MYVIDEO_MATCHER = re.compile(r"^###video(!photo)?###:")
MYVIDEONOTE_MATCHER = re.compile(r"^###video_note(!photo)?###:")
ENUM_FUNC_MAP = {
    sql.Types.TEXT.value: dispatcher.bot.send_message,
    sql.Types.BUTTON_TEXT.value: dispatcher.bot.send_message,
    sql.Types.STICKER.value: dispatcher.bot.send_sticker,
    sql.Types.DOCUMENT.value: dispatcher.bot.send_document,
    sql.Types.PHOTO.value: dispatcher.bot.send_photo,
    sql.Types.AUDIO.value: dispatcher.bot.send_audio,
    sql.Types.VOICE.value: dispatcher.bot.send_voice,
    sql.Types.VIDEO.value: dispatcher.bot.send_video,
}
def get(update: Update, context: CallbackContext, notename, show_none=True, no_format=False):
    bot = context.bot
    user = update.effective_user
    chat_id = update.effective_message.chat.id
    note_chat_id = update.effective_chat.id
    note = sql.get_note(note_chat_id, notename)
    message = update.effective_message  # type: Optional[Message]

    if note:
        if MessageHandlerChecker.check_user(update.effective_user.id):
            return
        # If we're replying to a message, reply to that message (unless it's an error)
        if message.reply_to_message:
            reply_id = message.reply_to_message.message_id
        else:
            reply_id = message.message_id
        if note.is_reply:
            if JOIN_LOGGER:
                try:
                    bot.forward_message(
                        chat_id=chat_id, from_chat_id=JOIN_LOGGER, message_id=note.value
                    )
                except BadRequest as excp:
                    if excp.message == "Message to forward not found":
                        message.reply_text(
                            f"{ALKL}This message seems to have been lost - I'll remove it "
                            "from your notes list."
                        )
                        sql.rm_note(note_chat_id, notename)
                    else:
                        raise
            else:
                try:
                    bot.forward_message(
                        chat_id=chat_id, from_chat_id=chat_id, message_id=note.value
                    )
                except BadRequest as excp:
                    if excp.message == "Message to forward not found":
                        message.reply_text(
                            f"{ALKL}Looks like the original sender of this note has deleted "
                            "their message - sorry! Get your bot admin to start using a "
                            "message dump to avoid this. I'll remove this note from "
                            "your saved notes."
                        )
                        sql.rm_note(note_chat_id, notename)
                    else:
                        raise
        else:
            VALID_NOTE_FORMATTERS = [
                "first",
                "last",
                "fullname",
                "username",
                "id",
                "chatname",
                "mention",
            ]
            valid_format = escape_invalid_curly_brackets(
                note.value, VALID_NOTE_FORMATTERS
            )
            if valid_format:
                if not no_format:
                    if "%%%" in valid_format:
                        split = valid_format.split("%%%")
                        if all(split):
                            text = random.choice(split)
                        else:
                            text = valid_format
                    else:
                        text = valid_format
                else:
                    text = valid_format
                text = text.format(
                    first=escape_markdown(message.from_user.first_name),
                    last=escape_markdown(
                        message.from_user.last_name or message.from_user.first_name
                    ),
                    fullname=escape_markdown(
                        " ".join(
                            [message.from_user.first_name, message.from_user.last_name]
                            if message.from_user.last_name
                            else [message.from_user.first_name]
                        )
                    ),
                    username="@" + message.from_user.username
                    if message.from_user.username
                    else mention_markdown(
                        message.from_user.id, message.from_user.first_name
                    ),
                    mention=mention_markdown(
                        message.from_user.id, message.from_user.first_name
                    ),
                    chatname=escape_markdown(
                        message.chat.title
                        if message.chat.type != "private"
                        else message.from_user.first_name
                    ),
                    id=message.from_user.id,
                )
            else:
                text = ""

            keyb = []
            parseMode = ParseMode.MARKDOWN
            buttons = sql.get_buttons(note_chat_id, notename)
            if no_format:
                parseMode = None
                text += revert_buttons(buttons)
            else:
                keyb = build_keyboard(buttons)

            keyboard = InlineKeyboardMarkup(keyb)

            try:
                setting = getprivatenotes(chat_id)
                if note.msgtype in (sql.Types.BUTTON_TEXT, sql.Types.TEXT):
                    if setting:
                        bot.send_message(
                            user.id,
                            text,
                            parse_mode=parseMode,
                            disable_web_page_preview=True,
                            reply_markup=keyboard,
                        )
                    else:
                        delmsg = bot.send_message(
                            chat_id,
                            text,
                            reply_to_message_id=reply_id,
                            parse_mode=parseMode,
                            disable_web_page_preview=True,
                            reply_markup=keyboard,
                        )

                        cleartime = get_clearcmd(chat_id, "notes")

                        if cleartime:
                            context.dispatcher.run_async(delete, delmsg, cleartime.time)

                elif note.msgtype in (sql.Types.STICKER, sql.Types.STICKER):
                    if setting:
                        ENUM_FUNC_MAP[note.msgtype](
                            user.id,
                            note.file,
                            reply_to_message_id=reply_id,
                            reply_markup=keyboard,
                        )
                    else:
                        delmsg = ENUM_FUNC_MAP[note.msgtype](
                            chat_id,
                            note.file,
                            reply_to_message_id=reply_id,
                            reply_markup=keyboard,
                        )

                        cleartime = get_clearcmd(chat_id, "notes")

                        if cleartime:
                            context.dispatcher.run_async(delete, delmsg, cleartime.time)
                else:
                    if setting:
                        ENUM_FUNC_MAP[note.msgtype](
                            user.id,
                            note.file,
                            caption=text,
                            reply_to_message_id=reply_id,
                            parse_mode=parseMode,
                            reply_markup=keyboard,
                        )
                    else:
                        delmsg = ENUM_FUNC_MAP[note.msgtype](
                            chat_id,
                            note.file,
                            caption=text,
                            reply_to_message_id=reply_id,
                            parse_mode=parseMode,
                            reply_markup=keyboard,
                        )

                        cleartime = get_clearcmd(chat_id, "notes")

                        if cleartime:
                            context.dispatcher.run_async(delete, delmsg, cleartime.time)

            except BadRequest as excp:
                if excp.message == "Entity_mention_user_invalid":
                    message.reply_text(
                        f"{ALKL}Looks like you tried to mention someone I've never seen before. If you really "
                        "want to mention them, forward one of their messages to me, and I'll be able "
                        "to tag them!"
                    )
                elif FILE_MATCHER.match(note.value):
                    message.reply_text(
                        f"{ALKL}This note was an incorrectly imported file from another bot - I can't use "
                        "it. If you really need it, you'll have to save it again. In "
                        "the meantime, I'll remove it from your notes list."
                    )
                    sql.rm_note(note_chat_id, notename)
                else:
                    message.reply_text(
                        f"{ALKL}This note could not be sent, as it is incorrectly formatted. Ask in "
                        f"@hypevoids | @hypevoidsoul if you can't figure out why!"
                    )
                    LOGGER.exception(
                        "Could not parse message #%s in chat %s",
                        notename,
                        str(note_chat_id),
                    )
                    LOGGER.warning("Message was: %s", str(note.value))
        return
    elif show_none:
        message.reply_text(f"{ALKL}This note doesn't exist")


@connection_status
def cmd_get(update: Update, context: CallbackContext):
    bot, args = context.bot, context.args
    if len(args) >= 2 and args[1].lower() == "noformat":
        get(update, context, args[0].lower(), show_none=True, no_format=True)
    elif len(args) >= 1:
        get(update, context, args[0].lower(), show_none=True)
    else:
        update.effective_message.reply_text("Get rekt")


@connection_status
def hash_get(update: Update, context: CallbackContext):
    message = update.effective_message.text
    fst_word = message.split()[0]
    no_hash = fst_word[1:].lower()
    get(update, context, no_hash, show_none=False)


@connection_status
def slash_get(update: Update, context: CallbackContext):
    message, chat_id = update.effective_message.text, update.effective_chat.id
    no_slash = message[1:]
    note_list = sql.get_all_chat_notes(chat_id)

    try:
        noteid = note_list[int(no_slash) - 1]
        note_name = str(noteid).strip(">").split()[1]
        get(update, context, note_name, show_none=False)
    except IndexError:
        update.effective_message.reply_text(f"{ALKL}Wrong Note ID 😾")


@user_admin
@connection_status
def save(update: Update, context: CallbackContext):
    chat_id = update.effective_chat.id
    msg = update.effective_message  # type: Optional[Message]

    note_name, text, data_type, content, buttons = get_note_type(msg)
    note_name = note_name.lower()
    if data_type is None:
        msg.reply_text(f"{ALKL}Dude, there's no note")
        return

    sql.add_note_to_db(
        chat_id, note_name, text, data_type, buttons=buttons, file=content
    )

    msg.reply_text(
        f"{ALKL}Yas! Added `{note_name}`.\nGet it with /get `{note_name}`, or `#{note_name}`",
        parse_mode=ParseMode.MARKDOWN,
    )

    if msg.reply_to_message and msg.reply_to_message.from_user.is_bot:
        if text:
            msg.reply_text(
                f"{ALKL}Seems like you're trying to save a message from a bot. Unfortunately, "
                "bots can't forward bot messages, so I can't save the exact message. "
                "\nI'll save all the text I can, but if you want more, you'll have to "
                "forward the message yourself, and then save it."
            )
        else:
            msg.reply_text(
                f"{ALKL}Bots are kinda handicapped by telegram, making it hard for bots to "
                "interact with other bots, so I can't save this message "
                "like I usually would - do you mind forwarding it and "
                "then saving that new message? Thanks!"
            )
        return


@user_admin
@connection_status
def clear(update: Update, context: CallbackContext):
    args = context.args
    chat_id = update.effective_chat.id
    if len(args) >= 1:
        notename = args[0].lower()

        if sql.rm_note(chat_id, notename):
            update.effective_message.reply_text(f"{ALKL}Successfully removed note.")
        else:
            update.effective_message.reply_text(f"{ALKL}That's not a note in my database!")


def clearall(update: Update, context: CallbackContext):
    chat = update.effective_chat
    user = update.effective_user
    member = chat.get_member(user.id)
    if member.status != "creator" and user.id not in KLAW_LINGS:
        update.effective_message.reply_text(
            f"{ALKL}Only the chat owner can clear all notes at once."
        )
    else:
        buttons = InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton(
                        text="Delete all notes", callback_data="notes_rmall"
                    )
                ],
                [InlineKeyboardButton(text="Cancel", callback_data="notes_cancel")],
            ]
        )
        update.effective_message.reply_text(
            f"{ALKL}Are you sure you would like to clear ALL notes in {chat.title}? This action cannot be undone.",
            reply_markup=buttons,
            parse_mode=ParseMode.MARKDOWN,
        )


def clearall_btn(update: Update, context: CallbackContext):
    query = update.callback_query
    chat = update.effective_chat
    message = update.effective_message
    member = chat.get_member(query.from_user.id)
    if query.data == "notes_rmall":
        if member.status == "creator" or query.from_user.id in KLAW_LINGS:
            note_list = sql.get_all_chat_notes(chat.id)
            try:
                for notename in note_list:
                    note = notename.name.lower()
                    sql.rm_note(chat.id, note)
                message.edit_text("Deleted all notes.")
            except BadRequest:
                return

        if member.status == "administrator":
            query.answer(f"{ALKL}Only owner of the chat can do this.")

        if member.status == "member":
            query.answer(f"{ALKL}You need to be admin to do this.")
    elif query.data == "notes_cancel":
        if member.status == "creator" or query.from_user.id in KLAW_LINGS:
            message.edit_text(f"{ALKL}Clearing of all notes has been cancelled.")
            return
        if member.status == "administrator":
            query.answer(f"{ALKL}Only owner of the chat can do this.")
        if member.status == "member":
            query.answer(f"{ALKL}You need to be admin to do this.")


@connection_status
def list_notes(update: Update, context: CallbackContext):
    bot = context.bot
    user = update.effective_user
    chat_id = update.effective_chat.id
    note_list = sql.get_all_chat_notes(chat_id)
    notes = len(note_list) + 1
    msg = f"{ALKL}Get note by `/notenumber` or `#notename` \n\n  *ID*    *Note* \n"
    msg_pm = f"{ALKL}*Notes from {update.effective_chat.title}* \nGet note by `/notenumber` or `#notename` in group \n\n  *ID*    *Note* \n"
    for note_id, note in zip(range(1, notes), note_list):
        if note_id < 10:
            note_name = f"{note_id:2}.  `{(note.name.lower())}`\n"
        else:
            note_name = f"{note_id}.  `{(note.name.lower())}`\n"
        if len(msg) + len(note_name) > MAX_MESSAGE_LENGTH:
            update.effective_message.reply_text(msg, parse_mode=ParseMode.MARKDOWN)
            msg = ""
            msg_pm = ""
        msg += note_name
        msg_pm += note_name

    if not note_list:
        try:
            update.effective_message.reply_text(f"{ALKL}No notes in this chat!")
        except BadRequest:
            update.effective_message.reply_text(f"{ALKL}No notes in this chat!", quote=False)

    elif len(msg) != 0:
        setting = getprivatenotes(chat_id)
        if setting == True:
            bot.send_message(user.id, msg_pm, parse_mode=ParseMode.MARKDOWN)
        else:
            delmsg = update.effective_message.reply_text(msg, parse_mode=ParseMode.MARKDOWN)

            cleartime = get_clearcmd(chat_id, "notes")

            if cleartime:
                context.dispatcher.run_async(delete, delmsg, cleartime.time)


def __import_data__(chat_id, data):
    failures = []
    for notename, notedata in data.get("extra", {}).items():
        match = FILE_MATCHER.match(notedata)
        matchsticker = STICKER_MATCHER.match(notedata)
        matchbtn = BUTTON_MATCHER.match(notedata)
        matchfile = MYFILE_MATCHER.match(notedata)
        matchphoto = MYPHOTO_MATCHER.match(notedata)
        matchaudio = MYAUDIO_MATCHER.match(notedata)
        matchvoice = MYVOICE_MATCHER.match(notedata)
        matchvideo = MYVIDEO_MATCHER.match(notedata)
        matchvn = MYVIDEONOTE_MATCHER.match(notedata)

        if match:
            failures.append(notename)
            notedata = notedata[match.end() :].strip()
            if notedata:
                sql.add_note_to_db(chat_id, notename[1:], notedata, sql.Types.TEXT)
        elif matchsticker:
            content = notedata[matchsticker.end() :].strip()
            if content:
                sql.add_note_to_db(
                    chat_id, notename[1:], notedata, sql.Types.STICKER, file=content
                )
        elif matchbtn:
            parse = notedata[matchbtn.end() :].strip()
            notedata = parse.split("<###button###>")[0]
            buttons = parse.split("<###button###>")[1]
            buttons = ast.literal_eval(buttons)
            if buttons:
                sql.add_note_to_db(
                    chat_id,
                    notename[1:],
                    notedata,
                    sql.Types.BUTTON_TEXT,
                    buttons=buttons,
                )
        elif matchfile:
            file = notedata[matchfile.end() :].strip()
            file = file.split("<###TYPESPLIT###>")
            notedata = file[1]
            content = file[0]
            if content:
                sql.add_note_to_db(
                    chat_id, notename[1:], notedata, sql.Types.DOCUMENT, file=content
                )
        elif matchphoto:
            photo = notedata[matchphoto.end() :].strip()
            photo = photo.split("<###TYPESPLIT###>")
            notedata = photo[1]
            content = photo[0]
            if content:
                sql.add_note_to_db(
                    chat_id, notename[1:], notedata, sql.Types.PHOTO, file=content
                )
        elif matchaudio:
            audio = notedata[matchaudio.end() :].strip()
            audio = audio.split("<###TYPESPLIT###>")
            notedata = audio[1]
            content = audio[0]
            if content:
                sql.add_note_to_db(
                    chat_id, notename[1:], notedata, sql.Types.AUDIO, file=content
                )
        elif matchvoice:
            voice = notedata[matchvoice.end() :].strip()
            voice = voice.split("<###TYPESPLIT###>")
            notedata = voice[1]
            content = voice[0]
            if content:
                sql.add_note_to_db(
                    chat_id, notename[1:], notedata, sql.Types.VOICE, file=content
                )
        elif matchvideo:
            video = notedata[matchvideo.end() :].strip()
            video = video.split("<###TYPESPLIT###>")
            notedata = video[1]
            content = video[0]
            if content:
                sql.add_note_to_db(
                    chat_id, notename[1:], notedata, sql.Types.VIDEO, file=content
                )
        elif matchvn:
            video_note = notedata[matchvn.end() :].strip()
            video_note = video_note.split("<###TYPESPLIT###>")
            notedata = video_note[1]
            content = video_note[0]
            if content:
                sql.add_note_to_db(
                    chat_id, notename[1:], notedata, sql.Types.VIDEO_NOTE, file=content
                )
        else:
            sql.add_note_to_db(chat_id, notename[1:], notedata, sql.Types.TEXT)

    if failures:
        with BytesIO(str.encode("\n".join(failures))) as output:
            output.name = "failed_imports.txt"
            dispatcher.bot.send_document(
                chat_id,
                document=output,
                filename="failed_imports.txt",
                caption="These files/photos failed to import due to originating "
                "from another bot. This is a telegram API restriction, and can't "
                "be avoided. Sorry for the inconvenience!",
            )


def __stats__():
    return f"{ALKL}• {sql.num_notes()} notes, across {sql.num_chats()} chats."


def __migrate__(old_chat_id, new_chat_id):
    sql.migrate_chat(old_chat_id, new_chat_id)


def __chat_settings__(chat_id, user_id):
    notes = sql.get_all_chat_notes(chat_id)
    return f"{ALKL}There are `{len(notes)}` notes in this chat."


__help__ = f"""{ALKL}
⚔️ •/get <notename>-\n get the note with this notename
⚔️ •#<notename>-\n same as /get
⚔️ •/notes or /saved-\n list all saved notes in this chat
⚔️ •/number*-\n Will pull the note of that number in the list
If you would like to retrieve the contents of a note without any formatting, use `/get <notename> noformat`. This can \
be useful when updating a current note

*Admins only*-\n
⚔️ •/save <notename> <notedata>-\n saves notedata as a note with name notename
A button can be added to a note by using standard markdown link syntax - the link should just be prepended with a \
`buttonurl:` section, as such: `[somelink](buttonurl:example.com)`. Check `/markdownhelp` for more info
⚔️ •/save <notename>-\n save the replied message as a note with name notename
 Separate diff replies by `%%%` to get random notes
 *Example*-\n 
 `/save notename
 Reply 1
 %%%
 Reply 2
 %%%
 Reply 3
⚔️ •/clear <notename>-\n clear note with this name
⚔️ •/removeallnotes-\n removes all notes from the group
 *Note*-\n Note names are case-insensitive, and they are automatically converted to lowercase before getting saved.
⚔️ •/privatenotes <on/yes/1/off/no/0>: enable or disable private notes in chat
"""



GET_WORK = CommandHandler("get", cmd_get, run_async=True)
HASH_GET_WORK = MessageHandler(Filters.regex(r"^#[^\s]+"), hash_get, run_async=True)
SLASH_GET_WORK = MessageHandler(Filters.regex(r"^/\d+$"), slash_get, run_async=True)
SAVE_WORK = CommandHandler("save", save, run_async=True)
DELETE_WORK = CommandHandler("clear", clear, run_async=True)

LIST_WORK = DisableAbleCommandHandler(["notes", "saved"], list_notes, admin_ok=True, run_async=True)

CLEARALL = DisableAbleCommandHandler("removeallnotes", clearall, run_async=True)
CLEARALL_BTN = CallbackQueryHandler(clearall_btn, pattern=r"notes_.*", run_async=True)

dispatcher.add_handler(GET_WORK)
dispatcher.add_handler(SAVE_WORK)
dispatcher.add_handler(LIST_WORK)
dispatcher.add_handler(DELETE_WORK)
dispatcher.add_handler(HASH_GET_WORK)
dispatcher.add_handler(SLASH_GET_WORK)
dispatcher.add_handler(CLEARALL)
dispatcher.add_handler(CLEARALL_BTN)
