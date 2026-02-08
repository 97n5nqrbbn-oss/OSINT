
import os
from dotenv import load_dotenv

load_dotenv()

def env_bool(name: str, default: str = "0") -> bool:
return os.getenv(name, default).strip() in ("1", "true", "True", "yes", "Y")

DATABASE_URL = os.getenv("DATABASE_URL", "postgresql://km:km@db:5432/km")

COLLECT_REDDIT = env_bool("COLLECT_REDDIT", "1")
COLLECT_GOOGLE_NEWS_RSS = env_bool("COLLECT_GOOGLE_NEWS_RSS", "1")
COLLECT_GDELT = env_bool("COLLECT_GDELT", "1")

REDDIT_USER_AGENT = os.getenv("REDDIT_USER_AGENT", "keyword-machine/1.0")
REDDIT_SUBREDDITS = [s.strip() for s in os.getenv("REDDIT_SUBREDDITS", "wallstreetbets").split(",") if s.strip()]

KEYWORDS = [k.strip() for k in os.getenv("KEYWORDS", "").split(",") if k.strip()]

GNEWS_LANG = os.getenv("GNEWS_LANG", "en")
GNEWS_COUNTRY = os.getenv("GNEWS_COUNTRY", "US")

GDELT_MAX = int(os.getenv("GDELT_MAX", "50"))

ALERT_VELOCITY_Z = float(os.getenv("ALERT_VELOCITY_Z", "3.0"))
ALERT_DISPERSION_SOURCES = int(os.getenv("ALERT_DISPERSION_SOURCES", "2"))
