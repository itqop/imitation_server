import asyncio


async def tcp_start():
    while True:
        await asyncio.sleep(1)
        print("tcp")
