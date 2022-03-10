import json
import requests
from requests.exceptions import ConnectionError, Timeout, HTTPError
from logging import getLogger
from .config_init import Config

class TrashcanMon:
    """
        TrashcanMon is used to gather information about the Home Internet Device.
    """
    config = None
    log = None
    container_id = "tcm"
    target_gateway_url = "http://192.168.12.1/"
    radio_info_url = target_gateway_url + "fastmile_radio_status_web_app.cgi"
    inet_stats_url = target_gateway_url + "statistics_status_web_app.cgi"
    lan_stats_url = target_gateway_url + "lan_status_web_app.cgi"
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

                if self.config.target_gateway_url:
                    self.target_gateway_url = self.config.target_gateway_url

                if self.config.container_id:
                    self.container_id = self.config.container_id

                # if self.config.request_timeout:
                #     if isinstance(self.config.request_timeout, int):
                #         self.request_timeout = self.config.request_timeout

        # kwargs will take priority over configuration and env
        if "target_gateway_url" in kwargs:
            self.target_gateway_url = kwargs.get("target_gateway_url")
        if "container_id" in kwargs:
            self.container_id = kwargs.get("container_id")


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
            raise ConnectionError(err)
        except Timeout as err:
            raise Timeout(err)
        except HTTPError as err:
            raise HTTPError(err)
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
            raise ConnectionError(err)
        except Timeout as err:
            raise Timeout(err)
        except HTTPError as err:
            raise HTTPError(err)
        else:
            return json.loads(data.text)

    def get_inet_data(self):
        """
        This will collect data related to the modems interface statistics , and will return a dict of that information.
        :return: dict: interface_statistics
        """

        try:
            interface_statistics = requests.get(self.inet_stats_url, timeout=self.request_timeout, headers=self.header)
        except ConnectionError as err:
            raise ConnectionError(err)
        except Timeout as err:
            raise Timeout(err)
        except HTTPError as err:
            raise HTTPError(err)
        else:
            return json.loads(interface_statistics.text)

    def get_lanstat_data(self):
        """
        This will collect data related to the modems lan status, and will return a dict of that information.
        :return: dict: lan_status
        """

        try:
            lan_status = requests.get(self.inet_stats_url, timeout=self.request_timeout, headers=self.header)
        except ConnectionError as err:
            raise ConnectionError(err)
        except Timeout as err:
            raise Timeout(err)
        except HTTPError as err:
            raise HTTPError(err)
        else:
            return json.loads(lan_status.text)

    def start_test(self):

        """
        This will check the connection to the gateway can be established, and then proceeds to collect information from
        each of the modems api end points.
        :return: Returns a dict of ResultsSchema and a time stamp. Using the following schema.
            {
                "timestamp" : datetime.now(tz=utc)
                "gateway_check" : True/False,
                "radio_raw_data" : radio_data_results,
                "interface_data_raw" : interface_statistics_results
                "lan_status_raw" : lan_status_results
            }
        """

        results = {
            "container_id": self.container_id,
            "gateway_check" : False
        }

        # Check Connection to gateway,
        try:
            self.check_gateway_url()
        except ConnectionError as err:
            self.log.critical(f"Could not establish connection to gateway: { str(err) }")
            raise ConnectionError(err)
        except Timeout as err:
            self.log.critical(f"Connection Timed out while trying to access gateway: { str(err) }")
            raise Timeout(err)
        except HTTPError as err:
            self.log.critical(f"Gateway responded with a invalid status code: { str(err) }")
            raise HTTPError(err)
        else:
            results["gateway_check"] = True

        # Get Radio Info
        try:
            radio_data = self.get_radio_data()
        except ConnectionError as err:
            self.log.critical(f"Could not access radio information: {str(err)}")
            raise ConnectionError(err)
        except Timeout as err:
            self.log.critical(f"Connection for radio information timed out: {str(err)}")
            raise Timeout(err)
        except HTTPError as err:
            self.log.critical(f"Request for radio information returned an invalid status code: {str(err)}")
            raise HTTPError(err)
        else:
            results['radio_raw_data'] = radio_data

        # Get Interface Statistics
        try:
            interface_data = self.get_inet_data()
        except ConnectionError as err:
            self.log.critical(f"Could not access interface information: {str(err)}")
            raise ConnectionError(err)
        except Timeout as err:
            self.log.critical(f"Connection for interface information timed out: {str(err)}")
            raise Timeout(err)
        except HTTPError as err:
            self.log.critical(f"Request for interface information returned an invalid status code: {str(err)}")
            raise HTTPError(err)
        else:
            results['interface_data_raw'] = interface_data

        # Get Web Usage
        try:
            lan_status = self.get_lanstat_data()
        except ConnectionError as err:
            self.log.critical(f"Could not access lan status information: {str(err)}")
            raise ConnectionError(err)
        except Timeout as err:
            self.log.critical(f"Connection for lan status information timed out: {str(err)}")
            raise Timeout(err)
        except HTTPError as err:
            self.log.critical(f"Request for lan status information returned an invalid status code: {str(err)}")
            raise HTTPError(err)
        else:
            results['lan_status_raw'] = lan_status

        return results


if __name__ == "__main__":
    tcm = TrashcanMon()

    results = tcm.start_test()
    print(results)