import asyncio
import datetime
import pathlib
import json
import logging


async def tcp_start():
    """
    ?
    :return: -async-
    """
    logging.info(msg="Starting tcp server..")
    await asyncio.sleep(1)
    path = pathlib.Path.cwd() / 'json_cache'
    while True:
        files = path.glob("*.json")
        for p in files:
            with open(p) as json_file:
                data = json.load(json_file)
                data["timestamp_push"] = int(datetime.datetime.now().timestamp())
            with open(p, "w") as outfile:
                json.dump(data, outfile)
            logging.info(msg="Send " + p.name)
            await asyncio.sleep(1)
            p.unlink()
            logging.info(msg="Deleting " + p.name)
        await asyncio.sleep(10)
