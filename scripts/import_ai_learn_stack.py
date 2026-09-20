import urllib.request
import json
import sqlite3
import os
import time
import sys

sys.stdout.reconfigure(encoding="utf-8")

AI_LEARN_REPOS = [
    {
        "repo": "jackfrued/Python-100-Days",
        "title": "Python 100 Days",
        "main_cat": "Produktivitás & Irodai Munka",
        "sub_cat": "Automatizáció & Produktivitás",
        "stars": 156000,
        "desc_hu": "100 napos átfogó Python oktatási tananyag az alapoktól az adatfeldolgozáson és webfejlesztésen át a gépi tanulásig.",
        "desc_en": "Comprehensive 100-day Python curriculum from fundamentals and algorithms to data analysis, web scraping, and frameworks."
    },
    {
        "repo": "microsoft/generative-ai-for-beginners",
        "title": "Generative AI for Beginners",
        "main_cat": "Mesterséges Intelligencia & Adat",
        "sub_cat": "Nagy Nyelvi Modellek & LLM",
        "stars": 74000,
        "desc_hu": "A Microsoft 21 leckés hivatalos kurzusa generatív AI-hoz: prompt engineering, RAG architektúrák, ágensek és finomhangolás.",
        "desc_en": "21 Lessons to get started building Generative AI apps with LLMs, prompt engineering, RAG, agents, and fine-tuning by Microsoft."
    },
    {
        "repo": "rasbt/LLMs-from-scratch",
        "title": "LLMs from Scratch",
        "main_cat": "Mesterséges Intelligencia & Adat",
        "sub_cat": "Nagy Nyelvi Modellek & LLM",
        "stars": 49000,
        "desc_hu": "Építs saját GPT nyelvi modellt nulláról PyTorch-ban Sebastian Raschka könyve alapján: tokenizálás, attention és betanítás.",
        "desc_en": "Implementing a ChatGPT-like LLM from scratch step-by-step in PyTorch by Sebastian Raschka."
    },
    {
        "repo": "microsoft/ML-For-Beginners",
        "title": "ML for Beginners",
        "main_cat": "Mesterséges Intelligencia & Adat",
        "sub_cat": "Gépi Tanulás & Neurális Hálók",
        "stars": 69000,
        "desc_hu": "A Microsoft 26 leckéből álló, 12 hetes klasszikus gépi tanulás tananyaga gyakorlati Scikit-learn kódokkal és vizualizációkkal.",
        "desc_en": "26 Lessons, 12 weeks of structured curriculum covering classical machine learning concepts and applications by Microsoft."
    },
    {
        "repo": "openai/openai-cookbook",
        "title": "OpenAI Cookbook",
        "main_cat": "Mesterséges Intelligencia & Adat",
        "sub_cat": "Autonóm Ágensek & Automatizáció",
        "stars": 63000,
        "desc_hu": "A hivatalos OpenAI példatár: azonnal futtatható kódok és bevált receptek GPT-4, embeddingek, finomhangolás és ágensek építéséhez.",
        "desc_en": "Official examples, recipes, and guides for building with the OpenAI API, GPT-4, embeddings, and autonomous agents."
    },
    {
        "repo": "CompVis/stable-diffusion",
        "title": "Stable Diffusion",
        "main_cat": "Kreatív Média, Videóvágás & Fotó",
        "sub_cat": "3D Modellezés & Képszerkesztés",
        "stars": 68000,
        "desc_hu": "Az eredeti látens diffúziós kutatási implementáció, amely forradalmasította a nyílt forráskódú képgenerálást és AI művészetet.",
        "desc_en": "High-Resolution Image Synthesis with Latent Diffusion Models by CompVis and Stability AI."
    },
    {
        "repo": "microsoft/ai-agents-for-beginners",
        "title": "AI Agents for Beginners",
        "main_cat": "Mesterséges Intelligencia & Adat",
        "sub_cat": "Autonóm Ágensek & Automatizáció",
        "stars": 23000,
        "desc_hu": "A Microsoft legújabb tananyaga az autonóm AI ágensek építéséről: eszközhasználat (tools), memória, tervezés és multi-ágens rendszerek.",
        "desc_en": "Learn to build autonomous AI agents from scratch: agent architectures, tool use, memory, and multi-agent coordination."
    },
    {
        "repo": "microsoft/AI-For-Beginners",
        "title": "AI for Beginners",
        "main_cat": "Mesterséges Intelligencia & Adat",
        "sub_cat": "Gépi Tanulás & Neurális Hálók",
        "stars": 38000,
        "desc_hu": "12 hetes, 24 leckés átfogó mesterséges intelligencia alaptanfolyam neurális hálókról, számítógépes látásról és NLP-ről.",
        "desc_en": "12 Weeks, 24 Lessons Curriculum about Artificial Intelligence, symbolic AI, neural networks, computer vision, and NLP."
    },
    {
        "repo": "pathwaycom/llm-app",
        "title": "LLM App (Pathway)",
        "main_cat": "Mesterséges Intelligencia & Adat",
        "sub_cat": "RAG & Dokumentumelemzés",
        "stars": 9200,
        "desc_hu": "Valós idejű, streamelt RAG pipeline-ok és enterprise keresőrendszerek építése élő adatfolyamokra és vektoros indexelésre.",
        "desc_en": "Production-ready streaming RAG pipelines, enterprise search, and real-time LLM applications using Pathway."
    },
    {
        "repo": "facebookresearch/segment-anything",
        "title": "Segment Anything (SAM)",
        "main_cat": "Mesterséges Intelligencia & Adat",
        "sub_cat": "Gépi Tanulás & Neurális Hálók",
        "stars": 49000,
        "desc_hu": "A Meta áttörést hozó alapmodellje univerzális képszegmentálásra: bármilyen objektum azonnali kivágása egyetlen kattintással.",
        "desc_en": "The Segment Anything Model (SAM) by Meta FAIR: zero-shot image segmentation across arbitrary images and objects."
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

    print("Importing 10 AI / ML Learning & Foundation Repos...")

    for item in AI_LEARN_REPOS:
        repo = item["repo"]
        stars = item["stars"]
        title = item["title"]
        title_en = f"{title} — {item['desc_en'][:80]}..."
        desc_hu = item["desc_hu"]
        desc_en = item["desc_en"]
        function_title = f"{title} — {desc_hu[:60]}..."
        year = 2023
        tags = [title.lower(), "ai", "machine-learning", "open-source"]

        clean_item = {
            "id": f"learn-{repo.replace('/', '-')}",
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
            "url": f"https://github.com/{repo}",
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

        time.sleep(0.2)

    conn.commit()
    conn.close()

    cat["last_updated"] = time.strftime("%Y-%m-%d %H:%M:%S")
    with open(cat_path, "w", encoding="utf-8") as f:
        json.dump(cat, f, ensure_ascii=False, indent=2)

    print(f"\nDone! Inserted: {inserted}, Updated: {updated}")

if __name__ == "__main__":
    run_import()
