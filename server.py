"""
NexusHub Production Server
Serves static web files and provides API endpoints for catalogue retrieval, taxonomy,
and hardened, anti-spam quality-gated repository submissions.
Zero external dependencies, works with standard Python library.
"""

import http.server
import json
import os
import re
import socketserver
import subprocess
import sys
import time
import urllib.request
import urllib.error

PORT = int(os.environ.get("PORT", 8765))
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
WEB_DIR = os.path.join(BASE_DIR, "web")
DATA_DIR = os.path.join(BASE_DIR, "data")
CATALOGUE_PATH = os.path.join(DATA_DIR, "catalogue.json")
TAXONOMY_PATH = os.path.join(DATA_DIR, "taxonomy_map.json")
CURATED_PATH = os.path.join(DATA_DIR, "curated_picks.json")
SUBMISSIONS_QUEUE_PATH = os.path.join(DATA_DIR, "submissions_queue.json")

# In-memory IP submission tracking for rate-limiting
IP_SUBMISSION_HISTORY = {}


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

    # 2. Time-Trap: humans take >= 2.5s to fill out the form
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
        # API: Return catalogue data
        if self.path.startswith("/api/catalogue"):
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
        if self.path.startswith("/api/taxonomy"):
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
        if self.path.startswith("/api/curated"):
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
                "description": submission.get("description", "").strip(),
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
                "tags": ["community-submission", "quality-verified", "hidden-gem"]
            }

            # 1. Store in submissions queue archive
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

            # 2. Insert into live catalogue
            if os.path.exists(CATALOGUE_PATH):
                try:
                    with open(CATALOGUE_PATH, "r", encoding="utf-8") as cf:
                        cat_data = json.load(cf)
                    cat_data.setdefault("items", []).insert(0, clean_item)
                    cat_data["last_updated"] = time.strftime("%Y-%m-%d %H:%M:%S")
                    with open(CATALOGUE_PATH, "w", encoding="utf-8") as cf:
                        json.dump(cat_data, cf, ensure_ascii=False, indent=2)
                except Exception as e:
                    print(f"[-] Error writing to catalogue: {e}")

            self.send_response(200)
            self.send_header("Content-Type", "application/json; charset=utf-8")
            self.send_header("Access-Control-Allow-Origin", "*")
            self.end_headers()
            self.wfile.write(json.dumps({
                "status": "success",
                "message": "A minőségellenőrzés sikeresen lezajlott! A projekt azonnal bekerült a katalógusba.",
                "item": clean_item
            }).encode("utf-8"))
            return

        self.send_error(404, "Not Found")


def run():
    port = PORT
    try:
        socketserver.TCPServer.allow_reuse_address = True
        with socketserver.TCPServer(("", port), CatalogueRequestHandler) as httpd:
            print(f"=======================================================")
            print(f"  NexusHub Production Server running on port {port}")
            print(f"  Quality Gate: ACTIVE (Honeypot + GitHub Validator)")
            print(f"=======================================================", flush=True)
            httpd.serve_forever()
    except Exception as e:
        print(f"[-] Server failed on port {port}: {e}", flush=True)


if __name__ == "__main__":
    run()
