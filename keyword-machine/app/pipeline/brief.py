
from future import annotations
from datetime import datetime, timedelta, timezone
from app.db import get_conn

def run(top_n: int = 12, hours_back: int = 24) -> dict:
now = datetime.now(timezone.utc)
start = now - timedelta(hours=hours_back)

with get_conn() as conn:\n    with conn.cursor() as cur:\n        cur.execute(\n            """\n            SELECT keyword,\n                   SUM(total_mentions) AS mentions,\n                   MAX(z_velocity) AS max_z,\n                   MAX(dispersion_sources) AS max_dispersion\n            FROM keyword_stats\n            WHERE window_start >= %s\n            GROUP BY keyword\n            ORDER BY MAX(z_velocity) DESC, SUM(total_mentions) DESC\n            LIMIT %s\n            """,\n            (start, top_n)\n        )\n        rows = cur.fetchall()\n\n        cur.execute(\n            """\n            SELECT keyword, window_start, window_end, z_velocity, dispersion_sources, created_at\n            FROM alerts\n            WHERE created_at >= %s\n            ORDER BY created_at DESC\n            LIMIT 50\n            """,\n            (start,)\n        )\n        alerts = cur.fetchall()\n\nreturn {\n    "since": start.isoformat(),\n    "top": rows,\n    "alerts": alerts\n}\n
 def print_brief(data: dict):
print("\n=== KEYWORD MACHINE — DAILY BRIEF ===")
print(f"Window (lookback): {data['since']} → now\n")
print("Top movers (by max z-velocity):")
for r in data["top"]:
print(f" - {r['keyword']}: mentions={r['mentions']} max_z={round(float(r['max_z']),2)} max_dispersion={int(r['max_dispersion'])}")
print("\nRecent alerts:")
if not data["alerts"]:
print(" (none)")
else:
for a in data["alerts"][:15]:
print(f" ! {a['keyword']} z={round(float(a['z_velocity']),2)} dispersion={int(a['dispersion_sources'])} at {a['created_at']}")
print("")
