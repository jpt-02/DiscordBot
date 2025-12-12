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

try:
    with yt_dlp.YoutubeDL(YDL_OPTIONS) as ydl:
        info = ydl.extract_info(link, download=False)
except yt_dlp.utils.DownloadError as e:
    error_message = str(e)
    if 'Private video' in error_message or 'unavailable' in error_message:
        info = {'error',"Handling Error: Video is private or unavailable."}
    elif 'geographical region' in error_message:
        info = {'error',"Handling Error: Video is geographically restricted."}
    elif 'Age-restricted' in error_message:
        info = {'error',"Handling Error: Video is age-restricted and authentication failed."}
    else:
        info = {'error',"Handling Error: Unknown download/network error."}
except Exception as e:
    info = {'error', f"An unexpected non-download error occurred: {e}"}




if info is not None:
    for key in info:
        print(key)

print(info['title'])

#print('entries' in info)

# title, duration, url