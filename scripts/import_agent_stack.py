import urllib.request
import json
import sqlite3
import os
import time

REPOS_TO_IMPORT = [
    {"repo": "bytedance/deer-flow", "main_cat": "Mesterséges Intelligencia & Adat", "sub_cat": "Autonóm Ágensek & Automatizáció"},
    {"repo": "infiniflow/ragflow", "main_cat": "Mesterséges Intelligencia & Adat", "sub_cat": "RAG & Dokumentumelemzés"},
    {"repo": "QuivrHQ/quivr", "main_cat": "Produktivitás & Irodai Munka", "sub_cat": "Jegyzetelés & Ismeretbázis (Obsidian / Logseq)"},
    {"repo": "MemPalace/mempalace", "main_cat": "Mesterséges Intelligencia & Adat", "sub_cat": "Autonóm Ágensek & Automatizáció"},
    {"repo": "RSSNext/Folo", "main_cat": "Produktivitás & Irodai Munka", "sub_cat": "Automatizáció & Produktivitás"},
    {"repo": "OpenBB-finance/OpenBB", "main_cat": "Pénzügy, Tőzsde & Kripto Elemzés", "sub_cat": "Piaci Elemzés & Diagramok"},
    {"repo": "mindsdb/mindshub", "main_cat": "Mesterséges Intelligencia & Adat", "sub_cat": "Autonóm Ágensek & Automatizáció"},
    {"repo": "agno-agi/agno", "main_cat": "Mesterséges Intelligencia & Adat", "sub_cat": "Autonóm Ágensek & Automatizáció"},
    {"repo": "code-yeongyu/oh-my-openagent", "main_cat": "Rendszer, Biztonság & Segédprogramok", "sub_cat": "Terminálok & Shell Eszközök"},
    {"repo": "block/goose", "alt_repo": "aaif-goose/goose", "main_cat": "Mesterséges Intelligencia & Adat", "sub_cat": "Autonóm Ágensek & Automatizáció"},
    {"repo": "continuedev/continue", "main_cat": "Produktivitás & Irodai Munka", "sub_cat": "Automatizáció & Produktivitás"},
    {"repo": "unslothai/unsloth", "main_cat": "Mesterséges Intelligencia & Adat", "sub_cat": "Gépi Tanulás & Neurális Hálók"},
    {"repo": "hiyouga/LlamaFactory", "main_cat": "Mesterséges Intelligencia & Adat", "sub_cat": "Gépi Tanulás & Neurális Hálók"},
    {"repo": "CopilotKit/CopilotKit", "main_cat": "Produktivitás & Irodai Munka", "sub_cat": "Automatizáció & Produktivitás"},
    {"repo": "Dokploy/dokploy", "main_cat": "Self-Hosted & Otthoni Szerverek", "sub_cat": "Privát Felhő & Fájlkezelés (Nextcloud)"}
]

CUSTOM_METADATA = {
    "bytedance/deer-flow": {
        "title": "DeerFlow",
        "title_en": "DeerFlow — ByteDance's deep research and agentic workflow orchestration engine",
        "desc_hu": "A ByteDance kutatólaboratóriumának mély kutatási és multi-ágens munkafolyamat-szervező keretrendszere komplex feladatok párhuzamos végrehajtására.",
        "desc_en": "ByteDance's deep research and autonomous agent orchestration engine designed to decompose complex queries into parallel search and reasoning tasks."
    },
    "infiniflow/ragflow": {
        "title": "RAGFlow",
        "title_en": "RAGFlow — Next-generation RAG engine with deep document understanding for complex enterprise data",
        "desc_hu": "Következő generációs, nyílt forráskódú RAG motor, amely mély dokumentum-értelmezéssel strukturálja a legbonyolultabb PDF-eket, táblázatokat és prezentációkat.",
        "desc_en": "An open-source RAG engine based on deep document understanding, capable of extracting structured knowledge from complex templates, PDFs, and spreadsheets."
    },
    "QuivrHQ/quivr": {
        "title": "Quivr",
        "title_en": "Quivr — Your open-source generative second brain for all personal documents and files",
        "desc_hu": "A te privát 'második agyad': tölts fel PDF-eket, prezentációkat, képeket vagy linkeket, és a generatív AI azonnal válaszol belőlük 100% adatvédelemmel.",
        "desc_en": "Your open-source generative second brain. Dump your files (PDFs, docs, audio) and chat with them using local or cloud LLMs with total privacy."
    },
    "MemPalace/mempalace": {
        "title": "MemPalace",
        "title_en": "MemPalace — Persistent long-term associative memory architecture for autonomous AI agents",
        "desc_hu": "Hosszútávú asszociatív memóriapalota AI ágenseknek: lehetővé teszi, hogy az ágensek ne felejtsék el a korábbi munkameneteket és összefüggéseket.",
        "desc_en": "A long-term associative memory architecture for autonomous agents, inspired by the method of loci, maintaining persistent cross-session knowledge."
    },
    "RSSNext/Folo": {
        "title": "Folo",
        "title_en": "Folo — Intelligent, modern information feed and source monitor powered by AI",
        "desc_hu": "Intelligens információs hírfolyam és forrásfigyelő: összegzi a globális tech híreket, blogokat és RSS-eket, kiszűrve a zajt.",
        "desc_en": "A smart, minimalist information feed and source reader that curates, summarizes, and cleans tech feeds using AI."
    },
    "OpenBB-finance/OpenBB": {
        "title": "OpenBB Terminal",
        "title_en": "OpenBB — The premier open-source investment research terminal and financial intelligence platform",
        "desc_hu": "A Bloomberg Terminal nyílt forráskódú alternatívája: tőzsdei adatok, makrogazdaság, opciók, fundamentális elemzés és kriptovaluta egyetlen professzionális platformon.",
        "desc_en": "The premier open-source investment research terminal and financial intelligence ecosystem, democratizing access to institutional-grade market data."
    },
    "mindsdb/mindshub": {
        "title": "MindsHub",
        "title_en": "MindsHub — Connect enterprise databases directly to AI agents and automated workflows",
        "desc_hu": "Híd az adatbázisok (SQL, NoSQL, MongoDB) és az AI ágensek között: közvetlenül az adataid felett futtat prediktív és generatív modelleket.",
        "desc_en": "An open platform connecting enterprise data sources to AI agents, enabling direct database-level model training and automated inference workflows."
    },
    "agno-agi/agno": {
        "title": "Agno",
        "title_en": "Agno — Ultra-fast, lightweight multimodal multi-agent system (formerly Phidata)",
        "desc_hu": "Rendkívül gyors és pehelykönnyű multimodális multi-ágens rendszer (korábban Phidata), memóriával, tudásbázissal és autonóm eszköztárral.",
        "desc_en": "A lightweight and ultra-fast multi-agent framework (formerly Phidata) for building memory-enabled, multimodal agent teams with tool calling."
    },
    "code-yeongyu/oh-my-openagent": {
        "title": "Oh My OpenAgent",
        "title_en": "Oh My OpenAgent — CLI and terminal-native developer agent for automating command-line workflows",
        "desc_hu": "Fejlesztői terminál-ágens keretrendszer: automatizálja a parancssori feladatokat, hibakeresést, scriptírást és rendszeradminisztrációt.",
        "desc_en": "A terminal-native developer agent framework that automates CLI workflows, shell debugging, script authoring, and sysadmin tasks."
    },
    "block/goose": {
        "title": "Goose",
        "title_en": "Goose — Open-source on-machine autonomous AI agent for developers by Block",
        "desc_hu": "A Block (Square) által fejlesztett nyílt forráskódú autonóm fejlesztői ágens, amely a gépeden futva önállóan szerkeszt kódot és futtat parancsokat.",
        "desc_en": "An open-source, on-machine autonomous AI agent by Block that edits code, navigates directories, and executes terminal commands directly."
    },
    "unslothai/unsloth": {
        "title": "Unsloth",
        "title_en": "Unsloth — 5x faster and 80% less memory LLM fine-tuning engine",
        "desc_hu": "A leggyorsabb nyílt forráskódú LLM finomhangoló motor: 5-ször gyorsabb betanítás 80%-kal kevesebb memóriával Llama 3, Mistral és DeepSeek modellekhez.",
        "desc_en": "Finetune Llama 3.3, Mistral, and DeepSeek models 5x faster with 80% less VRAM using heavily optimized custom CUDA kernels."
    },
    "hiyouga/LlamaFactory": {
        "title": "LlamaFactory",
        "title_en": "LlamaFactory — Unified efficient fine-tuning framework for 100+ large language models",
        "desc_hu": "Univerzális finomhangoló stúdió több mint 100 LLM-hez (Llama, Qwen, DeepSeek), kényelmes webes felülettel és multi-GPU gyorsítással.",
        "desc_en": "A unified, efficient fine-tuning framework supporting 100+ LLMs and multimodal models with an intuitive WebUI and multi-GPU acceleration."
    },
    "CopilotKit/CopilotKit": {
        "title": "CopilotKit",
        "title_en": "CopilotKit — Open-source framework to build custom in-app AI copilots and agents",
        "desc_hu": "Könnyen beépíthető AI copilóták és ágensek bármilyen React / webes alkalmazásba: kontextustudatos csevegés, szövegmezők és automatikus műveletek.",
        "desc_en": "The open-source framework to build custom in-app AI copilots, AI textareas, and autonomous background agents inside any React application."
    },
    "Dokploy/dokploy": {
        "title": "Dokploy",
        "title_en": "Dokploy — Free, self-hosted deployment platform alternative to Vercel, Heroku, and Coolify",
        "desc_hu": "A Vercel, Heroku és Netlify ingyenes, saját szerveren futtatható (self-hosted) alternatívája: Docker konténerek és adatbázisok automatikus telepítése.",
        "desc_en": "An open-source, self-hosted PaaS alternative to Vercel, Heroku, and Coolify that deploys Docker containers, databases, and websites on your own server."
    }
}

base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
db_path = os.path.join(base_dir, "data", "nexus.db")
cat_path = os.path.join(base_dir, "data", "catalogue.json")

conn = sqlite3.connect(db_path)
cursor = conn.cursor()

# Get existing repo names
cursor.execute("SELECT repo_name FROM repositories")
existing_repos = {r[0].lower(): True for r in cursor.fetchall()}

with open(cat_path, "r", encoding="utf-8") as f:
    cat = json.load(f)

inserted_count = 0

for item_info in REPOS_TO_IMPORT:
    repo = item_info["repo"]
    alt = item_info.get("alt_repo")
    
    if repo.lower() in existing_repos or (alt and alt.lower() in existing_repos):
        print(f"[ALREADY EXISTS] {repo}")
        continue

    # Fetch live info from GitHub API
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
    title = meta.get("title") or gh_data.get("name") or repo.split("/")[1]
    title_en = meta.get("title_en") or f"{title} — {gh_data.get('description', '')}"
    desc_hu = meta.get("desc_hu") or gh_data.get("description") or ""
    desc_en = meta.get("desc_en") or gh_data.get("description") or ""
    function_title = f"{title} — {desc_hu[:60]}..."
    year = int((gh_data.get("created_at") or "2025")[:4])
    tags = (gh_data.get("topics") or [title.lower(), "agent", "open-source"])[:6]

    clean_item = {
        "id": f"agentstack-{live_repo.replace('/', '-')}",
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

    # Insert into SQLite nexus.db
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

# Save updated catalogue.json backup
cat["last_updated"] = time.strftime("%Y-%m-%d %H:%M:%S")
with open(cat_path, "w", encoding="utf-8") as f:
    json.dump(cat, f, ensure_ascii=False, indent=2)

print(f"\nSuccessfully imported {inserted_count} agent stack repos into nexus.db and catalogue.json!")
