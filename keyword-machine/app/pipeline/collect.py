
from future import annotations
import json
from app import config
from app.db import get_conn
from app.collectors import reddit, googlenews_rss, gdelt

def upsert_raw(items: list[dict]) -> int:
if not items:
return 0
inserted = 0
with get_conn() as conn:
with conn.cursor() as cur:
for it in items:
cur.execute(
"""
INSERT INTO raw_items
(source, source_detail, item_id, url, title, content, author, published_at, lang, extra)
VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)
ON CONFLICT (source, item_id) DO NOTHING
""",
(
it["source"], it.get("source_detail"), it["item_id"], it.get("url"),
it.get("title"), it.get("content"), it.get("author"),
it.get("published_at"), it.get("lang"),
json.dumps(it.get("extra") or {}),
)
)
if cur.rowcount == 1:
inserted += 1
conn.commit()
return inserted

def run() -> dict:
all_items: list[dict] = [] 

if config.COLLECT_REDDIT:\n    all_items.extend(reddit.collect(config.REDDIT_SUBREDDITS, user_agent=config.REDDIT_USER_AGENT))\n\nif config.COLLECT_GOOGLE_NEWS_RSS:\n    all_items.extend(googlenews_rss.collect(config.KEYWORDS, lang=config.GNEWS_LANG, country=config.GNEWS_COUNTRY))\n\nif config.COLLECT_GDELT:\n    all_items.extend(gdelt.collect(config.KEYWORDS, max_results=config.GDELT_MAX))\n\ninserted = upsert_raw(all_items)\nreturn {"fetched": len(all_items), "inserted": inserted}
