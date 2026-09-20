import urllib.request
import json
import sqlite3
import os
import time
import sys

sys.stdout.reconfigure(encoding="utf-8")


SKILL_REPOS = [
    {"repo": "santifer/career-ops", "main_cat": "Produktivitás & Irodai Munka", "sub_cat": "Automatizáció & Produktivitás"},
    {"repo": "Paramchoudhary/ResumeSkills", "main_cat": "Produktivitás & Irodai Munka", "sub_cat": "PDF & Dokumentumkezelés"},
    {"repo": "PleasePrompto/notebooklm-skill", "main_cat": "Mesterséges Intelligencia & Adat", "sub_cat": "RAG & Dokumentumelemzés"},
    {"repo": "bevibing/tutor-skills", "main_cat": "Mesterséges Intelligencia & Adat", "sub_cat": "Autonóm Ágensek & Automatizáció"},
    {"repo": "ZeroPointRepo/youtube-skills", "main_cat": "Kreatív Média, Videóvágás & Fotó", "sub_cat": "Videógenerálás & Mozgókép"},
    {"repo": "deusyu/translate-book", "main_cat": "Produktivitás & Irodai Munka", "sub_cat": "PDF & Dokumentumkezelés"},
    {"repo": "smixs/creative-director-skill", "main_cat": "Kreatív Média, Videóvágás & Fotó", "sub_cat": "Videógenerálás & Mozgókép"},
    {"repo": "meodai/skill.color-expert", "main_cat": "Kreatív Média, Videóvágás & Fotó", "sub_cat": "3D Modellezés & Képszerkesztés"},
    {"repo": "ehmo/platform-design-skills", "main_cat": "Produktivitás & Irodai Munka", "sub_cat": "Automatizáció & Produktivitás"},
    {"repo": "Digidai/product-manager-skills", "main_cat": "Produktivitás & Irodai Munka", "sub_cat": "Automatizáció & Produktivitás"},
    {"repo": "GanyuanRan/Aegis", "main_cat": "Rendszer, Biztonság & Segédprogramok", "sub_cat": "Kiberbiztonság & Jelszókezelők"},
    {"repo": "antonbabenko/terraform-skill", "main_cat": "Rendszer, Biztonság & Segédprogramok", "sub_cat": "Konténerek & Docker Környezetek"},
    {"repo": "qdrant/skills", "main_cat": "Mesterséges Intelligencia & Adat", "sub_cat": "RAG & Dokumentumelemzés"},
    {"repo": "foryourhealth111-pixel/Vibe-Skills", "main_cat": "Mesterséges Intelligencia & Adat", "sub_cat": "Autonóm Ágensek & Automatizáció"},
    {"repo": "yusufkaraaslan/Skill_Seekers", "main_cat": "Mesterséges Intelligencia & Adat", "sub_cat": "Autonóm Ágensek & Automatizáció"},
    {"repo": "gitroomhq/postiz-agent", "main_cat": "Produktivitás & Irodai Munka", "sub_cat": "Automatizáció & Produktivitás"},
    {"repo": "CosmoBlk/email-marketing-bible", "main_cat": "Produktivitás & Irodai Munka", "sub_cat": "Automatizáció & Produktivitás"},
    {"repo": "AIDevGTM/gtm-cofounder", "main_cat": "Produktivitás & Irodai Munka", "sub_cat": "Automatizáció & Produktivitás"},
    {"repo": "EveryInc/charlie-cfo-skill", "main_cat": "Pénzügy, Tőzsde & Kripto Elemzés", "sub_cat": "Költségvetés & Pénzügyi Tervezés"},
    {"repo": "ognjengt/founder-skills", "main_cat": "Produktivitás & Irodai Munka", "sub_cat": "Automatizáció & Produktivitás"}
]

CUSTOM_METADATA = {
    "santifer/career-ops": {
        "title": "Career Ops",
        "title_en": "Career Ops — Autonomous career management and job hunting skill for AI agents",
        "desc_hu": "Komplett karrierépítő és álláskeresési ágensképesség: önéletrajz-optimalizálás, interjúfelkészülés és álláskövetés.",
        "desc_en": "An autonomous career management skill for AI agents: resume targeting, application tracking, and interview prep."
    },
    "Paramchoudhary/ResumeSkills": {
        "title": "ResumeSkills",
        "title_en": "ResumeSkills — High-impact resume builder and ATS optimization agent skill",
        "desc_hu": "Ágensképesség ATS-barát, professzionális önéletrajzok generálására és kulcsszó-optimalizálásra.",
        "desc_en": "Agent skill for building ATS-friendly, high-conversion resumes tailored to specific job specs."
    },
    "PleasePrompto/notebooklm-skill": {
        "title": "NotebookLM Skill",
        "title_en": "NotebookLM Skill — Deep document reasoning and podcast generation skill for agents",
        "desc_hu": "NotebookLM képességcsomag AI ágenseknek: komplex dokumentumok szintézise, forrásalapú jegyzetelés és audio összefoglalók.",
        "desc_en": "NotebookLM-style agent skill for grounded document reasoning, podcast synthesis, and research."
    },
    "bevibing/tutor-skills": {
        "title": "Tutor Skills",
        "title_en": "Tutor Skills — Personalized multi-domain tutoring and pedagogical agent engine",
        "desc_hu": "Testreszabott oktatási ágensképesség sokféle szakterület lépésről lépésre történő tanításához és teszteléséhez.",
        "desc_en": "Pedagogical agent skill system for structured learning, personalized tutoring, and active concept mastery."
    },
    "ZeroPointRepo/youtube-skills": {
        "title": "YouTube Skills",
        "title_en": "YouTube Skills — Autonomous YouTube video extraction, transcript analysis, and content summarizer",
        "desc_hu": "YouTube videók átiratának kinyerése, mélyelemzése, időbélyeges összefoglalása és tartalomgyártási ágensképesség.",
        "desc_en": "Autonomous agent skill for YouTube video parsing, timestamped breakdown, transcript extraction, and content repurposing."
    },
    "deusyu/translate-book": {
        "title": "Translate Book",
        "title_en": "Translate Book — Whole-book AI translation skill preserving EPUB/PDF layout and terminology",
        "desc_hu": "Teljes könyvek és hosszú formátumú dokumentumok (EPUB/PDF) kontextushelyes, szaknyelvi fordítását végző ágensképesség.",
        "desc_en": "Autonomous book-length translation skill that preserves typography, terminology glossary, and document layout."
    },
    "smixs/creative-director-skill": {
        "title": "Creative Director Skill",
        "title_en": "Creative Director Skill — AI creative direction, visual branding, and multimodal campaign orchestration",
        "desc_hu": "Kreatív igazgatói képesség ágenseknek: vizuális arculattervezés, prompt-stilizálás és multimodális kampányvezetés.",
        "desc_en": "Virtual creative director skill for brand design, aesthetic consistency, prompt art directing, and campaign generation."
    },
    "meodai/skill.color-expert": {
        "title": "Color Expert Skill",
        "title_en": "Color Expert Skill — Algorithmic color harmony, contrast verification, and palette generation skill",
        "desc_hu": "Professzionális színpaletta-tervező, kontraszt-ellenőrző (WCAG) és színelméleti képesség AI ágensek számára.",
        "desc_en": "Expert color science skill for AI agents: accessible palettes, contrast checks, color naming, and harmonious theming."
    },
    "ehmo/platform-design-skills": {
        "title": "Platform Design Skills",
        "title_en": "Platform Design Skills — Enterprise UI/UX platform systems and design token architecture for agents",
        "desc_hu": "Vállalati szintű UI/UX platformtervezés, design tokenek és komponensrendszerek kezelése ágensekkel.",
        "desc_en": "Systematic design skill for UI platforms, token architectures, and scalable component specifications."
    },
    "Digidai/product-manager-skills": {
        "title": "Product Manager Skills",
        "title_en": "Product Manager Skills — PRD drafting, feature prioritization, and roadmapping agent skill",
        "desc_hu": "Termékmenedzsment ágensképesség: PRD-k készítése, RICE/Kano prioritásfelállítás és termék-roadmap generálás.",
        "desc_en": "Full-cycle product management skill for AI: PRD generation, user story mapping, and feature prioritization frameworks."
    },
    "GanyuanRan/Aegis": {
        "title": "Aegis",
        "title_en": "Aegis — Autonomous security audit, vulnerability scanning, and guardrail skill for agent stacks",
        "desc_hu": "Automatizált biztonsági audit, sebezhetőség-keresés és prompt injection elleni védelem ágensrendszerekhez.",
        "desc_en": "Autonomous security audit, secret leakage prevention, and vulnerability scanner skill for agent frameworks."
    },
    "antonbabenko/terraform-skill": {
        "title": "Terraform Skill",
        "title_en": "Terraform Skill — Declarative cloud infrastructure generation and IaC linting skill by Anton Babenko",
        "desc_hu": "Cloud infrastruktúra-kód (Terraform) generálása, modul-architektúra és biztonsági ellenőrzés ágensekkel.",
        "desc_en": "Production Terraform and AWS cloud architecture generation skill created by Terraform community leader Anton Babenko."
    },
    "qdrant/skills": {
        "title": "Qdrant Skills",
        "title_en": "Qdrant Skills — Official agent skills for Qdrant vector search, hybrid retrieval, and memory storage",
        "desc_hu": "A Qdrant hivatalos ágensképességei vektoros hasonlóságkereséshez, RAG-hoz és ágensmemória-kezeléshez.",
        "desc_en": "Official Qdrant vector database skills enabling dense vector search, hybrid filtering, and scalable agent memory."
    },
    "foryourhealth111-pixel/Vibe-Skills": {
        "title": "Vibe Skills",
        "title_en": "Vibe Skills — Dynamic behavioral persona and agent tonality calibration framework",
        "desc_hu": "Ágensek viselkedési tónusának, személyiségének és kontextuális stílusának dinamikus kalibrációja.",
        "desc_en": "Behavioral adaptation skill library for fine-tuning AI persona vibes, response resonance, and tone agility."
    },
    "yusufkaraaslan/Skill_Seekers": {
        "title": "Skill Seekers",
        "title_en": "Skill Seekers — Self-discovering and dynamically learning toolchain synthesizer for autonomous agents",
        "desc_hu": "Önállóan új eszközöket és API képességeket felkutató, tesztelő és integráló ágens-metarendszer.",
        "desc_en": "Meta-skill system that enables autonomous agents to discover, benchmark, and dynamically absorb new skills on the fly."
    },
    "gitroomhq/postiz-agent": {
        "title": "Postiz Agent",
        "title_en": "Postiz Agent — Autonomous cross-platform social media scheduling and viral distribution engine",
        "desc_hu": "Közösségi média automatizáció és többplatformos tartalom-időzítés AI ágensekkel a Postiz nyílt motorján.",
        "desc_en": "Open-source social distribution agent skill built on Postiz for cross-platform publishing and viral content growth."
    },
    "CosmoBlk/email-marketing-bible": {
        "title": "Email Marketing Bible",
        "title_en": "Email Marketing Bible — High-converting email copywriting sequences and cold outreach agent skills",
        "desc_hu": "Magas konverziójú e-mail kampányok, hírlevelek és hideg megkeresések szövegírási képessége ágenseknek.",
        "desc_en": "Comprehensive email marketing copy skill pack for automated drip sequences, outreach campaigns, and onboarding flows."
    },
    "AIDevGTM/gtm-cofounder": {
        "title": "GTM Co-founder",
        "title_en": "GTM Co-founder — Autonomous go-to-market strategy, launch playbook, and leadgen agent",
        "desc_hu": "Virtuális GTM társalapító: piacra lépési stratégiák, lead-generálás és termékbevezetési forgatókönyvek végrehajtása.",
        "desc_en": "Autonomous Go-To-Market co-founder skill orchestrating product launches, positioning teardowns, and user acquisition."
    },
    "EveryInc/charlie-cfo-skill": {
        "title": "Charlie CFO Skill",
        "title_en": "Charlie CFO Skill — Autonomous startup finance, runway forecasting, and unit economics agent",
        "desc_hu": "Virtuális CFO ágensképesség: pénzügyi kifutási idő (runway), egységnyi gazdaságtan (unit economics) és költségvetés-elemzés.",
        "desc_en": "Virtual Chief Financial Officer skill for AI agents: cash runway projection, SaaS unit metrics, and financial modeling."
    },
    "ognjengt/founder-skills": {
        "title": "Founder Skills",
        "title_en": "Founder Skills — Startup founder decision support, fundraising decks, and operational mastery skill",
        "desc_hu": "Startup alapítói döntéstámogatás, pitch deck készítés, befektetői kommunikáció és operatív vezetés ágensekkel.",
        "desc_en": "Executive founder skill set: investor pitching, problem validation, board memo drafting, and startup operations."
    }
}

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

    print(f"Starting import of 20 Agent Skills...")

    for item_info in SKILL_REPOS:
        repo = item_info["repo"]
        meta = CUSTOM_METADATA.get(repo, {})

        # Fetch repo details from GitHub API
        url = f"https://api.github.com/repos/{repo}"
        gh_data = {}
        try:
            req = urllib.request.Request(url, headers={"User-Agent": "NexusHub-Curator/2.0"})
            with urllib.request.urlopen(req, timeout=8) as resp:
                gh_data = json.loads(resp.read().decode("utf-8"))
        except Exception as e:
            print(f"[-] Could not fetch GitHub API for {repo}: {e}")

        stars = int(gh_data.get("stargazers_count") or 500)
        title = meta.get("title") or gh_data.get("name") or repo.split("/")[1]
        title_en = meta.get("title_en") or f"{title} — {gh_data.get('description', '')}"
        desc_hu = meta.get("desc_hu") or gh_data.get("description") or ""
        desc_en = meta.get("desc_en") or gh_data.get("description") or ""
        function_title = f"{title} — {desc_hu[:60]}..."
        year = int((gh_data.get("created_at") or "2025")[:4])
        tags = (gh_data.get("topics") or [title.lower(), "agent", "skill", "open-source"])[:6]

        clean_item = {
            "id": f"skill-{repo.replace('/', '-')}",
            "repo_name": repo,
            "title": title,
            "function_title": function_title,
            "title_en": title_en,
            "function_title_en": title_en,
            "description": desc_hu,
            "description_en": desc_en,
            "main_category": item_info["main_cat"],
            "sub_category": item_info["sub_cat"],
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
            # Update existing with rich metadata
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
            updated_count += 1
            print(f"  [*] Updated existing: {title} ({stars} ⭐)")
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
            existing_repos[repo.lower()] = True
            inserted_count += 1
            print(f"  [+] Inserted: {title} ({stars} ⭐) - {item_info['main_cat']}")

        time.sleep(0.4)

    conn.commit()
    conn.close()

    cat["last_updated"] = time.strftime("%Y-%m-%d %H:%M:%S")
    with open(cat_path, "w", encoding="utf-8") as f:
        json.dump(cat, f, ensure_ascii=False, indent=2)

    print(f"\nCompleted! Inserted: {inserted_count}, Updated: {updated_count}")

if __name__ == "__main__":
    run_import()
