import sqlite3
import json
import os

NEW_REPOS = [
    {
        "id": "repo-virattt-ai-hedge-fund",
        "repo_name": "virattt/ai-hedge-fund",
        "title": "AI Hedge Fund",
        "function_title": "AI Hedge Fund — Autonóm multi-ágens kereskedési döntéshozó tanács",
        "title_en": "AI Hedge Fund — Autonomous multi-agent investment committee for comprehensive trading decisions",
        "function_title_en": "AI Hedge Fund — Autonomous multi-agent investment committee for comprehensive trading decisions",
        "description": "Multi-ágens architektúra, ahol specializált AI ágensek (fundamentális elemző, technikai elemző és kockázatkezelő) vitatják meg a pozíciókat döntéshozatal előtt.",
        "description_en": "An autonomous multi-agent trading system where specialized AI agents (value investing, technical analysis, and risk management) collaborate and debate before making execution decisions.",
        "main_category": "Pénzügy, Tőzsde & Kripto Elemzés",
        "sub_category": "Algoritmikus Kereskedés & Botok",
        "thumbnail_url": "https://opengraph.githubassets.com/1/virattt/ai-hedge-fund",
        "video_url": "",
        "has_video": False,
        "video_demo": "",
        "stars": 63548,
        "year": 2026,
        "url": "https://github.com/virattt/ai-hedge-fund",
        "creator": "virattt",
        "tags": ["ai-hedge-fund", "multi-agent", "trading-agents", "quantitative-finance", "risk-management"],
        "is_pinned": False
    },
    {
        "id": "repo-nautechsystems-nautilus_trader",
        "repo_name": "nautechsystems/nautilus_trader",
        "title": "NautilusTrader",
        "function_title": "NautilusTrader — Nagy megbízhatóságú, determinisztikus Rust-alapú kereskedési és backtesting motor",
        "title_en": "NautilusTrader — High-performance deterministic Rust-native trading engine and backtesting platform",
        "function_title_en": "NautilusTrader — High-performance deterministic Rust-native trading engine and backtesting platform",
        "description": "Professzionális, eseményvezérelt algoritmikus kereskedési infrastruktúra. Mikroszekundumos végrehajtási késleltetés Rust maggal, determinisztikus backtestinggel és Python API-val.",
        "description_en": "A production-grade, highly-performant algorithmic trading platform developed in Rust, providing event-driven backtesting, live execution, and multi-asset connectivity.",
        "main_category": "Pénzügy, Tőzsde & Kripto Elemzés",
        "sub_category": "Backtesting & Portfóliókezelés",
        "thumbnail_url": "https://opengraph.githubassets.com/1/nautechsystems/nautilus_trader",
        "video_url": "",
        "has_video": False,
        "video_demo": "",
        "stars": 29143,
        "year": 2025,
        "url": "https://github.com/nautechsystems/nautilus_trader",
        "creator": "nautechsystems",
        "tags": ["nautilus-trader", "rust", "hft", "backtesting", "event-driven", "execution"],
        "is_pinned": False
    },
    {
        "id": "repo-elizaos-eliza",
        "repo_name": "elizaOS/eliza",
        "title": "Eliza (elizaOS)",
        "function_title": "Eliza — On-chain autonóm ágens operációs rendszer és kripto-tárca automatizáció",
        "title_en": "Eliza — Autonomous on-chain agent framework for DeFi, crypto wallets, and social intelligence",
        "function_title_en": "Eliza — Autonomous on-chain agent framework for DeFi, crypto wallets, and social intelligence",
        "description": "Nyílt forráskódú multi-ágens keretrendszer, amely lehetővé teszi, hogy az AI közvetlenül interakcióba lépjen okosszerződésekkel, kripto-tárcákkal és DeFi protokollokkal.",
        "description_en": "A simple, fast, and lightweight multi-agent operating system designed to build autonomous agents capable of interacting with on-chain protocols, crypto wallets, and social platforms.",
        "main_category": "Pénzügy, Tőzsde & Kripto Elemzés",
        "sub_category": "Kripto & On-Chain Metrikák",
        "thumbnail_url": "https://opengraph.githubassets.com/1/elizaOS/eliza",
        "video_url": "",
        "has_video": False,
        "video_demo": "",
        "stars": 19374,
        "year": 2026,
        "url": "https://github.com/elizaOS/eliza",
        "creator": "elizaOS",
        "tags": ["eliza", "elizaos", "crypto-agents", "defi", "onchain", "autonomous-agents"],
        "is_pinned": False
    },
    {
        "id": "repo-ai4finance-finrl",
        "repo_name": "AI4Finance-Foundation/FinRL",
        "title": "FinRL",
        "function_title": "FinRL — Megerősítéses tanulás (Reinforcement Learning) pénzügyi piacokhoz és portfólió-optimalizáláshoz",
        "title_en": "FinRL — Deep reinforcement learning framework for quantitative trading and financial market research",
        "function_title_en": "FinRL — Deep reinforcement learning framework for quantitative trading and financial market research",
        "description": "A Columbia Egyetem és az AI4Finance nyílt forráskódú keretrendszere, amely mély megerősítéses tanulási (DRL) algoritmusokat tanít be tőzsdei adatokon portfólióallokációra és arbitrázsra.",
        "description_en": "The first open-source framework dedicated to financial reinforcement learning, helping quant researchers train deep RL agents for stock trading, portfolio allocation, and automated execution.",
        "main_category": "Pénzügy, Tőzsde & Kripto Elemzés",
        "sub_category": "Algoritmikus Kereskedés & Botok",
        "thumbnail_url": "https://opengraph.githubassets.com/1/AI4Finance-Foundation/FinRL",
        "video_url": "",
        "has_video": False,
        "video_demo": "",
        "stars": 16329,
        "year": 2025,
        "url": "https://github.com/AI4Finance-Foundation/FinRL",
        "creator": "AI4Finance-Foundation",
        "tags": ["finrl", "reinforcement-learning", "deep-rl", "quantitative-trading", "portfolio-management"],
        "is_pinned": False
    },
    {
        "id": "repo-jesse-ai-jesse",
        "repo_name": "jesse-ai/jesse",
        "title": "Jesse",
        "function_title": "Jesse — Fejlett Python kripto kereskedési bot, valósághű backtestinggel és optimalizálással",
        "title_en": "Jesse — Advanced Python crypto trading bot designed for backtesting, optimizing, and live execution",
        "function_title_en": "Jesse — Advanced Python crypto trading bot designed for backtesting, optimizing, and live execution",
        "description": "Kifejezetten kriptovaluta kereskedésre tervezett Python keretrendszer, amely pontos csúszási (slippage) és megbízási könyv szimulációval akadályozza meg a túlillesztést (overfitting) backtest közben.",
        "description_en": "An advanced algorithmic crypto trading bot written in Python, featuring realistic backtesting that accounts for slippage, order books, and metrics to prevent overfitting.",
        "main_category": "Pénzügy, Tőzsde & Kripto Elemzés",
        "sub_category": "Backtesting & Portfóliókezelés",
        "thumbnail_url": "https://opengraph.githubassets.com/1/jesse-ai/jesse",
        "video_url": "",
        "has_video": False,
        "video_demo": "",
        "stars": 8534,
        "year": 2025,
        "url": "https://github.com/jesse-ai/jesse",
        "creator": "jesse-ai",
        "tags": ["jesse", "crypto-bot", "backtesting", "trading-strategy", "python"],
        "is_pinned": False
    }
]

db_path = "data/nexus.db"
conn = sqlite3.connect(db_path)
cursor = conn.cursor()

inserted_db = 0
for item in NEW_REPOS:
    cursor.execute("SELECT id FROM repositories WHERE repo_name = ?", (item["repo_name"],))
    if not cursor.fetchone():
        cursor.execute("""
            INSERT INTO repositories (
                id, repo_name, title, function_title, title_en, function_title_en,
                description, description_en, main_category, sub_category,
                thumbnail_url, video_url, video_demo, has_video, stars, year,
                url, creator, tags, is_pinned
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            item["id"],
            item["repo_name"],
            item["title"],
            item["function_title"],
            item["title_en"],
            item["function_title_en"],
            item["description"],
            item["description_en"],
            item["main_category"],
            item["sub_category"],
            item["thumbnail_url"],
            item["video_url"],
            item["video_demo"],
            1 if item["has_video"] else 0,
            item["stars"],
            item["year"],
            item["url"],
            item["creator"],
            json.dumps(item["tags"], ensure_ascii=False),
            1 if item["is_pinned"] else 0
        ))
        inserted_db += 1

conn.commit()
conn.close()
print(f"Inserted {inserted_db} new items into nexus.db")

# Backup to catalogue.json
cat_path = "data/catalogue.json"
with open(cat_path, "r", encoding="utf-8") as f:
    cat = json.load(f)

existing_repos = {i.get("repo_name") for i in cat.get("items", [])}
inserted_cat = 0
for item in NEW_REPOS:
    if item["repo_name"] not in existing_repos:
        cat.setdefault("items", []).insert(0, item)
        inserted_cat += 1

cat["last_updated"] = "2026-09-20 01:52:00"
with open(cat_path, "w", encoding="utf-8") as f:
    json.dump(cat, f, ensure_ascii=False, indent=2)

print(f"Inserted {inserted_cat} new items into catalogue.json")

# Verify new count in DB
conn = sqlite3.connect(db_path)
c = conn.cursor()
c.execute("SELECT COUNT(*) FROM repositories")
total_db = c.fetchone()[0]
c.execute("SELECT COUNT(*) FROM repositories WHERE main_category = 'Pénzügy, Tőzsde & Kripto Elemzés'")
fin_db = c.fetchone()[0]
print(f"Total repos in DB: {total_db}, in FinTech category: {fin_db}")
conn.close()
