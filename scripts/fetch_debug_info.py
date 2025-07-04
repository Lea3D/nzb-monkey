#!/usr/bin/env python3
"""Fetch debugging information for BinSearch and NZBIndex.

This script downloads search result pages and sample NZB files
for both search engines. The collected information is stored
in a JSON dump file that can be shared for debugging. Progress
and errors are logged to the console.

Usage:
    python fetch_debug_info.py "search term"

If no search term is supplied, ``test`` is used.
"""

import json
import logging
import re
import sys
from datetime import datetime
from pathlib import Path
from typing import Dict, Optional

import requests


logger = logging.getLogger(__name__)

# Definitions taken from nzbmonkey.py
SEARCH_ENGINES = {
    "binsearch": {
        "search_url": "https://binsearch.info/search?q={query}",
        "regex": re.compile(
            r'href="https?://(?:www\\.)?binsearch\\.info/(?:details/|\\?action=nzb&id=)(?P<id>[^"&/]+)'
        ),
        "download_url": "https://binsearch.info/nzb?{id}=on",
    },
    "nzbindex": {
        "search_url": (
            "https://nzbindex.com/rss?q={query}&hidespam=1&sort=agedesc&complete=1"
        ),
        "regex": re.compile(
            r"<link>https://nzbindex\\.com/download/(?P<id>[0-9a-fA-F-]{36})(?:\\.nzb)?</link>"
        ),
        "download_url": "https://nzbindex.com/download/{id}.nzb",
    },
}

DUMP_FILE = Path("nzbmonkey_debug_dump.json")


def fetch_url(url: str) -> Optional[str]:
    """Return content from URL or ``None`` on error."""
    logger.info("Fetching %s", url)
    try:
        response = requests.get(url, timeout=15)
        if response.status_code == 200:
            logger.info("Fetched %s bytes", len(response.text))
            return response.text
        logger.warning("Unexpected status %s for %s", response.status_code, url)
    except requests.RequestException as exc:
        logger.error("Request failed for %s: %s", url, exc)
    return None


def fetch_engine_data(engine: str, query: str) -> Dict[str, Optional[str]]:
    """Download information for a single search engine."""
    info = SEARCH_ENGINES[engine]
    search_url = info["search_url"].format(query=query)
    search_content = fetch_url(search_url)

    logger.info("Processing results from %s", engine)

    nzb_id = None
    nzb_content = None
    download_url = None

    if search_content:
        match = info["regex"].search(search_content)
        if match:
            nzb_id = match.group("id")
            logger.info("Found NZB ID %s", nzb_id)
            download_url = info["download_url"].format(id=nzb_id)
            nzb_content = fetch_url(download_url)
        else:
            logger.warning("No NZB ID found in search results for %s", engine)
    else:
        logger.error("Failed to fetch search results for %s", engine)

    return {
        "search_url": search_url,
        "search_content": search_content,
        "nzb_id": nzb_id,
        "download_url": download_url,
        "nzb_content": nzb_content,
    }


def main(query: str) -> None:
    logging.basicConfig(level=logging.INFO, format="%(levelname)s: %(message)s")
    logger.info("Starting debug info fetch for query '%s'", query)

    result = {
        "query": query,
        "timestamp": datetime.utcnow().isoformat() + "Z",
        "results": {},
    }

    for engine in SEARCH_ENGINES:
        result["results"][engine] = fetch_engine_data(engine, query)

    DUMP_FILE.write_text(json.dumps(result, indent=2))
    logger.info("Debug information written to %s", DUMP_FILE)


if __name__ == "__main__":
    search_query = "test"
    if len(sys.argv) > 1:
        search_query = sys.argv[1]
    main(search_query)
