import os
from typing import Any

from firecrawl import FirecrawlApp
from firecrawl.v2.types import Document, ScrapeOptions, SearchData


class SearchResults:
    """Wrapper so workflow code can keep using `.data` on search responses."""

    def __init__(self, data: list[dict[str, Any]] | None = None):
        self.data = data or []

    def __bool__(self) -> bool:
        return bool(self.data)


def _flatten_search_results(search_data: SearchData) -> list[dict[str, Any]]:
    results: list[dict[str, Any]] = []
    for item in search_data.web or []:
        if isinstance(item, Document):
            meta = item.metadata
            meta_dict = meta.model_dump() if meta else {}
            url = (meta.url if meta and meta.url else "") or meta_dict.get("url", "")
            results.append(
                {
                    "url": url,
                    "markdown": item.markdown or "",
                    "metadata": meta_dict,
                }
            )
        else:
            results.append(
                {
                    "url": item.url,
                    "markdown": getattr(item, "markdown", "") or "",
                    "metadata": {
                        "title": item.title,
                        "description": item.description,
                    },
                }
            )
    return results


class FirecrawlService:
    def __init__(self):
        api_key = os.getenv("FIRECRAWL_API_KEY")
        if not api_key:
            raise ValueError("Missing FIRECRAWL_API_KEY environment variable")
        self.app = FirecrawlApp(api_key=api_key)

    def search_companies(self, query: str, num_results: int = 5) -> SearchResults:
        try:
            result = self.app.search(
                query=f"{query} company pricing",
                limit=num_results,
                scrape_options=ScrapeOptions(formats=["markdown"]),
            )
            return SearchResults(_flatten_search_results(result))
        except Exception as e:
            print(e)
            return SearchResults()

    def scrape_company_pages(self, url: str) -> Document | None:
        try:
            return self.app.scrape_url(url, formats=["markdown"])
        except Exception as e:
            print(e)
            return None
