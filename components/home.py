from classes.request import RequestData
from components.article import input_article
from components.ui import ui_article
from utils.csv import concat_and_save_dfs
from classes.response import ResponseData
from classes.httpsclient import HttpsClient


def main_flow(client: HttpsClient, domain: str) -> bool:
    article = input_article(domain=domain)
    (
        areas,
        time_interval,
        contract_market_agreement,
        direction,
        auction_type,
    ) = ui_article(article=article)

    request = RequestData(
        article=article,
        time_interval=time_interval,
        contract_market_agreement=contract_market_agreement,
        direction=direction,
        auction_type=auction_type,
        areas=areas,
    )

    data = client.multiple_requests(request=request)

    res = [
        (ResponseData(content, article_code=request.article.code)).df
        for content in data
    ]

    concat_and_save_dfs(dfs=res, file_name=article.domain, suffix=article.code)

    return True
