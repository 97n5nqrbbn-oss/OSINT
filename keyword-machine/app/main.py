
from future import annotations
import sys
from app.db import init_db
from app.pipeline import collect, analyze, brief

def main():
if len(sys.argv) < 2:
print("Usage: python -m app.main [init|collect|analyze|brief]")
sys.exit(1)

cmd = sys.argv[1].lower()\n\nif cmd == "init":\n    init_db()\n    print("DB initialized.")\n    return\n\nif cmd == "collect":\n    res = collect.run()\n    print(res)\n    return\n\nif cmd == "analyze":\n    res = analyze.run(hours=1)\n    print(res)\n    return\n\nif cmd == "brief":\n    data = brief.run(top_n=12, hours_back=24)\n    brief.print_brief(data)\n    return\n\nraise SystemExit(f"Unknown command: {cmd}")\n
if name == "main":
main()
