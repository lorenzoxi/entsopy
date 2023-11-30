from classes.request import RequestData
from components.article import input_article
from components.ui import ui_article
from utils.date import get_format
from utils.csv import concat_and_save_dfs
from classes.response import ResponseData
from classes.httpsclient import HttpsClient


def home(client: HttpsClient, domain: str) -> str:
    """
    Executes the main flow of the program.

    Args:
        client (HttpsClient): The HTTPS client used to make requests.
        domain (str): The domain to be used for the request.

    Returns:
        str: The file name of the saved response.
    """

    article = input_article(domain=domain)
    (
        areas,
        time_interval,
        contract_market_agreement,
        direction,
        auction_type,
        docstatus,
        psrtype,
        market_product,
        registered_resource,
    ) = ui_article(article=article)

    print("Generate the request...")

    request = RequestData(
        article=article,
        time_interval=time_interval,
        contract_market_agreement=contract_market_agreement,
        direction=direction,
        auction_type=auction_type,
        areas=areas,
    )
    print("Sending the request...")

    data = client.multiple_requests(request=request)

    print("Processing the response...")

    res = [
        (ResponseData(content, article_code=request.article.code)).df
        for content in data
    ]

    print("Saving the response...")
    file_name = concat_and_save_dfs(
        dfs=res, file_name=article.domain, suffix=article.code
    )

    return file_name
