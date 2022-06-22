import pytube
import os
import asyncio
import eyed3
from secrets import token_hex as id


async def download(url: str, filetype="mp3") -> int:
    """
    Download audio of youtube video and automaticaly inject metadata.

    Args:
        url (str): URL of video to download.
        filename (str, optional): Output filename. Defaults to the Youtube video's name.
        filepath (str, optional): Output filepath. Defaults to home directory.
        filetype (str, optional): Output filetype (file extention). Defaults to mp3.

    Returns:
        string: Location/name of downloaded file. (name of file = "{filename}.mp4")
    """

    def fetch():
        """Download and convert youtube file. This function is blocking."""

        filename = filename = id(16)

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
        os.remove(f"{filename}.{stream.type}")  # remove unconverted file

        return f"{filename}.{filetype}"

    return await asyncio.to_thread(fetch)


def inject(name: str, title=None, released=None, artist=None, album=None):
    """
    Inject metadata into mp3 audiofile.

    Args:
        name (str): Name of song file
        artist (str, optional): Song artist. Defaults to not inject any artist.
        album (str, optional): Song album. Defaults to not inject any album.
    """

    if ".mp3" not in name:
        name = name + "mp3"
        
    audiofile = eyed3.load(name)

    if title is not None:
        audiofile.tag.title = title
    if released is not None:
        audiofile.tag.original_release_date = released
    if artist is not None:
        audiofile.tag.artist = artist
    if album is not None:
        audiofile.tag.album = album
        
    audiofile.tag.save()
