from numpy import isin
import pytube
from typing import Generator
import aiohttp
import json


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


async def metadata(query: str) -> dict:
    wikipedia = "https://en.wikipedia.org/w/api.php"

    async with aiohttp.ClientSession() as session:
        params = {
            'action': 'query',
            'format': 'json',
            'list': 'search',
            'srsearch': query,
            'utf8': '1'
        }

        async with session.get(url=wikipedia, params=params) as resp:
            page = await resp.json()
            if page["query"]["searchinfo"]["totalhits"] == 0:
                return None
            page = page["query"]["search"][0]["title"].replace(" ","_")

        async with session.get(url=f"http://dbpedia.org/data/{page}.json") as resp:
            resp = await resp.json()
            resp = resp[f"http://dbpedia.org/resource/{page}"]

        data = {
            "title": "http://dbpedia.org/property/name",
            "released": "http://dbpedia.org/property/relyear",
            "album": "http://dbpedia.org/ontology/recordLabel",
            "artist": "http://dbpedia.org/property/artist",
            "songwriter": "http://dbpedia.org/ontology/writer",
            "producer": "http://dbpedia.org/ontology/producer",
            "genre": "http://dbpedia.org/ontology/genre",
        }

        for key in data.keys():
            if data[key] in resp: # obtain data
                data[key] = resp[data[key]]
                data[key] = data[key][0]["value"]
                if isinstance(data[key], str): # clean data
                    data[key] = data[key].replace("http://dbpedia.org/resource/", "")
                    data[key] = data[key].replace("_", " ").replace("-", " ").replace("\u2013", ", ")
            else: # mark null if no data found
                data[key] = None

        if all(data.values()):
            return data