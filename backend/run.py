import discord

def get_token():
    '''
    Retrieves the bot token from a secure location
    '''
    # In a real application, retrieve this from an environment variable or secure vault
    return 'your token here'

def run_bot():
    '''
    Runs the bot
    '''
    intents = discord.Intents.default()
    intents.message_content = True

    client = discord.Client(intents=intents)

    @client.event
    async def on_ready():
        print(f'We have logged in as {client.user}')

    @client.event
    async def on_message(message):
        if message.author == client.user:
            return

        if message.content.startswith('$hello'):
            await message.channel.send('Hello!')

    client.run('your token here')  