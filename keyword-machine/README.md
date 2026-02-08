# keyword-machine

OSINT-compliant keyword trend engine:
- Collects from:
  - Reddit public JSON (no auth)
  - Google News RSS
  - GDELT 2.1 Doc API
- Stores raw items in Postgres
- Computes keyword velocity + dispersion
- Produces a daily brief + alerts

## Quickstart (Ubuntu VPS)
1) Copy `.env.example` to `.env` and edit the `REDDIT_USER_AGENT` contact field and keywords.

2) Run:
```bash
docker compose up -d --build
docker compose exec app python -m app.main collect
docker compose exec app python -m app.main analyze
docker compose exec app python -m app.main brief

crontab -e

*/15 * * * * cd /home/ubuntu/keyword-machine && docker compose exec -T app python -m app.main collect >/dev/null 2>&1
*/15 * * * * cd /home/ubuntu/keyword-machine && docker compose exec -T app python -m app.main analyze >/dev/null 2>&1
0 8 * * * cd /home/ubuntu/keyword-machine && docker compose exec -T app python -m app.main brief >> /home/ubuntu/keyword-brief.log 2>&1
