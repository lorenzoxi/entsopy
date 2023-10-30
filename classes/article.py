from dataclasses import dataclass


@dataclass
class Article:
    def __init__(self, article: dict):
        self.name = article["name"]
        self.code = article["code"]
        self.is_available = article["is_available"]
        self.document_type = article["document_type"]
        self.process_type = article["process_type"]
        self.key = article["key"]
        self.area = article["area"]
        self.range_limit = article["range_limit"]
        self.domain = article["domain"]
        self.time_type = article["time_type"]

    def __repr__(self):
        return f"Article(name='{self.name}', code='{self.code}', is_available='{self.is_available}', document_type='{self.document_type}', process_type='{self.process_type}', key='{self.key}', area='{self.area}')"
