import asyncio
import helpers
import logging

# https://www.youtube.com/playlist?list=PLycVTiaj8OI80AsTGjYJAPi7-i8kTH-Bq


async def main():
    playlist = input("Enter playlist URL: ")

    # obtain list of links of videos in playlist
    urls = helpers.locate.playlist(playlist)

    # queue tasks to fetch metadata for all videos
    videos = {}  # url:metadata
    for url in urls:
        title = helpers.locate.name(url)
        title = title[:title.find("(")]
        videos[url] = asyncio.create_task(helpers.locate.metadata(title, max_hits=1))
    await asyncio.gather(*tuple(videos[video] for video in videos.keys()))
    
    # choose first result for metadata
    for url in videos:
        videos[url] = videos[url].result()
        if len(videos[url]) > 0:
            videos[url] = videos[url][0]
        else:
            videos[url] = {"title": helpers.locate.name(url), "artist": None, "album": None}

    # queue tasks to download all videos
    tasks = []
    for url in videos:
        tasks.append(helpers.data.download(url, filename=videos[url]["title"], filepath="output"))
    await asyncio.gather(*tasks)

    # inject metadata into items
    tasks = []
    for url in videos:
        try:
            if videos[url] is not None:
                helpers.data.inject(
                    "output/"+videos[url]["title"]+".mp3",
                    title=videos[url]["title"],
                    artist=videos[url]["artist"],
                    album=videos[url]["album"],
                )
        except:
            pass


asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
asyncio.run(main())
