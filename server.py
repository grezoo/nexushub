"""
NexusHub Local Server
Serves static web files and provides API endpoints for catalogue retrieval, taxonomy, and GitHub sync.
Zero external dependencies, works with standard Python library.
"""

import http.server
import json
import os
import socketserver
import subprocess
import sys

PORT = 8765
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
WEB_DIR = os.path.join(BASE_DIR, "web")
DATA_DIR = os.path.join(BASE_DIR, "data")
CATALOGUE_PATH = os.path.join(DATA_DIR, "catalogue.json")
TAXONOMY_PATH = os.path.join(DATA_DIR, "taxonomy_map.json")


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

        # Serve static assets from WEB_DIR
        super().do_GET()

    def do_POST(self):
        if self.path.startswith("/api/submit"):
            content_length = int(self.headers.get("Content-Length", 0))
            post_data = self.rfile.read(content_length)
            try:
                new_item = json.loads(post_data.decode("utf-8"))
                print(f"[+] Received user submission: {new_item.get('title')}")
                if os.path.exists(CATALOGUE_PATH):
                    with open(CATALOGUE_PATH, "r", encoding="utf-8") as f:
                        data = json.load(f)
                    data.setdefault("items", []).insert(0, new_item)
                    with open(CATALOGUE_PATH, "w", encoding="utf-8") as f:
                        json.dump(data, f, ensure_ascii=False, indent=2)
            except Exception as e:
                print(f"[-] Submit parse error: {e}")

            self.send_response(200)
            self.send_header("Content-Type", "application/json; charset=utf-8")
            self.send_header("Access-Control-Allow-Origin", "*")
            self.end_headers()
            self.wfile.write(b'{"status":"success"}')
            return

        if self.path.startswith("/api/sync"):
            print("[*] Triggering catalogue sync via harvester...")
            harvester_script = os.path.join(BASE_DIR, "crawler", "fetch_topics_map.py")
            try:
                subprocess.run([sys.executable, harvester_script], check=True, timeout=30)
            except Exception as e:
                print(f"[-] Harvest error: {e}")

            self.send_response(200)
            self.send_header("Content-Type", "application/json; charset=utf-8")
            self.send_header("Access-Control-Allow-Origin", "*")
            self.end_headers()

            if os.path.exists(CATALOGUE_PATH):
                with open(CATALOGUE_PATH, "rb") as f:
                    self.wfile.write(f.read())
            else:
                self.wfile.write(b'{"status":"ok"}')
            return

        self.send_error(404, "Not Found")


def run():
    port = PORT
    try:
        # Allow immediate port reuse
        socketserver.TCPServer.allow_reuse_address = True
        with socketserver.TCPServer(("", port), CatalogueRequestHandler) as httpd:
            print(f"=======================================================")
            print(f"  NexusHub Universal Visual Catalogue is running!")
            print(f"  URL: http://localhost:{port}")
            print(f"  Web Root: {WEB_DIR}")
            print(f"=======================================================", flush=True)
            httpd.serve_forever()
    except Exception as e:
        print(f"[-] Server failed on port {port}: {e}", flush=True)


if __name__ == "__main__":
    run()
