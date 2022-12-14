import asyncio
import sqlite3
from datetime import datetime
import json
import logging

ID = 342  # ID комплекса
large_info = []
temp_times = dict()
fix_times = dict()


def db_search_periods(path: str, speed_x: int) -> dict:
    """
    Function to calculate a new acquisition interval time for each type of sensor.

    :param path: Path to sqlite3 database file
    :param speed_x: generation time acceleration multiplier
    :return: dictionary, format - sensor ID: time of data collection from sensors
    """
    conn = sqlite3.connect(path)
    cur = conn.cursor()
    query = f"SELECT id, interval FROM sensors;"
    cur.execute(query)
    rows = dict(tuple(map(lambda x: (int(x[0]), int(x[1] / speed_x)), cur.fetchall())))
    cur.close()
    conn.close()
    return rows


def db_generate_fake_actions(path: str, means_time: dict):
    """
    A function to generate data in its original form, but with a modified time.
    The resulting list of dictionaries is sorted by time,
    which allows it to be used without further processing.

    :param path: Path to sqlite3 database file
    :param means_time: dictionary, format - sensor ID: time of data collection from sensors
    :return: None, working with global var
    """
    global large_info, temp_times, fix_times
    fix_times = means_time.copy()
    conn = sqlite3.connect(path)
    cur = conn.cursor()
    # keys = ("sensor_id", "id_transaction", "value", "transaction_status", "transaction_type", "timestamp")
    keys = (0, 1, 2, 3, 4, 5)
    datetime.now()
    for idx in means_time.keys():
        query = "SELECT id, value, transaction_status, " \
                f"transaction_type from transactions WHERE sensor_id={idx}; "
        cur.execute(query)
        rows = tuple(map(lambda qur: (idx,) + qur, cur.fetchall()))

        temp_time = int(datetime.now().timestamp())
        for row in rows:
            temp_dict = dict(zip(keys, row + (temp_time,)))
            large_info.append(temp_dict)
            temp_time += means_time.get(idx)
        temp_times[idx] = temp_time
    cur.close()
    conn.close()
    # large_info.sort(key=lambda unit: unit.get("timestamp"))
    large_info.sort(key=lambda unit: unit.get(5))


def time_update() -> int:
    """
    The function updates the time (timestamp)
    to the current value without changing the data itself.
    That is, it allows you to loop the data simulation.

    :return: success code (1)
    """
    for i in range(len(large_info)):
        ids = large_info[i]["sensor_id"]
        temp_times[ids] += fix_times.get(ids)
        # large_info[i]["timestamp"] += temp_times[ids]
        large_info[i][5] += temp_times[ids]
    return 1


async def generate_json_dumps(interval: int):
    """
    Function for asynchronous generation of json snapshots from the database.
    :param interval: interval time in seconds
    :return: -async-
    """
    logging.info(msg="Starting generate json dumps..")
    i = 0
    # timestamp_dict = {"timestamp_push": 0, "timestamp_create": 0, "id": ID, "info": []}
    timestamp_dict = {"timestamp_push": 0, "timestamp_create": 0, "id": ID, "life": ["a few objects"], "info": []}
    # temp_stamp = large_info[i]["timestamp"]
    temp_stamp = large_info[i][5]
    while True:
        if i == len(large_info):
            time_update()
            i = 0
            continue
        if large_info[i][5] - temp_stamp > interval:
            # temp_stamp = large_info[i]["timestamp"]
            temp_stamp = large_info[i][5]
            timestamp_dict["timestamp_create"] = temp_stamp
            with open(f"json_cache/{temp_stamp}.json", "w") as outfile:
                json.dump(timestamp_dict, outfile)
            logging.info(msg="Creating " + f"{temp_stamp}.json")
            await asyncio.sleep(interval)
            timestamp_dict["info"] = []
            continue
        timestamp_dict["info"].append(large_info[i])
        i += 1
