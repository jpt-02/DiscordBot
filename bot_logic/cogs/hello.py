from discord.ext import commands
import discord

class Messaging(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name='hello')
    async def hello_command(self, ctx):
        await ctx.send(f'Hello there, {ctx.author.display_name}!')

    @commands.Cog.listener()
    async def on_message(self, message):
        if message.author == self.bot.user:
            return

        if 'ping' in message.content.lower():
            await message.channel.send('response')

    @commands.command(name='push')
    async def push_to_db(self, ctx):
        guild = ctx.guild
        guild_name = guild.name
        guild_id = guild.id

        #code to test databse here
        await ctx.send('Pushing ' + str(guild_id) + " to database")
        


# Setup function required to load cog
async def setup(bot):
    await bot.add_cog(Messaging(bot))