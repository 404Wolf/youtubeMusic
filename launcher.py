import helpers
import asyncio

# the beatles' White Album playlist (posted by the official beatles channel)
beatlesWhiteAlbum = (
    "https://www.youtube.com/playlist?list=OLAK5uy_njHTOnoK_aQOAa3XvnvmzZ76n8cBIJquI"
)


async def main():
    videos = await helpers.locate.playlist(beatlesWhiteAlbum)
    tasks = []
    for url in videos:
        tasks.append(asyncio.create_task(helpers.download(url)))
    tasks = await asyncio.gather(*tasks)


asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
asyncio.run(main())
