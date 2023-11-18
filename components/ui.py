from const import DIRS
from components.auction import input_auction_type
from components.docstatus import input_docstatus
from components.marketagreement import input_market_agreement
from classes.article import Article
from components.areas import input_areas
from components.dates import input_date
from components.direction import input_direction
from rich import print
import json
from components.marketproduct import input_market_product

from components.psrtype import input_psrtype
from components.registeredresource import input_registeredsource


def ui_article(article: Article):
    attributes = json.load(open(DIRS["type_attributes"], "r"))
    attributes.sort(key=lambda x: x["priority"], reverse=True)

    areas = None
    time_interval = None
    contract_market_agreement = None
    direction = None
    auction_type = None
    docstatus = None
    psrtype = None
    market_product = None
    registered_resource = None

    for attribute in attributes:
        attribute = attribute["name"]
        if attribute in article.attributes and article.attributes[attribute] == 1:
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
                auction_type = input_auction_type()

            elif attribute == "Auction.Category":
                auction_type = input_auction_type(isCategory=True)

            elif attribute == "DocStatus":
                docstatus = input_docstatus()

            elif attribute == "PsrType":
                psrtype = input_psrtype()

            elif attribute == "Standard_MarketProduct":
                market_product = input_market_product()

            elif attribute == "Original_MarketProduct":
                market_product = input_market_product(is_standard=False)

            elif attribute == "RegisteredResource":
                registered_resource = input_registeredsource()

    return (
        areas,
        time_interval,
        contract_market_agreement,
        direction,
        auction_type,
        docstatus,
        psrtype,
        market_product,
        registered_resource,
    )
