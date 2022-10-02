from db_commands import generate_json_dumps
from tcp_serv import tcp_start
import asyncio
import logging


async def start(interval):
    logging.info(msg="Starting generate json dumps..")
    task_json = asyncio.create_task(generate_json_dumps(interval))
    logging.info(msg="Starting tcp server..")
    task_tcp_serv = asyncio.create_task(tcp_start())

    await task_json
    await task_tcp_serv


