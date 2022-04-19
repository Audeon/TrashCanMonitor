from logging import getLogger
from os import environ
from time import sleep

from app.functions import ConfigApp, TrashcanMonitor


def trashcan_monitor():
    # This is the preferred method of configuring the application, from config file.
    config = ConfigApp.from_config_file(environ.get("CONFIG_PATH"))

    # You can also get the configuration variables from environmental variables.
    # config = ConfigApp.from_env_vars()

    # You can also initialize the configuration variables via key word arguments
    # config_dict = {
    #     "trashcan_sleep_time": 30,
    #     "log_level": 10,
    #     "transport": "api"
    # }
    # config = ConfigApp(**config_dict)

    log = getLogger(__name__)
    tcm = TrashcanMonitor.from_config(config)

    while True:
        try:
            results = tcm.start_test()
        except Exception as err:
            results = {"gateway_check": False}
            log.critical(str(err))
        else:
            log.debug(results)

        log.debug(f"Pausing testing for {config.sleep_time}")
        sleep(config.sleep_time)
    #     mt = MongoTransport(from_config=config)

    #
    #     try:
    #         mt.add_data(results)
    #     except Exception as err:
    #         log.critical(err)
    #     else:
    #         log.info(f"Testing complete, document id: {mt.recent_id} added to db.")
    #
    #     log.debug(f"Pausing testing for {config.sleep_time}")


if __name__ == "__main__":
    trashcan_monitor()
