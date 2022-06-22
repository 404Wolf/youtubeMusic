import asyncio
import helpers
import os


async def main():
    playlist = input("Enter playlist URL: ")

    # obtain list of links of videos in playlist
    urls = helpers.locate.playlist(playlist)

    # queue tasks to fetch metadata for all videos
    videos = {}  # url:metadata
    for url in urls:
        title = helpers.locate.name(url)
        if "(" in title:
            title = title[: title.find("(")]
        videos[url] = asyncio.create_task(
            helpers.locate.metadata(title + " song", max_hits=1)
        )
    await asyncio.wait(videos.values())
    for url in videos:
        result = videos[url].result()
        if result is not None:
            videos[url] = result[0]
        else:
            videos[url] = {"title":helpers.locate.name(url), "artist": None, "released": None, "album": None}
        
    downloads = []
    for url, metadata in videos.items():
        downloads.append([asyncio.create_task(helpers.data.download(url)), metadata])
    await asyncio.wait([download[0] for download in downloads])

    for filename, metadata in downloads:
        filename = filename.result()
        helpers.data.inject(
            filename,
            artist=metadata["artist"],
            released=metadata["released"],
            album=metadata["album"],
        )
        os.rename(filename, f"output/{metadata['title']}.mp3")


asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
asyncio.run(main())
