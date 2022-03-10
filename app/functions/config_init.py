import logging
import json
import os
from os import environ, path
from pathlib import Path
from datetime import datetime, timezone, timedelta

class Config():

    """
        This configuration file handles passing data about how the application should run through and provides shared
         data across the differnt modules. It also makes configuring it to work with docker-compose and other containers
         easier.

         Unless noted all parameters have the ability to be set using a config.json file, a env variable or a kwarg.
         Most variables also have a set defaults geared towards running it in docker using the supplied docker compose
         file. The prefrence for loading goes kwarg > env-var > config.json > default.
         for example:
            Given this configuration of myconfig.json
            myconfig.json:
                { sleep_time = 20 }

            Then initializing the configuration like this:
            config = config(sleep_time=10, config_path="./myconfig.json")

            print(config.sleep_time)
            10

        :param no_config_file: Use this if you do not want to use any configuration files, either accepting defaults or
            using kwargs, defaults to False
        :type no_config_file: Boolean, required

        Config
        ------
        :param config_path: This is the location of the config.json file. This path must be set via env variable
            or kwarg else, defaults to /code/config/config.json
        :type config_path: String, optional

        Logging
        -------
        This section lays out the parameters required for the logging part of this application.

        :param log_level: The loglevel as described by python logging: https://docs.python.org/3/library/logging.html#logging-levels.
            defaults to 10 (debug)
        :type log_level: int, optional

        :param log_path: The path the logs are stored to.,
            defaults to ./logs/
        :type log_path: String, optional

        :param log_format: The format the logs are written in.
            defaults to '%(asctime)s %(name)s %(levelname)s %(message)s'
        :type log_format: String, optional

        :param log_encoding: The encoding used in the logging.
            defaults to utf-8
        :type log_encoding: String, optional

        :param log2console: Setting this to false will prevent the logs outputting to the console stream.
            defaults to True
        :type log2console: Boolean, optional

        Application Specific
        -------
        This section lays out the parameters required for the functioning of the application.

        :param sleep_time: The sleep_time between each main loop execution, in seconds.
            defaults to 60
        :type sleep_time: int, optional

        :param trashcanmon_sleep_time: Overrides the sleep_time between each main loop execution, this allows fine tuning
            of the main loop execution if there are multiple modules using sleep_time.
        :type trashcanmon_sleep_time: int, optional

        :param target_gateway_url: The url to the management address of the modem,
            defaults to 'http://192.168.12.1'
        :type target_gateway_url: String, optional

        :param transport: This is the transport layer used for the application.
            options are ['mongodb', 'sqlalchemy', 'csv_file'],
            defaults to 'mongodb'
        :type transport: String, optional

        Mongodb Transport Specific
        -------
        This section deals with parameters required for connection and storing information into a mongodb.

        :param mongodb_uri: The URI String to the mongodb that is to be used,
            defaults to 'mongodb://tc_usr:trashcan@tcmongodb:27017/tcresults'
        :type mongodb_uri: String, optional

        :param results_db: The database that the results collection should reside in,
            defaults to 'tcresults'
        :type results_db: String, optional

        :param db_collection: The collection in the database results should be stored in,
            defaults to 'results'
        :type db_collection: String, optional

    """

    CONTAINER_NAME = "TrashcanMonitor"
    config_path = "./config.json"


    log_level = 10
    log_path = "./logs/"
    log_format = '%(asctime)s %(name)s %(levelname)s %(message)s'
    log_encoding = 'utf-8'
    log2console = True

    sleep_time = 60
    target_gateway_url = "http://192.168.12.1"
    transport = "mongodb"

    # Mongo transport defaults.
    mongodb_uri = "mongodb://tc_usr:trashcan@tcmongodb:27017/tcresults"
    results_db = "tcresults"
    db_collection = "results"

    def __init__(self, no_config_file=False, **kwargs):

        config = {}
        # Set up configuration variables.
        if not no_config_file:

            # Configuration path from env or kwag.
            if environ.get('config_path'):
                self.config_path = environ.get('config_path')
            if 'config_path' in kwargs:
                self.config_path = kwargs.get('config_path')

            print((self.config_path))
            try:
                with open(Path(self.config_path), "r") as f:
                    config = json.load(f)
            except Exception as err:
                print(f"Container Name: { self.CONTAINER_NAME }")
                print(f"Config Path: { str(Path(self.config_path)) }")
                print(str(err))
                raise Exception(str(err))

        # Log Level
        if 'log_level' in config:
            self.log_level = int(config['log_level'])
        if environ.get('log_level'):
            self.log_level = int(environ.get('log_level'))
        if 'log_level' in kwargs:
            self.log_level = int(kwargs.get('log_level'))

        # Log path preference - KWARGS > ENV > CONFIG
        if 'log_path' in config:
            self.log_path = config['log_path']
        if environ.get('LOG_PATH'):
            self.log_path = environ.get('LOG_PATH')
        if 'log_path' in kwargs:
            self.log_path = kwargs.get('log_path')

        # Log Format
        if 'log_format' in config:
            self.log_format = config['log_format']
        if environ.get('log_format'):
            self.log_format = environ.get('log_format')
        if 'log_format' in kwargs:
            self.log_format = kwargs.get('log_format')

        # Log Encoding
        if 'log_encoding' in config:
            self.log_encoding = config['log_encoding']
        if environ.get('log_encoding'):
            self.log_encoding = environ.get('log_encoding')
        if 'log_encoding' in kwargs:
            self.log_encoding = kwargs.get('log_encoding')

        # Log Console Stream
        if 'log2console' in config:
            self.log2console = config['log2console']
        if environ.get('log2console'):
            self.log2console = environ.get('log2console')
        if 'log2console' in kwargs:
            self.log2console = kwargs.get('log2console')

        # Sleep Time.
        if 'sleep_time' in config:
            self.sleep_time = int(config['sleep_time'])
        if environ.get('sleep_time'):
            self.sleep_time = int(environ.get('sleep_time'))
        if 'sleep_time' in kwargs:
            self.sleep_time = int(kwargs.get('sleep_time'))

        # This will overide the global sleep_time.
        if 'trashcanmon_sleep_time' in config:
            self.sleep_time = int(config['trashcanmon_sleep_time'])
        if environ.get('trashcanmon_sleep_time'):
            self.sleep_time = int(environ.get('trashcanmon_sleep_time'))
        if 'trashcanmon_sleep_time' in kwargs:
            self.sleep_time = int(kwargs.get('trashcanmon_sleep_time'))

        # Target Gateway url
        if 'target_gateway_url' in config:
            self.target_gateway_url = config['target_gateway_url']
        if environ.get('target_gateway_url'):
            self.target_gateway_url = environ.get('target_gateway_url')
        if 'sleep_time' in kwargs:
            self.target_gateway_url = kwargs.get('target_gateway_url')

        # Pick which transport to use
        if 'transport' in config:
            self.transport = config['transport']
        if environ.get('transport'):
            self.transport = environ.get('transport')
        if 'transport' in kwargs:
            self.transport = kwargs.get('transport')

        ###
        # Monogo Transport Configurations
        ###

        # Mongo Connection URI.
        if 'mongodb_uri' in config:
            self.mongodb_uri = config['mongodb_uri']
        if environ.get('mongodb_uri'):
            self.mongodb_uri = environ.get('mongodb_uri')
        if 'mongodb_uri' in kwargs:
            self.mongodb_uri = kwargs.get('mongodb_uri')

        # DB Where results are stored
        if 'results_db' in config:
            self.results_db = config['results_db']
        if environ.get('results_db'):
            self.results_db = environ.get('results_db')
        if 'results_db' in kwargs:
            self.results_db = kwargs.get('results_db')

        # Collection where results are stored
        if 'db_collection' in config:
            self.db_collection = config['db_collection']
        if environ.get('db_collection'):
            self.db_collection = environ.get('db_collection')
        if 'db_collection' in kwargs:
            self.db_collection = kwargs.get('db_collection')

        self.start_new_log()


        logging.debug(f"config.json: {str(config)}")


    def start_new_log(self):
        # Logging basic setup.
        # self.log_reset_time = datetime.now(tz=timezone.utc) + timedelta(**self.log_reset_timer)
        self.log_path = path.abspath(self.log_path)
        log_name = f"{datetime.now(timezone.utc).strftime('%d%m%Y-%H%M%S')}.log"
        log_name = path.join(self.log_path, log_name)
        if not path.isdir(self.log_path):
            os.mkdir(self.log_path)

        logging.basicConfig(
            filename=log_name,
            filemode='w',
            level=self.log_level,
            format=self.log_format
        )

        # This is for ouputing to the console
        if self.log2console:
            console = logging.StreamHandler()
            console.setFormatter(logging.Formatter(self.log_format))
            console.setLevel(self.log_level)
            logging.getLogger('').addHandler(console)

        logging.info("LOG START")
        logging.info(f"LOG_LEVEL: {self.log_level}")
        logging.info(f"LOG_NAME: {log_name}")