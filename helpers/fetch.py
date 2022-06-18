from distutils import extension
import pytube
import os
import asyncio
from random import randint


async def download(url: str, filetype="wav", filename=False) -> int:
    """
    Download audio of youtube video and automaticaly inject metadata.

    Args:
        url (str): URL of video to download.
        filetype (str, optional): output filetype (file extention).
        filename (str, optional): name of output file.

    Returns:
        filename of downloaded file. (name of file = "{filename}.mp4")
    """

    if not bool(filename):
        filename=randint(1000000, 9999999)

    def threaded():
        """Download and convert youtube file. This function is blocking."""

        # fetch youtube file
        stream = pytube.YouTube(url)
        stream = stream.streams.filter(only_audio=True)
        
        # sort out highest quality audio stream
        stream = sorted(stream, key=lambda stream: stream.bitrate, reverse=True)
        stream = stream[0]
        stream.type = stream.mime_type.split("/")[1]

        # download youtube file
        stream.download(filename=f"{filename}.{stream.type}")

        # mp4 -> mp3
        os.system(
            f'ffmpeg -i "{filename}.{stream.type}" "{filename}.{filetype}" -hide_banner -loglevel error'
        )

        # remove unconverted format
        os.remove(f"{filename}.{stream.type}")  # remove unconverted mp4

    await asyncio.to_thread(threaded)
    return filename
