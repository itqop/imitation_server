import asyncio
import datetime
import pathlib
import json
import logging
import requests


async def generate_start():
    """
    ?
    :return: -async-
    """
    logging.info(msg="Starting json generate..")
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


async def get_intervals(rhost: str):

    pass


async def post_snapshots(rhost: str):
    pass
