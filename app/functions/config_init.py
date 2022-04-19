import logging
import json
from os import environ, path, mkdir
from pathlib import Path
from datetime import datetime, timezone
from app.models import ConfigIgnoreExtra

__all__ = ["ConfigApp"]


class ConfigApp:

    """
    This is designed to pull in all the configuration settings for the application. These settings can be stored in env
    variables, or in a json configuration file.
    """

    def __init__(self, **kwargs):
        """
            This initializes configuration variables based on kwargs.
        """
        for key, value in ConfigIgnoreExtra.parse_obj(kwargs):
            setattr(self, key, value)

        self.start_new_log()

    @classmethod
    def from_config_file(cls, config_path: str):
        """
            This initializes all the configuration variables from a config file.

            :param config_path: str, The file path of the configuration file to be used.
        """
        if not isinstance(config_path, str):
            raise ValueError("Path must be a string. ")
        else:
            config_path = Path(config_path)

        if not config_path.exists():
            raise ValueError(f"Configuration file missing. Please check path.")
        if not config_path.suffix == ".json":
            raise ValueError(f"Expecting: .json, Actual: { config_path.suffix }")

        with open(config_path, "r") as f:
            config_file = json.load(f)

        if "trashcan_sleep_time" in config_file:
            config_file['sleep_time'] = config_file['trashcan_sleep_time']
            del config_file['trashcan_sleep_time']

        try:
            config_parsed = ConfigIgnoreExtra.parse_obj(config_file)
        except Exception as err:
            raise ValueError(str(err))

        for key, value in config_parsed:
            setattr(cls, key, value)

        cls.start_new_log(cls)
        return super().__new__(cls)

    @classmethod
    def from_env_vars(cls):
        """
            This initializes all the configuration variables from environmental variables.
        """
        env_data = {str(key).lower(): value for key, value in environ.items()}

        # This will move the potential trashcan sleep time variable to the normal sleep time variable.
        if env_data['trashcan_sleep_time']:
            env_data['sleep_time'] = env_data['trashcan_sleep_time']
            del env_data['trashcan_sleep_time']

        for key, value in ConfigIgnoreExtra.parse_obj(env_data):
            setattr(cls, key, value)
        cls.start_new_log(cls)
        return super().__new__(cls)

    def start_new_log(self) -> None:
        # Logging basic setup.
        self.log_path = path.abspath(self.log_path)
        log_name = f"{datetime.now(timezone.utc).strftime('%d%m%Y')}.log"
        log_name = path.join(self.log_path, log_name)
        if not path.isdir(self.log_path):
            mkdir(self.log_path)

        logging.basicConfig(
            filename=log_name,
            filemode='a',
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
