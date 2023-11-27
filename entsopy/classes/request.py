from dataclasses import dataclass
from classes.article import Article


@dataclass
class RequestData:
    def __init__(
        self,
        article: Article,
        areas: list,
        time_interval: str,
        contract_market_agreement: str = None,
        direction: str = None,
        auction_type: str = None,
    ):
        self.article = article
        self.areas = areas
        self.direction = direction
        self.params = {}

        for key, value in self.article.attributes.items():
            if value != (-1) and value != 0 and value is not None:
                self.params[key] = value

        self.params["TimeInterval"] = time_interval

        if contract_market_agreement is not None:
            self.params["Contract_MarketAgreement.Type"] = contract_market_agreement

        if auction_type is not None:
            self.params["Auction.Type"] = auction_type

    def __repr__(self) -> str:
        return f"RequestData(domain='{self.article.domain}', article='{self.article}', areas='{self.areas}', params='{self.params}')"

    def set_custom_attribute(self, param: str, value: str):
        self.params[param] = value

    def set_custom_attribute_by_domain(self, value: str | dict):
        if self.article.domain in "generation":
            self.params["In_Domain"] = value["code"]
        elif self.article.domain in "load":
            self.params["OutBiddingZone_Domain"] = value["code"]
        elif self.article.domain in "transmission":
            if (
                self.article.attributes["In_Domain"] == 1
                and self.article.attributes["Out_Domain"] == 1
            ):
                if self.article.area == "BZNS":
                    self.params["In_Domain"] = value["In_Domain"]
                    self.params["Out_Domain"] = value["Out_Domain"]
                else:
                    self.params["In_Domain"] = value["code"]
                    self.params["Out_Domain"] = value["code"]

            if self.direction == "export":
                self.switch_two_params("In_Domain", "Out_Domain")

        elif self.article.domain in "balancing":
            if self.article.attributes["ControlArea_Domain"] == 1:
                self.params["ControlArea_Domain"] = value["code"]
            elif (
                self.article.attributes["Acquiring_Domain"] == 1
                and self.article.attributes["Connecting_Domain"] == 1
            ):
                self.params["Acquiring_Domain"] = value["Acquiring_Domain"]
                self.params["Connecting_Domain"] = value["Connecting_Domain"]

    def switch_two_params(self, key1: str, key2: str):
        tmp = self.params[key1]
        self.params[key1] = self.params[key2]
        self.params[key2] = tmp
