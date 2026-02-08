
from future import annotations
import time
import feedparser
from app.utils import stable_id, safe_dt

def rss_url(keyword: str, lang: str = "en", country: str = "US") -> str:
q = keyword.replace(" ", "+")
return f"https://news.google.com/rss/search?q={q}&hl={lang}&gl={country}&ceid={country}:{lang}
"

def collect(keywords: list[str], lang: str, country: str, max_per_kw: int = 30) -> list[dict]:
out: list[dict] = []
for kw in keywords:
url = rss_url(kw, lang=lang, country=country)
try:
feed = feedparser.parse(url)
for e in feed.entries[:max_per_kw]:
title = e.get("title", "")
link = e.get("link", "")
published = e.get("published") or e.get("updated")
out.append({
"source": "google_news_rss",
"source_detail": f"q={kw}",
"item_id": stable_id("gnews", kw, title, link),
"url": link,
"title": title,
"content": e.get("summary", ""),
"author": None,
"published_at": safe_dt(published),
"lang": lang,
"extra": {"keyword": kw},
})
except Exception:
pass
time.sleep(0.7)
return out
