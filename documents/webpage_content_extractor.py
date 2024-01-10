import re
from pathlib import Path
from pprint import pprint
from bs4 import BeautifulSoup
from tiktoken import get_encoding as tiktoken_get_encoding
from utils.logger import logger
from markdownify import markdownify
from networks.network_configs import IGNORE_TAGS, IGNORE_CLASSES
from termcolor import colored


class WebpageContentExtractor:
    def __init__(self):
        self.tokenizer = tiktoken_get_encoding("cl100k_base")

    def count_tokens(self, text):
        tokens = self.tokenizer.encode(text)
        token_count = len(tokens)
        return token_count

    def html_to_markdown(self, html_str, ignore_links=True):
        if ignore_links:
            markdown_str = markdownify(html_str, strip="a")
        else:
            markdown_str = markdownify(html_str)
        markdown_str = re.sub(r"\n{3,}", "\n\n", markdown_str)

        self.markdown_token_count = self.count_tokens(markdown_str)
        logger.mesg(f'- Tokens: {colored(self.markdown_token_count,"light_green")}')

        self.markdown_str = markdown_str

        return self.markdown_str

    def remove_elements_from_html(self, html_str):
        soup = BeautifulSoup(html_str, "html.parser")
        ignore_classes_pattern = f'{"|".join(IGNORE_CLASSES)}'
        removed_element_counts = 0
        for element in soup.find_all():
            class_str = ""
            id_str = ""
            try:
                class_attr = element.get("class", [])
                if class_attr:
                    class_str = " ".join(list(class_attr))
                if id_str:
                    class_str = f"{class_str} {id_str}"
            except:
                pass

            try:
                id_str = element.get("id", "")
            except:
                pass

            if (
                (not element.text.strip())
                or (element.name in IGNORE_TAGS)
                or (re.search(ignore_classes_pattern, class_str, flags=re.IGNORECASE))
                or (re.search(ignore_classes_pattern, id_str, flags=re.IGNORECASE))
            ):
                element.decompose()
                removed_element_counts += 1

        logger.mesg(
            f"- Elements: "
            f'{colored(len(soup.find_all()),"light_green")} / {colored(removed_element_counts,"light_red")}'
        )

        html_str = str(soup)
        self.html_str = html_str

        return self.html_str

    def extract(self, html_path):
        logger.note(f"Extracting content from: {html_path}")

        if not Path(html_path).exists():
            logger.warn(f"File not found: {html_path}")
            return ""

        with open(html_path, "r", encoding="utf-8") as rf:
            html_str = rf.read()

        html_str = self.remove_elements_from_html(html_str)
        markdown_str = self.html_to_markdown(html_str)
        return markdown_str


if __name__ == "__main__":
    html_path = (
        Path(__file__).parents[1]
        / "files"
        / "urls"
        # / "stackoverflow.com_questions_295135_turn-a-string-into-a-valid-filename.html"
        # / "www.liaoxuefeng.com_wiki_1016959663602400_1017495723838528.html"
        # / "docs.python.org_zh-cn_3_tutorial_interpreter.html"
        / "zh.wikipedia.org_zh-hans_%E7%94%B0%E4%B8%AD%E6%9F%A0%E6%AA%AC.html"
    )
    extractor = WebpageContentExtractor()
    main_content = extractor.extract(html_path)
