from db_commands import generate_json_dumps
from tcp_serv import tcp_start
import asyncio


async def start(interval: int):
    """
    Function for asynchronous launch of tasks.
    :param interval: json data sending interval time !IN SECONDS!
    :return: -async-
    """
    task_json = asyncio.create_task(generate_json_dumps(interval))
    task_tcp_serv = asyncio.create_task(tcp_start())

    await task_json
    await task_tcp_serv
