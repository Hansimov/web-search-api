IGNORE_TAGS = ["script", "style", "button"]
IGNORE_CLASSES = [
    "sidebar",
    "footer",
    "related",
    "comment",
    "topbar",
    # "menu",
    "offcanvas",
    "navbar",
    # 163.com
    "post_(top)|(side)|(recommends)|(crumb)|(statement)|(next)|(jubao)",
    "ntes\-.*nav",
    "nav\-bottom",
]

IGNORE_HOSTS = [
    "weibo.com",
    "hymson.com",
    "yahoo.com",
]

REQUESTS_HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/111.0.0.0 Safari/537.36 Edg/111.0.1661.62",
}
