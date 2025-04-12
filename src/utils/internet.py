import traceback
from typing import Optional
from dataclasses import dataclass

import aiohttp
from markdownify import markdownify

__all__ = (
    "SearchResult",
    "get_raw_content_data",
    "read_website",
    "search_web",
)


@dataclass
class SearchResult:
    url: str
    title: Optional[str]
    content: Optional[str]
    published_date: Optional[str]
    engines: list[str]
    score: float


async def ensure_session(
    session: Optional[aiohttp.ClientSession] = None,
) -> aiohttp.ClientSession:
    """Ensures that an aiohttp.ClientSession is returned."""
    if session is None:
        async with aiohttp.ClientSession() as session:
            return session
    return session


async def get_raw_content_data(
    url: str, session: Optional[aiohttp.ClientSession] = None, **kwargs
) -> bytes:
    """Get raw content like files and media as bytes"""
    session = await ensure_session(session)

    async with session.get(
        url, ssl=True if url.lower().startswith("https") else False, **kwargs
    ) as response:
        return await response.content.read()


async def read_website(
    url: str, *, session: Optional[aiohttp.ClientSession] = None, **kwargs
) -> str:
    """Reads a website and returns markdown."""
    session = await ensure_session(session)

    async with session.get(
        url,
        ssl=True if url.lower().startswith("https") else False,
        allow_redirects=True,
        **kwargs
    ) as response:
        response.raise_for_status()
        html = await response.text()

        # Only get the visible text as markdown, not the entire HTML
        return markdownify(html)


async def search_web(
    query: str,
    pages: int = 1,
    *,
    session: Optional[aiohttp.ClientSession] = None,
    searxng_url: str,
    **kwargs
) -> list[SearchResult] | str:
    """Searches the web using SearXNG."""
    session = await ensure_session(session)

    search_results = []
    try:
        for pageno in range(1, pages + 1):
            async with session.get(
                searxng_url,
                params={"q": query, "format": "json", "pageno": pageno},
                ssl=True if searxng_url.lower().startswith("https") else False,
                **kwargs
            ) as response:
                response.raise_for_status()
                data = await response.json()
                search_results += [
                    SearchResult(
                        url=r["url"],
                        title=r.get("title"),
                        content=r.get("content"),
                        published_date=r.get("publishedDate"),
                        engines=r["engines"],
                        score=r["score"],
                    )
                    for r in data["results"]
                ]

    except Exception as e:
        return "".join(traceback.format_exception(e))

    return sorted(search_results, key=lambda x: x.score, reverse=True)
