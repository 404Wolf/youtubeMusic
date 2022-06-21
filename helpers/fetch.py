import pytube
import os
import asyncio
from random import randint
from sanitize_filename import sanitize


async def download(url: str, folder, filetype="mp3") -> int:
    """
    Download audio of youtube video and automaticaly inject metadata.

    Args:
        url (str): URL of video to download.
        filetype (str, optional): output filetype (file extention).

    Returns:
        filename of downloaded file. (name of file = "{filename}.mp4")
    """

    def threaded():
        """Download and convert youtube file. This function is blocking."""

        # fetch youtube file
        stream = pytube.YouTube(url)
        stream = stream.streams.filter(only_audio=True)

        # sort out highest quality audio stream
        stream = sorted(stream, key=lambda stream: stream.bitrate, reverse=True)
        stream = stream[0]
        stream.type = stream.mime_type.split("/")[1]
        filename = sanitize(stream.title)

        # download youtube file
        stream.download(filename=f"{filename}.{stream.type}")

        # mp4 -> mp3
        os.system(
            f'ffmpeg -i "{filename}.{stream.type}" "{filename}.{filetype}" -hide_banner -loglevel error'
        )

        # remove unconverted format
        os.remove(f"{filename}.{stream.type}")  # remove unconverted mp4
        os.rename(f"{filename}.{filetype}", f"{folder}/{filename}.{filetype}")

    await asyncio.to_thread(threaded)
