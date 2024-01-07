import platform
import re
from pathlib import Path
from urllib.parse import quote


# What characters are forbidden in Windows and Linux directory names?
#   https://stackoverflow.com/questions/1976007/what-characters-are-forbidden-in-windows-and-linux-directory-names

INVALID_FILE_PATH_CHARS = [
    "\\",
    "/",
    ":",
    "*",
    "?",
    '"',
    "<",
    ">",
    "|",
    "\n",
    "\t",
    "\r",
    *[chr(i) for i in range(32)],
]

WINDOWS_INVALID_FILE_PATH_NAMES = [
    "con",
    "prn",
    "aux",
    "nul",
    *[f"com{i+1}" for i in range(10)],
    *[f"lpt{i+1}" for i in range(10)],
]


class FilepathConverter:
    def __init__(self):
        self.output_root = Path(__file__).parents[1] / "files"

    def preprocess(self, input_string):
        return input_string

    def validate(self, input_string):
        filename = input_string
        for char in INVALID_FILE_PATH_CHARS:
            filename = filename.replace(char, "_")
        if platform.system() == "Windows":
            filename_base = filename.split(".")[0]
            if filename_base.lower() in WINDOWS_INVALID_FILE_PATH_NAMES:
                filename_base = filename_base + "_"
                filename = ".".join([filename_base, *filename.split(".")[1:]])
        return filename

    def append_extension(self, filename, accept_exts=[".html", ".htm"], ext=".html"):
        if ext:
            filename_ext = "." + filename.split(".")[-1]
            if filename_ext.lower() not in accept_exts:
                filename += ext
        return filename

    def convert(self, input_string, parent=None):
        filename = self.preprocess(input_string)
        filename = self.validate(filename)
        filename = self.append_extension(filename)

        if parent:
            filepath = self.output_root / parent / filename
        else:
            filepath = self.output_root / filename

        self.filename = filename
        self.filepath = filepath

        return {"filename": self.filename, "filepath": self.filepath}


class UrlToFilepathConverter(FilepathConverter):
    def __init__(self):
        super().__init__()
        self.output_root = self.output_root / "urls"

    def preprocess(self, url):
        filename = url.split("//")[1]
        return filename


class QueryToFilepathConverter(FilepathConverter):
    def __init__(self):
        super().__init__()
        self.output_root = self.output_root / "queries"


if __name__ == "__main__":
    query = "python 教程"
    query_converter = QueryToFilepathConverter()
    print(query_converter.convert(query)["filename"])

    # url = "https://trafilatura.readthedocs.io/en/latest/quickstart.html"
    url = "https://www.bing.com/search?q=Bing+AI&showconv=1&setlang=en&cc=us"
    # url = (
    #     "https://stackoverflow.com/questions/295135/turn-a-string-into-a-valid-filename"
    # )
    url_converter = UrlToFilepathConverter()
    print(url_converter.convert(url, parent=query)["filepath"])
