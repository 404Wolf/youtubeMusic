import pytube
import os
import subprocess
import threading
import asyncio
from random import randint
from mutagen.mp3 import MP3


async def fetch(url: str) -> int:
    """
    Download audio of youtube video and automaticaly inject metadata

    Args:
        url (str): URL of video to download.
        filepath (str, optional): Filepath up to the name of file. File extension automatically added.

    Returns:
        id of downloaded file. (name of file = "{id}.mp4")
    """

    id = randint(1000000, 9999999)

    # fetch and download youtube .webm audio for given URL
    stream = pytube.YouTube(url)
    stream = stream.streams.filter(only_audio=True, mime_type="audio/webm")
    stream = sorted(stream, key=lambda stream: stream.filesize, reverse=True)
    stream = stream[0]
    stream.download()
    os.rename(f"{stream.title}.webm", f"{id}.webm")

    # convert audio file
    def convert():
        subprocess.run(
            f'ffmpeg -i "{id}.webm" "{id}.mp3" -hide_banner -loglevel error'
        )
        os.remove(f"{id}.webm")
    
    conversion = threading.Thread(target=convert).start()
    while conversion.is_alive():
        await asyncio.sleep(.2)

    audio = MP3(f"{id}.mp3")
    print(audio.info.length)
    print(audio.info.bitrate)

    return id
