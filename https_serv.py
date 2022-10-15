import asyncio
import datetime
import pathlib
import json
import logging
import requests
from urllib3 import PoolManager

from db_commands import ID
headers = {'Content-type': 'application/json', 'Accept': 'text/plain'}


async def post_snapshots(rhost: str):
    """
    Function to send a snapshots to the server by POST request
    :param rhost: https host address
    :return: -async-
    """
    logging.info(msg="Starting json generate..")
    await asyncio.sleep(1)
    path = pathlib.Path.cwd() / 'json_cache'
    https_post = PoolManager()
    while True:
        files = path.glob("*.json")
        for p in files:
            with open(p) as json_file:
                data = json.load(json_file)
                data["timestamp_push"] = int(datetime.datetime.now().timestamp())
                encoded_data = json.dumps(data).encode('utf-8')
            with open(p, "w") as outfile:
                json.dump(data, outfile)

            logging.info(msg="Send " + p.name)
            try:
                post = https_post.request('POST', rhost + str(ID), body=encoded_data, headers=headers)
                if post.status == 200:
                    logging.info(msg="Successful post snapshot! ~ " + p.name)
                    p.unlink()
                    logging.info(msg="Deleting " + p.name)
                else:
                    logging.info(msg="ERROR post snapshot! ~ " + str(post.status))
                post.close()
            except requests.exceptions.ConnectionError:
                logging.error(msg="SERVER UNAVAILABLE!!!")
                continue
        await asyncio.sleep(10)


async def get_intervals(rhost: str):
    """
    Function to get updated intervals from the server
    :param rhost: https host address
    :return: -async-
    """
    https_get = PoolManager()
    while True:
        con = https_get.request('GET', rhost + str(ID))
        if con.status == 200:
            intervals = json.loads(con.data.decode('utf-8'))  # json with intervals
            logging.info(msg="Successful get json with intervals! ")
        else:
            logging.info(msg="ERROR get json with intervals! ~ " + str(con.status))
        # For fake server this feature needless
        await asyncio.sleep(10)
