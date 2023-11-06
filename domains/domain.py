from classes.request import RequestData
from ui.inputArticle import inputArticle
from ui.ui import UiArticle
from utils.csv import concat_and_save_dfs
from classes.response import ResponseData
from classes.httpsclient import HttpsClient


def domain(client: HttpsClient, domain: str):
    article = inputArticle(domain=domain)
    (
        areas,
        time_interval,
        contract_market_agreement,
        direction,
        auction_type,
    ) = UiArticle(article=article)
    # print(areas, "\n", time_interval, "\n", contract_market_agreement, "\n", direction)

    request = RequestData(
        article=article,
        time_interval=time_interval,
        contract_market_agreement=contract_market_agreement,
        direction=direction,
        auction_type=auction_type,
        areas=areas,
    )

    data = client.multiple_requests(request=request)
    # print(data)

    res = [
        (ResponseData(content, article_code=request.article.code)).df
        for content in data
    ]

    concat_and_save_dfs(dfs=res, file_name=article.domain, suffix=article.code)

    return True
