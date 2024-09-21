"""
    CUSTOM READERS MODULE FOR GOOGLE SEARCH CONSOLE
"""
# pylint: disable=no-member,too-many-locals,broad-except,too-few-public-methods,arguments-differ,too-many-arguments
import os
from typing import Any, List, Dict, Union
from googleapiclient import discovery
from googleapiclient.errors import HttpError
from google.oauth2 import service_account

from sdc_dp_helpers.base_readers import BaseReader

from sdc_dp_helpers.api_utilities.date_managers import date_range_iterator
from sdc_dp_helpers.api_utilities.retry_managers import retry_handler, request_handler
from sdc_dp_helpers.api_utilities.file_managers import load_file

class GSCQuotaException(Exception):
    """Class for GSC Quota Exception"""

class HttpErrorException(Exception):
    """Class to raise other Http Errors"""


class GoogleSearchConsoleReader(BaseReader):
    """
    Google Search Console Reader v1
    """

    def __init__(self, creds_filepath: str, config_filepath: str):
        self.secrets: Dict[Any, Any] = load_file(creds_filepath)
        self.config: Dict[Any, Any] = load_file(config_filepath)
        self.service = self._get_auth()
        self.success: List[bool] = []

    def _get_auth(self):
        """
        Get our credentials initialised above and use those to get client

        """
        credentials = service_account.Credentials.from_service_account_info(
            info=self.secrets,
            scopes=["https://www.googleapis.com/auth/webmasters.readonly"],
        )
        service = discovery.build(
            serviceName="searchconsole", version="v1", credentials=credentials
        )
        return service

    def _normalize(
        self, response: Dict[Any, Any], date, query_dim_list: List[str],site_url
    ) -> List[Dict[str, Any]]:
        """Method to normalize data into a flat structure and add metadata

        Args:
            response (Dict[Any, Any]): api response in dictionary format
            query_dim_list (List[str]): Zero or more dimensions to group results.

        Returns:
            Dict[str, Any]: flattened data dictionary
        """

        # added additional data that the api does not provide
        dataset_list: List[Dict[str, Any]] = []
        for _, row in enumerate(response["rows"]):
            row_dataset: Dict[str, Any] = {}
            if "searchAppearance" in query_dim_list:
                row_dataset = {
                    "date": date,
                    "site_url": site_url,
                    # keeping original search_type name for reporting
                    "search_type": self.config.get("search_type"),
                }
            else:
                row_dataset = {
                    "site_url": site_url,
                    # keeping original search_type name for reporting
                    "search_type": self.config.get("search_type"),
                }

            # get dimension data keys and values
            row_dataset.update(
                dict(
                    zip(
                        query_dim_list,
                        row.get("keys", []),
                    )
                )
            )

            # get metrics data
            for metric in self.config.get("metrics", []):
                row_dataset[metric] = row.get(metric)

            dataset_list.append(row_dataset)

        return dataset_list

    @request_handler(
        wait=float(os.environ.get("API_WAIT_TIME", 5)),
        backoff_factor=0.01,
        backoff_method='random'
    )
    @retry_handler(exceptions=GSCQuotaException,
                   total_tries=3,
                   initial_wait=61,
                   backoff_factor=2
                )
    @retry_handler(exceptions=HttpErrorException,
                   total_tries=3,
                   initial_wait=61,
                   backoff_factor=2
                )
    def _query_handler(
        self,
        start_date: str,
        end_date: str,
        start_row: int,
        site_url: str,
        query_dim_list: List[str]
    ) -> Union[Dict[Any, Any], None]:
        """Function to make api call

        Args:
            start_date (str): start of range inclusive 'YYYY-MM-DD'
            end_date (str): end of range inclusive 'YYYY-mm-dd'
            query_dim_list (List[str]): Zero or more dimensions to group results.

        Returns:
            Dict[Any, Any]: dictionary of response
        """
        response: Union[Dict[Any, Any], None] = None
        try:
            request = {
                "startDate": start_date,
                "endDate": end_date,
                "dimensions": query_dim_list,
                "metrics": self.config.get("metrics"),
                "searchType": self.config.get("search_type"),
                "rowLimit": self.config.get("row_limit", 25000),
                "startRow": start_row * self.config.get("row_limit", 25000),
                "aggregationType": self.config.get("aggregation_type", "auto"),
                "dimensionFilterGroups": self.config.get("dimension_filter_groups", []),
                "dataState": self.config.get("data_state", "final"),
            }
            response = (
                self.service.searchanalytics()
                .query(siteUrl=site_url, body=request)
                .execute()
            )

        except HttpError as err:
            status_code = err.resp.status
            reason = err._get_reason()

            if status_code == 403:
                raise GSCQuotaException(
                    f"GSC Quota Reached. Status code: {status_code}, Reason: {reason}"
                )from err

            raise HttpErrorException(
                f"Unexpected error Status code : {status_code}, Reason : {reason}"
                )from err

        return response

    def run_query(self):
        """Main Class Method"""
        # site_list = self.service.sites().list().execute()
        # print(site_list)
        for dimension in self.config["dimensions"]:
            for start_date, end_date in date_range_iterator(
                start_date=self.config["start_date"],
                end_date=self.config["end_date"],
                interval=self.config.get("interval", "day"),
                end_inclusive=True,
                time_format="%Y-%m-%d",
            ):
                if dimension == 'searchAppearance':
                    query_dim_list: List[str] = list(dict.fromkeys([dimension]))
                else:
                    query_dim_list: List[str] = list(dict.fromkeys(["date", dimension]))

                for brand, site_url in self.config.get("site_urls").items():
                    start_row: int = 0
                    dataset: List[Dict[str, Any]] = []
                    while True:
                        response = self._query_handler(
                            start_date=start_date,
                            end_date=end_date,
                            start_row=start_row,
                            site_url=site_url,
                            query_dim_list=query_dim_list,
                        )

                        if response is None:
                            self.not_success()
                            print(
                                f"response is 'None' for date dimension row: "
                                f"'{start_date}' '{dimension}' '{start_row}'"
                            )
                            break
                        if "rows" not in response:
                            self.not_success()
                            print(
                                f"No more data for date dimension row: "
                                f"'{start_date}' '{dimension}' '{start_row}'"
                            )
                            break

                        self.is_success()
                        normalised_dataset = self._normalize(
                            response,
                            start_date,
                            query_dim_list,
                            site_url
                        )
                        dataset.extend(normalised_dataset)
                        start_row += 1

                        yield {
                            "date": start_date.replace("-", ""),
                            "dimension": dimension,
                            "brand" : brand,
                            "data": dataset
                        }
