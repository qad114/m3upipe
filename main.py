import base64
import json
import requests
import urllib
from sources import source_dict
from flask import Flask, redirect

IP_ADDR = '127.0.0.1'
PORT = 5000

app = Flask("m3upipe")

def add_stream(stream):
    """ Adds stream handling rule to Flask """
    stream_name = stream['name']

    def _stream_handler():
        source_type = stream['src-type']
        if source_type == 'as-is':
            # Don't use Flask - skip
            return
        else:
            source_handler = source_dict[stream['src-type']]
        return source_handler(stream['src'])

    app.add_url_rule('/' + stream_name, stream_name, _stream_handler)

def gen_m3u(playlist):
    streams = playlist['streams']
    s = "#EXTM3U\n"

    for stream in streams:
        if stream['src-type'] == 'as-is':
            s += f"#EXTINF:-1,{stream['name']}\n{stream['src']}\n"
        else:
            s += f"#EXTINF:-1,{stream['name']}\nhttp://{IP_ADDR}:{PORT}/{urllib.parse.quote(stream['name'])}\n"
    
    return s

def start_server():
    app.run(host='0.0.0.0', debug=True)

def main():
    # Get the playlist
    with open('playlist.json', 'r') as f:
        playlist = json.load(f)

    try:
        streams = playlist['streams']
    except KeyError:
        raise KeyError("Playlist file is invalid!")

    # Add each stream to the Flask app
    for stream in streams:
        add_stream(stream)

    # Add M3U playlist rule
    app.add_url_rule('/playlist', 'playlist', lambda: gen_m3u(playlist))

    # Start the server
    start_server()

if __name__ == '__main__':
    main()