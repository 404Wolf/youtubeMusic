import asyncio
import helpers
import os

async def main():
    title = input("Enter song name: ")
    data = await helpers.locate.metadata(f"{title} song", max_hits=1)
    data = data[0] # choose first wiki result
    data["url"] = helpers.locate.song(f"{data['title']} by {data['artist']}", max_hits=1)
    data["url"] = data["url"][0] # choose first youtube result
    filename = await helpers.data.download(data["url"])
    
    helpers.data.inject(
            filename,
            title=data["title"],
            artist=data["artist"],
            released=data["released"],
            album=data["album"],
        )
    os.rename(filename, f"output/{data['title']}.mp3")

asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
while True:
    asyncio.run(main())

