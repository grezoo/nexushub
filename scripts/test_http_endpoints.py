import urllib.request
import urllib.parse
import json

base = 'http://localhost:8765'

# 1. Test HTML
req = urllib.request.urlopen(f'{base}/')
print('Index HTML status:', req.status)

# 2. Test Stats
req = urllib.request.urlopen(f'{base}/api/stats')
stats = json.loads(req.read().decode('utf-8'))
print('API Stats:', stats)

# 3. Test Categories
req = urllib.request.urlopen(f'{base}/api/categories')
cats = json.loads(req.read().decode('utf-8'))
print('API Categories count:', len(cats))

# 4. Test Items Default
req = urllib.request.urlopen(f'{base}/api/items?page=1&limit=5')
data = json.loads(req.read().decode('utf-8'))
print(f'API Items (Page 1): total = {data["total"]}, count = {len(data["items"])}, pages = {data["total_pages"]}')

# 5. Test FTS Search 'whisper'
req = urllib.request.urlopen(f'{base}/api/items?search=whisper&limit=5')
data_search = json.loads(req.read().decode('utf-8'))
print(f'API FTS Search "whisper": total = {data_search["total"]}, titles = {[i["title"] for i in data_search["items"]]}')

# 6. Test FTS Search 'trading'
req = urllib.request.urlopen(f'{base}/api/items?search=trading&limit=5')
data_trading = json.loads(req.read().decode('utf-8'))
print(f'API FTS Search "trading": total = {data_trading["total"]}, titles = {[i["title"] for i in data_trading["items"]]}')

# 7. Test Category Filter
cat_url = urllib.parse.quote('Pénzügy, Tőzsde & Kripto Elemzés')
req = urllib.request.urlopen(f'{base}/api/items?category={cat_url}&limit=5')
data_cat = json.loads(req.read().decode('utf-8'))
print(f'API Category Filter: total = {data_cat["total"]}, titles = {[i["title"] for i in data_cat["items"]]}')

print("\nALL HTTP ENDPOINTS TESTED AND WORKING 100%!")
