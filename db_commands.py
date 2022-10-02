import sqlite3


def db_search_periods(path: str, speed_x: int) -> dict:
    conn = sqlite3.connect(path)
    cur = conn.cursor()
    query = f"SELECT id, interval FROM sensors;"
    cur.execute(query)
    rows = dict(tuple(map(lambda x: (int(x[0]), int(x[1]) / speed_x), cur.fetchall())))
    cur.close()
    conn.close()
    return rows


def db_generate_fake_actions(path: str, means_time: dict) -> list:
    conn = sqlite3.connect(path)
    cur = conn.cursor()
    large_dict = []
    for idx in means_time.keys():
        query = "SELECT id, value, transaction_status, " \
                f"transaction_type from transactions WHERE sensor_id={idx}; "
        cur.execute(query)
        # rows = cur.fetchall()
        # large_dict.append(dict(zip(("sensor_id", "id_transaction", "transaction_status", "transaction_type"),(idx,
        # ) + rows)))
    cur.close()
    conn.close()
    return large_dict
