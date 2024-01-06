from bs4 import BeautifulSoup
from pathlib import Path


class SearchResultsExtractor:
    def __init__(self) -> None:
        pass

    def load_html(self, html_path):
        with open(html_path, "r", encoding="utf-8") as f:
            html = f.read()
        self.soup = BeautifulSoup(html, "html.parser")

    def extract_search_results(self):
        search_result_elements = self.soup.find_all("div", class_="g")

        for result in search_result_elements:
            site = result.find("cite").find_previous("span").text
            link = result.find("a")["href"]
            title = result.find("h3").text

            abstract_element = result.find("div", {"data-sncf": "1"})
            if abstract_element is None:
                abstract_element = result.find("div", class_="ITZIwc")
            abstract = abstract_element.text.strip()

            print(
                f"{title}\n" f"  - {site}\n" f"  - {link}\n" f"  - {abstract}\n" f"\n"
            )
        print(len(search_result_elements))

    def extract_related_questions(self):
        related_question_elements = self.soup.find_all(
            "div", class_="related-question-pair"
        )
        for question_element in related_question_elements:
            question = question_element.find("span").text.strip()
            print(question)
        print(len(related_question_elements))

    def extract(self, html_path):
        self.load_html(html_path)
        self.extract_search_results()
        self.extract_related_questions()


if __name__ == "__main__":
    html_path_root = Path(__file__).parents[1] / "files"
    # html_filename = "python教程"
    html_filename = "python_tutorials"
    html_path = html_path_root / f"{html_filename}.html"
    extractor = SearchResultsExtractor()
    extractor.extract(html_path)
