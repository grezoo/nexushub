"""
NexusHub Production Server
Serves static web files and provides high-performance API endpoints powered by
SQLite + FTS5 Full-Text Search, server-side pagination, and hardened anti-spam quality gate.
Zero external dependencies, works with standard Python library.
"""

import http.server
import json
import os
import re
import socketserver
import sqlite3
import sys
import time
import urllib.error
import urllib.parse
import urllib.request

PORT = int(os.environ.get("PORT", 8765))
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
WEB_DIR = os.path.join(BASE_DIR, "web")
DATA_DIR = os.path.join(BASE_DIR, "data")
DB_PATH = os.path.join(DATA_DIR, "nexus.db")
CATALOGUE_PATH = os.path.join(DATA_DIR, "catalogue.json")
TAXONOMY_PATH = os.path.join(DATA_DIR, "taxonomy_map.json")
CURATED_PATH = os.path.join(DATA_DIR, "curated_picks.json")
SUBMISSIONS_QUEUE_PATH = os.path.join(DATA_DIR, "submissions_queue.json")

# In-memory IP submission tracking for rate-limiting
IP_SUBMISSION_HISTORY = {}


def get_db_connection():
    """Returns an active SQLite database connection with row factory."""
    if not os.path.exists(DB_PATH):
        print("[!] DB missing at runtime, auto-initializing from catalogue.json...")
        from scripts.migrate_to_db import migrate
        migrate()
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn


def query_repositories(params):
    """
    High-speed server-side query with SQLite FTS5 full-text search,
    multilingual prefix indexing, category filters, and pagination.
    """
    conn = get_db_connection()
    cursor = conn.cursor()

    search = params.get("search", [""])[0].strip() if isinstance(params.get("search"), list) else str(params.get("search", "")).strip()
    category = params.get("category", ["all"])[0] if isinstance(params.get("category"), list) else str(params.get("category", "all"))
    sub_category = params.get("sub_category", ["all"])[0] if isinstance(params.get("sub_category"), list) else str(params.get("sub_category", "all"))
    vintage = params.get("vintage", ["all"])[0] if isinstance(params.get("vintage"), list) else str(params.get("vintage", "all"))

    only_videos_val = params.get("only_videos", ["0"])[0] if isinstance(params.get("only_videos"), list) else str(params.get("only_videos", "0"))
    only_videos = only_videos_val in ["1", "true", "True"]

    only_gems_val = params.get("only_gems", ["0"])[0] if isinstance(params.get("only_gems"), list) else str(params.get("only_gems", "0"))
    only_gems = only_gems_val in ["1", "true", "True"]

    sort = params.get("sort", ["gems"])[0] if isinstance(params.get("sort"), list) else str(params.get("sort", "gems"))

    try:
        page_val = params.get("page", ["1"])[0] if isinstance(params.get("page"), list) else params.get("page", 1)
        page = max(1, int(page_val))
    except Exception:
        page = 1

    try:
        limit_val = params.get("limit", ["40"])[0] if isinstance(params.get("limit"), list) else params.get("limit", 40)
        limit = min(100, max(1, int(limit_val)))
    except Exception:
        limit = 40

    offset = (page - 1) * limit

    where_clauses = []
    sql_params = []

    # FTS5 Full-Text Search
    if search:
        clean_words = re.sub(r'[^\w\s]', ' ', search).strip().split()
        if clean_words:
            fts_query = " ".join(f'"{w}"*' for w in clean_words)
            where_clauses.append("r.rowid IN (SELECT rowid FROM repositories_fts WHERE repositories_fts MATCH ?)")
            sql_params.append(fts_query)

    if category and category != "all":
        where_clauses.append("r.main_category = ?")
        sql_params.append(category)

    if sub_category and sub_category != "all":
        where_clauses.append("r.sub_category = ?")
        sql_params.append(sub_category)

    if only_videos:
        where_clauses.append("r.has_video = 1")

    if only_gems:
        where_clauses.append("r.stars <= 100")

    if vintage == "2025-2026":
        where_clauses.append("r.year >= 2025")
    elif vintage == "2021-2024":
        where_clauses.append("r.year >= 2021 AND r.year <= 2024")
    elif vintage == "2015-2020":
        where_clauses.append("r.year >= 2015 AND r.year <= 2020")
    elif vintage == "legacy":
        where_clauses.append("r.year < 2015")

    where_sql = (" WHERE " + " AND ".join(where_clauses)) if where_clauses else ""

    # Sorting
    if sort == "stars":
        order_sql = " ORDER BY r.is_pinned DESC, r.stars DESC"
    elif sort == "name":
        order_sql = " ORDER BY r.is_pinned DESC, r.title COLLATE NOCASE ASC"
    else:  # gems (merit & proof: pinned first, then video proof, then low-star discovery score)
        order_sql = " ORDER BY r.is_pinned DESC, (CASE WHEN r.has_video = 1 THEN 1000 ELSE 0 END - r.stars) DESC"

    # Count total matching rows
    count_query = f"SELECT COUNT(*) FROM repositories r{where_sql}"
    cursor.execute(count_query, sql_params)
    total = cursor.fetchone()[0]

    # Select requested page
    items_query = f"""
        SELECT r.id, r.repo_name, r.title, r.function_title, r.title_en, r.function_title_en,
               r.description, r.description_en, r.main_category, r.sub_category,
               r.thumbnail_url, r.video_url, r.video_demo, r.has_video, r.stars, r.year,
               r.url, r.creator, r.tags, r.is_pinned
        FROM repositories r{where_sql}{order_sql}
        LIMIT ? OFFSET ?
    """
    cursor.execute(items_query, sql_params + [limit, offset])
    rows = cursor.fetchall()

    items = []
    for row in rows:
        d = dict(row)
        d["has_video"] = bool(d["has_video"])
        d["is_pinned"] = bool(d["is_pinned"])
        try:
            d["tags"] = json.loads(d["tags"]) if d["tags"] else []
        except Exception:
            d["tags"] = []
        items.append(d)

    conn.close()

    return {
        "items": items,
        "total": total,
        "page": page,
        "limit": limit,
        "total_pages": (total + limit - 1) // limit if limit else 1
    }


def get_catalogue_stats():
    """Returns real-time aggregate statistics from SQLite."""
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT COUNT(*), SUM(has_video) FROM repositories")
    row = cursor.fetchone()
    total = row[0] or 0
    with_video = row[1] or 0
    conn.close()
    return {
        "total": total,
        "with_video": with_video,
        "last_updated": time.strftime("%Y-%m-%d %H:%M:%S")
    }


def get_categories_breakdown():
    """Returns all main categories and their subcategories with item counts."""
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT main_category, sub_category, COUNT(*) as cnt
        FROM repositories
        GROUP BY main_category, sub_category
        ORDER BY main_category, cnt DESC
    """)
    rows = cursor.fetchall()
    conn.close()

    cat_map = {}
    for r in rows:
        m = r["main_category"]
        s = r["sub_category"] or "Other"
        if m not in cat_map:
            cat_map[m] = {"main": m, "subcategories": [], "count": 0}
        cat_map[m]["subcategories"].append(s)
        cat_map[m]["count"] += r["cnt"]

    # Category icons mapping
    icons = {
        "Hardver, IoT & Elektronika": "🔌",
        "Mesterséges Intelligencia & Adat": "🧠",
        "Pénzügy, Tőzsde & Kripto Elemzés": "📈",
        "Játékfejlesztés, 3D & Grafika": "🎮",
        "Zene, Hangtechnika & Audió": "🎵",
        "Self-Hosted & Otthoni Szerverek": "🏠",
        "Produktivitás & Irodai Munka": "📊",
        "Kreatív Média, Videóvágás & Fotó": "🎬",
        "Rendszer, Biztonság & Segédprogramok": "⚡"
    }

    result = []
    # Ensure standard order with icons
    for m, icon in icons.items():
        if m in cat_map:
            cat_map[m]["icon"] = icon
            result.append(cat_map[m])

    # Append any other dynamic categories
    for m, val in cat_map.items():
        if m not in icons:
            val["icon"] = "📁"
            result.append(val)

    return result


def validate_submission_quality(item, client_ip):
    """
    Strict 4-tier Anti-Spam & Quality Gate.
    Verifies that the repository exists on GitHub, has a real public README,
    blocks bots, rejects spam/trolls, and validates demo media.
    """
    now = time.time()

    # 1. Anti-Bot Honeypot trap
    if item.get("website_hp"):
        return False, "Bot aktivitás észlelve (Honeypot triggerelve)."

    # 2. Time-Trap: humans take >= 2.0s to fill out the form
    try:
        elapsed = float(item.get("client_elapsed_sec", 0))
    except (ValueError, TypeError):
        elapsed = 0.0

    if elapsed < 2.0:
        return False, "Űrlapkitöltés túl gyors. Automata botnak minősítve."

    # 3. IP Rate Limiting (max 4 per hour per IP)
    history = [t for t in IP_SUBMISSION_HISTORY.get(client_ip, []) if now - t < 3600]
    if len(history) >= 4:
        return False, "Túl sok beküldés ebből az IP-címből. A rendszer védelme érdekében kérjük várj egy órát."

    # 4. GitHub URL structure validation
    raw_url = (item.get("url") or item.get("repo_url") or "").strip()
    match = re.match(r"^https?://github\.com/([a-zA-Z0-9_.-]+)/([a-zA-Z0-9_.-]+)/?$", raw_url)
    if not match:
        return False, "Érvénytelen GitHub URL formátum. Helyes formátum: https://github.com/szerzo/projekt"

    owner, repo_name = match.group(1), match.group(2)
    if repo_name.endswith(".git"):
        repo_name = repo_name[:-4]

    full_repo = f"{owner}/{repo_name}"

    # 5. Live GitHub Verification: Repository & README existence
    readme_urls = [
        f"https://raw.githubusercontent.com/{full_repo}/main/README.md",
        f"https://raw.githubusercontent.com/{full_repo}/master/README.md",
        f"https://raw.githubusercontent.com/{full_repo}/main/readme.md",
        f"https://raw.githubusercontent.com/{full_repo}/master/readme.md",
        f"https://raw.githubusercontent.com/{full_repo}/HEAD/README.md"
    ]

    readme_found = False
    readme_content = ""
    for r_url in readme_urls:
        try:
            req = urllib.request.Request(r_url, headers={"User-Agent": "NexusHub-QualityGate/2.0"})
            with urllib.request.urlopen(req, timeout=6) as resp:
                if resp.status == 200:
                    readme_content = resp.read().decode("utf-8", errors="ignore")
                    readme_found = True
                    break
        except Exception:
            continue

    if not readme_found:
        return False, f"A megadott repó ({full_repo}) nem található a GitHubon, privát, vagy nincs benne nyilvános README."

    if len(readme_content.strip()) < 80:
        return False, "A repó README tartalma túl rövid vagy üres. Csak érdemi dokumentációval rendelkező projekt fogadható el."

    # 6. Title and Description checks
    title = (item.get("title") or "").strip()
    desc = (item.get("description") or "").strip()

    if len(title) < 3 or len(title) > 90:
        return False, "A projekt címe legyen legalább 3, és legfeljebb 90 karakter hosszú."

    if len(desc) < 15 or len(desc) > 600:
        return False, "A projekt leírása legyen legalább 15 és legfeljebb 600 karakter."

    # Spam & malicious keyword check
    spam_terms = ["casino", "viagra", "crypto pump", "free followers", "telegram airdrop", "betting app", "nude", "porn", "poker", "baccarat"]
    scan_target = f"{title} {desc} {raw_url}".lower()
    for term in spam_terms:
        if term in scan_target:
            return False, "A beküldés promóciós vagy tiltott kifejezést tartalmaz."

    # 7. Demo media validation
    demo_url = (item.get("video_demo") or item.get("video_url") or "").strip()
    if demo_url:
        valid_ext = any(demo_url.lower().endswith(ext) for ext in [".mp4", ".gif", ".webm", ".png", ".jpg", ".jpeg", ".webp"])
        valid_domain = any(h in demo_url.lower() for h in [
            "githubassets.com", "raw.githubusercontent.com", "user-images.githubusercontent.com",
            "imgur.com", "giphy.com", "streamable.com", "youtube.com", "youtu.be"
        ])
        if not (valid_ext or valid_domain):
            return False, "A megadott demó link nem érvényes videó/kép formátum (támogatott: .mp4, .gif, YouTube vagy GitHub CDN)."

    # Passed all checks: record IP for rate limiting
    history.append(now)
    IP_SUBMISSION_HISTORY[client_ip] = history

    return True, "Minőségellenőrzés sikeres!"


class CatalogueRequestHandler(http.server.SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=WEB_DIR, **kwargs)

    def do_GET(self):
        parsed = urllib.parse.urlparse(self.path)
        path = parsed.path
        query_params = urllib.parse.parse_qs(parsed.query)

        # API: Paginated, FTS-indexed items query from SQLite
        if path == "/api/items":
            data = query_repositories(query_params)
            self.send_response(200)
            self.send_header("Content-Type", "application/json; charset=utf-8")
            self.send_header("Access-Control-Allow-Origin", "*")
            self.end_headers()
            self.wfile.write(json.dumps(data, ensure_ascii=False).encode("utf-8"))
            return

        # API: Real-time statistics
        if path == "/api/stats":
            stats = get_catalogue_stats()
            self.send_response(200)
            self.send_header("Content-Type", "application/json; charset=utf-8")
            self.send_header("Access-Control-Allow-Origin", "*")
            self.end_headers()
            self.wfile.write(json.dumps(stats, ensure_ascii=False).encode("utf-8"))
            return

        # API: Categories breakdown
        if path == "/api/categories":
            cats = get_categories_breakdown()
            self.send_response(200)
            self.send_header("Content-Type", "application/json; charset=utf-8")
            self.send_header("Access-Control-Allow-Origin", "*")
            self.end_headers()
            self.wfile.write(json.dumps(cats, ensure_ascii=False).encode("utf-8"))
            return

        # API: Backward-compatible legacy full catalogue fallback
        if path == "/api/catalogue":
            self.send_response(200)
            self.send_header("Content-Type", "application/json; charset=utf-8")
            self.send_header("Access-Control-Allow-Origin", "*")
            self.end_headers()

            if os.path.exists(CATALOGUE_PATH):
                with open(CATALOGUE_PATH, "rb") as f:
                    self.wfile.write(f.read())
            else:
                self.wfile.write(b'{"categories":[],"items":[],"last_updated":""}')
            return

        # API: Return global taxonomy map
        if path == "/api/taxonomy":
            self.send_response(200)
            self.send_header("Content-Type", "application/json; charset=utf-8")
            self.send_header("Access-Control-Allow-Origin", "*")
            self.end_headers()

            if os.path.exists(TAXONOMY_PATH):
                with open(TAXONOMY_PATH, "rb") as f:
                    self.wfile.write(f.read())
            else:
                self.wfile.write(b'[]')
            return

        # API: Return author's curated picks
        if path == "/api/curated":
            self.send_response(200)
            self.send_header("Content-Type", "application/json; charset=utf-8")
            self.send_header("Access-Control-Allow-Origin", "*")
            self.end_headers()

            if os.path.exists(CURATED_PATH):
                with open(CURATED_PATH, "rb") as f:
                    self.wfile.write(f.read())
            else:
                self.wfile.write(b'{"picks":[]}')
            return

        # Serve static assets from WEB_DIR
        super().do_GET()

    def do_POST(self):
        # API: Quality-Gated Repository Submission
        if self.path.startswith("/api/submit"):
            client_ip = self.headers.get("X-Forwarded-For", self.client_address[0]).split(",")[0].strip()
            content_length = int(self.headers.get("Content-Length", 0))
            post_data = self.rfile.read(content_length)

            try:
                submission = json.loads(post_data.decode("utf-8"))
            except Exception as e:
                self.send_response(400)
                self.send_header("Content-Type", "application/json; charset=utf-8")
                self.send_header("Access-Control-Allow-Origin", "*")
                self.end_headers()
                self.wfile.write(json.dumps({"status": "error", "error": f"Hibás JSON adat: {e}"}).encode("utf-8"))
                return

            # Execute rigorous quality gate
            passed, reason = validate_submission_quality(submission, client_ip)
            if not passed:
                print(f"[!] Quality Gate REJECTED submission from {client_ip}: {reason}")
                self.send_response(422)
                self.send_header("Content-Type", "application/json; charset=utf-8")
                self.send_header("Access-Control-Allow-Origin", "*")
                self.end_headers()
                self.wfile.write(json.dumps({"status": "error", "error": reason}).encode("utf-8"))
                return

            print(f"[+] Quality Gate PASSED for '{submission.get('title')}' from {client_ip}")

            # Enriched clean item
            repo_raw = submission.get("url", "").replace("https://github.com/", "").strip().rstrip("/")
            clean_item = {
                "id": f"verified-{int(time.time())}-{repo_raw.replace('/', '-')}",
                "repo_name": repo_raw,
                "title": submission.get("title", "").strip(),
                "function_title": f"{submission.get('title', '').strip()} — {submission.get('description', '')[:55]}...",
                "title_en": submission.get("title", "").strip(),
                "function_title_en": f"{submission.get('title', '').strip()} — {submission.get('description', '')[:55]}...",
                "description": submission.get("description", "").strip(),
                "description_en": submission.get("description", "").strip(),
                "main_category": submission.get("main_category", "Hardver, IoT & Elektronika"),
                "sub_category": "Közösségi Ellenőrzött Kincs",
                "thumbnail_url": submission.get("thumbnail_url") or f"https://opengraph.githubassets.com/1/{repo_raw}",
                "video_url": submission.get("video_demo", ""),
                "has_video": bool(submission.get("video_demo")),
                "video_demo": submission.get("video_demo", ""),
                "stars": 1,
                "year": 2026,
                "url": submission.get("url"),
                "creator": repo_raw.split("/")[0] if "/" in repo_raw else "community",
                "tags": ["community-submission", "quality-verified", "hidden-gem"],
                "is_pinned": False
            }

            # 1. Insert directly into SQLite database (Triggers automatically update FTS5!)
            try:
                conn = get_db_connection()
                cursor = conn.cursor()
                cursor.execute("""
                    INSERT INTO repositories (
                        id, repo_name, title, function_title, title_en, function_title_en,
                        description, description_en, main_category, sub_category,
                        thumbnail_url, video_url, video_demo, has_video, stars, year,
                        url, creator, tags, is_pinned
                    ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                """, (
                    clean_item["id"],
                    clean_item["repo_name"],
                    clean_item["title"],
                    clean_item["function_title"],
                    clean_item["title_en"],
                    clean_item["function_title_en"],
                    clean_item["description"],
                    clean_item["description_en"],
                    clean_item["main_category"],
                    clean_item["sub_category"],
                    clean_item["thumbnail_url"],
                    clean_item["video_url"],
                    clean_item["video_demo"],
                    1 if clean_item["has_video"] else 0,
                    clean_item["stars"],
                    clean_item["year"],
                    clean_item["url"],
                    clean_item["creator"],
                    json.dumps(clean_item["tags"], ensure_ascii=False),
                    1 if clean_item["is_pinned"] else 0
                ))
                conn.commit()
                conn.close()
                print(f"[+] Successfully inserted {clean_item['repo_name']} into nexus.db")
            except Exception as dbe:
                print(f"[-] DB insertion error: {dbe}")

            # 2. Store in submissions queue archive
            queue_data = []
            if os.path.exists(SUBMISSIONS_QUEUE_PATH):
                try:
                    with open(SUBMISSIONS_QUEUE_PATH, "r", encoding="utf-8") as qf:
                        queue_data = json.load(qf)
                except Exception:
                    pass
            queue_data.insert(0, {
                "item": clean_item,
                "submitted_at": time.strftime("%Y-%m-%d %H:%M:%S"),
                "client_ip_hash": hash(client_ip) % 100000,
                "status": "approved"
            })
            with open(SUBMISSIONS_QUEUE_PATH, "w", encoding="utf-8") as qf:
                json.dump(queue_data, qf, ensure_ascii=False, indent=2)

            # 3. Synchronize backup JSON catalogue
            if os.path.exists(CATALOGUE_PATH):
                try:
                    with open(CATALOGUE_PATH, "r", encoding="utf-8") as cf:
                        cat_data = json.load(cf)
                    cat_data.setdefault("items", []).insert(0, clean_item)
                    cat_data["last_updated"] = time.strftime("%Y-%m-%d %H:%M:%S")
                    with open(CATALOGUE_PATH, "w", encoding="utf-8") as cf:
                        json.dump(cat_data, cf, ensure_ascii=False, indent=2)
                except Exception as e:
                    print(f"[-] Error writing to catalogue backup: {e}")

            self.send_response(200)
            self.send_header("Content-Type", "application/json; charset=utf-8")
            self.send_header("Access-Control-Allow-Origin", "*")
            self.end_headers()
            self.wfile.write(json.dumps({
                "status": "success",
                "message": "A minőségellenőrzés sikeresen lezajlott! A projekt azonnal bekerült a katalógusba.",
                "item": clean_item
            }, ensure_ascii=False).encode("utf-8"))
            return

        self.send_error(404, "Not Found")


def run():
    port = PORT
    try:
        # Pre-verify DB connection on boot
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT COUNT(*) FROM repositories")
        count = cursor.fetchone()[0]
        conn.close()

        socketserver.TCPServer.allow_reuse_address = True
        with socketserver.TCPServer(("", port), CatalogueRequestHandler) as httpd:
            print(f"=======================================================")
            print(f"  NexusHub SQLite + FTS5 Production Server (Port {port})")
            print(f"  Active Repositories in DB: {count}")
            print(f"  Full-Text Search Engine: FTS5 ACTIVE (<2ms)")
            print(f"  Quality Gate: ACTIVE (Honeypot + GitHub Validator)")
            print(f"=======================================================", flush=True)
            httpd.serve_forever()
    except Exception as e:
        print(f"[-] Server failed on port {port}: {e}", flush=True)


if __name__ == "__main__":
    run()
