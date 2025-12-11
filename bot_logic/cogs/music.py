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
        self.queue = []

    def _makelink(self, query):
        return
    
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
            info = info['entries'][0] # Handles playlists
        
        return info



class MusicCommands(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.playerdict = {} # { guild_id : Player object }

    def get_player(self, guild_id):
        if guild_id not in self.playerdict:
            self.playerdict[guild_id] = Player(guild_id)
        return self.playerdict[guild_id]
    
    async def queue(self,ctx,info):
        '''
        Adds an info dictionary to the queue. Must inherit ctx from a command
        '''
    
    async def playnext(self,ctx,guild_id):
        '''
        Plays whatever is next in the queue. Must inherit ctx from a command
        '''
    
    async def resume(self,ctx):
        '''
        Resumes music. Must inherit ctx from a command
        '''

    
    @commands.command(name='skip')
    async def skip(self,ctx):
        '''
        Mainly handles playnext
        '''

    @commands.command(name='play')
    async def play(self,ctx,*,query:str):
        '''
        Resumes paused music, queues if done with query
        If queue is empty, calls queue and playnext
        If queue is not empty, calls queue
        '''
        player = self.get_player(ctx.guild.id) # get the player object for the server

    @commands.command(name='pause')
    async def pause(self,ctx):
        '''
        Pauses music
        '''

    @commands.command(name='resume')
    async def resume_command(self,ctx):
        '''
        Calls resume
        '''
    
    @commands.command(name='queue')
    async def showqueue(self,ctx,*,query:str):
        '''
        Show the queue.
        '''


    


# Setup function required to load cog
async def setup(bot):
    await bot.add_cog(MusicCommands(bot))