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
        params={},
    ):
        self.domain = article.domain
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
        return f"RequestData(domain='{self.domain}', article='{self.article}', areas='{self.areas}', params='{self.params}')"

    def set_custom_attribute(self, param: str, value: str):
        self.params[param] = value

    def set_custom_attribute_by_domain(self, value: str | dict):
        if self.domain in "generation":
            self.params["In_Domain"] = value["code"]
        elif self.domain in "load":
            self.params["OutBiddingZone_Domain"] = value["code"]
        elif self.domain in "transmission":
            self.params["In_Domain"] = value["In_Domain"]
            self.params["Out_Domain"] = value["Out_Domain"]
            if self.article.code == "11.1.B" or self.article.code == "12.1.D":
                self.params["In_Domain"] = value["code"]
                self.params["Out_Domain"] = value["code"]
            if (
                self.article.code == "12.1.B"
                or self.article.code == "12.1.E"
                or self.article.code == "12.1.F"
                or self.article.code == "12.1.G"
            ):
                self.params["In_Domain"] = value["In_Domain"]
                self.params["Out_Domain"] = value["Out_Domain"]

            if self.direction == "export":
                self.params["In_Domain"] = value["Out_Domain"]
                self.params["Out_Domain"] = value["In_Domain"]
            elif self.direction == "import":
                self.params["In_Domain"] = value["In_Domain"]
                self.params["Out_Domain"] = value["Out_Domain"]

            if (
                self.article.code == "12.1.B"
                or self.article.code == "12.1.E"
                or self.article.code == "12.1.F"
                or self.article.code == "12.1.G"
            ):
                self.params["In_Domain"] = value["In_Domain"]
                self.params["Out_Domain"] = value["Out_Domain"]

    def switch_two_params(self, key1: str, key2: str):
        tmp = self.params[key1]
        self.params[key1] = self.params[key2]
        self.params[key2] = tmp
