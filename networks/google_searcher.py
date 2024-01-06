import requests
from pathlib import Path
from utils.enver import enver


class RequestHeaderConstructor:
    def __init__(self):
        self.construct()

    def construct(self):
        self.headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/111.0.0.0 Safari/537.36 Edg/111.0.1661.62",
        }


class GoogleSearcher:
    # https://github.com/Nv7-GitHub/googlesearch/blob/master/googlesearch/__init__.py
    def __init__(self):
        self.url = "https://www.google.com/search"
        self.enver = enver
        self.enver.set_envs(proxies=True)
        self.output_root = Path(__file__).parents[1] / "files"

    def send_request(self, query, result_num=10):
        res = requests.get(
            url=self.url,
            headers=RequestHeaderConstructor().headers,
            params={
                "q": self.query,
                "num": result_num,
                # "hl": "en",
                # "start": 0,
            },
            proxies=self.enver.requests_proxies,
        )
        return res

    def save_response(self, res, query):
        output_filename = query.replace(" ", "_") + ".html"
        if not self.output_root.exists():
            self.output_root.mkdir(parents=True, exist_ok=True)
        output_path = self.output_root / output_filename
        with open(output_path, "wb") as wf:
            wf.write(res.content)

    def search(self, query):
        self.query = query
        res = self.send_request(query)
        self.save_response(res, query)


if __name__ == "__main__":
    searcher = GoogleSearcher()
    # searcher.search("python tutorials")
    searcher.search("python教程")
