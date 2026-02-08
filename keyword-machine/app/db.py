
from future import annotations
import psycopg
from psycopg.rows import dict_row
from app.config import DATABASE_URL

def get_conn():
return psycopg.connect(DATABASE_URL, row_factory=dict_row)

def init_db():
from pathlib import Path
sql = Path("/app/app/models.sql").read_text(encoding="utf-8")
with get_conn() as conn:
with conn.cursor() as cur:
cur.execute(sql)
conn.commit()
