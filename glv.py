from colorama import Fore, Back, Style
import os

# colorama.init(autoreset=True)  # Optional for automatic reset

def set_color(color, style=None):
    """Prints text in the specified color and style."""
    print(getattr(Fore, color), end="")
    if style:
        print(getattr(Style, style), end="")

def reset():
    """Resets text color and style to defaults."""
    print(Style.RESET_ALL, end="")

def print_colored(text, color, style=None):
    """Prints text in the specified color and style, resetting afterward."""
    set_color(color, style)
    print(text)
    reset()

def dprint(text):
    """Prints debug text in yellow."""
    print_colored(text, "YELLOW")

def errprint(text):
    """Prints error text in red."""
    print_colored(text, "RED")

def setDebug():
    """Sets the text color to yellow (for debugging)."""
    set_color("YELLOW")

def setSuccess():
    """Sets the text color to green (for success messages)."""
    set_color("GREEN")

vout = True
SUDO_KEY = 'd26g5bnklkwsh4'
OUT_DIRECTORY = str(os.getcwd()).replace('\\', '/')
