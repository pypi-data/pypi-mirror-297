import urllib.parse
from datetime import datetime
import requests
from sdc_dp_helpers.api_utilities.file_managers import load_file
from sdc_dp_helpers.api_utilities.retry_managers import retry_handler


class WebVitalReader:
    """
    Custom FTP Reader
    """

    def __init__(self, creds_file, config_file):
        self._creds: dict = load_file(creds_file, "yml")

        self.config = load_file(config_file)

    @retry_handler(exceptions=TimeoutError, total_tries=5, initial_wait=900)
    def _query_handler(self, venture: str, venture_url: str) -> dict:
        """
        Fetch json from API
        """
        url = self.build_url(venture_url=venture_url)

        headers = {
            "Authorization": self._creds.get("bearer_token")
        }

        ts_now = int(datetime.timestamp(datetime.now()))
        print("Getting data for: ", venture)

        return {
            "response": requests.get(url=url, headers=headers, timeout=30).json(),
            "venture": venture,
            "ts_now": ts_now
        }

    def build_url(self, venture_url) -> str:

        endpoint = self.config.get("endpoint")
        use_case = self.config.get("use_case")

        params_dict = self.config.get("url_params", "")
        params = urllib.parse.urlencode(params_dict)

        url = f"{endpoint}/{use_case}/{venture_url}"

        return url + f"?{params}" if params else url

    def run_query(self) -> dict:

        for venture, url in self.config.get("ventures").items():
            yield self._query_handler(venture=venture, venture_url=url)
