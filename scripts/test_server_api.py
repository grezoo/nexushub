import sys
import os

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from server import query_repositories, get_catalogue_stats, get_categories_breakdown

print("--- Testing get_catalogue_stats ---")
stats = get_catalogue_stats()
print("Stats:", stats)
assert stats["total"] == 1522, f"Expected 1522, got {stats['total']}"

print("\n--- Testing get_categories_breakdown ---")
cats = get_categories_breakdown()
print(f"Categories count: {len(cats)}")
for c in cats[:3]:
    print(f"  {c['icon']} {c['main']}: {c['count']} items, {len(c['subcategories'])} subcategories")

print("\n--- Testing query_repositories (Default page 1) ---")
res = query_repositories({"page": 1, "limit": 10, "sort": "gems"})
print(f"Total matching: {res['total']}, Page count: {len(res['items'])}, Total pages: {res['total_pages']}")
print("First item:", res['items'][0]['title'], "| Stars:", res['items'][0]['stars'])

print("\n--- Testing query_repositories with FTS5 search 'whisper' ---")
res_fts = query_repositories({"search": "whisper", "page": 1, "limit": 10})
print(f"Total matching 'whisper': {res_fts['total']}")
for item in res_fts['items']:
    print("  *", item['title'], "| Stars:", item['stars'], "| Main Cat:", item['main_category'])

print("\n--- Testing query_repositories with Category 'Pénzügy, Tőzsde & Kripto Elemzés' ---")
res_cat = query_repositories({"category": "Pénzügy, Tőzsde & Kripto Elemzés", "page": 1, "limit": 10})
print(f"Total in FinTech category: {res_cat['total']}")
for item in res_cat['items'][:5]:
    print("  *", item['title'], "| Stars:", item['stars'])

print("\n--- Testing query_repositories with only_gems filter ---")
res_gems = query_repositories({"only_gems": "1", "page": 1, "limit": 5})
print(f"Total hidden gems (<=100 stars): {res_gems['total']}")
for item in res_gems['items']:
    print("  *", item['title'], "| Stars:", item['stars'], "| Video:", item['has_video'])

print("\nALL BACKEND API TESTS PASSED PERFECTLY!")
