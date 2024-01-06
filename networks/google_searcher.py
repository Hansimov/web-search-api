import requests
from pathlib import Path
from utils.enver import enver
from utils.logger import logger


class GoogleSearcher:
    # https://github.com/Nv7-GitHub/googlesearch/blob/master/googlesearch/__init__.py
    def __init__(self):
        self.url = "https://www.google.com/search"
        self.enver = enver
        self.enver.set_envs(proxies=True)
        self.output_root = Path(__file__).parents[1] / "files"

    def send_request(self, result_num=10):
        logger.note(f"Searching: [{self.query}]")
        self.request_response = requests.get(
            url=self.url,
            headers={
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/111.0.0.0 Safari/537.36 Edg/111.0.1661.62",
            },
            params={
                "q": self.query,
                "num": result_num,
            },
            proxies=self.enver.requests_proxies,
        )

    def save_response(self):
        output_filename = self.query.replace(" ", "_") + ".html"
        if not self.output_root.exists():
            self.output_root.mkdir(parents=True, exist_ok=True)
        output_path = self.output_root / output_filename
        logger.note(f"Saving to: [{output_path}]")
        with open(output_path, "wb") as wf:
            wf.write(self.request_response.content)

    def search(self, query):
        self.query = query
        self.send_request()
        self.save_response()


if __name__ == "__main__":
    searcher = GoogleSearcher()
    # searcher.search("python教程")
    searcher.search("python tutorials")
