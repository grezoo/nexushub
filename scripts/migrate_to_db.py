import json
import sqlite3
import os
import sys

def migrate():
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    json_path = os.path.join(base_dir, "data", "catalogue.json")
    db_path = os.path.join(base_dir, "data", "nexus.db")
    schema_path = os.path.join(base_dir, "data", "schema.sql")

    if not os.path.exists(json_path):
        print(f"Error: {json_path} not found!")
        sys.exit(1)

    print(f"Initializing database at: {db_path}")
    if os.path.exists(db_path):
        os.remove(db_path)

    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    with open(schema_path, "r", encoding="utf-8") as f:
        schema_sql = f.read()
    cursor.executescript(schema_sql)

    with open(json_path, "r", encoding="utf-8") as f:
        cat = json.load(f)

    items = cat.get("items", [])
    print(f"Loaded {len(items)} items from catalogue.json")

    inserted = 0
    for item in items:
        tags_json = json.dumps(item.get("tags", []), ensure_ascii=False)
        cursor.execute("""
            INSERT INTO repositories (
                id, repo_name, title, function_title, title_en, function_title_en,
                description, description_en, main_category, sub_category,
                thumbnail_url, video_url, video_demo, has_video, stars, year,
                url, creator, tags, is_pinned
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            item.get("id") or item.get("repo_name"),
            item.get("repo_name", ""),
            item.get("title", ""),
            item.get("function_title", ""),
            item.get("title_en", ""),
            item.get("function_title_en", ""),
            item.get("description", ""),
            item.get("description_en", ""),
            item.get("main_category", ""),
            item.get("sub_category", ""),
            item.get("thumbnail_url", ""),
            item.get("video_url", ""),
            item.get("video_demo", ""),
            1 if item.get("has_video") else 0,
            int(item.get("stars") or 0),
            int(item.get("year") or 2024),
            item.get("url", ""),
            item.get("creator", ""),
            tags_json,
            1 if item.get("is_pinned") else 0
        ))
        inserted += 1

    conn.commit()
    print(f"Successfully inserted {inserted} items into repositories table!")

    # Verify FTS index
    cursor.execute("SELECT COUNT(*) FROM repositories_fts")
    fts_count = cursor.fetchone()[0]
    print(f"FTS5 virtual table count: {fts_count}")

    # Test FTS query
    test_terms = ["whisper", "esp32", "trading", "quant"]
    for term in test_terms:
        cursor.execute("""
            SELECT r.title, r.stars FROM repositories r
            JOIN repositories_fts fts ON r.rowid = fts.rowid
            WHERE repositories_fts MATCH ?
            LIMIT 3
        """, (f"{term}*",))
        results = cursor.fetchall()
        print(f"FTS query '{term}*' returned {len(results)} sample matches: {[r[0] for r in results]}")

    conn.close()
    print("Migration completed successfully!")

if __name__ == "__main__":
    migrate()
