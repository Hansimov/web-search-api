import re
from pathlib import Path
from pprint import pprint
from bs4 import BeautifulSoup, Comment, NavigableString, Tag
from tiktoken import get_encoding as tiktoken_get_encoding
from utils.logger import logger
from markdownify import markdownify

# from trafilatura import extract as extract_text_from_html
# from inscriptis import get_text as extract_text_from_html
# from html_text import extract_text as extract_text_from_html
# from readabilipy import simple_json_from_html_string as extract_text_from_html


class WebpageContentExtractor:
    def __init__(self):
        self.tokenizer = tiktoken_get_encoding("cl100k_base")

    def count_tokens(self, text):
        tokens = self.tokenizer.encode(text)
        token_count = len(tokens)
        return token_count

    def filter_html_str(self, html_str):
        soup = BeautifulSoup(html_str, "html.parser")

        ignore_tags = ["script", "style", "button"]

        ignore_classes = [
            "sidebar",
            "footer",
            "related",
            "comment",
            "topbar",
            "menu",
            "offcanvas",
            "navbar",
        ]
        ignore_classes_pattern = f'{"|".join(ignore_classes)}'
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
                or (element.name in ignore_tags)
                or (re.search(ignore_classes_pattern, class_str, flags=re.IGNORECASE))
                or (re.search(ignore_classes_pattern, id_str, flags=re.IGNORECASE))
            ):
                # try:
                #     logger.note(f"Removing:\n{element}")
                # except:
                #     logger.note(f"Removing unknown element")
                element.decompose()
                removed_element_counts += 1

        logger.note(
            f"Elements Removed/Remained:  {removed_element_counts}/{len(soup.find_all())}"
        )

        html_str = str(soup)
        return html_str

    def extract(self, html_path):
        logger.note(f"Extracing content from:{html_path}")
        with open(html_path, "r", encoding="utf-8") as f:
            html_str = f.read()

        html_str = self.filter_html_str(html_str)

        # self.main_content = extract_text_from_html(html_str)

        # # when using `readabilipy`
        # self.main_content = extract_text_from_html(html_str)["plain_content"]
        # self.main_content = "\n".join(
        #     item["text"] for item in extract_text_from_html(html_str)["plain_text"]
        # )
        # self.main_content = markdownify(extract_text_from_html(html_str)["content"])

        # self.main_content = markdownify(extract_text_from_html(html_str))

        self.main_content = markdownify(html_str, strip="a")
        self.main_content = re.sub(r"\n{3,}", "\n\n", self.main_content)
        # logger.line(self.main_content)
        # pprint(self.main_content)
        token_count = self.count_tokens(self.main_content)
        logger.note(f"Token Count: {token_count}")
        return self.main_content


if __name__ == "__main__":
    html_path = (
        Path(__file__).parents[1]
        / "files"
        / "urls"
        # / "stackoverflow.com_questions_295135_turn-a-string-into-a-valid-filename.html"
        / "www.liaoxuefeng.com_wiki_1016959663602400_1017495723838528.html"
        # / "docs.python.org_zh-cn_3_tutorial_interpreter.html"
    )
    extractor = WebpageContentExtractor()
    main_content = extractor.extract(html_path)
