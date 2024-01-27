from colorama import *
import os
#colorama.init(autoreset=True)

def dprint(text):
    debug_text = f"{Fore.YELLOW}{text}{Style.RESET_ALL}"
    print(debug_text)


def errprint(text):
    err_text = f"{Fore.RED}{text}{Style.RESET_ALL}"
    print(err_text)


def setDebug():
    print(f'{Fore.YELLOW}',end="")

def setSuccess():
    print(f'{Fore.GREEN}',end="")

def reset():
    print(f'{Style.RESET_ALL}',end="")
    
vout = True
SUDO_KEY = 'd26g5bnklkwsh4'
OUT_DIRECTORY = str(os.getcwd()).replace('\\','/')