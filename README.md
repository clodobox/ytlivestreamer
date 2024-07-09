# Ytlivestreamer

This Python script allows you to monitor and download live streams from a YouTube channel.
It can download current live streams, wait for future streams, and even download past streams (when configured).

## Features

- Monitor a YouTube channel for live streams
- Download current live streams
- Wait for and download future live streams
- Configurable video quality and encapsulation format
- Logging of all activities

## Requirements

- Python 3.6+
- yt-dlp library

## Installation

1. Clone this repository:
```
git clone https://github.com/clodobox/ytlivestreamer
cd ytlivestreamer
```

2. Install the required Python packages:
```
pip install yt-dlp
```

## Usage

Basic usage:
```
python ytlivestreamer.py [CHANNEL_URL] [OPTIONS]
Options:

-f, --future: Download current and future live streams
-a, --all: Download all old and future live streams
-c, --current-only: Download only the current live stream and stop
-e {mkv,mp4}, --encapsulation {mkv,mp4}: Encapsulation format (default: mkv)
-q QUALITY, --quality QUALITY: Video quality (default: best)
```

## Example:
```
python ytlivestreamer.py https://www.youtube.com/channel/CHANNEL_ID -f -e mp4
```

This will monitor the specified channel for current and future live streams, downloading them in MP4 format.

Running in the Background
To run the script in the background, you can use screen:

```
screen -S ytlivestreamer python ytlivestreamer.py [CHANNEL_URL] [OPTIONS]
screen -r ytlivestreamer
```

## Notes

The script creates a downloads folder in the same directory to store downloaded videos.
The script checks for new live streams every minute.
You can interrupt the script at any time by pressing Ctrl+C.

## Contributing

Contributions, issues, and feature requests are welcome.
Feel free to check issues page if you want to contribute.

## License

What ?