# utils/colors.py
RED = "\033[91m"
GREEN = "\033[92m"
YELLOW = "\033[93m"
BLUE = "\033[94m"
RESET = "\033[0m"

def paint(text, color):
    return f"{color}{text}{RESET}"