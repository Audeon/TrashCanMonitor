from logging import getLogger
from time import sleep
from functions.trascan_mon import TrashcanMon
from functions.config_init import Config


if __name__ == "__main__":
    config_path = "."
    config = Config(config_path=config_path)
    log = getLogger(__name__)

    while(True):

        tcm = TrashcanMon(from_config=config)

        try:
            results = tcm.start_test()
        except Exception as err:
            log.critical(str(err))
        else:
            log.debug(results)

        log.info("Testing complete, results ready for transport.")
        log.debug(f"Pausing testing for { config.sleep_time }")
        sleep(config.sleep_time)


