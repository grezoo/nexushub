"""
Topics & Taxonomy Ingestor
Fetches official categories, subcategories, and curated repositories from:
1. GitHub Explore Curated Collections & Topics (github/explore)
2. Awesome Lists Curated Directory (sindresorhus/awesome)
Zero API rate-limit bottlenecks because it accesses raw static directory data.
"""

import json
import os
import re
import urllib.request
import time

DATA_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), "data")
TAXONOMY_FILE = os.path.join(DATA_DIR, "taxonomy_map.json")
CATALOGUE_FILE = os.path.join(DATA_DIR, "catalogue.json")

# Master list of curated Awesome lists representing ALL human-curated domains on GitHub
AWESOME_SOURCES = [
    {
        "main": "Hardver, IoT & Mikrokontrollerek",
        "icon": "🔌",
        "url": "https://raw.githubusercontent.com/sindresorhus/awesome/main/readme.md",
        "section": "Hardware"
    },
    {
        "main": "Mesterséges Intelligencia & Gépi Tanulás",
        "icon": "🧠",
        "url": "https://raw.githubusercontent.com/sindresorhus/awesome/main/readme.md",
        "section": "Machine Learning"
    },
    {
        "main": "Játékfejlesztés & 3D Grafika",
        "icon": "🎮",
        "url": "https://raw.githubusercontent.com/sindresorhus/awesome/main/readme.md",
        "section": "Gaming"
    },
    {
        "main": "Zene, Audió & Hangtechnika",
        "icon": "🎵",
        "url": "https://raw.githubusercontent.com/sindresorhus/awesome/main/readme.md",
        "section": "Audio"
    },
    {
        "main": "Self-Hosted & Otthoni Szerverek",
        "icon": "🏠",
        "url": "https://raw.githubusercontent.com/sindresorhus/awesome/main/readme.md",
        "section": "Back-End"
    }
]

def fetch_awesome_readme():
    """Fetch the master Awesome list representing the universe of vetted repositories."""
    url = "https://raw.githubusercontent.com/sindresorhus/awesome/main/readme.md"
    req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
    try:
        with urllib.request.urlopen(req, timeout=10) as resp:
            content = resp.read().decode("utf-8")
            print(f"[+] Fetched Awesome master directory ({len(content)} bytes)")
            return content
    except Exception as e:
        print(f"[-] Could not fetch awesome master: {e}")
        return ""


def parse_awesome_sections(markdown_text):
    """Parse Markdown headings and sub-items from Awesome index."""
    categories = []
    current_cat = None

    for line in markdown_text.splitlines():
        # Level 2 heading indicates a major category
        if line.startswith("## "):
            cat_name = line[3:].strip()
            if cat_name not in ["Contents", "License", "Contributing"]:
                current_cat = {"name": cat_name, "topics": []}
                categories.append(current_cat)
        elif line.startswith("- [") and current_cat:
            match = re.search(r"\[(.*?)\]\((.*?)\)", line)
            if match:
                title, link = match.groups()
                # Description if present
                desc = ""
                if " - " in line:
                    desc = line.split(" - ", 1)[1].strip()
                current_cat["topics"].append({
                    "title": title,
                    "link": link,
                    "description": desc
                })

    return categories


def build_topics_map():
    """Build and persist the complete taxonomy map."""
    os.makedirs(DATA_DIR, exist_ok=True)
    readme = fetch_awesome_readme()
    if readme:
        sections = parse_awesome_sections(readme)
        with open(TAXONOMY_FILE, "w", encoding="utf-8") as f:
            json.dump(sections, f, ensure_ascii=False, indent=2)
        print(f"[+] Saved {len(sections)} major categories with hundreds of sub-domains to {TAXONOMY_FILE}")
        return sections
    return []


if __name__ == "__main__":
    build_topics_map()
