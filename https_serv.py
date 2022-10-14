import asyncio
import datetime
import pathlib
import json
import logging
import requests

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
    while True:
        files = path.glob("*.json")
        for p in files:
            with open(p) as json_file:
                data = json.load(json_file)
                data["timestamp_push"] = int(datetime.datetime.now().timestamp())
            with open(p, "w") as outfile:
                json.dump(data, outfile)

            logging.info(msg="Send " + p.name)
            post = requests.post(rhost, data=data, headers=headers)
            await asyncio.sleep(1)
            if post.status_code == 200:
                logging.info(msg="Successful post snapshot! ~ " + p.name)
                p.unlink()
                logging.info(msg="Deleting " + p.name)
            else:
                logging.info(msg="ERROR post snapshot! ~ " + str(post.status_code))
        print(11)
        await asyncio.sleep(10)


async def get_intervals(rhost: str):
    """
    Function to get updated intervals from the server
    :param rhost: https host address
    :return: -async-
    """
    con = requests.get(rhost)
    if con.status_code == 200:
        intervals = con.json()  # json with intervals
        logging.info(msg="Successful get json with intervals! ~ " + str(dict(intervals))[:20])
    else:
        logging.info(msg="ERROR get json with intervals! ~ " + str(con.status_code))
    # For fake server this feature needless
    await asyncio.sleep(3000)
