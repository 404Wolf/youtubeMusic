import pytube
import os
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
    stream = stream.streams.filter(only_audio=True, file_extension='mp4')
    stream = sorted(stream, key=lambda stream: stream.filesize, reverse=True)
    stream = stream[0]
    await asyncio.to_thread(stream.download)
    os.rename(f"{stream.title}.mp4", f"{id}.mp4")

    # convert audio file
    await asyncio.to_thread(lambda: os.system(f'ffmpeg -i "{id}.mp4" "{id}.mp3" -hide_banner -loglevel error'))
    os.remove(f"{id}.mp4")

    # modify metadata of audio file (incomplete)
    audio = MP3(f"{id}.mp3")
    print(audio.info.length)
    print(audio.info.bitrate)

    return id
