from db_commands import generate_json_dumps
from https_serv import post_snapshots, get_intervals
import asyncio


async def start(interval: int, rhost: str, rhost_get: str):
    """
    Function for asynchronous launch of tasks.
    :param rhost_get: https host address for get intervals
    :param rhost: https host address for post json snapshots
    :param interval: json data sending interval time !IN SECONDS!
    :return: -async-
    """
    task_json = asyncio.create_task(generate_json_dumps(interval))
    task_requests_serv = asyncio.create_task(post_snapshots(rhost))
    task_get_intervals = asyncio.create_task(get_intervals(rhost_get))
    await task_json
    await task_requests_serv
    await task_get_intervals
