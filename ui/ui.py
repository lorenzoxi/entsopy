from const import DIRS
from ui.auction import input_auctiont_type
from ui.marketagreement import input_market_agreement
from classes.article import Article
from ui.areas import input_areas
from ui.dates import input_date
from ui.direction import input_direction
from rich import print
import json


def ui_article(article: Article):
    attributes = json.load(open(DIRS["type_attributes"], "r"))
    attributes.sort(key=lambda x: x["priority"], reverse=True)

    for attribute in attributes:
        attribute = attribute["name"]
        if attribute in article.attributes and article.attributes[attribute] == 1:
            print(f"{attribute}: {article.attributes[attribute]}")
            if attribute == "TimeInterval":
                time_interval = input_date(article.time_type)
            elif (
                attribute == "OutBiddingZone_Domain"
                or attribute == "BiddingZone_Domain"
                or attribute == "ControlArea_Domain"
                or attribute == "In_Domain"
                or attribute == "Out_Domain"
                or attribute == "Acquiring_Domain"
                or attribute == "Connecting_Domain"
            ):
                areas = input_areas(article.area)

            elif attribute == "Contract_MarketAgreement.Type":
                contract_market_agreement = input_market_agreement()
                direction = input_direction()

            elif attribute == "Type_MarketAgreement.Type":
                contract_market_agreement = input_market_agreement(isType=True)

            elif attribute == "Auction.Type":
                auction_type = input_auctiont_type()

        # TODO: manage optional attributes == 0

    return areas, time_interval, contract_market_agreement, direction, auction_type
