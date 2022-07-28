import asyncio
import helpers
import os
import threading


async def fetch(title, url=None):
    data = await helpers.locate.metadata(f"{title} song", max_hits=1)

    try:
        data = data[0]  # choose first wiki result
    except IndexError:
        data = {"title": title, "artist": None, "released": None, "album": None}

    if url is None:
        data["url"] = helpers.locate.song(
            f"{data['title']} by {data['artist']}", max_hits=1
        )
        url = data["url"] = data["url"][0]  # choose first youtube result

    filename = await helpers.data.download(url)

    helpers.data.inject(
        filename,
        title=data["title"],
        artist=data["artist"],
        released=data["released"],
        album=data["album"],
    )
    try:
        os.rename(filename, f"output/{data['title']}.mp3", )
    except FileExistsError:
        os.remove(filename)


async def main(query):
    if "http" in query:
        if "playlist" in query:
            songs = helpers.locate.playlist(query)
            await asyncio.gather(
                *[
                    asyncio.create_task(fetch(helpers.locate.name(song), url=song))
                    for song in songs
                ]
            )
        else:
            await fetch(helpers.locate.name(query), url=query)
    else:
        await fetch(query)

asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())

while True:
    print("[i]nput.txt or [m]anual input?")
    mode = input("> ")
    if mode == "i":
        threads = []
        for line in open("input.txt").read().split("\n"):
            print(f"\"{line}\"...")
            asyncio.run(main(line))
    elif mode == "m":
        while True:
            query = input("Enter song name, video url, or playlist url: ")
            asyncio.run(main(query))
    else:
        print("Invalid mode.")

