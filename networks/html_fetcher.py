import requests
from pathlib import Path
from utils.enver import enver
from utils.logger import logger
from networks.filepath_converter import UrlToFilepathConverter


class HTMLFetcher:
    def __init__(self):
        self.enver = enver
        self.enver.set_envs(proxies=True)

    def send_request(self):
        logger.note(f"Fetching: [{self.url}]")
        self.request_response = requests.get(
            url=self.url,
            headers={
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/111.0.0.0 Safari/537.36 Edg/111.0.1661.62",
            },
            proxies=self.enver.requests_proxies,
        )

    def save_response(self):
        self.output_path = UrlToFilepathConverter().convert(self.url)
        if not self.output_path.exists():
            self.output_path.parent.mkdir(parents=True, exist_ok=True)

        logger.success(f"Saving to: [{self.output_path}]")

        with open(self.output_path, "wb") as wf:
            wf.write(self.request_response.content)

    def fetch(self, url):
        self.url = url
        self.send_request()
        self.save_response()
        return self.output_path


if __name__ == "__main__":
    url = (
        # "https://stackoverflow.com/questions/295135/turn-a-string-into-a-valid-filename"
        # "https://www.liaoxuefeng.com/wiki/1016959663602400/1017495723838528"
        "https://docs.python.org/zh-cn/3/tutorial/interpreter.html"
    )
    fetcher = HTMLFetcher()
    fetcher.fetch(url)
