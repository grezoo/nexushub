import json
import sqlite3
import os

STRICT_SAAS_MAP = {
    "immich-app/immich": ("Google Photos / iCloud", "$10–30 / hó tárhelymegtakarítás"),
    "bitwarden/server": ("1Password / LastPass", "$3–8 / hó megtakarítás"),
    "dani-garcia/vaultwarden": ("1Password", "$3–8 / hó megtakarítás"),
    "calcom/cal.com": ("Calendly", "$16 / hó / felhasználó"),
    "penpot/penpot": ("Figma", "$15 / hó / szerkesztő"),
    "appflowy-io/appflowy": ("Notion", "$20 / hó / felhasználó"),
    "plausible/analytics": ("Google Analytics", "$19–100 / hó megtakarítás"),
    "umami-software/umami": ("Google Analytics", "Cookie- és AdBlock-mentes 0 Ft"),
    "lllyasviel/fooocus": ("Midjourney", "$30 / hó (korlátlan ingyen)"),
    "vllm-project/vllm": ("Felhős GPU API", "$100–500 / hó megtakarítás"),
    "mendableai/firecrawl": ("ScrapingBee / BrightData", "$49–249 / hó megtakarítás"),
    "n8n-io/n8n": ("Zapier / Make", "$50–300 / hó megtakarítás"),
    "activepieces/activepieces": ("Zapier", "$50–250 / hó megtakarítás"),
    "browser-use/browser-use": ("Fizetős AI Scraper & RPA", "$50–200 / hó megtakarítás"),
    "ollama/ollama": ("OpenAI / Claude API", "$50–500 / hó megtakarítás"),
    "posthog/posthog": ("Mixpanel / Amplitude", "$150+ / hó megtakarítás"),
    "yt-dlp/yt-dlp": ("YouTube Premium", "$16 / hó megtakarítás"),
    "openai/whisper": ("Otter.ai / Descript", "$20–30 / hó megtakarítás"),
    "ggml-org/whisper.cpp": ("Otter.ai / Descript", "$20–30 / hó megtakarítás"),
    "tryghost/ghost": ("Medium / Substack", "Platform jutalékok megtakarítása"),
    "zulip/zulip": ("Slack / Teams", "$8 / hó / felhasználó"),
    "documenso/documenso": ("DocuSign", "$15–40 / hó megtakarítás"),
    "formbricks/formbricks": ("Typeform", "$35–99 / hó megtakarítás"),
    "makeplane/plane": ("Jira / Linear", "$12–25 / hó / felhasználó"),
    "nocodb/nocodb": ("Airtable", "$20 / hó / felhasználó"),
    "baserow/baserow": ("Airtable", "$20 / hó / felhasználó"),
    "twentyhq/twenty": ("HubSpot / Salesforce", "$50–150 / hó / felhasználó"),
    "mattermost/mattermost": ("Slack", "$8.75 / hó / felhasználó"),
    "hoppscotch/hoppscotch": ("Postman", "$15 / hó / felhasználó"),
    "affine-design/affine": ("Notion + Miro", "$25 / hó megtakarítás")
}

def run_enrichment():
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    db_path = os.path.join(base_dir, "data", "nexus.db")

    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    # Ensure columns exist before doing any updates
    cursor.execute("PRAGMA table_info(repositories)")
    cols = {r[1] for r in cursor.fetchall()}
    if "replaces_saas" not in cols:
        cursor.execute("ALTER TABLE repositories ADD COLUMN replaces_saas TEXT")
    if "saas_savings" not in cols:
        cursor.execute("ALTER TABLE repositories ADD COLUMN saas_savings TEXT")
    conn.commit()

    # Clear previous tags
    cursor.execute("UPDATE repositories SET replaces_saas = NULL, saas_savings = NULL")

    # Match each strict repo
    matched = 0
    for repo_name, (replaces, savings) in STRICT_SAAS_MAP.items():
        cursor.execute("""
            UPDATE repositories
            SET replaces_saas = ?, saas_savings = ?
            WHERE LOWER(repo_name) = LOWER(?)
        """, (replaces, savings, repo_name))
        if cursor.rowcount > 0:
            matched += cursor.rowcount
            print(f"[+] Exact match: {repo_name} -> {replaces} ({savings})")
        else:
            # Fallback to suffix match e.g. "ghost" or "fooocus"
            cursor.execute("""
                UPDATE repositories
                SET replaces_saas = ?, saas_savings = ?
                WHERE LOWER(repo_name) LIKE ?
            """, (replaces, savings, f"%/{repo_name.split('/')[-1]}"))
            if cursor.rowcount > 0:
                matched += cursor.rowcount
                print(f"[+] Suffix match: {repo_name} -> {replaces} ({savings})")

    conn.commit()
    conn.close()
    print(f"\n[OK] Pristine SaaS enrichment complete! Total verified: {matched}")

if __name__ == "__main__":
    run_enrichment()
