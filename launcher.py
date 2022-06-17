import helpers
import asyncio

async def main():
    await helpers.fetch("https://www.youtube.com/watch?v=dQw4w9WgXcQ", "test/bobby")

asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
asyncio.run(main())