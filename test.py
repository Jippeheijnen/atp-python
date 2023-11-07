import asyncio
import time


def sync_code():
    while True:
        print("e")
        time.sleep(0.5)
async def start_timer(secs):
    await asyncio.sleep(secs)
    raise Exception
async def main():
    asyncio.create_task(start_timer(5))
    loop = asyncio.get_event_loop()
    # use run_in_executor to run sync code in a separate thread
    # while this thread runs the event loop
    await loop.run_in_executor(None, sync_code)

asyncio.run(main())