import helpers
import asyncio

videos = [
    "https://www.youtube.com/watch?v=EwXsiXTzXLk",
    "https://www.youtube.com/watch?v=c96uOVJk-8g",
    # "https://www.youtube.com/watch?v=WPs67ap6AeY",
    # "https://www.youtube.com/watch?v=kG5LCoRqGSI",
    # "https://www.youtube.com/watch?v=x0NDkRxG0-8",
    # "https://www.youtube.com/watch?v=QvqjVCWT_4g",
]


async def main():
    tasks = [asyncio.create_task(helpers.fetch(video)) for video in videos]
    await asyncio.gather(*tasks)


asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
asyncio.run(main())
