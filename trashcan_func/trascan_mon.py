import json

import requests
from requests.exceptions import ConnectionError, Timeout, HTTPError
from logging import getLogger
from trashcan_func.config_init import Config

class trashcan_mon:
    """
        Trashcan_mon is used to gather information about the Home Internet Device.
    """
    config = None
    log = None

    target_gateway_url = "http://192.168.12.1/"
    radio_info_url = target_gateway_url + "fastmile_radio_status_web_app.cgi"
    inet_stats_url = target_gateway_url + "statistics_status_web_app.cgi"
    request_timeout = 8
    header = {'Accept': 'application/json',
               'Cache-Control': 'no-cache',
               'Connection': 'close',
               'User-Agent': 'TrashCanMonitor'}

    def __init__(self, **kwargs):
        """
        Construct a new trashcan_mon object. This can be initialized alone with its built in class defaults, or using
        the Config() to gather a configuration file from the container volume and use its variables.

        Keyword Args:
            :param from_config: type: class: This should be an initialized Config() object.
            :param target_gateway: type: Str: default: http://192.168.12.1: URL String for home internet modem managment page..
            :param request_timeout: type: Int: default: 30: time out for requests in seconds.
                :exception: TypeError: request_timeout must be an integer.

        """

        self.log = getLogger(__name__)

        if "from_config" in kwargs:
            # TODO: Add info to pull out of config
            if isinstance(kwargs.get("from_config"), Config):
                self.config = kwargs.get("from_config")

        if "target_gateway_url" in kwargs:
            self.target_gateway_url = kwargs.get("target_gateway_url")

        if "request_timeout" in kwargs:
            if isinstance(kwargs.get("request_timeout"), int):
                self.request_timeout = kwargs.get("request_timeout")
            else:
                raise TypeError("request_timeout must be an integer.")

        self.log.info(f"{__name__} initialized and ready to test: {self.target_gateway_url}")

    def check_gateway_url(self):
        """
        This make a request to the target_gateway_url to determine if connection is possible
        :return: True on successful request
        :exception: ConnectionError:
        :exception: Timeout
        """
        header = {
            'Accept': 'text/html',
            'Cache-Control': 'no-cache',
            'Connection': 'close',
            'User-Agent': 'TrashCanMonitor'
        }
        try:
            requests.get(self.target_gateway_url, timeout=self.request_timeout, headers=header)
        except ConnectionError as err:
            raise Exception(err)
        except Timeout as err:
            raise Exception(err)
        except HTTPError as err:
            raise Exception(err)
        else:
            return True
        return False

    def get_radio_data(self):
        """
        This will collect data related to the hint modems radio, and will return a dict of that information.
        :return: dict: radio_information
        """

        try:
            data = requests.get(self.radio_info_url, timeout=self.request_timeout, headers=self.header)
        except ConnectionError as err:
            raise Exception(err)
        except Timeout as err:
            raise Exception(err)
        except HTTPError as err:
            raise Exception(err)
        else:
            test = json.loads(data.text)
            testb = data.text
            print(test['apn_cfg'])


        return data

    def start_test(self):
        # Check Connection to gateway,
        try:
            self.check_gateway_url()
        except Exception as err:
            self.log.critical(f"Could not establish connection to gateway: { str(err) }")
            raise Exception(err)

        # Get Radio Info and store in dictionary object for parsing late
        print(self.radio_info_url)

        # Get Web Usage



if __name__ == "__main__":
    tcm = trashcan_mon()
    test = tcm.get_radio_data()