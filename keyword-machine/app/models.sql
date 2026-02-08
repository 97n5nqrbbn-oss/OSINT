
CREATE TABLE IF NOT EXISTS raw_items (
id BIGSERIAL PRIMARY KEY,
source TEXT NOT NULL, -- reddit | google_news_rss | gdelt
source_detail TEXT, -- subreddit, rss query, etc.
item_id TEXT NOT NULL, -- platform id or stable hash
url TEXT,
title TEXT,
content TEXT,
author TEXT,
published_at TIMESTAMPTZ,
collected_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
lang TEXT,
extra JSONB,
UNIQUE(source, item_id)
);

CREATE TABLE IF NOT EXISTS keyword_stats (
id BIGSERIAL PRIMARY KEY,
keyword TEXT NOT NULL,
window_start TIMESTAMPTZ NOT NULL,
window_end TIMESTAMPTZ NOT NULL,
total_mentions INT NOT NULL,
sources JSONB NOT NULL, -- {"reddit": 12, "gdelt": 4, ...}
z_velocity DOUBLE PRECISION NOT NULL,
dispersion_sources INT NOT NULL,
created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
UNIQUE(keyword, window_start, window_end)
);

CREATE TABLE IF NOT EXISTS alerts (
id BIGSERIAL PRIMARY KEY,
keyword TEXT NOT NULL,
window_start TIMESTAMPTZ NOT NULL,
window_end TIMESTAMPTZ NOT NULL,
z_velocity DOUBLE PRECISION NOT NULL,
dispersion_sources INT NOT NULL,
created_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);
