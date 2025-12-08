# Imports

import discord
import os
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

def run_bot():
    '''
    Runs the bot
    '''
    TOKEN = get_token()

    intents = discord.Intents.default()
    intents.message_content = True

    client = discord.Client(intents=intents)

    @client.event
    async def on_ready():
        print(f'Successfully logged in as {client.user}')

    @client.event
    async def on_message(message):
        if message.author == client.user:
            return

        if message.content.startswith('$hello'):
            await message.channel.send('Hello!')

    client.run(TOKEN) 


# Main Execution
if __name__ == '__main__':
    run_bot()