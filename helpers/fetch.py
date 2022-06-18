import pytube
import os
import asyncio
from random import randint


async def fetch(url: str, filetype="mp3", filename=randint(1000000, 9999999)) -> int:
    """
    Download audio of youtube video and automaticaly inject metadata.

    Args:
        url (str): URL of video to download.
        filetype (str, optional): output filetype (file extention).
        filename (str, optional): name of output file.

    Returns:
        filename of downloaded file. (name of file = "{filename}.mp4")
    """

    def threaded():
        """Download and convert youtube file. This function is blocking."""

        # fetch youtube file
        stream = pytube.YouTube(url)
        stream = stream.streams.filter(only_audio=True, file_extension="mp4")
        stream = sorted(stream, key=lambda stream: stream.filesize, reverse=True)
        stream = stream[0]

        # download youtube file
        stream.download(filename=f"{filename}.mp4")

        # mp4 -> mp3
        os.system(
            f'ffmpeg -i "{filename}.mp4" -c:v libx264 -qp 0 "{filename}.{filetype}" -hide_banner -loglevel error'
        )

    await asyncio.to_thread(threaded)
    os.remove(f"{filename}.mp4")  # remove unconverted mp4

    return filename
