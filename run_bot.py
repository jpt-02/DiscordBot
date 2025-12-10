from bot_logic import bot
import os
import sys

def get_base_dir():
    # Check if the app is frozen (compiled by PyInstaller)
    if getattr(sys, 'frozen', False):
    # If compiled, the base path is the executable path
        base_path = sys._MEIPASS
    else:
    # If running normally, the base path is the script's directory
        base_path = os.path.dirname(os.path.abspath(__file__))
    return base_path

def get_cogs_dir():
    base_path = get_base_dir()
    # Define the path to the cogs folder using the determined base_path
    bot_dir = os.path.join(base_path, 'bot_logic')
    cogs_dir = os.path.join(bot_dir, 'cogs')
    print(cogs_dir)
    return cogs_dir

bot.run_bot(get_cogs_dir())