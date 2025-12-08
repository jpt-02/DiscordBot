from discord.ext import commands
import discord

class Messaging(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    # A simple command (user types: !hello)
    @commands.command(name='hello')
    async def hello_command(self, ctx):
        """Responds with a simple greeting."""
        await ctx.send(f'Hello there, {ctx.author.display_name}!')

    # A listener for specific messages (user types: 'ping' anywhere in a message)
    @commands.Cog.listener()
    async def on_message(self, message):
        # Prevent the bot from responding to its own messages
        if message.author == self.bot.user:
            return

        if 'ping' in message.content.lower():
            await message.channel.send('response')

# The setup function is REQUIRED to load the cog
async def setup(bot):
    await bot.add_cog(Messaging(bot))