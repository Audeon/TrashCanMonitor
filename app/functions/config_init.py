import logging
import json
from os import environ, path
from datetime import datetime, timezone

class Config():
    PROBE_NAME="default"
    CONTAINER_NAME = "TrashcanMonitor"
    CONFIG_PATH = "/code/config"

    log_level = 10
    log_path = "./logs/"
    log_format = '%(asctime)s %(name)s %(levelname)s %(message)s'
    log_encoding = 'utf-8'

    sleep_time = 60
    target_gateway_url = "http://192.168.12.1"

    def __init__(self, **kwargs):
        # Getting Configuration path from env or kwag.
        if environ.get('CONFIG_PATH'):
            self.CONFIG_PATH = environ.get('CONFIG_PATH')
        if 'config_path' in kwargs:
            self.CONFIG_PATH = kwargs.get('config_path')


        # Set up configuration variables.
        try:
            with open(path.abspath(path.join(self.CONFIG_PATH, 'config.json')), "r") as f:
                config = json.load(f)
        except Exception as err:
            print(f"Probe Name: { self.PROBE_NAME }")
            print(f"Container Name: { self.CONTAINER_NAME }")
            print(f"Config Path: { str(path.abspath(path.join(self.CONFIG_PATH, 'config.json'))) }")
            print(str(err))
            raise Exception(str(err))

        # This section has to do with getting logging data from the config ready.
        if 'log_level' in config:
            self.log_level = int(config['log_level'])

        # Log path preference - KWARGS > ENV > CONFIG
        if 'log_path' in config:
            self.log_path = config['log_path']

        if environ.get('LOG_PATH'):
            self.log_path = environ.get('LOG_PATH')

        if 'log_path' in kwargs:
            self.log_path = kwargs.get('log_path')

        if 'log_format' in config:
            self.log_format = config['log_format']

        if 'log_encoding' in config:
            self.log_encoding = config['log_encoding']

        # Getting furthur variables setup or defaulted from the config file.
        if 'trashcanmon_sleeptime' in config:
            self.sleep_time = int(config['trashcanmon_sleeptime'])

        if 'target_gateway_url' in config:
            self.target_gateway_url = config['target_gateway_url']

        if 'target_gateway_url' in kwargs:
            self.target_gateway_url = kwargs.get('target_gateway_url')

        self.start_new_log()


        logging.debug(f"config.json: {str(config)}")

    def start_new_log(self):
        # Logging basic setup.
        self.log_path = path.abspath(self.log_path)
        log_name = f"{datetime.now(timezone.utc).strftime('%d%m%Y-%H%M%S')}.log"
        log_name = path.join(self.log_path, log_name)

        logging.basicConfig(
            filename=log_name,
            filemode='w',
            level=self.log_level,
            format=self.log_format
        )

        # This is for ouputing to the console
        console = logging.StreamHandler()
        console.setFormatter(logging.Formatter(self.log_format))
        console.setLevel(self.log_level)
        logging.getLogger('').addHandler(console)

        logging.info("LOG START")
        logging.info(f"LOG_LEVEL: {self.log_level}")
        logging.info(f"LOG_NAME: {log_name}")