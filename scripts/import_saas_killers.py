import urllib.request
import json
import sqlite3
import os
import time
import sys

sys.stdout.reconfigure(encoding="utf-8")

SAAS_KILLERS = [
    {
        "repo": "yt-dlp/yt-dlp",
        "title": "yt-dlp",
        "main_cat": "Kreatív Média, Videóvágás & Fotó",
        "sub_cat": "Videógenerálás & Mozgókép",
        "desc_hu": "Ingyenes, parancssori multimédia letöltő több ezer weboldalhoz. A legnépszerűbb nyílt forráskódú YouTube és videó letöltő motor.",
        "desc_en": "A feature-rich command-line audio/video downloader with support for thousands of sites. Complete free alternative to video subscription tools."
    },
    {
        "repo": "ollama/ollama",
        "title": "Ollama",
        "main_cat": "Mesterséges Intelligencia & Adat",
        "sub_cat": "Nagy Nyelvi Modellek & LLM",
        "desc_hu": "Futtass nyílt AI modelleket a saját laptopodon fizetős API költségek nélkül. Havi többszáz dolláros számlát vált ki ingyen.",
        "desc_en": "Run open-source large language models locally without paying for API tokens. Replaces expensive monthly subscriptions with zero running cost."
    },
    {
        "repo": "lllyasviel/Fooocus",
        "title": "Fooocus",
        "main_cat": "Kreatív Média, Videóvágás & Fotó",
        "sub_cat": "3D Modellezés & Képszerkesztés",
        "desc_hu": "Midjourney minőségű képgenerálás a saját videokártyádon. Teljesen ingyenes, korlátlan offline alternatíva drága képgeneráló előfizetések helyett.",
        "desc_en": "Midjourney-quality image generation on your own GPU. Free, offline, unlimited alternative to paid image generation subscriptions."
    },
    {
        "repo": "openai/whisper",
        "title": "Whisper",
        "main_cat": "Mesterséges Intelligencia & Adat",
        "sub_cat": "Hang, Beszéd & Zene AI",
        "desc_hu": "Ingyenes, rendkívül pontos hang-szöveg átíró modell 99 nyelven az OpenAI-tól. Kiváltja a drága havidíjas átíró szolgáltatásokat (Otter.ai).",
        "desc_en": "Robust speech recognition via large-scale weak supervision across 99 languages. High-accuracy open alternative to paid transcription SaaS like Otter."
    },
    {
        "repo": "plausible/analytics",
        "title": "Plausible Analytics",
        "main_cat": "Produktivitás & Irodai Munka",
        "sub_cat": "Automatizáció & Produktivitás",
        "desc_hu": "Könnyűsúlyú, adatvédelmet tisztelő nyílt forráskódú webanalitika. Cookie-mentes, GDPR-kompatibilis Google Analytics alternatíva.",
        "desc_en": "Simple, open-source, lightweight (< 1 KB) and privacy-first web analytics. Free self-hosted Google Analytics alternative."
    },
    {
        "repo": "AppFlowy-IO/AppFlowy",
        "title": "AppFlowy",
        "main_cat": "Produktivitás & Irodai Munka",
        "sub_cat": "Automatizáció & Produktivitás",
        "desc_hu": "A nyílt forráskódú Notion alternatíva: feladatkezelés, wiki, adatbázisok és jegyzetek saját szerveren vagy lokálisan, korlátlan felhasználóval.",
        "desc_en": "Open-source Notion alternative giving you 100% data control with wiki, docs, and project boards without per-user subscription fees."
    },
    {
        "repo": "penpot/penpot",
        "title": "Penpot",
        "main_cat": "Kreatív Média, Videóvágás & Fotó",
        "sub_cat": "3D Modellezés & Képszerkesztés",
        "desc_hu": "A Figma első számú nyílt forráskódú alternatívája: web-alapú UI/UX tervezés és prototípus-készítés szabványos SVG formátumban csapatoknak.",
        "desc_en": "The open-source design and prototyping platform for product teams. Native web standards (SVG/CSS) alternative to Figma."
    },
    {
        "repo": "n8n-io/n8n",
        "title": "n8n",
        "main_cat": "Produktivitás & Irodai Munka",
        "sub_cat": "Automatizáció & Produktivitás",
        "desc_hu": "A Zapier nyílt forráskódú kihívója: vizuális munkafolyamat-automatizáció több száz integrációval, natív AI lépésekkel és korlátlan futtatással.",
        "desc_en": "Fair-code workflow automation platform with native AI capabilities. Self-hostable alternative to Zapier without task limits."
    },
    {
        "repo": "calcom/cal.com",
        "title": "Cal.com",
        "main_cat": "Produktivitás & Irodai Munka",
        "sub_cat": "Automatizáció & Produktivitás",
        "desc_hu": "A Calendly nyílt forráskódú alternatívája: időpontfoglalási infrastruktúra fejlesztőknek és cégeknek naptárszinkronizációval és beágyazhatósággal.",
        "desc_en": "Scheduling infrastructure for everyone. Open source Calendly alternative with white-labeling, calendar sync, and API integrations."
    },
    {
        "repo": "bitwarden/server",
        "title": "Bitwarden",
        "main_cat": "Rendszer, Biztonság & Segédprogramok",
        "sub_cat": "Kiberbiztonság & Jelszókezelők",
        "desc_hu": "A legmegbízhatóbb nyílt forráskódú jelszókezelő (1Password / LastPass alternatíva): végpontok közötti titkosítás, kétlépcsős azonosítás.",
        "desc_en": "Open source password management solution with end-to-end zero-knowledge encryption. Free self-hosted alternative to 1Password."
    }
]

def run_import():
    db_path = os.path.join(os.path.dirname(__file__), "..", "data", "nexus.db")
    cat_path = os.path.join(os.path.dirname(__file__), "..", "data", "catalogue.json")

    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    existing_repos = {}
    for row in cursor.execute("SELECT repo_name FROM repositories"):
        if row[0]:
            existing_repos[row[0].lower()] = True

    with open(cat_path, "r", encoding="utf-8") as f:
        cat = json.load(f)

    inserted = 0
    updated = 0

    print("Importing 10 Open-Source SaaS Killers...")

    for item in SAAS_KILLERS:
        repo = item["repo"]
        # Query GitHub API
        gh_data = {}
        try:
            req = urllib.request.Request(f"https://api.github.com/repos/{repo}", headers={"User-Agent": "NexusHub-Curator/2.0"})
            with urllib.request.urlopen(req, timeout=8) as resp:
                gh_data = json.loads(resp.read().decode("utf-8"))
        except Exception:
            pass

        stars = int(gh_data.get("stargazers_count") or 25000)
        title = item["title"]
        title_en = f"{title} — {item['desc_en'][:80]}..."
        desc_hu = item["desc_hu"]
        desc_en = item["desc_en"]
        function_title = f"{title} — {desc_hu[:60]}..."
        year = int((gh_data.get("created_at") or "2023")[:4])
        tags = (gh_data.get("topics") or [title.lower(), "saas-alternative", "open-source", "self-hosted"])[:6]

        clean_item = {
            "id": f"saas-{repo.replace('/', '-')}",
            "repo_name": repo,
            "title": title,
            "function_title": function_title,
            "title_en": title_en,
            "function_title_en": title_en,
            "description": desc_hu,
            "description_en": desc_en,
            "main_category": item["main_cat"],
            "sub_category": item["sub_cat"],
            "thumbnail_url": f"https://opengraph.githubassets.com/1/{repo}",
            "video_url": "",
            "has_video": False,
            "video_demo": "",
            "stars": stars,
            "year": year,
            "url": gh_data.get("html_url", f"https://github.com/{repo}"),
            "creator": repo.split("/")[0],
            "tags": tags,
            "is_pinned": False
        }

        if repo.lower() in existing_repos:
            cursor.execute("""
                UPDATE repositories 
                SET title = ?, function_title = ?, title_en = ?, function_title_en = ?,
                    description = ?, description_en = ?, stars = ?, main_category = ?, sub_category = ?
                WHERE LOWER(repo_name) = LOWER(?)
            """, (
                clean_item["title"], clean_item["function_title"], clean_item["title_en"], clean_item["function_title_en"],
                clean_item["description"], clean_item["description_en"], clean_item["stars"],
                clean_item["main_category"], clean_item["sub_category"], repo
            ))
            for it in cat.get("items", []):
                if it.get("repo_name", "").lower() == repo.lower():
                    it.update(clean_item)
            updated += 1
            print(f"  [*] Updated: {title} ({stars} ⭐)")
        else:
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
            cat.setdefault("items", []).insert(0, clean_item)
            existing_repos[repo.lower()] = True
            inserted += 1
            print(f"  [+] Inserted: {title} ({stars} ⭐) - {item['main_cat']}")

        time.sleep(0.3)

    conn.commit()
    conn.close()

    cat["last_updated"] = time.strftime("%Y-%m-%d %H:%M:%S")
    with open(cat_path, "w", encoding="utf-8") as f:
        json.dump(cat, f, ensure_ascii=False, indent=2)

    print(f"\nDone! Inserted: {inserted}, Updated: {updated}")

if __name__ == "__main__":
    run_import()
