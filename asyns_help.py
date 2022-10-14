from db_commands import generate_json_dumps
from https_serv import post_snapshots, get_intervals
import asyncio


def convert_format(address: str) -> str:
    """
    Function for format input address
    :param address: RHOST address
    :return: formatted address
    """
    if not address.endswith('/'):
        address += '/'
    elif not address.startswith("https://"):
        address += "https://"
    return address


async def start(interval: int, rhost: str):
    """
    Function for asynchronous launch of tasks.
    :param rhost: https host address
    :param interval: json data sending interval time !IN SECONDS!
    :return: -async-
    """
    rhost = convert_format(rhost)

    task_json = asyncio.create_task(generate_json_dumps(interval))
    task_requests_serv = asyncio.create_task(post_snapshots(rhost))
    task_get_intervals = asyncio.create_task(get_intervals(rhost))

    await task_json
    await task_requests_serv
    await task_get_intervals
