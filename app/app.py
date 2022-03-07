from datetime import datetime, timedelta, timezone
from logging import getLogger
from time import sleep
from transport.mongodb import *
from functions.trascan_mon import TrashcanMon
from functions.config_init import Config


if __name__ == "__main__":
    config_path = "."
    config = Config(config_path=config_path)
    log = getLogger(__name__)

    while(True):
        tcm = TrashcanMon(from_config=config)
        mt = MongoTransport(from_config=config)
        try:
            results = tcm.start_test()
        except Exception as err:
            results = { "gateway_check" : False }
            log.critical(str(err))
        else:
            log.debug(results)

        try:
            mt.add_data(results)
        except Exception as err:
            log.critical(err)
        else:
            log.info(f"Testing complete, document id: { mt.recent_id } added to db.")

        log.debug(f"Pausing testing for { config.sleep_time }")
        sleep(config.sleep_time)


