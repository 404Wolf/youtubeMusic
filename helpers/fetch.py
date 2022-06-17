import pytube
import os
import asyncio
from random import randint
from mutagen.mp3 import MP3
import threading

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
    stream = stream.streams.filter(only_audio=True, file_extension='mp4')
    stream = sorted(stream, key=lambda stream: stream.filesize, reverse=True)
    stream = stream[0]

    # prevent main-thread-blocking by sending download+convert to new thread
    def threaded():
        # fetch youtube file
        stream = pytube.YouTube(url)
        stream = stream.streams.filter(only_audio=True, file_extension='mp4')
        stream = sorted(stream, key=lambda stream: stream.filesize, reverse=True)
        stream = stream[0]

        # download file and convert to mp3
        stream.download(filename=f"{id}.mp4")
        os.system(f'ffmpeg -i "{id}.mp4" "{id}.mp3" -hide_banner -loglevel error')
        os.remove(f"{id}.mp4")
    thread = threading.Thread(target=threaded)
    thread.start()
    while thread.is_alive():
        await asyncio.sleep(.15)

    # modify metadata of audio file (incomplete)
    audio = MP3(f"{id}.mp3")
    print(audio.info.length)
    print(audio.info.bitrate)

    return id
