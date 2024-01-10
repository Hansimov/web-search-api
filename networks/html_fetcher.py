import requests
import tldextract
from pathlib import Path
from utils.enver import enver
from utils.logger import logger
from networks.filepath_converter import UrlToFilepathConverter
from networks.network_configs import IGNORE_HOSTS, REQUESTS_HEADERS


class HTMLFetcher:
    def __init__(self):
        self.enver = enver
        self.enver.set_envs(proxies=True)
        self.filepath_converter = UrlToFilepathConverter()

    def is_ignored_host(self, url):
        self.host = tldextract.extract(url).registered_domain
        if self.host in IGNORE_HOSTS:
            return True
        else:
            return False

    def send_request(self):
        self.request_response = requests.get(
            url=self.url,
            headers=REQUESTS_HEADERS,
            proxies=self.enver.requests_proxies,
        )

    def save_response(self):
        if not self.output_path.exists():
            self.output_path.parent.mkdir(parents=True, exist_ok=True)
        logger.success(f"Saving to: [{self.output_path}]")
        with open(self.output_path, "wb") as wf:
            wf.write(self.request_response.content)

    def fetch(self, url, overwrite=False):
        self.url = url
        logger.note(f"Fetching: [{self.url}]")
        self.output_path = self.filepath_converter.convert(self.url)

        if self.is_ignored_host(self.url):
            logger.warn(f"Ignore host: [{self.host}]")
            return self.output_path

        if self.output_path.exists() and not overwrite:
            logger.success(f"HTML existed: [{self.output_path}]")
        else:
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
