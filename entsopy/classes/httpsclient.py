import datetime
import requests
from requests.adapters import HTTPAdapter
import urllib3
from dataclasses import dataclass
from entsopy.classes.request import RequestData
from entsopy.classes.request import RequestData
from entsopy.utils.const import API_ENDPOINT
from entsopy.logger.logger import LOGGER
from entsopy.utils.date import split_interval, get_interval, date_diff
from entsopy.utils.utils import get_time_interval, split_in_intervals_load, split_in_intervals_generation, split_to_intervals


@dataclass
class HttpsClient:
    """
    A class representing an HTTPS client.

    Attributes:
        client (requests.Session): The HTTP client session.
        retry_policy (urllib3.Retry): The retry policy for HTTP requests.
        adapter (HTTPAdapter): The HTTP adapter for handling retries.
        security_token (str): The security token for authentication.
        api_endpoint (str): The API endpoint URL.

    Methods:
        __init__(self, security_token: str): Initializes the HttpsClient object.
        get_request(self, params: dict): Sends a GET request to the API endpoint.
        multiple_requests(self, request: RequestData) -> list: Sends multiple requests to the API endpoint.

    """

    client: requests.Session
    retry_policy: urllib3.Retry
    adapter: HTTPAdapter
    security_token: str
    api_endpoint = API_ENDPOINT

    def __init__(self, security_token: str):
        """
        Initializes the HttpsClient object.

        Args:
            security_token (str): The security token for authentication.

        """
        self.security_token = security_token
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
        """
        Sends a GET request to the API endpoint.

        Args:
            params (dict): The parameters for the request.

        Returns:
            list: The response content.

        """
        params["securityToken"] = self.security_token
        response = self.client.get(url=self.api_endpoint, params=params)
        LOGGER.info(f"GET: {response.url}")
        return [response.content]

    def multiple_requests(self, request: RequestData, is_request_week_based: bool) -> list:
        """
        Sends multiple requests to the API endpoint.

        Args:
            request (RequestData): The request data object.

        Returns:
            list: The response content.

        """
        request.params["securityToken"] = self.security_token
        res = []
        start_date, end_date = split_interval(interval=request.params["TimeInterval"])
        time_type = request.article.time_type
        
        # if domain == "1": #load
        #     intervals = split_in_intervals_load(start_date, end_date, time_type)
        # elif domain == "4": #generation
        #     is_request_start_with_a_week = True if request.article.code == "16.1.D" else False
        #     intervals = split_in_intervals_generation(start_date, end_date, time_type, is_request_start_with_a_week)
        
        intervals = split_to_intervals(start_date, end_date, time_type, is_request_week_based)
        
 
        for interval in intervals:
            for i in request.areas:
                request.set_custom_attribute_by_domain(value=i)
                
                time_time_interval = f"{interval[0]}/{interval[1]}"
                request.set_custom_attribute("TimeInterval", time_time_interval)

                # print(request.params)
                response = self.client.get(
                    url=self.api_endpoint, params=request.params
                )
                LOGGER.info(f"MULTI-GET: {response.url}")
                res.append(response.content)
        

        return res
