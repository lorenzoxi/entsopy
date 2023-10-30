from rich import print
from classes.request import RequestData
from utils.csv import concat_and_save_dfs
from classes.article import Article
from classes.response import ResponseData
from ui.inputAreas import inputAreas
from classes.client import HttpsClient
from ui.inputDate import inputDate
from ui.table import createTable
import json
import typer


def domain(client: HttpsClient, domain: str):
    if domain == "1":
        f = open("./data/generation.articles.data.json", "r")
    elif domain == "2":
        f = open("./data/load.articles.data.json", "r")
    data_articles = json.load(f)
    articles = [Article(art) for art in data_articles]

    # Article
    table = createTable(
        ["Article", "Code", "Key"],
        title="Select the Article of the data you want to download from the list below",
        rows=data_articles,
    )

    ## input Article
    print(table)
    selected_article = str(
        typer.prompt(
            "Insert the code of the Article you want to download data from",
        )
    ).lower()

    article = next(
        (article for article in articles if str(article.key) == str(selected_article)),
        None,
    )
    time_interval = inputDate(article.time_type)

    areas = inputAreas(
        article.area,
    )

    request = RequestData(
        article=article,
        time_interval=time_interval,
        areas=areas,
        custom_params=["in_domain"],
    )
    data = client.multiple_requests(request=request)
    res = [(ResponseData(content, article_code=request.code)).df for content in data]

    concat_and_save_dfs(dfs=res, file_name=article.domain, suffix=request.code)

    return True
