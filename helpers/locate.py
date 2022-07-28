import pytube
from typing import Generator
import aiohttp
from urllib.parse import urlparse

def name(url: str) -> str:
    """Return the title of a given youtube URL's video"""
    return pytube.YouTube(url).title

def song(query: str, max_hits=3) -> tuple:
    """
    Song name to youtube URL.

    Args:
        query (str): Song name.
        max_hits (int, optional): Max amount of wiki pages to scan. Defaults to 3.
    """
    urls = pytube.Search(query)

    output = []
    for result in urls.results:
        output.append(result.watch_url)
        if len(output) == max_hits:
            return output
    return output

def playlist(url: str) -> Generator:
    """
    Youtube playlist URL to generator of all videos in playlist.

    Args:
        url (str): URL of playlist.

    Returns:
        Generator: Generator with all URLs of videos in youtube playlist.
    """
    urls = pytube.contrib.playlist.Playlist(url)
    urls = urls.url_generator()
    return urls


def artist(url: str) -> Generator:
    """
    Youtube channel (artist) URL to generator of all videos of artist.

    Args:
        url (str): URL of channel.

    Returns:
        Generator: Generator with all URLs of videos of youtube channel.
    """
    urls = pytube.contrib.channel.Channel(url)
    urls = urls.url_generator()
    return urls


async def metadata(query: str, max_hits=3) -> list:
    """
    Obtain metadata for music.

    Args:
        query (str): Song name.
        max_hits (int, optional): Max amount of wiki pages to scan. Defaults to 3.

    Returns:
        list: List of wiki page results' data.
    """
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
            hits = page["query"]["search"]
            hits = (hit["title"].replace(" ","_") for hit in hits)

        output = []
        for hit in hits:
            async with session.get(url=urlparse(f"http://dbpedia.org/data/{hit}.json").geturl()) as resp:
                try:
                    resp = await resp.json()
                except aiohttp.client_exceptions.ContentTypeError:
                    continue
                try:
                    resp = resp[f"http://dbpedia.org/resource/{hit}"]
                except:
                    return None

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

            if tuple(data.values()).count(None) >= len(data)-2:
                continue

            output.append(data)

            if len(output) == max_hits:
                return output

    return output