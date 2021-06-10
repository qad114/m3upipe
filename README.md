# m3upipe
m3upipe is a Python script which allows you to pipe streams from various sources (for example YouTube) into a dynamic M3U file that is compatible with any IPTV player. The piping is handled by a local web server, powered by Flask.

## Usage
- Install the following dependencies using `pip`: `flask`, `requests`, `youtube_dl`
- Clone or download the repository to a folder where you have read/write permissions
- Create a playlist file in the same folder, named `playlist.json` (the format of this file is shown below), and add your streams to it
- Run `main.py`
- Open your IPTV player and configure it to fetch the playlist from `http://127.0.0.1:5000/playlist`
- Your channels should show in the IPTV player

## Playlist format (playlist.json)
Here is a sample file with 2 channels added. You may add as many channels as you like.
```json
{
  "streams": [
    {
      "name": "<insert name of channel 1>",
      "src": "<insert source URL of channel 1>",
      "src-type": "<insert source type of channel 1>"
    },
    {
      "name": "<insert name of channel 2>",
      "src": "<insert source URL of channel 2>",
      "src-type": "<insert source type of channel 2>"
    },
  ]
}
```

## Supported source types
- `filmon`
- `ustvgo`
- `youtube`

## Adding more source types (for developers)
Source types are defined in the sources.py file. To add a new source type, write a function to parse that source, and then add it to the `source_dict` dictionary.

## TODO:
- Make a helper script or GUI to add, remove and modify streams
- Make it possible to run the script on an external server
- Implement XMLTV (EPG) scraping