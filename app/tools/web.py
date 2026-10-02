from __future__ import annotations

import httpx


async def web_search(query: str, limit: int = 5) -> list[dict[str, str]]:
    params = {"q": query, "format": "json", "no_redirect": 1, "no_html": 1, "skip_disambig": 1}
    response = httpx.get("https://api.duckduckgo.com/", params=params, timeout=20)
    response.raise_for_status()
    data = response.json()
    results: list[dict[str, str]] = []

    for item in data.get("RelatedTopics", [])[:limit]:
        if isinstance(item, dict):
            text = item.get("Text") or ""
            url = item.get("FirstURL") or ""
            if text:
                results.append({"title": text.split(" - ")[0][:80], "url": url, "snippet": text})

    if not results:
        abstract = data.get("AbstractText")
        if abstract:
            results.append({"title": data.get("Heading", "Search result"), "url": data.get("AbstractURL", ""), "snippet": abstract})

    return results


async def fetch_url(url: str) -> dict[str, str]:
    response = httpx.get(url, timeout=20)
    response.raise_for_status()
    return {"url": url, "title": response.url.host, "content": response.text[:2000]}
