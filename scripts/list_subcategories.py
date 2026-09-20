import sqlite3
import json
import sys

sys.stdout.reconfigure(encoding="utf-8")

conn = sqlite3.connect("data/nexus.db")
cur = conn.cursor()
cur.execute("SELECT DISTINCT sub_category FROM repositories WHERE sub_category IS NOT NULL AND sub_category != '' ORDER BY sub_category")
subcats = [r[0] for r in cur.fetchall()]

print(f"Total distinct subcategories in DB: {len(subcats)}")
for sc in subcats:
    print(f"  {sc}")
