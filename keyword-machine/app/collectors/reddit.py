
from future import annotations
import time
import requests
from typing import Iterable
from app.utils import stable_id, safe_dt

BASE = "https://www.reddit.com
"

def fetch_subreddit_new(subreddit: str, user_agent: str, limit: int = 100) -> list[dict]:
url = f"{BASE}/r/{subreddit}/new.json?limit={limit}"
headers = {"User-Agent": user_agent}
r = requests.get(url, headers=headers, timeout=20)
r.raise_for_status()
data = r.json()
children = data.get("data", {}).get("children", [])
items = []
for c in children:
d = c.get("data", {})
title = d.get("title", "")
selftext = d.get("selftext", "")
permalink = d.get("permalink", "")
full_url = f"{BASE}{permalink}" if permalink else d.get("url", "")
created = d.get("created_utc")
published_at = None
if created:
published_at = safe_dt(str(created))
items.append({
"source": "reddit",
"source_detail": f"r/{subreddit}",
"item_id": d.get("id") or stable_id(subreddit, title, full_url),
"url": full_url,
"title": title,
"content": selftext,
"author": d.get("author"),
"published_at": published_at,
"lang": "en",
"extra": {"score": d.get("score"), "num_comments": d.get("num_comments")},
})
return items

def collect(subreddits: Iterable[str], user_agent: str) -> list[dict]:
out: list[dict] = []
for s in subreddits:
s = s.strip()
if not s:
continue
try:
out.extend(fetch_subreddit_new(s, user_agent=user_agent))
except Exception:
continue
time.sleep(1.2) # polite rate limit
return out
