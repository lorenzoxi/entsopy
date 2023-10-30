from dataclasses import dataclass
from classes.article import Article


@dataclass
class RequestData:
    def __init__(
        self,
        article: Article,
        areas: list,
        time_interval: str,
        custom_params: list,
        default_params: list = ["documentType", "processType", "TimeInterval"],
        params={},
        multiple_areas=True,
        multiple_time_intervals=True,
        multiple_psr_types=False,
    ):
        self.name = article.name
        self.code = article.code
        self.is_available = article.is_available
        self.document_type = article.document_type
        self.process_type = article.process_type
        self.key = article.key
        self.area = article.area
        self.time_type = article.time_type
        self.range_limit = article.range_limit
        self.domain = article.domain
        self.default_params = default_params
        self.custom_params = custom_params
        self.params = params
        self.areas = areas
        self.time_interval = time_interval
        self.multiple_areas = multiple_areas
        self.multiple_time_intervals = multiple_time_intervals
        self.multiple_psr_types = multiple_psr_types

        for param in self.default_params:
            if param == "documentType":
                self.params[param] = self.document_type
            elif param == "processType":
                self.params[param] = self.process_type
            elif param == "TimeInterval":
                self.params[param] = self.time_interval

    def __repr__(self) -> str:
        return f"RequestData(name='{self.name}', code='{self.code}', is_available='{self.is_available}', document_type='{self.document_type}', process_type='{self.process_type}', key='{self.key}', area='{self.area}', time_type='{self.time_type}', range_limit='{self.range_limit}', domain='{self.domain}', default_params='{self.default_params}', custom_params='{self.custom_params}', params='{self.params}', areas='{self.areas}', multiple_areas='{self.multiple_areas}', multiple_time_intervals='{self.multiple_time_intervals}', multiple_psr_types='{self.multiple_psr_types}')"

    def set_time_interval_param(self, time_interval: str):
        self.params["TimeInterval"] = time_interval

    def set_custom_param(self, param: str, value: str):
        self.params[param] = value

    def set_custom_param(self, value: str):
        if self.domain in "generation":
            self.params["in_Domain"] = value
        elif self.domain in "load":
            self.params["OutBiddingZone_Domain"] = value
