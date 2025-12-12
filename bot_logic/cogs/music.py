from discord.ext import commands
import yt_dlp

YDL_OPTIONS = {
    'skip_download': True,
    'noplaylist': True,
    'no_warnings': True,
    'quiet': True,
    'format': 'bestaudio/best',
    
    'external_downloader_args': {
        'ffmpeg_i': [
            # Standard args for streaming via FFmpeg
            '-reconnect', '1', 
            '-reconnect_streamed', '1', 
            '-reconnect_delay_max', '5'
        ]
    }
}

class Player():
    def __init__(self, serverID):
        self.serverID = serverID
        self.isPlaying = False
        self.queuelist = []

    def _makelink(self, query):
        if 'youtube.com' in query or 'youtu.be' in query:
            return query
        else:
            return 'ytsearch:'+query
    
    def download(self, query):
        link = self._makelink(query)
        try:
            with yt_dlp.YoutubeDL(YDL_OPTIONS) as ydl:
                info = ydl.extract_info(link, download=False)
        except yt_dlp.utils.DownloadError as e:
            error_message = str(e)
            if 'Private video' in error_message or 'unavailable' in error_message:
                info = {'error',"Video is private or unavailable."}
            elif 'geographical region' in error_message:
                info = {'error',"Video is geographically restricted."}
            elif 'Age-restricted' in error_message:
                info = {'error',"Video is age-restricted and authentication failed."}
            else:
                info = {'error',"Unknown download/network error."}
        except Exception as e:
            info = {'error', f"An unexpected non-download error occurred: {e}"}

        if 'entries' in info:
            info = info['entries'][0] # Handles playlists and searches
        
        return info



class MusicCommands(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.playerdict = {} # { guild_id : Player object }

    def convert_time(seconds):
        '''
        Turns duration into mm:ss and returns it
        '''
        minutes = seconds // 60
        remainder_seconds = seconds % 60
        if remainder_seconds < 10:
            remainder_seconds = '0' + str(remainder_seconds)
        return str(minutes) + ':' + str(remainder_seconds)

    def get_player(self, ctx):
        '''
        Returns the player object associated with a server ID.
        '''
        guild_id = ctx.guild.id
        if guild_id not in self.playerdict:
            self.playerdict[guild_id] = Player(guild_id)
        return self.playerdict[guild_id]
    
    def in_vc(self,ctx):
        '''
        Returns true if bot is in a VC in the server where a user is commanding it, else False
        '''
        if ctx.voice_client is not None:
            return True
        else:
            return False

    async def join(self,ctx,target_vc):
        '''
        Joins a VC.
        '''
        if not self.in_vc(ctx):
            await target_vc.connect()
        else:
            await ctx.voice_client.move_to(target_vc)

    
    async def queue_show(self,ctx):
        '''
        Displays the queue in chat. If queue is empty, says so.
        '''
        player = self.get_player(ctx)

    async def queue_add(self,ctx,info):
        '''
        Adds an info dictionary to the queue.
        '''
        player = self.get_player(ctx)
    
    async def playnext(self,ctx,guild_id):
        '''
        Plays whatever is next in the queue.
        '''
        player = self.get_player(ctx)
    
    async def resume(self,ctx):
        '''
        Resumes music.
        '''
        player = self.get_player(ctx)

    async def pause(self,ctx):
        '''
        Pauses music.
        '''
        player = self.get_player(ctx)

    
    @commands.command(name='skip')
    async def skip_command(self,ctx):
        '''
        Mainly handles playnext
        '''

    @commands.command(name='play')
    async def play_command(self,ctx,*,query:str):
        '''
        Resumes paused music, queues if done with query
        If queue is empty, calls queue and playnext
        If queue is not empty, calls queue
        '''

    @commands.command(name='pause')
    async def pause_command(self,ctx):
        '''
        calls pause
        '''
        await self.pause(ctx)

    @commands.command(name='resume')
    async def resume_command(self,ctx):
        '''
        Calls resume
        '''
    
    @commands.command(name='queue')
    async def showqueue_command(self,ctx,*,query:str):
        '''
        Show the queue or add a query to the queue
        '''

    @commands.command(name='join')
    async def join_command(self,ctx):
        '''
        Calls join
        '''
        if ctx.author.voice is None:
            await ctx.send("Join a VC first")
            return
        target_vc = ctx.author.voice.channel
        await self.join(ctx,target_vc)


# Setup function required to load cog
async def setup(bot):
    await bot.add_cog(MusicCommands(bot))