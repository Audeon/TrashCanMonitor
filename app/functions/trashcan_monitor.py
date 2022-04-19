import json
import requests
from requests.exceptions import ConnectionError, Timeout, HTTPError
from logging import getLogger, Logger
from app.functions import ConfigApp

__all__ = ['TrashcanMonitor']


class TrashcanMonitor:
    """
        TrashcanMonitor is used to gather information about the Home Internet Device.
    """
    config = None
    log: Logger  = getLogger(__name__)
    target_gateway_url: str = "http://192.168.12.1/"
    radio_info_url: str = target_gateway_url + "fastmile_radio_status_web_app.cgi"
    inet_stats_url: str = target_gateway_url + "statistics_status_web_app.cgi"
    lan_stats_url: str = target_gateway_url + "lan_status_web_app.cgi"
    request_timeout: int = 8
    header = {'Accept': 'application/json',
              'Cache-Control': 'no-cache',
              'Connection': 'close',
              'User-Agent': 'TrashcanMonitor'}

    @classmethod
    def from_config(cls, config: ConfigApp):
        cls.log.debug(f"Starting {__name__} from config.")
        cls.config = config
        cls.target_gateway_url = config.target_gateway_url
        return super().__new__(cls)

    def check_gateway_url(self) -> bool:
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

    def get_radio_data(self) -> dict:
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

    def get_inet_data(self) -> dict:
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

    def get_lanstat_data(self) -> dict:
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


    def start_test(self) -> dict:

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
            "gateway_check": False
        }

        # Check Connection to gateway,
        try:
            self.check_gateway_url()
        except ConnectionError as err:
            self.log.critical(f"Could not establish connection to gateway: {str(err)}")
            raise ConnectionError(err)
        except Timeout as err:
            self.log.critical(f"Connection Timed out while trying to access gateway: {str(err)}")
            raise Timeout(err)
        except HTTPError as err:
            self.log.critical(f"Gateway responded with a invalid status code: {str(err)}")
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
