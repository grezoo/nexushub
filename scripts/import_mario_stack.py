import urllib.request
import json
import sqlite3
import os
import time

MARIO_REPOS = [
    {"repo": "NousResearch/hermes-agent", "main_cat": "Mesterséges Intelligencia & Adat", "sub_cat": "Autonóm Ágensek & Automatizáció"},
    {"repo": "Fission-AI/OpenSpec", "main_cat": "Mesterséges Intelligencia & Adat", "sub_cat": "Autonóm Ágensek & Automatizáció"},
    {"repo": "JuliusBrussee/caveman", "main_cat": "Mesterséges Intelligencia & Adat", "sub_cat": "Autonóm Ágensek & Automatizáció"},
    {"repo": "D4Vinci/Scrapling", "main_cat": "Rendszer, Biztonság & Segédprogramok", "sub_cat": "Gyorsindítók & Asztali Kiegészítők"},
    {"repo": "DS4SD/docling", "alt_repo": "docling-project/docling", "main_cat": "Produktivitás & Irodai Munka", "sub_cat": "PDF & Dokumentumkezelés"},
    {"repo": "VectifyAI/PageIndex", "main_cat": "Mesterséges Intelligencia & Adat", "sub_cat": "RAG & Dokumentumelemzés"},
    {"repo": "mem0ai/mem0", "main_cat": "Mesterséges Intelligencia & Adat", "sub_cat": "Autonóm Ágensek & Automatizáció"},
    {"repo": "headroomlabs-ai/headroom", "main_cat": "Mesterséges Intelligencia & Adat", "sub_cat": "Autonóm Ágensek & Automatizáció"},
    {"repo": "daytonaio/daytona", "main_cat": "Rendszer, Biztonság & Segédprogramok", "sub_cat": "Konténerek & Docker Környezetek"},
    {"repo": "sansan0/TrendRadar", "main_cat": "Produktivitás & Irodai Munka", "sub_cat": "Automatizáció & Produktivitás"},
    {"repo": "danielmiessler/Fabric", "main_cat": "Produktivitás & Irodai Munka", "sub_cat": "Automatizáció & Produktivitás"},
    {"repo": "github/spec-kit", "main_cat": "Mesterséges Intelligencia & Adat", "sub_cat": "Autonóm Ágensek & Automatizáció"},
    {"repo": "heygen-com/hyperframes", "main_cat": "Kreatív Média, Videóvágás & Fotó", "sub_cat": "Videógenerálás & Mozgókép"},
    {"repo": "calesthio/OpenMontage", "main_cat": "Kreatív Média, Videóvágás & Fotó", "sub_cat": "Videógenerálás & Mozgókép"},
    {"repo": "patchy631/ai-engineering-hub", "main_cat": "Mesterséges Intelligencia & Adat", "sub_cat": "Gépi Tanulás & Neurális Hálók"}
]

CUSTOM_METADATA = {
    "NousResearch/hermes-agent": {
        "title": "Hermes Agent",
        "title_en": "Hermes Agent — Frontier autonomous agent framework by Nous Research",
        "desc_hu": "A Nous Research zászlóshajó autonóm ágensrendszere: mély reasoning és lépésről-lépésre történő problémamegoldás fejlett nyílt modellekkel.",
        "desc_en": "Frontier autonomous agent architecture by Nous Research, featuring deep multi-step reasoning and function calling on open models."
    },
    "Fission-AI/OpenSpec": {
        "title": "OpenSpec",
        "title_en": "OpenSpec — Standardized open specification protocol for multi-agent interoperability",
        "desc_hu": "Nyílt specifikáció és protokoll autonóm AI ágensek közötti kommunikációhoz, adatcseréhez és feladat-átadáshoz.",
        "desc_en": "An open standard specification defining protocols for agent communication, task handoffs, and interoperable multi-agent systems."
    },
    "JuliusBrussee/caveman": {
        "title": "Caveman",
        "title_en": "Caveman — Ultra-minimalist, fast and resilient AI agent execution framework",
        "desc_hu": "Extrém minimalista, megbízható és pehelykönnyű ágens-keretrendszer, amely sallangok nélkül futtat feladatokat.",
        "desc_en": "An ultra-minimalist, zero-bloat autonomous agent engine designed for raw speed, deterministic execution, and simplicity."
    },
    "D4Vinci/Scrapling": {
        "title": "Scrapling",
        "title_en": "Scrapling — Undetectable, lightning-fast intelligent web scraper for AI agents",
        "desc_hu": "Észrevehetetlen és intelligens web-adatbányász motor AI ágenseknek: megkerüli a bot-blokkolókat és strukturált adatot ad vissza.",
        "desc_en": "An undetectable, ultra-fast web scraping library engineered for AI agents to bypass anti-bot protections and extract clean structured text."
    },
    "DS4SD/docling": {
        "title": "Docling",
        "title_en": "Docling — Deep document parsing and multimodal PDF conversion by IBM Research",
        "desc_hu": "Az IBM Research mély dokumentum-értelmezője: átalakítja a komplex PDF-eket, beágyazott táblázatokat és képleteket tiszta Markdown/JSON formátumba.",
        "desc_en": "IBM Research's state-of-the-art document conversion engine, parsing complex PDFs, formulas, and nested tables into clean Markdown."
    },
    "VectifyAI/PageIndex": {
        "title": "PageIndex",
        "title_en": "PageIndex — High-precision page-level vector indexing and hybrid RAG search",
        "desc_hu": "Precíziós oldal-szintű vektoros indexelő: pontos forrásmegjelöléssel és minimális hallucinációval keres nagy dokumentumtárakban.",
        "desc_en": "Page-level vector indexing and retrieval framework offering pinpoint citation accuracy for complex document intelligence."
    },
    "mem0ai/mem0": {
        "title": "Mem0",
        "title_en": "Mem0 — The universal memory layer for personalized AI assistants and autonomous agents",
        "desc_hu": "Az AI ágensek univerzális memóriarétege: megjegyzi a felhasználói szokásokat, korábbi kéréseket és kontextust minden platformon.",
        "desc_en": "The leading memory layer for AI agents and personalized assistants, maintaining long-term user context across sessions and LLMs."
    },
    "headroomlabs-ai/headroom": {
        "title": "Headroom",
        "title_en": "Headroom — Context window optimization and token compression for LLM agents",
        "desc_hu": "Kontextus-optimalizáló és token-tömörítő motor: drasztikusan csökkenti az API költségeket és növeli az ágensek memóriáját.",
        "desc_en": "Intelligent context-window optimizer and token compressor for agents, slashing inference costs while preserving critical semantic context."
    },
    "daytonaio/daytona": {
        "title": "Daytona",
        "title_en": "Daytona — The open-source automated development environment and dev workspace manager",
        "desc_hu": "Egyetlen paranccsal felépülő, teljes értékű felhős és helyi fejlesztői környezet, amit AI ágensek és fejlesztők is azonnal használhatnak.",
        "desc_en": "The open-source development environment manager that automates standardized dev workspace creation locally or in the cloud."
    },
    "sansan0/TrendRadar": {
        "title": "TrendRadar",
        "title_en": "TrendRadar — Real-time multi-platform trend scanner and intelligence aggregator",
        "desc_hu": "Valós idejű többplatformos trendfigyelő: egyszerre pásztázza a GitHubot, Twittert, Redditet és hírportálokat a kitörő trendekért.",
        "desc_en": "A real-time trend intelligence scanner monitoring GitHub, social media, and developer communities for breaking technological shifts."
    },
    "danielmiessler/Fabric": {
        "title": "Fabric",
        "title_en": "Fabric — Open-source human augmentation framework and AI prompt architecture by Daniel Miessler",
        "desc_hu": "Daniel Miessler híres nyílt forráskódú prompt-architektúrája: moduláris feladat-minták (Patterns) cikkösszegzésre, kódolásra és elemzésre.",
        "desc_en": "Daniel Miessler's celebrated open-source framework for augmenting humans with AI through modular, task-specific prompt patterns."
    },
    "github/spec-kit": {
        "title": "Spec Kit",
        "title_en": "Spec Kit — GitHub's official toolkit for defining structured repository specifications and agent actions",
        "desc_hu": "A GitHub hivatalos eszközkészlete: strukturált repó-specifikációk definiálása és összekötése autonóm AI folyamatokkal.",
        "desc_en": "GitHub's toolkit for creating structured repository specifications, enabling automated agent workflows and programmatic actions."
    },
    "patchy631/ai-engineering-hub": {
        "title": "AI Engineering Hub",
        "title_en": "AI Engineering Hub — Production-grade AI architectures, tutorials, and agent code templates",
        "desc_hu": "Gyakorlati AI mérnöki tudástár: élesben bevált multi-ágens sablonok, RAG architektúrák, finomhangolási és deploy receptek.",
        "desc_en": "A comprehensive repository of production-ready AI engineering templates, agent workflows, RAG pipelines, and LLM implementations."
    }
}

base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
db_path = os.path.join(base_dir, "data", "nexus.db")
cat_path = os.path.join(base_dir, "data", "catalogue.json")

conn = sqlite3.connect(db_path)
cursor = conn.cursor()
cursor.execute("SELECT repo_name FROM repositories")
existing_repos = {r[0].lower(): True for r in cursor.fetchall()}

with open(cat_path, "r", encoding="utf-8") as f:
    cat = json.load(f)

inserted_count = 0

for item_info in MARIO_REPOS:
    repo = item_info["repo"]
    alt = item_info.get("alt_repo")
    
    if repo.lower() in existing_repos or (alt and alt.lower() in existing_repos):
        print(f"[ALREADY EXISTS] {repo}")
        continue

    live_repo = repo
    try:
        url = f"https://api.github.com/repos/{repo}"
        req = urllib.request.Request(url, headers={"User-Agent": "NexusHub-Importer/2.0"})
        with urllib.request.urlopen(req, timeout=8) as resp:
            gh_data = json.loads(resp.read().decode("utf-8"))
    except Exception as e:
        if alt:
            try:
                url = f"https://api.github.com/repos/{alt}"
                req = urllib.request.Request(url, headers={"User-Agent": "NexusHub-Importer/2.0"})
                with urllib.request.urlopen(req, timeout=8) as resp:
                    gh_data = json.loads(resp.read().decode("utf-8"))
                    live_repo = alt
            except Exception as e2:
                print(f"[-] Could not fetch {repo} or {alt}: {e2}")
                continue
        else:
            print(f"[-] Could not fetch {repo}: {e}")
            continue

    meta = CUSTOM_METADATA.get(repo) or CUSTOM_METADATA.get(live_repo) or {}
    stars = int(gh_data.get("stargazers_count") or 1000)
    title = meta.get("title") or gh_data.get("name") or live_repo.split("/")[1]
    title_en = meta.get("title_en") or f"{title} — {gh_data.get('description', '')}"
    desc_hu = meta.get("desc_hu") or gh_data.get("description") or ""
    desc_en = meta.get("desc_en") or gh_data.get("description") or ""
    function_title = f"{title} — {desc_hu[:60]}..."
    year = int((gh_data.get("created_at") or "2025")[:4])
    tags = (gh_data.get("topics") or [title.lower(), "agent", "open-source"])[:6]

    clean_item = {
        "id": f"mario-{live_repo.replace('/', '-')}",
        "repo_name": live_repo,
        "title": title,
        "function_title": function_title,
        "title_en": title_en,
        "function_title_en": title_en,
        "description": desc_hu,
        "description_en": desc_en,
        "main_category": item_info["main_cat"],
        "sub_category": item_info["sub_cat"],
        "thumbnail_url": f"https://opengraph.githubassets.com/1/{live_repo}",
        "video_url": "",
        "has_video": False,
        "video_demo": "",
        "stars": stars,
        "year": year,
        "url": gh_data.get("html_url", f"https://github.com/{live_repo}"),
        "creator": live_repo.split("/")[0],
        "tags": tags,
        "is_pinned": False
    }

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
    existing_repos[live_repo.lower()] = True
    inserted_count += 1
    print(f"  [+] Added: {title} ({stars} ⭐) - {item_info['main_cat']}")
    time.sleep(0.5)

conn.commit()
conn.close()

cat["last_updated"] = time.strftime("%Y-%m-%d %H:%M:%S")
with open(cat_path, "w", encoding="utf-8") as f:
    json.dump(cat, f, ensure_ascii=False, indent=2)

print(f"\nSuccessfully imported {inserted_count} new repos from Mario Nawfal list!")
