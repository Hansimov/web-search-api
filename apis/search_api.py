import argparse
import os
import sys
import uvicorn

from fastapi import FastAPI, Depends
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from pydantic import BaseModel, Field
from typing import Union
from sse_starlette.sse import EventSourceResponse, ServerSentEvent
from utils.logger import logger
from networks.google_searcher import GoogleSearcher
from networks.webpage_fetcher import WebpageFetcher
from documents.query_results_extractor import QueryResultsExtractor
from documents.webpage_content_extractor import WebpageContentExtractor
from utils.logger import logger


class SearchAPIApp:
    def __init__(self):
        self.app = FastAPI(
            docs_url="/",
            title="Web Search API",
            swagger_ui_parameters={"defaultModelsExpandDepth": -1},
            version="1.0",
        )
        self.setup_routes()

    class QueriesToSearchResultsPostItem(BaseModel):
        queries: list = Field(
            default=[""],
            description="(list[str]) Queries to search",
        )
        result_num: int = Field(
            default=10,
            description="(int) Number of search results",
        )
        safe: bool = Field(
            default=False,
            description="(bool) Enable SafeSearch",
        )
        types: list = Field(
            default=["web"],
            description="(list[str]) Types of search results: `web`, `image`, `videos`, `news`",
        )
        extract_content: bool = Field(
            default=False,
            description="(bool) Enable extracting main text contents from webpage, will add `text` filed in each `query_result` dict",
        )
        overwrite_query_html: bool = Field(
            default=False,
            description="(bool) Overwrite HTML file of query results",
        )
        overwrite_webpage_html: bool = Field(
            default=False,
            description="(bool) Overwrite HTML files of webpages from query results",
        )

    def queries_to_search_results(self, item: QueriesToSearchResultsPostItem):
        google_searcher = GoogleSearcher()
        query_results_extractor = QueryResultsExtractor()
        queries_search_results = []
        for query in item.queries:
            if not query.strip():
                continue
            query_html_path = google_searcher.search(
                query=query,
                result_num=item.result_num,
                safe=item.safe,
                overwrite=item.overwrite_query_html,
            )
            query_search_results = query_results_extractor.extract(query_html_path)
            queries_search_results.append(query_search_results)
        logger.note(queries_search_results)

        if item.extract_content:
            webpage_fetcher = WebpageFetcher()
            webpage_content_extractor = WebpageContentExtractor()
            for query_idx, query_search_result in enumerate(queries_search_results):
                for query_result_idx, query_result in enumerate(
                    query_search_result["query_results"]
                ):
                    webpage_html_path = webpage_fetcher.fetch(
                        query_result["url"],
                        overwrite=item.overwrite_webpage_html,
                        output_parent=query_search_result["query"],
                    )
                    extracted_content = webpage_content_extractor.extract(
                        webpage_html_path
                    )
                    queries_search_results[query_idx]["query_results"][
                        query_result_idx
                    ]["text"] = extracted_content
        return queries_search_results

    def setup_routes(self):
        self.app.post(
            "/queries_to_search_results",
            summary="Search queries, and extract contents from results",
        )(self.queries_to_search_results)


class ArgParser(argparse.ArgumentParser):
    def __init__(self, *args, **kwargs):
        super(ArgParser, self).__init__(*args, **kwargs)

        self.add_argument(
            "-s",
            "--server",
            type=str,
            default="0.0.0.0",
            help="Server IP for Web Search API",
        )
        self.add_argument(
            "-p",
            "--port",
            type=int,
            default=21111,
            help="Server Port for Web Search API",
        )

        self.add_argument(
            "-d",
            "--dev",
            default=False,
            action="store_true",
            help="Run in dev mode",
        )

        self.args = self.parse_args(sys.argv[1:])


app = SearchAPIApp().app

if __name__ == "__main__":
    args = ArgParser().args
    if args.dev:
        uvicorn.run("__main__:app", host=args.server, port=args.port, reload=True)
    else:
        uvicorn.run("__main__:app", host=args.server, port=args.port, reload=False)

    # python -m apis.search_api      # [Docker] in product mode
    # python -m apis.search_api -d   # [Dev]    in develop mode
