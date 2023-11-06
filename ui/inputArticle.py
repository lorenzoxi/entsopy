import typer
from classes.article import Article
from ui.table import createTable
from rich import print
import json


def extractArticle(articles, article_to_extract: str) -> Article:
    for art in articles:
        if art["key"] == article_to_extract:
            return Article(article=art)


def inputArticle(domain: str) -> Article:
    if domain == "1":
        f = open("./data/generation.articles.json", "r")
    elif domain == "2":
        f = open("./data/load.articles.json", "r")
    elif domain == "3":
        f = open("./data/transmission.articles.json", "r")

    data_articles = json.load(f)

    table = createTable(
        ["Article", "Code", "Key"],
        title="Select the Article of the data you want to download from the list below",
        rows=data_articles,
    )
    print(table)

    selected_article = str(
        typer.prompt(
            "Insert the code of the Article you want to download data from",
        )
    ).lower()

    return extractArticle(articles=data_articles, article_to_extract=selected_article)
