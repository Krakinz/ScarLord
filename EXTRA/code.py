DESC = """\n
| =================     🚀🔥 ΉYPΣ VӨID LΛB 🔥🚀     =================| 

『  ∆   ʜᴜʙ ᴏꜰ ʙᴏᴛꜱ ᴡɪᴛʜ ᴇᴍᴏᴛɪᴏɴ  ∆ 』

The hub of awsome Telegram Bots.
Keep eye on us to get to use new and interesting bots.

🎶 𝙵𝚛𝚒𝚎𝚗𝚍𝚕𝚢 𝙶𝚛𝚘𝚞𝚙 • @hypevoids  💬
🍻 𝙶𝚒𝚝𝚑𝚞𝚋 • @HYPEVOIDBOT 🤖 or https://github.com/Krakinz

👑 𝙳𝚛𝚎𝚊𝚖𝚝 𝙱𝚢 • @HypeVoidSoul 
"""

print("\n\n\n✨----------------------------------------------------------------✨")
YORN = input("Hey Boi do you want to manually install modules needed for this code or do you want to let this python code handle itself?\n📟  Y or N:  \n\n\n").upper()
import sys
import os
import asyncio
import shutil
import time
from time import sleep
from os import system, name
from time import sleep
import platform
p = "|--------------------" + platform.system() + "--------------------|\n"
pt = print(p.upper())
def _auto_purge_():
    if name == 'nt':
        os.system('cls')
    else:
        os.system('clear')
import platform
p = "|--------------------" + platform.system() + "--------------------|\n"
pt = print(p.upper())
try:    
    if YORN == "Y" or "YES":
        f = open("whatthefuckisthisdamn.txt","w+")
        f.write("termcolor\nplaysound\ngtts\ngoto-statement")
        f.close() 
        os.system("pip install -U -r whatthefuckisthisdamn.txt")
        os.remove("whatthefuckisthisdamn.txt")
        _auto_purge_()
        from termcolor import colored, cprint
        from gtts import gTTS as Hyperg
        from playsound import  playsound
        T1 = colored("\n\n✨----------------------------------------------------------------✨\n", "magenta", attrs=['blink','bold'])
        cprint("I am a Google Test To Speech simple test bot.", "yellow")
        cprint("I was coded by @HypeVoidSoul {find all my codes in github or in telegram @HypeVoidLab}\nto test gTTS and create a QR code for the output. The QR part is not yet ready but you can try the Text To Speech.", "yellow")
        T1 = colored("\n✨----------------------------------------------------------------✨", "magenta", attrs=['blink','bold'])
        while True:
            T1 = colored("\n\n✨----------------------------------------------------------------✨", "magenta", attrs=['blink','bold'])
            print(T1)
            start = SPEECH_ = input(cprint("Type The Text you want to get as a speech\n  🎤:", "green"))
            language='en'
            myobj=Hyperg(text=SPEECH_,lang=language,slow=True)
            myobj.save("SPEECH.mp3")
            time.sleep(1)
            T1 = colored("\n\n✨----------------------------------------------------------------✨", "magenta", attrs=['blink','bold'])
            print(T1)
            LISTEN = input(cprint("Do you want to hear the audio?\n📟  Y or N:  ", "yellow"))
            HOWMANYTIMES__ = int(input(cprint("How many times should i play {should be less then 50}?\n📟:  ", "cyan")))
            # if LISTEN == "Y" or "YES":
            #     playsound("SPEECH.mp3")
            # else:
            cprint("Terminated code!", "cyan")
            #sys.exit()
            count = 0
            while count < HOWMANYTIMES__ and not count == 50:
                print('The count is:', count+1)
                playsound("SPEECH.mp3")            
                count = count + 1
            cprint("Good bye!", "magenta")
            cprint(DESC, "cyan")
            T1 = colored("\n\n✨----------------------------------------------------------------✨", "magenta", attrs=['blink','bold'])
            print(T1)
            DEL = input(cprint("Do you want to keep the audio or delete it?\n📟  Y or N:  ", "yellow")).upper()
            if DEL == "Y" or "YES":
                cprint("Terminated AutoClean codec!", "cyan")
                sys.exit()
            else:
                os.remove("SPEECH.mp3")
                sys.exit()
    elif YORN == "N" or "NO":
        from termcolor import colored, cprint
        GET_ = cprint("So You wanna do it yourself.\nFollow these then:\n", "yellow")
        time.sleep(1)
        GET__ = cprint("    Open 'whatthefuckisthisdamn.txt' file", "blue")
        time.sleep(1)
        GET___ = cprint("       Open terminal and type this:\n pip install -U -r whatthefuckisthisdamn.txt", "green")
        time.sleep(1)
    else:
        from termcolor import colored, cprint
        cprint("You are really trying to test this.", "red")
        time.sleep(1)
        cprint("\nGoodbye", "yellow")
        cprint(DESC, "cyan")
        time.sleep(1)
        import platform
        p = "|--------------------" + platform.system() + "--------------------|\n"
        pt = print(p.upper())
        sys.exit()
except Exception as shit:
    from termcolor import colored, cprint
    cprint(shit, "red")