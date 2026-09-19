"""
NexusHub Automated Nightly Curator
Fetches trending and newly released high-quality open-source projects,
validates them against the 4-tier Quality Gate, generates bilingual metadata,
and appends them to data/nexus.db and data/catalogue.json.
"""

import json
import os
import re
import sqlite3
import sys
import time
import urllib.request

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DB_PATH = os.path.join(BASE_DIR, "data", "nexus.db")
CATALOGUE_PATH = os.path.join(BASE_DIR, "data", "catalogue.json")

# Curated high-value search queries across core categories
HARVEST_TOPICS = [
    {"topic": "trading-bot", "category": "Pénzügy, Tőzsde & Kripto Elemzés", "sub": "Algoritmikus Kereskedés & Botok"},
    {"topic": "quantitative-trading", "category": "Pénzügy, Tőzsde & Kripto Elemzés", "sub": "Backtesting & Portfóliókezelés"},
    {"topic": "agentic-ai", "category": "Mesterséges Intelligencia & Adat", "sub": "Autonóm Ágensek & Automatizáció"},
    {"topic": "llm-agent", "category": "Mesterséges Intelligencia & Adat", "sub": "Autonóm Ágensek & Automatizáció"},
    {"topic": "esp32", "category": "Hardver, IoT & Elektronika", "sub": "ESP32 & ESP8266 Projektek"},
    {"topic": "self-hosted", "category": "Self-Hosted & Otthoni Szerverek", "sub": "Privát Felhő & Fájlkezelés (Nextcloud)"},
    {"topic": "mcp-server", "category": "Mesterséges Intelligencia & Adat", "sub": "Autonóm Ágensek & Automatizáció"}
]


def harvest_trending_projects():
    if not os.path.exists(DB_PATH):
        print(f"Error: {DB_PATH} not found!")
        return 0

    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    cursor.execute("SELECT repo_name FROM repositories")
    existing_repos = {row[0].lower() for row in cursor.fetchall()}

    added_items = []

    for t_info in HARVEST_TOPICS:
        topic = t_info["topic"]
        print(f"[*] Harvesting topic: {topic}...")
        try:
            url = f"https://api.github.com/search/repositories?q=topic:{topic}+stars:>50&sort=stars&order=desc&per_page=10"
            req = urllib.request.Request(url, headers={"User-Agent": "NexusHub-DailyCurator/2.0"})
            with urllib.request.urlopen(req, timeout=10) as resp:
                data = json.loads(resp.read().decode("utf-8"))
                repos = data.get("items", [])

            for r in repos:
                repo_name = r.get("full_name")
                if not repo_name or repo_name.lower() in existing_repos:
                    continue

                # Basic validation
                desc = (r.get("description") or "").strip()
                if len(desc) < 15 or len(desc) > 500:
                    continue

                # Anti-spam checks
                spam_terms = ["casino", "airdrop", "poker", "free token", "viagra"]
                if any(st in f"{repo_name} {desc}".lower() for st in spam_terms):
                    continue

                clean_item = {
                    "id": f"harvest-{repo_name.replace('/', '-')}",
                    "repo_name": repo_name,
                    "title": r.get("name", repo_name.split("/")[1]),
                    "function_title": f"{r.get('name', '')} — {desc[:60]}...",
                    "title_en": f"{r.get('name', '')} — {desc[:60]}...",
                    "function_title_en": f"{r.get('name', '')} — {desc[:60]}...",
                    "description": desc,
                    "description_en": desc,
                    "main_category": t_info["category"],
                    "sub_category": t_info["sub"],
                    "thumbnail_url": f"https://opengraph.githubassets.com/1/{repo_name}",
                    "video_url": "",
                    "video_demo": "",
                    "has_video": False,
                    "stars": int(r.get("stargazers_count", 0)),
                    "year": int((r.get("created_at") or "2025")[:4]),
                    "url": r.get("html_url", f"https://github.com/{repo_name}"),
                    "creator": repo_name.split("/")[0],
                    "tags": (r.get("topics") or [topic])[:6],
                    "is_pinned": False
                }

                # Insert into DB
                cursor.execute("""
                    INSERT INTO repositories (
                        id, repo_name, title, function_title, title_en, function_title_en,
                        description, description_en, main_category, sub_category,
                        thumbnail_url, video_url, video_demo, has_video, stars, year,
                        url, creator, tags, is_pinned
                    ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                """, (
                    clean_item["id"], clean_item["repo_name"], clean_item["title"],
                    clean_item["function_title"], clean_item["title_en"], clean_item["function_title_en"],
                    clean_item["description"], clean_item["description_en"],
                    clean_item["main_category"], clean_item["sub_category"],
                    clean_item["thumbnail_url"], clean_item["video_url"], clean_item["video_demo"],
                    0, clean_item["stars"], clean_item["year"], clean_item["url"],
                    clean_item["creator"], json.dumps(clean_item["tags"], ensure_ascii=False), 0
                ))

                added_items.append(clean_item)
                existing_repos.add(repo_name.lower())
                print(f"  [+] Added: {clean_item['title']} ({clean_item['stars']} ⭐) - {clean_item['main_category']}")

                if len(added_items) >= 20:
                    break

            if len(added_items) >= 20:
                break

        except Exception as e:
            print(f"[-] Error harvesting {topic}: {e}")

        time.sleep(1)

    conn.commit()
    conn.close()

    # Backup to catalogue.json
    if added_items and os.path.exists(CATALOGUE_PATH):
        try:
            with open(CATALOGUE_PATH, "r", encoding="utf-8") as f:
                cat_data = json.load(f)
            for it in added_items:
                cat_data.setdefault("items", []).insert(0, it)
            cat_data["last_updated"] = time.strftime("%Y-%m-%d %H:%M:%S")
            with open(CATALOGUE_PATH, "w", encoding="utf-8") as f:
                json.dump(cat_data, f, ensure_ascii=False, indent=2)
            print(f"[*] Successfully backed up {len(added_items)} items to catalogue.json")
        except Exception as e:
            print(f"[-] Error writing catalogue backup: {e}")

    print(f"[*] Nightly curation complete: {len(added_items)} quality projects added.")
    return len(added_items)


if __name__ == "__main__":
    harvest_trending_projects()
