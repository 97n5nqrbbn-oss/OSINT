
from future import annotations
import json
from datetime import datetime, timedelta, timezone
from collections import defaultdict
from app.db import get_conn
from app import config
from app.utils import contains_keyword

def _window(now: datetime, hours: int) -> tuple[datetime, datetime]:
end = now.replace(minute=0, second=0, microsecond=0)
start = end - timedelta(hours=hours)
return start, end

def _count_mentions(start: datetime, end: datetime) -> tuple[dict[str, int], dict[str, dict[str, int]]]:
totals: dict[str, int] = defaultdict(int)
sources: dict[str, dict[str, int]] = defaultdict(lambda: defaultdict(int))

 with get_conn() as conn:\n    with conn.cursor() as cur:\n        cur.execute(\n            """\n            SELECT source, title, content\n            FROM raw_items\n            WHERE collected_at >= %s AND collected_at < %s\n            """,\n            (start, end)\n        )\n        rows = cur.fetchall()\n\nfor r in rows:\n    text = f"{r.get('title') or ''}\n{r.get('content') or ''}"\n    for kw in config.KEYWORDS:\n        if contains_keyword(text, kw):\n            totals[kw] += 1\n            sources[kw][r["source"]] += 1\n\nreturn totals, sources

def _baseline_mean_std(keyword: str, lookback_days: int = 7) -> tuple[float, float]:
with get_conn() as conn:
with conn.cursor() as cur:
cur.execute(
"""
SELECT total_mentions
FROM keyword_stats
WHERE keyword = %s
AND window_start >= NOW() - (%s || ' days')::interval
""",
(keyword, lookback_days)
)
vals = [int(r["total_mentions"]) for r in cur.fetchall()]

if len(vals) < 10:\n    return (max(1.0, sum(vals)/max(1, len(vals))) if vals else 1.0, 1.0)\n\nmean = sum(vals) / len(vals)\nvar = sum((v - mean) ** 2 for v in vals) / (len(vals) - 1)\nstd = (var ** 0.5) if var > 0 else 1.0\nreturn mean, std\n
def run(hours: int = 1) -> dict:
now = datetime.now(timezone.utc)
start, end = _window(now, hours=hours)
totals, sources = _count_mentions(start, end)

inserted_stats = 0\ninserted_alerts = 0\n\nwith get_conn() as conn:\n    with conn.cursor() as cur:\n        for kw in config.KEYWORDS:\n            total = int(totals.get(kw, 0))\n            src_map = dict(sources.get(kw, {}))\n            dispersion = len([s for s, n in src_map.items() if n > 0])\n\n            mean, std = _baseline_mean_std(kw)\n            z = (total - mean) / (std if std else 1.0)\n\n            cur.execute(\n                """\n                INSERT INTO keyword_stats\n                (keyword, window_start, window_end, total_mentions, sources, z_velocity, dispersion_sources)\n                VALUES (%s,%s,%s,%s,%s,%s,%s)\n                ON CONFLICT (keyword, window_start, window_end) DO NOTHING\n                """,\n                (kw, start, end, total, json.dumps(src_map), float(z), int(dispersion))\n            )\n            if cur.rowcount == 1:\n                inserted_stats += 1\n\n            if z >= config.ALERT_VELOCITY_Z and dispersion >= config.ALERT_DISPERSION_SOURCES:\n                cur.execute(\n                    """\n                    INSERT INTO alerts\n                    (keyword, window_start, window_end, z_velocity, dispersion_sources)\n                    VALUES (%s,%s,%s,%s,%s)\n                    """,\n                    (kw, start, end, float(z), int(dispersion))\n                )\n                inserted_alerts += 1\n\n    conn.commit()\n\nreturn {\n    "window_start": start.isoformat(),\n    "window_end": end.isoformat(),\n    "stats_rows_inserted": inserted_stats,\n    "alerts_inserted": inserted_alerts,\n}\n
