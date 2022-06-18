import pytube
from typing import Generator


async def playlist(url: str) -> Generator:
    """
    Youtube playlist URL to generator of all videos in playlist.

    Args:
        url (str): URL of playlist.

    Returns:
        Generator: generator with all URLs of videos in youtube playlist.
    """
    urls = pytube.contrib.playlist.Playlist(url)
    urls = urls.url_generator()
    return urls


async def artist(url: str) -> Generator:
    """
    Youtube channel (artist) URL to generator of all videos of artist.

    Args:
        url (str): URL of channel.

    Returns:
        Generator: generator with all URLs of videos of youtube channel.
    """
    urls = pytube.contrib.channel.Channel(url)
    urls = urls.url_generator()
    return urls
