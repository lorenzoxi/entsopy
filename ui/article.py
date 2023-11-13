import typer
from classes.article import Article
from const import DIRS
from ui.table import create_table
from rich import print
import json


def extractArticle(articles, article_to_extract: str) -> Article:
    for art in articles:
        if art["key"] == article_to_extract:
            return Article(article=art)


def input_article(domain: str) -> Article:
    if domain == "1":
        f = open(DIRS["articles_load"], "r")
    elif domain == "2":
        f = open(DIRS["articles_ncm"], "r")
    elif domain == "3":
        f = open(DIRS["articles_transmission"], "r")
    elif domain == "4":
        f = open(DIRS["articles_generation"], "r")
    elif domain == "5":
        f = open(DIRS["articles_balancing"], "r")
    elif domain == "6":
        f = open(DIRS["articles_outages"], "r")
    data_articles = json.load(f)

    table = create_table(
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

    article = extractArticle(
        articles=data_articles, article_to_extract=selected_article
    )
    return article
