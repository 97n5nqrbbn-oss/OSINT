
from future import annotations
import time
import requests
from app.utils import stable_id, safe_dt

BASE = "https://api.gdeltproject.org/api/v2/doc/doc
"

def collect(keywords: list[str], max_results: int = 50) -> list[dict]:
out: list[dict] = []
for kw in keywords:
params = {
"query": kw,
"mode": "ArtList",
"format": "json",
"maxrecords": max_results,
"sort": "HybridRel",
}
try:
r = requests.get(BASE, params=params, timeout=25)
r.raise_for_status()
data = r.json()
for art in data.get("articles", []) or []:
title = art.get("title") or ""
url = art.get("url") or ""
out.append({
"source": "gdelt",
"source_detail": f"query={kw}",
"item_id": stable_id("gdelt", kw, title, url),
"url": url,
"title": title,
"content": art.get("seendate") or "",
"author": art.get("sourceCountry"),
"published_at": safe_dt(art.get("seendate")),
"lang": art.get("language"),
"extra": {
"keyword": kw,
"source": art.get("sourceCollection"),
"domain": art.get("domain"),
},
})
except Exception:
pass
time.sleep(0.6)
return out
