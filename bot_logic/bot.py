# Imports

import discord
from discord.ext import commands
import os
import sys
from dotenv import load_dotenv

# Functions

def get_token():
    '''
    Retrieves the bot token from a secure location
    '''
    load_dotenv()
    TOKEN = os.getenv('DISCORD_BOT_TOKEN')

    assert TOKEN, 'Token not found in .env'
    assert TOKEN!='your_discord_bot_token_here', 'Token not found in .env'

    return TOKEN

def run_bot(cogs_dir):
    '''
    Runs the bot
    '''
    TOKEN = get_token()
    
    intents = discord.Intents.default()
    intents.message_content = True
    intents.members = True

    bot = commands.Bot(command_prefix=';;', intents=intents)

    async def load_cogs():
        """Loads all Python files (cogs) found in the 'cogs' directory."""
        for filename in os.listdir(cogs_dir):
            # Check if the file is a Python file and not a utility file
            if filename.endswith('.py') and not filename.startswith('__'):
                try:
                    # Load the cog, e.g., 'cogs.messaging'
                    await bot.load_extension('bot_logic.cogs.'+filename[:-3])
                    print(f"Loaded Cog: {filename[:-3]}")
                except Exception as e:
                    print(f"Failed to load cog {filename[:-3]}. Error: {e}")

    @bot.event
    async def on_ready():
        """Confirms the bot is online and loads cogs on startup."""
        print(f'Logged in as {bot.user} (ID: {bot.user.id})')
        await load_cogs()
        print('Bot is ready!')

    bot.run(TOKEN) 