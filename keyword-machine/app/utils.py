
from future import annotations
import hashlib
import re
from datetime import datetime, timezone
from dateutil import parser as dtparser

_word_re = re.compile(r"[A-Za-z0-9$#@']+")

def stable_id(*parts: str) -> str:
h = hashlib.sha256("||".join([p or "" for p in parts]).encode("utf-8")).hexdigest()
return h[:24]

def safe_dt(s: str | None) -> datetime | None:
if not s:
return None
try:
dt = dtparser.parse(s)
if not dt.tzinfo:
dt = dt.replace(tzinfo=timezone.utc)
return dt.astimezone(timezone.utc)
except Exception:
return None

def contains_keyword(text: str, keyword: str) -> bool:
if not text or not keyword:
return False
return keyword.lower() in text.lower()
