from discord.ext import commands
import discord
import yt_dlp
import asyncio

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
        self.isPaused = False
        self.current_track_repr = ''
        self.queuelist = []
        self.timer_running = False
        self.leaveflags = [False,False,False]

    def _convert_time(self,seconds):
        '''
        Turns duration into mm:ss and returns it
        '''
        minutes = seconds // 60
        remainder_seconds = seconds % 60
        if remainder_seconds < 10:
            remainder_seconds = '0' + str(remainder_seconds)
        return '(' + str(minutes) + ':' + str(remainder_seconds) + ')'
    
    def _makelink(self, query):
        if 'youtube.com' in query or 'youtu.be' in query:
            return query
        else:
            return 'ytsearch:'+query
    
    def _download(self, query):
        link = self._makelink(query)
        try:
            with yt_dlp.YoutubeDL(YDL_OPTIONS) as ydl:
                info = ydl.extract_info(link, download=False)
        except yt_dlp.utils.DownloadError as e:
            error_message = str(e)
            if 'Private video' in error_message or 'unavailable' in error_message:
                info = {'error':"Video is private or unavailable."}
            elif 'geographical region' in error_message:
                info = {'error':"Video is geographically restricted."}
            elif 'Age-restricted' in error_message:
                info = {'error':"Video is age-restricted and authentication failed."}
            else:
                info = {'error':"Unknown download/network error."}
        except Exception as e:
            info = {'error': f"An unexpected non-download error occurred: {e}"}

        if 'entries' in info:
            info = info['entries'][0] # Handles playlists and searches
        
        if 'url' not in info:
            info.update({'error':'Could not find streamable audio source.'})

        title = info['title'] if 'title' in info else ''
        duration = self._convert_time(info['duration']) if 'duration' in info else ''

        info.update({'discord_repr':title +' '+duration})
        return info
    
    def queue_add(self,query):
        info = self._download(query)
        if 'error' not in info:
            self.queuelist.append(info)
            return 'Queued ' + info['discord_repr']
        else:
            return 'Error: ' + info['error']
    
    def queue_pop(self):
        if len(self.queuelist) != 0:
            self.queuelist.pop(0)

    def repr_queue(self):
        if len(self.queuelist) == 0:
            return 'Queue is empty'
        else:
            returnstring = '**CURRENT QUEUE**'
            for i in range(len(self.queuelist)):
                returnstring = returnstring + '\n' + str(i+1) + '. ' + self.queuelist[i]['discord_repr']
            return returnstring

    


class MusicCommands(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.playerdict = {} # { guild_id : Player object }

    def get_player(self, ctx):
        '''
        Returns the player object associated with a server ID.
        '''
        guild_id = ctx.guild.id
        if guild_id not in self.playerdict:
            self.playerdict[guild_id] = Player(guild_id)
        return self.playerdict[guild_id]
    
    async def remove_player(self,ctx):
        '''
        removes the player object associated with a server ID
        '''
        guild_id = ctx.guild.id
        if guild_id in self.playerdict:
            del self.playerdict[guild_id]
            await ctx.voice_client.disconnect()

    def in_vc(self,ctx):
        '''
        Returns true if bot is in a VC in the server where a user is commanding it, else False
        '''
        if ctx.voice_client is not None:
            return True
        else:
            return False

    def get_queue(self,ctx):
        '''
        Returns the queue for a context dependent player. Queue is a list of info dicts
        '''
        player = self.get_player(ctx)
        queuelist = player.queuelist
        return queuelist
    
    def get_queue_repr(self,ctx):
        '''
        Returns the text list of the queue items for a context dependent player
        '''
        player = self.get_player(ctx)
        reprstring = player.repr_queue()
        return reprstring

    def queue_add(self,ctx,query):
        '''
        Adds an info dictionary to the queue for a context dependent player
        '''
        player = self.get_player(ctx)
        return player.queue_add(query)
    
    def clear(self,ctx):
        '''
        Clears the queue
        '''
        player = self.get_player(ctx)
        player.queuelist = []

    async def join(self,ctx):
        '''
        Joins a VC based on context dependence
        '''
        player = self.get_player(ctx)

        if ctx.author.voice is not None:
            target_vc = ctx.author.voice.channel
            if not self.in_vc(ctx):
                await target_vc.connect()
            else:
                await ctx.voice_client.move_to(target_vc)

            if not player.timer_running:
                self.start_timer(ctx)

    def start_timer(self,ctx):
        '''
        Called only after the player is initialzed or the last timer ends
        '''
        player = self.get_player(ctx)
        self.bot.loop.create_task(self.run_timer(ctx))
        player.timer_running = True
    
    async def run_timer(self,ctx):
        '''
        Manages timer for bot to auto leave if not in use
        '''
        player = self.get_player(ctx)
        await asyncio.sleep(100)
        player.leaveflags[0] = True if player.isPlaying == False else False
        print(f'Flag#1: {player.leaveflags[0]}')
        await asyncio.sleep(100)
        player.leaveflags[1] = True if player.isPlaying == False else False
        print(f'Flag#2: {player.leaveflags[0]}')
        await asyncio.sleep(100)
        player.leaveflags[2] = True if player.isPlaying == False else False
        print(f'Flag#3: {player.leaveflags[0]}')

        if False not in player.leaveflags:
            await self.remove_player(ctx)
        else:
            self.start_timer(ctx)


    
    def resume(self,ctx):
        '''
        Resumes music for a context dependent player
        '''
        player = self.get_player(ctx)
        voice_client = ctx.voice_client
        
        if voice_client is not None and voice_client.is_paused():
            voice_client.resume()
            player.isPlaying = True
            player.isPaused = False

    def pause(self,ctx):
        '''
        Pauses music for a context dependent player
        '''
        player = self.get_player(ctx)
        voice_client = ctx.voice_client
        
        if voice_client is not None and voice_client.is_playing():
            voice_client.pause()
            player.isPlaying = False
            player.isPaused = True

    async def skip(self,ctx):
        '''
        Stops context dependent voice client, which calls after_play
        '''
        if ctx.voice_client:
            ctx.voice_client.stop()

    def after_play(self,ctx):
        player = self.get_player(ctx)
        player.isPlaying=False
        self.bot.loop.create_task(self.playnext(ctx))

    async def playnext(self,ctx):
        '''
        Plays whatever is next in the queue for a context dependent player.
        Automatically play the next in queue when done
        Only non-command that is allowed to speak because it runs automatically
        '''
        player = self.get_player(ctx)
        
        queue = self.get_queue(ctx)
        if len(queue) == 0:
            return
        
        target_info = queue[0]
        player.current_track_repr = target_info['discord_repr']
        target_url = target_info['url']

        try:
            voice_client = ctx.voice_client
            # code for making voice client play audio
            source = await discord.FFmpegOpusAudio.from_probe(
                target_url, 
                # FFmpeg options for streaming stability (same as those passed to yt-dlp)
                before_options='-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5',
                executable='ffmpeg' # Ensure FFmpeg is accessible in your environment PATH
            )

            voice_client.play(source, after=lambda error: self.after_play(ctx)) # lambda - this may not be correct syntax
            await ctx.send('Now playing ' + player.current_track_repr)
            player.isPlaying = True
            player.queue_pop()


        except Exception as e:
            await ctx.send(f'Error playing {player.current_track_repr}: {e}')
            player.queue_pop()
            #await self.playnext(ctx)
            self.after_play(ctx)


    
    @commands.command(name='skip')
    async def skip_command(self,ctx):
        '''
        Skips the currently playing song.
        '''
        if self.in_vc(ctx) and ctx.voice_client.is_playing():
            await self.skip(ctx)
            player = self.get_player(ctx)
            await ctx.send('Skipped ' + player.current_track_repr)
        else:
            return

    @commands.command(name='play')
    async def play_command(self,ctx,*,query=None):
        '''
        Resumes paused music, queues if called with query
        Calls queue_add, which handles whether it is empty or not
        '''
        player = self.get_player(ctx)
    
        if (ctx.author.voice is None) and (not self.in_vc(ctx)): #if author is not in VC and neither is bot
            await ctx.send("Join a VC first")
            return
        await self.join(ctx) # Joins a VC
        
        if query is None:
            if player.isPaused:
                self.resume(ctx)
            if not player.isPlaying:
                await self.playnext(ctx)
        
        else:
            message = self.queue_add(ctx,query)
            await ctx.send(message) # Gives message that queue has been updated

            if player.isPaused:
                self.resume(ctx) # Always resume if play is called, even with query
                return

            if not player.isPlaying:
                await self.playnext(ctx) #Calls playnext to initialize loop

    @commands.command(name='pause')
    async def pause_command(self,ctx):
        '''
        calls pause
        '''
        self.pause(ctx)

    @commands.command(name='resume')
    async def resume_command(self,ctx):
        '''
        Calls resume
        '''
        self.resume(ctx)
    
    @commands.command(name='queue')
    async def queue_command(self,ctx,*,query=None):
        '''
        Show the queue or add a query to the queue
        '''
        if query is None:
            await ctx.send(self.get_queue_repr(ctx))
            return
        else:
            message = self.queue_add(ctx,query)
            await ctx.send(message)

    @commands.command(name='join')
    async def join_command(self,ctx):
        '''
        Calls join
        '''
        if ctx.author.voice is None:
            await ctx.send("Join a VC first")
            return
        await self.join(ctx)

    @commands.command(name='clear')
    async def clear_command(self,ctx):
        '''
        Calls clear
        '''
        self.clear(ctx)
        await ctx.send('Queue Cleared')

    @commands.command(name='killplayer')
    async def killplayer_command(self,ctx):
        '''
        kills the player object so that a new one can be created
        '''
        await self.remove_player(ctx)


    #leave command
    #figure out what happens when bot is disconnected, maybe have a listener clear the queue idk
    #when bot is disconnected set is_playing to false, clear the queue


# Setup function required to load cog
async def setup(bot):
    await bot.add_cog(MusicCommands(bot))