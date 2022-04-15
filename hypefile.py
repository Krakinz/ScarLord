import sys
import os
import subprocess
from termcolor import *


try:
    HYPEVOID=input("Are you a HypeVoid Dev?\nPlease Type y/n: ").lower()
    if HYPEVOID == "y":
        os.system("python -m SƈαɾLσɾԃ")
    else:
        VOIDYN=input("Is This a test process or server mode?\nPlease Type T/S: ").lower()
        VOIDWL=input("Is This Linus System or Windows System?\nPlease Type L/W: ").lower()
        if VOIDYN == 't' and VOIDWL == 'w':
            subprocess.run(
"python -m SƈαɾLσɾԃ",
shell=True)
        elif VOIDYN == 't' and VOIDWL == 'l':
            subprocess.run(
"python3 -m SƈαɾLσɾԃ",
shell=True)    
        elif VOIDYN == 's' and VOIDWL == 'w':
            subprocess.run(
"python -m SƈαɾLσɾԃ",
shell=True) 
        elif VOIDYN == 's' and VOIDWL == 'l':
            subprocess.run(
"python3 -m SƈαɾLσɾԃ",
shell=True)
except Exception as e:
    cprint(e)
    sys.exit()