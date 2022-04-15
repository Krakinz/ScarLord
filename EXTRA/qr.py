DESC = """\n
| =================     🚀🔥 ΉYPΣ VӨID LΛB 🔥🚀     =================| 

『  ∆   ʜᴜʙ ᴏꜰ ʙᴏᴛꜱ ᴡɪᴛʜ ᴇᴍᴏᴛɪᴏɴ  ∆ 』

The hub of awsome Telegram Bots.
Keep eye on us to get to use new and interesting bots.

🎶 𝙵𝚛𝚒𝚎𝚗𝚍𝚕𝚢 𝙶𝚛𝚘𝚞𝚙 • @hypevoids  💬
🍻 𝙶𝚒𝚝𝚑𝚞𝚋 • @HYPEVOIDBOT 🤖 or https://github.com/HypeVoidSoul

👑 𝙳𝚛𝚎𝚊𝚖𝚝 𝙱𝚢 • @HypeVoidSoul 
"""
print(DESC)

print('Initializing qr code generator')
import os
import time
import random
import platform
from os import name

p = '|--------------------' + platform.system() + '--------------------|\n'
pt = print(p.upper())
def _auto_purge_():
    if name == 'nt':
        os.system('cls')
    else:
        os.system('clear')

f = open('whatthefuckisthisdamn.txt','w+')
f.write('pyqrcode\ntermcolor\npypng')
f.close() 
os.system('pip install -U -r whatthefuckisthisdamn.txt')
os.remove('whatthefuckisthisdamn.txt')
_auto_purge_()
p = '|--------------------' + platform.system() + '--------------------|\n'
pt = print(p.upper())

import sys
import qrcode
import pyqrcode
from termcolor import * 

cprint(DESC, "yellow")
print('|-------------------------------------------------------------------|\n')

KB = input(cprint('Please put the information you want inside the QRCODE :', 'yellow'))   
KUSTM_BANK = ['red','green','yellow','blue','magenta','cyan','Brown',
'white','Azure','Ivory','Teal', 'Silver','Purple','Navy blue','Gray', 
'Orange','Maroon', 'Aquamarine','Coral', 'Fuchsia','Wheat',
'Lime', 'Crimson','pink', 'Golden', 'Plum','Olive']

KOL = cprint('Please choose the color of the background of your QRCODE', 'green')
KOL_1 = '1 - red'
cprint(KOL_1, 'red')
KOL_2 = '2 - green'
cprint(KOL_2, 'green')
KOL_3 = '3 - yellow'
cprint(KOL_3, 'yellow')
KOL_4 = '4 - blue'
cprint(KOL_4, 'blue')
KOL_5 = '5 - magenta'
cprint(KOL_5, 'magenta')
KOL_6 = '6 - cyan'
cprint(KOL_6, 'cyan')
KOL_7 = '7 - default white'
cprint(KOL_7)
cprint('8 - for a different color - {BETA}', 'white')
cprint('9 - for a random color - {BETA}', 'white')
time.sleep(1)
KOL_FINALLY = input(cprint('\nPlease Enter a valid Number from 1-9:   ', 'magenta')) #Humans will try anything but not what asked so not using integers

if KOL_FINALLY   == '1':
        BACKKOL = 'red'
elif KOL_FINALLY == '2':
        BACKKOL = 'green'
elif KOL_FINALLY == '3':
        BACKKOL = 'yellow'
elif KOL_FINALLY == '4':
        BACKKOL = 'blue'
elif KOL_FINALLY == '5':
        BACKKOL = 'magenta'
elif KOL_FINALLY == '6':
        BACKKOL = 'cyan'
elif KOL_FINALLY == '7':
        BACKKOL = 'white'
elif KOL_FINALLY == '8':
        OTHERKUSTOM  = '''
Brown          Azure           Ivory
Teal           Silver          Purple
Navy blue      Gray            Orange
Maroon         Charcoal        Aquamarine
Coral          Fuchsia         Wheat
Lime           Crimson         pink           
Olden          Plum            Olive'''
        cprint('Choose from these:\n', 'green')
        KUSTM = input(cprint(OTHERKUSTOM)).lower()
        BACKKOL = KUSTM
elif KOL_FINALLY == '9':
        BACKKOL =random.choice(KUSTM_BANK)
        print(BACKKOL)
else:
        print((colored("Given Wrong input so taking default choice", "red", "on_white", attrs=["bold"])))
        pass

url = pyqrcode.create(KB)   
input_data= input(cprint('Please type 1 for PNG\nPlease type 2 for SVG\nPlease type 3 for JPG\n\nPlease Type 4 to quit!', 'yellow'))


if input_data     ==    '1':
        qr = qrcode.QRCode(
                version=1,
                box_size=10,
                border=5)
        qr.add_data(input_data)
        qr.make(fit=True)
        img = qr.make_image(fill='black', back_color=BACKKOL)
        img.save('qrcode_png.png')
        "Get Desired output as a .png file"
        cprint(DESC, "yellow")
        
elif input_data   ==    '2':
        qr = qrcode.QRCode(
                version=1,
                box_size=10,
                border=5)
        qr.add_data(input_data)
        qr.make(fit=True)
        img = qr.make_image(fill='black', back_color=BACKKOL)
        img.save('qrcode_svg.svg')
        "Get Desired output as a .svg file"
        cprint(DESC, "yellow")
        
elif input_data   ==    '3':
        qr = qrcode.QRCode(
                version=1,
                box_size=10,
                border=5)
        qr.add_data(input_data)
        qr.make(fit=True)
        img = qr.make_image(fill='black', back_color=BACKKOL)
        img.save('qrcode_jpg.jpg')
        "Get Desired output as a .jpg file"
        cprint(DESC, "yellow")
        
elif input_data   ==    '4':
        sys.exit()
        
else:
        cprint('Too bad my coder knew that humans will try anything but 1 or 2', 'cyan')
        cprint('ReTry Lol!', 'red')
        cprint(DESC, "yellow")
        sys.exit()