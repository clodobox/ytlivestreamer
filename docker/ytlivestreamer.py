import sys
import time
import yt_dlp
import logging
import os
import argparse
from datetime import datetime

# Set up logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Define the downloads folder
DOWNLOADS_FOLDER = 'downloads'

def get_channel_id(url):
    ydl_opts = {
        'quiet': True,
        'extract_flat': True,
        'force_generic_extractor': True,
    }
    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            result = ydl.extract_info(url, download=False)
            return result.get('channel_id') or result.get('id')
    except Exception as e:
        logging.error(f"Error getting channel ID: {str(e)}")
        return None

def ensure_download_folder_exists():
    if not os.path.exists(DOWNLOADS_FOLDER):
        os.makedirs(DOWNLOADS_FOLDER)
        logging.info(f"Created downloads folder: {DOWNLOADS_FOLDER}")

def monitor_and_download(channel_id, args):
    logging.info(f"Starting to monitor channel ID: {channel_id}")
    
    ensure_download_folder_exists()
    
    ydl_opts = {
        'format': args.quality,
        'outtmpl': os.path.join(DOWNLOADS_FOLDER, '%(title)s-%(id)s.%(ext)s'),
        'merge_output_format': args.encapsulation,
        'live_from_start': True,
        'wait_for_video': (5, 60),
    }

    if args.current_only:
        download_current_live(channel_id, ydl_opts)
    elif args.future or args.all:
        monitor_future_live(channel_id, ydl_opts)

def download_current_live(channel_id, ydl_opts):
    url = f'https://www.youtube.com/channel/{channel_id}/live'
    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([url])
        logging.info("Successfully downloaded current live stream.")
    except Exception as e:
        logging.error(f"Error downloading current live stream: {str(e)}")

def monitor_future_live(channel_id, ydl_opts):
    while True:
        try:
            logging.info("Checking for live stream...")
            url = f'https://www.youtube.com/channel/{channel_id}/live'
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                info = ydl.extract_info(url, download=False)
                if info and info.get('is_live'):
                    logging.info(f"Live stream found: {info.get('title', 'Unknown title')}")
                    ydl.download([url])
                    logging.info("Download completed.")
                else:
                    logging.info("No live stream found.")
        except yt_dlp.utils.DownloadError as e:
            if "The channel is not currently live" in str(e):
                logging.info("The channel is not currently live.")
            else:
                logging.error(f"Download error: {str(e)}")
        except Exception as e:
            logging.error(f"An unexpected error occurred: {str(e)}", exc_info=True)
        
        logging.info("Waiting for 1 minute before checking again...")
        for _ in range(60):
            time.sleep(1)
            if check_interrupt():
                return

def check_interrupt():
    try:
        if sys.stdin.isatty():
            return sys.stdin.read(1) if os.name == 'nt' else sys.stdin.read(1) if select.select([sys.stdin], [], [], 0)[0] else False
    except:
        pass
    return False

def main():
    channel_url = os.environ.get('CHANNEL_URL')
    if not channel_url:
        logging.error("CHANNEL_URL environment variable is not set.")
        return

    args = argparse.Namespace()
    args.future = os.environ.get('FUTURE', 'true').lower() == 'true'
    args.all = os.environ.get('ALL', 'false').lower() == 'true'
    args.current_only = os.environ.get('CURRENT_ONLY', 'false').lower() == 'true'
    args.encapsulation = os.environ.get('ENCAPSULATION', 'mkv')
    args.quality = os.environ.get('QUALITY', 'bestvideo+bestaudio/best')

    if args.all:
        args.future = True

    if not (args.future or args.all or args.current_only):
        args.future = True  # Default behavior

    try:
        channel_id = get_channel_id(channel_url)
        if channel_id:
            monitor_and_download(channel_id, args)
        else:
            logging.error("Failed to get channel ID. Please check the URL and try again.")
    except KeyboardInterrupt:
        print("\nScript interrupted by user. Exiting...")
    finally:
        print("Script execution completed.")

if __name__ == "__main__":
    main()