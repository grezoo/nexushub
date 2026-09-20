import urllib.request
import json
import sqlite3
import os
import time
import sys

sys.stdout.reconfigure(encoding="utf-8")

FIFTY_REPOS = [
    {"repo": "ifixai-ai/iFix", "title": "iFixAi", "main_cat": "Mesterséges Intelligencia & Adat", "sub_cat": "Gépi Tanulás & Neurális Hálók", "desc_hu": "AI alignment és misalignment tesztelő keretrendszer LLM modellek biztonsági kiértékeléséhez.", "desc_en": "AI misalignment and safety testing framework for evaluating and aligning large language models."},
    {"repo": "public-apis/public-apis", "title": "Public APIs", "main_cat": "Rendszer, Biztonság & Segédprogramok", "sub_cat": "Gyorsindítók & Asztali Kiegészítők", "desc_hu": "A világ legnagyobb kollekciója ingyenesen használható nyilvános API-król fejlesztők számára.", "desc_en": "A collective list of free APIs for use in software and web development."},
    {"repo": "codecrafters-io/build-your-own-x", "alt": "danistefanovic/build-your-own-x", "title": "Build Your Own X", "main_cat": "Produktivitás & Irodai Munka", "sub_cat": "Automatizáció & Produktivitás", "desc_hu": "Építs saját adatbázist, operációs rendszert, git-et vagy nyelvet nulláról: gyakorlatorientált fejlesztői útmutató.", "desc_en": "Master programming by recreating your favorite technologies from scratch."},
    {"repo": "kamranahmedse/developer-roadmap", "title": "Developer Roadmap", "main_cat": "Produktivitás & Irodai Munka", "sub_cat": "Automatizáció & Produktivitás", "desc_hu": "Részletes, interaktív karrier- és tanulási útmutatók frontend, backend, AI és DevOps fejlesztőknek.", "desc_en": "Interactive roadmaps, guides and other educational content to help developers grow in their careers."},
    {"repo": "EbookFoundation/free-programming-books", "title": "Free Programming Books", "main_cat": "Produktivitás & Irodai Munka", "sub_cat": "PDF & Dokumentumkezelés", "desc_hu": "Több ezer ingyenesen elérhető szakmai programozási könyv, kurzus és oktatási anyag.", "desc_en": "Freely available programming books in dozens of languages covering all major software engineering disciplines."},
    {"repo": "donnemartin/system-design-primer", "title": "System Design Primer", "main_cat": "Rendszer, Biztonság & Segédprogramok", "sub_cat": "Konténerek & Docker Környezetek", "desc_hu": "A szoftverarchitektúra és nagyléptékű rendszerek tervezésének bibliája technológiai interjúkra és fejlesztőknek.", "desc_en": "Learn how to design large-scale systems and prepare for system design interview rounds."},
    {"repo": "jwasham/coding-interview-university", "title": "Coding Interview University", "main_cat": "Produktivitás & Irodai Munka", "sub_cat": "Automatizáció & Produktivitás", "desc_hu": "Teljes körű, több hónapos számítástudományi és algoritmus tanulási terv szoftvermérnököknek.", "desc_en": "A complete multi-month study plan for becoming a software engineer for a large tech company."},
    {"repo": "jlevy/the-art-of-command-line", "title": "The Art of Command Line", "main_cat": "Rendszer, Biztonság & Segédprogramok", "sub_cat": "Gyorsindítók & Asztali Kiegészítők", "desc_hu": "Parancssori mesterfogások és praktikus termináltrükkök fejlesztőknek Linux és macOS környezetben.", "desc_en": "Master the command line in one page with curated, high-value shell tips."},
    {"repo": "practical-tutorials/project-based-learning", "title": "Project Based Learning", "main_cat": "Produktivitás & Irodai Munka", "sub_cat": "Automatizáció & Produktivitás", "desc_hu": "Programozástanulás valós projektek építésén keresztül különböző programnyelveken.", "desc_en": "A curated list of project-based tutorials in which aspiring software engineers build applications from scratch."},
    {"repo": "getify/You-Dont-Know-JS", "title": "You Don't Know JS", "main_cat": "Produktivitás & Irodai Munka", "sub_cat": "PDF & Dokumentumkezelés", "desc_hu": "A mély JavaScript nyelv működésének legelismertebb könyvsorozata Kyle Simpsontól.", "desc_en": "Deep dive into the core mechanisms of the JavaScript language by Kyle Simpson."},
    {"repo": "trimstray/the-book-of-secret-knowledge", "title": "The Book of Secret Knowledge", "main_cat": "Rendszer, Biztonság & Segédprogramok", "sub_cat": "Kiberbiztonság & Jelszókezelők", "desc_hu": "Titkos tudás tárháza: hálózatbiztonság, OSINT eszközök, Linux trükkök és sysadmin segédletek.", "desc_en": "A collection of inspiring lists, manuals, cheatsheets, blogs, hacks, one-liners, cli/web tools and cybersecurity essentials."},
    {"repo": "yangshun/tech-interview-handbook", "title": "Tech Interview Handbook", "main_cat": "Produktivitás & Irodai Munka", "sub_cat": "Automatizáció & Produktivitás", "desc_hu": "Algoritmusok, viselkedési interjúk és ajánlati tárgyalások átfogó kézikönyve szoftvermérnököknek.", "desc_en": "Curated coding interview preparation materials for busy software engineers."},
    {"repo": "awesome-selfhosted/awesome-selfhosted", "title": "Awesome Self-Hosted", "main_cat": "Rendszer, Biztonság & Segédprogramok", "sub_cat": "Konténerek & Docker Környezetek", "desc_hu": "Saját szerveren üzemeltethető nyílt forráskódú hálózati szolgáltatások és alkalmazások végső listája.", "desc_en": "A list of Free Software network services and web applications which can be hosted on your own servers."},
    {"repo": "trekhleb/javascript-algorithms", "title": "JavaScript Algorithms", "main_cat": "Mesterséges Intelligencia & Adat", "sub_cat": "Gépi Tanulás & Neurális Hálók", "desc_hu": "Népszerű algoritmusok és adatstruktúrák tiszta JavaScript megvalósítása tesztekkel és magyarázatokkal.", "desc_en": "Algorithms and data structures implemented in JavaScript with explanations and links to further readings."},
    {"repo": "Chalarangelo/30-seconds-of-code", "title": "30 Seconds of Code", "main_cat": "Produktivitás & Irodai Munka", "sub_cat": "Automatizáció & Produktivitás", "desc_hu": "Rövid, hasznos és azonnal használható kódminták modern fejlesztési igényekhez.", "desc_en": "Short code snippets for all your development needs across modern programming languages."},
    {"repo": "github/gitignore", "title": "GitHub Gitignore Templates", "main_cat": "Rendszer, Biztonság & Segédprogramok", "sub_cat": "Gyorsindítók & Asztali Kiegészítők", "desc_hu": "A GitHub hivatalos, minden nyelvre és keretrendszerre kiterjedő .gitignore sablongyűjteménye.", "desc_en": "A collection of useful .gitignore templates directly from GitHub."},
    {"repo": "ollama/ollama", "title": "Ollama", "main_cat": "Mesterséges Intelligencia & Adat", "sub_cat": "Nagy Nyelvi Modellek & LLM", "desc_hu": "Futtass nyílt forráskódú nagy nyelvi modelleket lokálisan a saját gépeden egyetlen paranccsal.", "desc_en": "Get up and running with Llama 3, Mistral, Gemma, and other large language models locally."},
    {"repo": "langchain-ai/langchain", "title": "LangChain", "main_cat": "Mesterséges Intelligencia & Adat", "sub_cat": "Autonóm Ágensek & Automatizáció", "desc_hu": "A világ legnépszerűbb keretrendszere kontextus-vezérelt LLM alkalmazások és láncolatok építéséhez.", "desc_en": "Build context-aware, reasoning applications with LangChain's flexible components."},
    {"repo": "n8n-io/n8n", "title": "n8n", "main_cat": "Produktivitás & Irodai Munka", "sub_cat": "Automatizáció & Produktivitás", "desc_hu": "Fair-code licencű vizuális munkafolyamat-automatizációs platform AI és API integrációkkal.", "desc_en": "Fair-code workflow automation platform with native AI capabilities and hundreds of integrations."},
    {"repo": "openclaw/openclaw", "title": "OpenClaw", "main_cat": "Mesterséges Intelligencia & Adat", "sub_cat": "Autonóm Ágensek & Automatizáció", "desc_hu": "Lokális, adatvédelmet szem előtt tartó nyílt forráskódú intelligens asszisztens és ágens.", "desc_en": "Local and privacy-focused open-source intelligent personal AI assistant engine."},
    {"repo": "langgenius/dify", "title": "Dify", "main_cat": "Mesterséges Intelligencia & Adat", "sub_cat": "Autonóm Ágensek & Automatizáció", "desc_hu": "Nyílt forráskódú LLM alkalmazásfejlesztő platform vizuális ágens-munkafolyamatokkal és RAG-gal.", "desc_en": "An open-source LLM app development platform combining Agentic workflows with RAG and LLMOps."},
    {"repo": "langflow-ai/langflow", "title": "Langflow", "main_cat": "Mesterséges Intelligencia & Adat", "sub_cat": "Autonóm Ágensek & Automatizáció", "desc_hu": "Vizuális drag-and-drop felület multi-ágens rendszerek és RAG alkalmazások prototipizálásához.", "desc_en": "A visual framework for building multi-agent and RAG applications, open-source and python-powered."},
    {"repo": "browser-use/browser-use", "title": "Browser Use", "main_cat": "Mesterséges Intelligencia & Adat", "sub_cat": "Autonóm Ágensek & Automatizáció", "desc_hu": "Tedd képessé az AI ágenseket a webböngésző önálló irányítására, kattintásra és űrlapkitöltésre.", "desc_en": "Make websites accessible for AI agents with autonomous browser automation and interaction."},
    {"repo": "crewAIInc/crewAI", "title": "CrewAI", "main_cat": "Mesterséges Intelligencia & Adat", "sub_cat": "Autonóm Ágensek & Automatizáció", "desc_hu": "Élvonalbeli multi-ágens keretrendszer autonóm AI szerepkörök és csapatok együttműködéséhez.", "desc_en": "Framework for orchestrating role-playing, autonomous AI agents to solve complex tasks together."},
    {"repo": "geekan/MetaGPT", "title": "MetaGPT", "main_cat": "Mesterséges Intelligencia & Adat", "sub_cat": "Autonóm Ágensek & Automatizáció", "desc_hu": "Többágenses szoftverfejlesztő keretrendszer: komplett szoftvercég szimulációja termékmenedzserrel, mérnökökkel.", "desc_en": "The Multi-Agent Framework: First AI Software Company replicating product managers, architects, and engineers."},
    {"repo": "microsoft/autogen", "title": "AutoGen", "main_cat": "Mesterséges Intelligencia & Adat", "sub_cat": "Autonóm Ágensek & Automatizáció", "desc_hu": "A Microsoft fejlett multi-ágens keretrendszere társalgási AI ágensek zökkenőmentes együttműködéséhez.", "desc_en": "A programming framework for agentic AI by Microsoft allowing multiple agents to converse and execute code."},
    {"repo": "Aider-AI/aider", "title": "Aider", "main_cat": "Mesterséges Intelligencia & Adat", "sub_cat": "Autonóm Ágensek & Automatizáció", "desc_hu": "A világ egyik legnépszerűbb terminál-alapú AI páros programozó asszisztense közvetlen Git integrációval.", "desc_en": "AI pair programming in your terminal, capable of editing code across multiple files with automatic git commits."},
    {"repo": "microsoft/markitdown", "title": "MarkItDown", "main_cat": "Produktivitás & Irodai Munka", "sub_cat": "PDF & Dokumentumkezelés", "desc_hu": "A Microsoft eszköze különféle fájlformátumok (PDF, DOCX, XLSX, képek) tiszta Markdownná alakítására.", "desc_en": "Python tool for converting files and office documents into Markdown for LLM and RAG consumption."},
    {"repo": "open-webui/open-webui", "title": "Open WebUI", "main_cat": "Mesterséges Intelligencia & Adat", "sub_cat": "Nagy Nyelvi Modellek & LLM", "desc_hu": "Felhasználóbarát, önállóan hosztolható AI felület Ollama és OpenAI kompatibilis modellekhez.", "desc_en": "User-friendly AI interface for local LLMs, supporting Ollama, OpenAI-compatible APIs, and multi-user chat."},
    {"repo": "soxoj/maigret", "title": "Maigret", "main_cat": "Rendszer, Biztonság & Segédprogramok", "sub_cat": "Kiberbiztonság & Jelszókezelők", "desc_hu": "Erőteljes nyílt forráskódú OSINT felderítő eszköz felhasználónevek több mint 3000 weboldalon történő keresésére.", "desc_en": "Collect a dossier on a person by username across 3,000+ sites with recursive OSINT search."},
    {"repo": "TauricResearch/TradingAgents", "title": "TradingAgents", "main_cat": "Pénzügy, Tőzsde & Kripto Elemzés", "sub_cat": "Algoritmikus Kereskedés & Botok", "desc_hu": "Multi-ágens szimulációs és autonóm döntéshozatali keretrendszer pénzügyi kereskedéshez.", "desc_en": "Multi-agent LLM financial trading framework simulating trading desks with technical and fundamental analysts."},
    {"repo": "browserbase/stagehand", "title": "Stagehand", "main_cat": "Mesterséges Intelligencia & Adat", "sub_cat": "Autonóm Ágensek & Automatizáció", "desc_hu": "AI böngésző-automatizációs keretrendszer Playwright alapokon: öngyógyító lokátorok és természetes nyelvi utasítások.", "desc_en": "An AI browser automation framework built on Playwright with natural language navigation and extraction."},
    {"repo": "mendableai/firecrawl", "title": "Firecrawl", "main_cat": "Rendszer, Biztonság & Segédprogramok", "sub_cat": "Gyorsindítók & Asztali Kiegészítők", "desc_hu": "Alakíts bármilyen weboldalt LLM-kész tiszta Markdownná egyetlen API hívással.", "desc_en": "Turn entire websites into clean LLM-ready markdown or structured data with crawl and scrape APIs."},
    {"repo": "huggingface/transformers", "title": "Transformers", "main_cat": "Mesterséges Intelligencia & Adat", "sub_cat": "Gépi Tanulás & Neurális Hálók", "desc_hu": "A modern gépi tanulás alapköve a Hugging Face-től: ezerféle nyílt forráskódú SOTA modell PyTorch és TensorFlow alatt.", "desc_en": "State-of-the-art Machine Learning for Pytorch, TensorFlow, and JAX by Hugging Face."},
    {"repo": "vllm-project/vllm", "title": "vLLM", "main_cat": "Mesterséges Intelligencia & Adat", "sub_cat": "Nagy Nyelvi Modellek & LLM", "desc_hu": "Rendkívül gyors és egyszerűen használható nyílt forráskódú LLM inferencia és kiszolgáló motor PagedAttentionnel.", "desc_en": "A high-throughput and memory-efficient inference and serving engine for LLMs."},
    {"repo": "ggml-org/llama.cpp", "alt": "ggerganov/llama.cpp", "title": "llama.cpp", "main_cat": "Mesterséges Intelligencia & Adat", "sub_cat": "Nagy Nyelvi Modellek & LLM", "desc_hu": "LLM inferencia tiszta C/C++ nyelven minimális memóriaigénnyel és natív hardveres gyorsítással.", "desc_en": "LLM inference in C/C++ with zero dependencies, quantized execution, and Apple Silicon/GPU acceleration."},
    {"repo": "run-llama/llama_index", "title": "LlamaIndex", "main_cat": "Mesterséges Intelligencia & Adat", "sub_cat": "RAG & Dokumentumelemzés", "desc_hu": "A vezető adatkeretrendszer LLM és RAG alkalmazásokhoz: strukturálatlan adatok vektoros indexelése.", "desc_en": "Data framework for your LLM applications, connecting custom data sources to large language models."},
    {"repo": "karpathy/nanoGPT", "title": "nanoGPT", "main_cat": "Mesterséges Intelligencia & Adat", "sub_cat": "Gépi Tanulás & Neurális Hálók", "desc_hu": "A legegyszerűbb, leggyorsabb és legtisztább repó közepes méretű GPT modellek tanításához Andrej Karpathytól.", "desc_en": "The simplest, fastest repository for training and finetuning medium-sized GPTs by Andrej Karpathy."},
    {"repo": "infiniflow/ragflow", "title": "RAGFlow", "main_cat": "Mesterséges Intelligencia & Adat", "sub_cat": "RAG & Dokumentumelemzés", "desc_hu": "Nyílt forráskódú RAG motor mély dokumentum-értelmezéssel és strukturált tartalom-kinyeréssel.", "desc_en": "An open-source RAG engine based on deep document understanding and multimodal chunking."},
    {"repo": "supermemoryai/supermemory", "title": "Supermemory", "main_cat": "Mesterséges Intelligencia & Adat", "sub_cat": "RAG & Dokumentumelemzés", "desc_hu": "A te személyes AI második agyad: könyvjelzők, weboldalak és jegyzetek intelligens keresőmotorja.", "desc_en": "Build your personal second brain: bookmarking and AI search across all your saved knowledge."},
    {"repo": "ComposioHQ/awesome-claude-skills", "title": "Awesome Claude Skills", "main_cat": "Mesterséges Intelligencia & Adat", "sub_cat": "Autonóm Ágensek & Automatizáció", "desc_hu": "Válogatott eszközök, API integrációk és képességcsomagok Claude Code és Anthropic ágensekhez.", "desc_en": "Curated collection of tools, API connectors, and MCP capabilities for Claude and Anthropic agents."},
    {"repo": "comfyanonymous/ComfyUI", "title": "ComfyUI", "main_cat": "Kreatív Média, Videóvágás & Fotó", "sub_cat": "3D Modellezés & Képszerkesztés", "desc_hu": "A legrugalmasabb moduláris csomópont-alapú felület Stable Diffusion és generatív AI modellek futtatásához.", "desc_en": "The most powerful and modular diffusion model GUI and backend with graph/nodes interface."},
    {"repo": "deepseek-ai/DeepSeek-Coder-V2", "alt": "deepseek-ai/DeepSeek-V3", "title": "DeepSeek Coder / V3", "main_cat": "Mesterséges Intelligencia & Adat", "sub_cat": "Nagy Nyelvi Modellek & LLM", "desc_hu": "A DeepSeek nyílt súlyú Mixture-of-Experts (MoE) kódoló és általános reasoning modellje.", "desc_en": "Open-source state-of-the-art Mixture-of-Experts coding and reasoning models by DeepSeek AI."},
    {"repo": "lobehub/lobe-chat", "title": "Lobe Chat", "main_cat": "Mesterséges Intelligencia & Adat", "sub_cat": "Nagy Nyelvi Modellek & LLM", "desc_hu": "Modern, gyönyörű nyílt forráskódú AI csevegőplatform multi-modell támogatással és pluginekkel.", "desc_en": "Modern open-source AI chat workspace supporting multi-modal models, TTS, and extensive plugin ecosystem."},
    {"repo": "freeCodeCamp/freeCodeCamp", "title": "freeCodeCamp", "main_cat": "Produktivitás & Irodai Munka", "sub_cat": "Automatizáció & Produktivitás", "desc_hu": "A világ legnagyobb nyílt közösségi programozás-tanuló platformja interaktív feladatokkal és minősítésekkel.", "desc_en": "freeCodeCamp.org's open-source codebase and curriculum to learn to code for free."}
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

    inserted_count = 0
    updated_count = 0

    print(f"Starting import of 50 Useful Repos...")

    for item in FIFTY_REPOS:
        repo = item["repo"]
        alt = item.get("alt")
        
        # Try fetching from GitHub API
        gh_data = {}
        target_repo = repo
        for r_candidate in [repo, alt] if alt else [repo]:
            try:
                req = urllib.request.Request(f"https://api.github.com/repos/{r_candidate}", headers={"User-Agent": "NexusHub-Curator/2.0"})
                with urllib.request.urlopen(req, timeout=8) as resp:
                    gh_data = json.loads(resp.read().decode("utf-8"))
                    target_repo = r_candidate
                    break
            except Exception as e:
                pass

        stars = int(gh_data.get("stargazers_count") or 1000)
        title = item.get("title") or gh_data.get("name") or target_repo.split("/")[1]
        title_en = f"{title} — {item.get('desc_en', '')}"
        desc_hu = item.get("desc_hu") or gh_data.get("description") or ""
        desc_en = item.get("desc_en") or gh_data.get("description") or ""
        function_title = f"{title} — {desc_hu[:60]}..."
        year = int((gh_data.get("created_at") or "2024")[:4])
        tags = (gh_data.get("topics") or [title.lower(), "open-source", "developer-tools"])[:6]

        clean_item = {
            "id": f"useful-{target_repo.replace('/', '-')}",
            "repo_name": target_repo,
            "title": title,
            "function_title": function_title,
            "title_en": title_en,
            "function_title_en": title_en,
            "description": desc_hu,
            "description_en": desc_en,
            "main_category": item["main_cat"],
            "sub_category": item["sub_cat"],
            "thumbnail_url": f"https://opengraph.githubassets.com/1/{target_repo}",
            "video_url": "",
            "has_video": False,
            "video_demo": "",
            "stars": stars,
            "year": year,
            "url": gh_data.get("html_url", f"https://github.com/{target_repo}"),
            "creator": target_repo.split("/")[0],
            "tags": tags,
            "is_pinned": False
        }

        # Check if either target_repo or alt exists in DB
        found_in_db = False
        match_name = target_repo
        if target_repo.lower() in existing_repos:
            found_in_db = True
            match_name = target_repo
        elif alt and alt.lower() in existing_repos:
            found_in_db = True
            match_name = alt

        if found_in_db:
            # Update existing with enriched metadata & real stars
            cursor.execute("""
                UPDATE repositories 
                SET title = ?, function_title = ?, title_en = ?, function_title_en = ?,
                    description = ?, description_en = ?, stars = ?, main_category = ?, sub_category = ?
                WHERE LOWER(repo_name) = LOWER(?)
            """, (
                clean_item["title"], clean_item["function_title"], clean_item["title_en"], clean_item["function_title_en"],
                clean_item["description"], clean_item["description_en"], clean_item["stars"],
                clean_item["main_category"], clean_item["sub_category"], match_name
            ))
            for it in cat.get("items", []):
                if it.get("repo_name", "").lower() == match_name.lower():
                    it.update(clean_item)
            updated_count += 1
            print(f"  [*] Updated: {title} ({stars} ⭐)")
        else:
            # Insert new
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
            existing_repos[target_repo.lower()] = True
            inserted_count += 1
            print(f"  [+] Inserted: {title} ({stars} ⭐) - {item['main_cat']}")

        time.sleep(0.35)

    conn.commit()
    conn.close()

    cat["last_updated"] = time.strftime("%Y-%m-%d %H:%M:%S")
    with open(cat_path, "w", encoding="utf-8") as f:
        json.dump(cat, f, ensure_ascii=False, indent=2)

    print(f"\nCompleted! Inserted: {inserted_count}, Updated: {updated_count}")

if __name__ == "__main__":
    run_import()
