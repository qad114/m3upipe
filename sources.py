import json
import requests
from flask import redirect
from youtube_dl import YoutubeDL, cache
from youtube_dl.utils import DownloadError

CACHE_FILENAME = 'cache.json'

def src_filmon(url):
    api_base_url = "http://www.filmon.com/api-v2/channel/"
    channel_id = url.split('/')[-1]
    res = requests.get(api_base_url + channel_id)
    if res.status_code != 200:
        raise Exception("Channel not found or API not working!")
    j = json.loads(res.text)
    streams = j['data']['streams']
    
    url = None
    for stream in streams:
        if stream['quality'] == 'high':
            url = stream['url']
    if url == None: url = streams[0]['url']

    base_url = url.split('?')[0].replace('playlist.m3u8', '')
    m3u = requests.get(url).text
    for token in m3u.split():
        if '.ts' in token:
            m3u = m3u.replace(token, base_url + token)

    return m3u

def src_ustvgo(url):
    def get_channel_id(url):
        page = requests.get(url)
        id = page.text.split('/clappr.php?stream=')[1].split('\'')[0]
        return id

    # Attempt to get channel ID from cache, otherwise fetch it and write it to cache
    cache_modified = False
    try:
        with open(CACHE_FILENAME, 'r') as f:
            j = json.load(f)
            if 'ustvgo' in j:
                if url in j['ustvgo']:
                    channel_id = j['ustvgo'][url]
                else:
                    channel_id = get_channel_id(url)
                    j['ustvgo'][url] = channel_id
                    cache_modified = True
            else:
                channel_id = get_channel_id(url)
                j['ustvgo'] = {}
                j['ustvgo'][url] = channel_id
                cache_modified = True

    except FileNotFoundError:
        channel_id = get_channel_id(url)
        j = {}
        j['ustvgo'] = {}
        j['ustvgo'][url] = channel_id
        cache_modified = True

    if cache_modified:
        with open(CACHE_FILENAME, 'w') as f:
            json.dump(j, f)

    response = requests.post('https://ustvgo.tv/data.php', data={'stream': channel_id}) # TODO: get ID from URL
    url = response.text

    base_url = url.split('playlist.m3u8')[0]
    m3u = requests.get(url).text
    for token in m3u.split():
        if 'chunks.m3u8' in token:
            m3u = m3u.replace(token, base_url + token)

    return m3u

def src_youtube(url):
    with YoutubeDL({}) as ydl:
        try:
            res = ydl.extract_info(url, download=False)
        except DownloadError:
            raise Exception("Video not found!")

        # Get the highest quality stream
        highest_fmt = res['format']
        highest_stream = [i for i in res['formats'] if i['format'] == highest_fmt][0]['url']
        
        return redirect(highest_stream) # TODO: Sending a redirect may cause the stream to stop working after some time

source_dict = {
    'filmon': src_filmon,
    'ustvgo': src_ustvgo,
    'youtube': src_youtube
}

if __name__ == '__main__':
    print(src_youtube("https://www.youtube.com/watch?v=38IEolI8f-w"))
    pass