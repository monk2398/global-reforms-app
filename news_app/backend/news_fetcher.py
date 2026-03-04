from __future__ import annotations

import re
from datetime import datetime, timezone

import feedparser
import requests
from bs4 import BeautifulSoup

from database import insert_news

RSS_SOURCES = {
    "geopolitics": [
        "https://feeds.reuters.com/Reuters/worldNews",
        "http://feeds.bbci.co.uk/news/world/rss.xml",
    ],
    "defense": [
        "https://www.defensenews.com/arc/outboundfeeds/rss/category/global/?outputType=xml",
    ],
}

COUNTRY_KEYWORDS = {
    "usa": "USA",
    "united states": "USA",
    "russia": "Russia",
    "ukraine": "Ukraine",
    "china": "China",
    "israel": "Israel",
    "iran": "Iran",
    "india": "India",
    "pakistan": "Pakistan",
    "taiwan": "Taiwan",
}

WAR_KEYWORDS = {"war", "missile", "strike", "troops", "battle", "conflict", "invasion"}
DEFENSE_KEYWORDS = {"defense", "military", "navy", "air force", "army", "security"}
DIPLOMACY_KEYWORDS = {"summit", "talks", "sanctions", "treaty", "diplomacy", "ceasefire"}


def extract_article_text(url: str) -> str:
    try:
        response = requests.get(url, timeout=12)
        response.raise_for_status()
    except requests.RequestException:
        return ""

    soup = BeautifulSoup(response.text, "html.parser")
    paragraphs = [p.get_text(" ", strip=True) for p in soup.find_all("p")]
    return " ".join(paragraphs)


def summarize_text(text: str, max_words: int = 60) -> str:
    clean = re.sub(r"\s+", " ", text).strip()
    if not clean:
        return "Summary unavailable from source content."

    words = clean.split()
    short = words[:max_words]
    summary = " ".join(short)
    if len(words) > max_words:
        summary += "..."
    return summary


def detect_tags(text: str) -> list[str]:
    lowered = text.lower()
    tags = set()

    if any(word in lowered for word in WAR_KEYWORDS):
        tags.add("war")
    if any(word in lowered for word in DEFENSE_KEYWORDS):
        tags.add("defense")
    if any(word in lowered for word in DIPLOMACY_KEYWORDS):
        tags.add("diplomacy")
    if any(word in lowered for word in COUNTRY_KEYWORDS):
        tags.add("geopolitics")

    countries = {label for key, label in COUNTRY_KEYWORDS.items() if key in lowered}
    tags.update(sorted(countries))

    return sorted(tags) if tags else ["geopolitics"]


def map_source_to_category(source_name: str) -> str:
    normalized = source_name.lower()
    if "defense" in normalized:
        return "defense"
    if any(word in normalized for word in ["war", "military"]):
        return "war"
    return "geopolitics"


def fetch_and_store_news() -> int:
    inserted_count = 0
    for _, feeds in RSS_SOURCES.items():
        for feed_url in feeds:
            parsed_feed = feedparser.parse(feed_url)
            for entry in parsed_feed.entries[:8]:
                article_url = entry.get("link")
                if not article_url:
                    continue

                content = extract_article_text(article_url)
                source_text = f"{entry.get('title', '')} {entry.get('summary', '')} {content}"
                summary = summarize_text(source_text)
                tags = detect_tags(source_text)

                news_record = {
                    "title": entry.get("title", "Untitled"),
                    "summary": summary,
                    "category": map_source_to_category(entry.get("source", {}).get("title", "")),
                    "image_url": "https://images.unsplash.com/photo-1585829365295-ab7cd400c167",
                    "source": entry.get("source", {}).get("title", "RSS Feed"),
                    "published_at": datetime.now(timezone.utc).isoformat(),
                    "tags": ",".join(tags),
                }
                insert_news(news_record)
                inserted_count += 1

    return inserted_count
