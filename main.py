from exceptions import NotExists
import logging
from pathlib import Path
import sys
from db_commands import db_search_periods, db_generate_fake_actions
import asyns_help
import asyncio


MULTIPLE_NUM = 20
PATH = None
FORMAT = '%(asctime)s %(message)s'
INTERVAL = 10
RHOST = "localhost"


if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO, format=FORMAT, datefmt='[%d.%m.%y %H:%M:%S]')

    try:
        PATH = sys.argv[1]
        if not Path(PATH).is_file() or not PATH.endswith(".db"):
            raise NotExists
        MULTIPLE_NUM = int(sys.argv[2])
        if len(sys.argv) > 3:
            INTERVAL = int(sys.argv[3])
        elif len(sys.argv) > 4:
            RHOST = str(sys.argv[4])
        else:
            logging.warning(msg="Set default interval time to 10.\n "
                                "Set default address to localhost \n"
                                "usage: main.py <path to db file> "
                                "<MULTIPLE_NUM generation time acceleration multiplier (maybe 60?)>"
                                "<json data sending period time !IN SECONDS!> (maybe 10?)"
                                "<https host address for POST>"
                                "<https host address for GET>")
    except (IndexError, ValueError):
        logging.error("usage: main.py <path to db file> "
                      "<MULTIPLE_NUM generation time acceleration multiplier (maybe 30?)>"
                      "<json data sending interval time !IN SECONDS!> (maybe 10?)"
                      "<https host address for POST>"
                      "<https host address for GET>")
        exit(1)
    except NotExists:
        logging.error("Not found db on path - " + PATH)
        exit(1)

    logging.info(msg="Starting imitation server..")
    logging.info(msg="Starting calculation interval time..")
    periods = db_search_periods(PATH, MULTIPLE_NUM)
    logging.info(msg="Successful calculation interval time")
    logging.info(msg="Starting generate fake actions..")
    db_generate_fake_actions(PATH, periods)
    logging.info(msg="Starting async processing..")
    asyncio.run(asyns_help.start(INTERVAL, RHOST))

