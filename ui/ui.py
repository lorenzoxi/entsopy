from ui.inputAuction import inputAuctionType
from ui.inputMarketAgreement import inputMarketAgreement
from classes.article import Article
from ui.inputAreas import inputAreas
from ui.inputDate import inputDate
from ui.inputDirection import inputDirection


def UiArticle(article: Article):
    ask_contract_market_agreement = False
    ask_auction_type = False
    contract_market_agreement = None
    ask_only_two_areas = False
    direction = None
    auction_type = None

    if (
        article.domain == "transmission"
    ):  # TODO: refactor this (see attributes of article to generate input)
        ask_contract_market_agreement = True
        if article.name == "Offered Capacity":
            ask_auction_type = True
        elif article.name == "Flow based - day ahead":
            ask_contract_market_agreement = False

        if article.code == "11.1.B":
            ask_contract_market_agreement = False

        if (
            article.code == "12.1.B"
            or article.code == "12.1.E"
            or article.code == "12.1.F"
            or article.code == "12.1.G"
        ):
            ask_contract_market_agreement = False
            ask_only_two_areas = True

        if article.code == "12.1.E":
            ask_contract_market_agreement = True

    time_interval = inputDate(article.time_type)

    areas = inputAreas(
        article.area,
        ask_only_two_areas=ask_only_two_areas,
    )

    if ask_contract_market_agreement:
        contract_market_agreement = inputMarketAgreement()
        direction = inputDirection()

    if ask_auction_type:
        auction_type = inputAuctionType()

    return (areas, time_interval, contract_market_agreement, direction, auction_type)
