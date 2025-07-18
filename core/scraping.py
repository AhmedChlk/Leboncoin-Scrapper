from __future__ import annotations

import json
import re
from typing import List, Dict

from scrap.infra.http_client import HttpClient
from scrap.tools.sleep_between import sleep_between

# Regex used to extract the JSON array of ads from the HTML response
_ADS_REGEX = re.compile(r'"ads"\s*:\s*(\[.*?\])', re.DOTALL)


def _replace_page(url: str, page: int) -> str:
    """Return *url* with the page query parameter set to *page*."""
    if "page=" in url:
        return re.sub(r"page=\d+", f"page={page}", url)
    sep = "&" if "?" in url else "?"
    return f"{url}{sep}page={page}"


def _extract_ads(html: str) -> List[Dict]:
    """Extract the list of ads from a Leboncoin search HTML page."""
    match = _ADS_REGEX.search(html)
    if not match:
        return []
    try:
        return json.loads(match.group(1))
    except json.JSONDecodeError:
        return []


def scrape_ads(url: str, pages: int) -> List[Dict]:
    """Scrape *pages* pages of *url* and return a list of ads as dictionaries."""
    client = HttpClient()
    all_ads: List[Dict] = []
    for i in range(1, pages + 1):
        page_url = _replace_page(url, i)
        sleep_between(1, 3)
        html = client.get(page_url)
        if not html:
            continue
        ads = _extract_ads(html)
        all_ads.extend(ads)
    return all_ads


def fetch_description_ads(url: str) -> str:
    """Return the description text from an ad page."""
    client = HttpClient()
    texte = client.get(url)
    pattern = r'"description"\s*:\s*"((?:[^"\\]|\\.)*)"'
    match = re.search(pattern, texte or "", re.DOTALL)
    if match:
        import codecs
        return codecs.decode(match.group(1), "unicode_escape")
    raise ValueError("Description non trouvée")
