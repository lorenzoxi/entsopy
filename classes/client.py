from datetime import timedelta
import requests
from requests.adapters import HTTPAdapter
import urllib3
from dataclasses import dataclass
from classes.request import RequestData
from utils.date import split_interval, get_interval, date_diff
import os


@dataclass
class HttpsClient:
    """Class for sending https call."""

    _client: requests.Session
    _retry_policy: urllib3.Retry
    _adapter: HTTPAdapter
    _security_token = os.getenv("SECURITY_TOKEN")
    _api_endpoint = os.getenv("API_ENDPOINT")

    def __init__(self):
        self._client = requests.Session()
        self._retry_policy = urllib3.Retry(connect=15, backoff_factor=0.5, total=10)
        self._adapter = HTTPAdapter(max_retries=self._retry_policy)
        self._client.mount("http://", self._adapter)
        self._client.mount("https://", self._adapter)
        self.header = {
            "Content-Type": "application/xml",
            "SECURITY_TOKEN": self._security_token,
        }

    @property
    def security_token(self) -> str:
        """Get the current security_token."""
        return self._security_token

    @security_token.setter
    def security_token(self, value):
        """Set the security_token as value."""
        self._security_token = value

    @property
    def api_endpoint(self) -> str:
        """Get the current api_endpoint."""
        return self._api_endpoint

    @api_endpoint.setter
    def api_endpoint(self, value: str):
        """Set the api_endpoint as value."""
        self._api_endpoint = value

    def get_request(self, params: dict):
        params["securityToken"] = self._security_token
        response = self._client.get(url=self._api_endpoint, params=params)
        return [response.content]

    def multiple_requests(self, request: RequestData) -> list:
        request.params["securityToken"] = self._security_token
        res = []
        dates = split_interval(interval=request.params["TimeInterval"])
        dates_diff = date_diff(dates["begin"], dates["end"])
        start_date = dates["begin"]
        end_date = dates["end"]
        delta = timedelta(days=request.range_limit)

        if dates_diff > delta.days:
            count = 0
            while start_date < end_date:
                interval_starting_date = start_date
                interval_ending_date = start_date + delta
                if interval_ending_date > end_date:
                    interval_ending_date = end_date
                for i in request.areas:
                    request.set_custom_param(value=i["code"])
                    tmp_params = request.params
                    tmp_time_interval = get_interval(
                        interval_starting_date, interval_ending_date
                    )
                    # print(
                    #     f"{count} - {start_date} - {end_date} || interval: "
                    #     + tmp_time_interval
                    # )
                    tmp_params["TimeInterval"] = tmp_time_interval
                    response = self._client.get(
                        url=self.api_endpoint, params=tmp_params
                    )
                    res.append(response.content)

                start_date += delta
                count += 1
            return res
        else:
            for i in request.areas:
                request.set_custom_param(value=i["code"])
                response = self._client.get(
                    url=self.api_endpoint, params=request.params
                )
                res.append(response.content)
            return res

    def get_multiple_requests_load(
        self, list: list, params: dict, article: int, delta: int = 365
    ):
        data = self.multiple_requests_each_area(
            client=self,
            list=list,
            params=params,
            area_param="OutBiddingZone_Domain",
        )
        return data
