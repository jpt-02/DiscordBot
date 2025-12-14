# delte this when packaging

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

link = 'https://www.youtube.com/shorts/nGNVMbKGyjc'


query = 'ytsearch:' +'black dog'

def _convert_time(seconds):
    '''
    Turns duration into mm:ss and returns it
    '''
    minutes = seconds // 60
    remainder_seconds = seconds % 60
    if remainder_seconds < 10:
        remainder_seconds = '0' + str(remainder_seconds)
    return '(' + str(minutes) + ':' + str(remainder_seconds) + ')'

def _makelink(query):
    if 'youtube.com' in query or 'youtu.be' in query:
        return query
    else:
        return 'ytsearch:'+query

def _download(query):
    link = _makelink(query)
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
    
    if 'url' not in info:
        info.update({'error':'Could not find streamable audio source.'})

    title = info['title'] if 'title' in info else ''
    duration = _convert_time(info['duration']) if 'duration' in info else ''

    info.update({'discord_repr':title +''+duration})
    return info


info = _download('anything')

print(type(info['duration']))
print(info['duration'])

#print('entries' in info)

# title, duration, url