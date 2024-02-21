import os
import sys
import time
from pytube import YouTube
# from pytube.cli import on_progress
from pydub import AudioSegment
import ffmpeg
import re
import subprocess

start_time = time.time()

def convert_audio_with_progress(input_file, output_file, output_format):
    command = [
        'ffmpeg',
        '-y',  # Overwrite output file if it exists
        '-i', input_file,  # Input file
        output_file  # Output file
    ]

    process = subprocess.Popen(command, stderr=subprocess.PIPE, universal_newlines=True)
    while True:
        output = process.stderr.readline()
        if output == '' and process.poll() is not None:
            break
        if output:
            match = re.search(r"time=(\d+:\d+:\d+.\d+)", output)
            if match:
                elapsed_time = match.group(1)
                print(f"\rConverting... {elapsed_time}", end='')
    if process.poll() == 0:
        print("\nConversion completed successfully.")
    else:
        print("\nConversion failed.")

def custom_on_progress(stream, chunk, bytes_remaining):
    """
    Custom callback function to handle progress updates.

    Args:
    stream: A pytube Stream object.
    chunk: The bytes received from the last chunk. This argument is not used in this function but required by the callback signature.
    bytes_remaining: The number of bytes remaining to be downloaded.
    """
    total_size = stream.filesize
    bytes_downloaded = total_size - bytes_remaining
    percentage_of_completion = (bytes_downloaded / total_size) * 100
    if bytes_remaining == 0:
        print(f"Downloaded {bytes_downloaded} of {total_size} bytes ({percentage_of_completion:.2f}%)", end='\n')
    else:
        print(f"Downloaded {bytes_downloaded} of {total_size} bytes ({percentage_of_completion:.2f}%)", end='\r')

def is_valid_url(url):
    youtube_url_pattern = r'https?://www\.youtube\.com/watch\?v=[\w-]+'
    return re.match(youtube_url_pattern, url) is not None

def download_audio(youtube_url, output_file=None):
    yt = YouTube(youtube_url, on_progress_callback=custom_on_progress)
    audio_stream = yt.streams.filter(only_audio=True).first()
    output_file = output_file or "yt_audio.mp3"
    audio_file = audio_stream.download(output_path=".", filename="audio")
    return audio_file

def main():
    if len(sys.argv) > 1:
        youtube_url = sys.argv[1]
        if not is_valid_url(youtube_url):
            print("The provided URL does not appear to be a valid YouTube video URL.")
            return
    else:
        youtube_url = input("Enter the URL of the YouTube video: ")
        if not is_valid_url(youtube_url):
            print("The provided URL does not appear to be a valid YouTube video URL.")
            return

    audio_file = download_audio(youtube_url)
    convert_audio_with_progress(audio_file, "yt_audio.mp3", "mp3")
    os.remove(audio_file)

    end_time = time.time()
    execution_time = end_time - start_time
    print(f"\nExecution time: {execution_time:.2f} seconds")

if __name__ == "__main__":
    main()
