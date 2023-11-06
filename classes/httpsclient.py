from datetime import timedelta
import requests
from requests.adapters import HTTPAdapter
import urllib3
from dataclasses import dataclass
from classes.request import RequestData
from classes.request import RequestData
from utils.date import split_interval, get_interval, date_diff
import os
from dotenv import load_dotenv

load_dotenv()


@dataclass
class HttpsClient:
    """Class for sending https call."""

    client: requests.Session
    retry_policy: urllib3.Retry
    adapter: HTTPAdapter
    security_token = os.getenv("SECURITY_TOKEN")
    api_endpoint = os.getenv("API_ENDPOINT")

    def __init__(self):
        self.client = requests.Session()
        self.retry_policy = urllib3.Retry(connect=15, backoff_factor=0.5, total=10)
        self.adapter = HTTPAdapter(max_retries=self.retry_policy)
        self.client.mount("http://", self.adapter)
        self.client.mount("https://", self.adapter)
        self.header = {
            "Content-Type": "application/xml",
            "SECURITY_TOKEN": self.security_token,
        }

    def get_request(self, params: dict):
        params["securityToken"] = self.security_token
        response = self.client.get(url=self.api_endpoint, params=params)
        return [response.content]

    def multiple_requests(self, request: RequestData) -> list:
        request.params["securityToken"] = self.security_token
        res = []
        start_date, end_date = split_interval(interval=request.params["TimeInterval"])
        dates_diff = date_diff(start_date, end_date)
        delta = timedelta(days=request.article.range_limit)

        if dates_diff > delta.days:
            # count = 0
            while start_date < end_date:
                interval_starting_date = start_date
                interval_ending_date = start_date + delta
                if interval_ending_date > end_date:
                    interval_ending_date = end_date
                for i in request.areas:
                    request.set_custom_attribute_by_domain(value=i)

                    tmp_time_interval = get_interval(
                        interval_starting_date, interval_ending_date
                    )
                    request.set_custom_attribute("TimeInterval", tmp_time_interval)

                    print(request.params)
                    response = self.client.get(
                        url=self.api_endpoint, params=request.params
                    )
                    res.append(response.content)

                start_date += delta

            return res
        else:
            for i in request.areas:
                request.set_custom_attribute_by_domain(i)
                print(request.params)
                response = self.client.get(url=self.api_endpoint, params=request.params)
                res.append(response.content)

        return res
