import sqlite3
import json

db_path = 'data/nexus.db'
conn = sqlite3.connect(db_path)
c = conn.cursor()

c.execute("SELECT id FROM repositories WHERE repo_name = 'jarrodwatts/jev-trader'")
row = c.fetchone()

if row:
    c.execute("""
        UPDATE repositories SET
            title = 'Jev Trader — Monad AI Orderbook Bot',
            function_title = 'Jev Trader — AI kereskedési döntés minden Monad blokkban (~300 ms)',
            title_en = 'Jev Trader — Autonomous AI trading bot on Monad (Kuru MON-USDC)',
            function_title_en = 'Jev Trader — Autonomous AI trading bot on Monad (Kuru MON-USDC)',
            description = 'Minden Monad blokkban döntést hozó AI trading bot. Egy Jev modell figyeli a Kuru MON-USDC ajánlati könyvet, és ~300 ms-onként helyez el limit megbízásokat a spread learatására.',
            description_en = 'Autonomous AI trading bot making trade decisions on every Monad block (~300ms). Watches Kuru MON-USDC order book and places post-only limit orders to capture the spread.',
            main_category = 'Pénzügy, Tőzsde & Kripto Elemzés',
            sub_category = 'Algoritmikus Kereskedés & Botok',
            stars = 1247,
            tags = '["monad", "kuru", "ai-trader", "orderbook", "high-frequency", "hft"]'
        WHERE repo_name = 'jarrodwatts/jev-trader'
    """)
    print("Updated existing jev-trader in local nexus.db")
else:
    c.execute("""
        INSERT INTO repositories (
            id, repo_name, title, function_title, title_en, function_title_en,
            description, description_en, main_category, sub_category,
            thumbnail_url, video_url, video_demo, has_video, stars, year,
            url, creator, tags, is_pinned
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, (
        'verified-jarrodwatts-jev-trader',
        'jarrodwatts/jev-trader',
        'Jev Trader — Monad AI Orderbook Bot',
        'Jev Trader — AI kereskedési döntés minden Monad blokkban (~300 ms)',
        'Jev Trader — Autonomous AI trading bot on Monad (Kuru MON-USDC)',
        'Jev Trader — Autonomous AI trading bot on Monad (Kuru MON-USDC)',
        'Minden Monad blokkban döntést hozó AI trading bot. Egy Jev modell figyeli a Kuru MON-USDC ajánlati könyvet, és ~300 ms-onként helyez el limit megbízásokat a spread learatására.',
        'Autonomous AI trading bot making trade decisions on every Monad block (~300ms). Watches Kuru MON-USDC order book and places post-only limit orders to capture the spread.',
        'Pénzügy, Tőzsde & Kripto Elemzés',
        'Algoritmikus Kereskedés & Botok',
        'https://opengraph.githubassets.com/1/jarrodwatts/jev-trader',
        '', '', 0, 1247, 2026,
        'https://github.com/jarrodwatts/jev-trader',
        'jarrodwatts',
        json.dumps(['monad', 'kuru', 'ai-trader', 'orderbook', 'high-frequency', 'hft']),
        0
    ))
    print("Inserted jev-trader into local nexus.db")

conn.commit()
conn.close()

# Also sync to catalogue.json
with open('data/catalogue.json', 'r', encoding='utf-8') as f:
    cat = json.load(f)

existing = next((i for i in cat.get('items', []) if i.get('repo_name') == 'jarrodwatts/jev-trader'), None)
if not existing:
    cat.setdefault('items', []).insert(0, {
        'id': 'verified-jarrodwatts-jev-trader',
        'repo_name': 'jarrodwatts/jev-trader',
        'title': 'Jev Trader — Monad AI Orderbook Bot',
        'function_title': 'Jev Trader — AI kereskedési döntés minden Monad blokkban (~300 ms)',
        'title_en': 'Jev Trader — Autonomous AI trading bot on Monad (Kuru MON-USDC)',
        'function_title_en': 'Jev Trader — Autonomous AI trading bot on Monad (Kuru MON-USDC)',
        'description': 'Minden Monad blokkban döntést hozó AI trading bot. Egy Jev modell figyeli a Kuru MON-USDC ajánlati könyvet, és ~300 ms-onként helyez el limit megbízásokat a spread learatására.',
        'description_en': 'Autonomous AI trading bot making trade decisions on every Monad block (~300ms). Watches Kuru MON-USDC order book and places post-only limit orders to capture the spread.',
        'main_category': 'Pénzügy, Tőzsde & Kripto Elemzés',
        'sub_category': 'Algoritmikus Kereskedés & Botok',
        'thumbnail_url': 'https://opengraph.githubassets.com/1/jarrodwatts/jev-trader',
        'video_url': '',
        'has_video': False,
        'video_demo': '',
        'stars': 1247,
        'year': 2026,
        'url': 'https://github.com/jarrodwatts/jev-trader',
        'creator': 'jarrodwatts',
        'tags': ['monad', 'kuru', 'ai-trader', 'orderbook', 'high-frequency', 'hft'],
        'is_pinned': False
    })
    with open('data/catalogue.json', 'w', encoding='utf-8') as f:
        json.dump(cat, f, ensure_ascii=False, indent=2)
    print("Synced jev-trader to catalogue.json")
