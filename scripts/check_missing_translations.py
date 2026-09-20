import sqlite3
import re
import sys

sys.stdout.reconfigure(encoding="utf-8")

with open("web/app.js", "r", encoding="utf-8") as f:
    app_js = f.read()

conn = sqlite3.connect("data/nexus.db")
cur = conn.cursor()
cur.execute("SELECT DISTINCT sub_category FROM repositories WHERE sub_category IS NOT NULL AND sub_category != ''")
subcats = [r[0] for r in cur.fetchall()]

missing = []
for sc in subcats:
    if f'"{sc}"' not in app_js:
        missing.append(sc)

print(f"Total DB subcategories: {len(subcats)}")
print(f"Missing from SUBCATEGORY_TRANSLATIONS ({len(missing)}):")
for m in missing:
    print(f'  "{m}": "",')
