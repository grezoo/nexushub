"""
AI Curator & Bookshop-Style Author's Picks Engine
Powered by Google Gemini Free API (with automatic fallback to curated rules).
Analyses open-source repositories across visual proof (preview.mp4 / preview.gif),
functional merit, and real-world utility.
Generates 'Author's Pick (grezoo)' badges and bespoke curator notes.
"""

import json
import os
import re
import datetime
import urllib.request
import urllib.error

DATA_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), "data")
CATALOGUE_FILE = os.path.join(DATA_DIR, "catalogue.json")
CURATED_FILE = os.path.join(DATA_DIR, "curated_picks.json")

# Try to load .env if present
env_file = os.path.join(os.path.dirname(os.path.dirname(__file__)), ".env")
if os.path.exists(env_file):
    try:
        with open(env_file, "r", encoding="utf-8") as ef:
            for line in ef:
                line = line.strip()
                if "=" in line and not line.startswith("#"):
                    k, v = line.split("=", 1)
                    os.environ.setdefault(k.strip(), v.strip().strip('"').strip("'"))
    except Exception:
        pass

GEMINI_API_KEY = (os.environ.get("GEMINI_API_KEY") or os.environ.get("GOOGLE_API_KEY") or "").strip()

# High quality fallbacks if Gemini API is not configured or offline
CURATOR_ARCHETYPES = [
    {
        "domain": "Visual Discovery Standard",
        "match_keys": ["nexushub", "grezoo/nexushub"],
        "curator_note_hu": "A vizuális nyílt forráskód forradalma: a GitHub régi kódközpontú keresője helyett mozgó, élményalapú funkciókatalógus. A 15-30 mp-es demó videók és a 0 csillagos rejtett kincsek felfedezésének alapköve.",
        "curator_note_en": "The visual revolution of open source: replacing code-centric browsing with dynamic, motion-first discovery. The cornerstone for 15-30s preview demos and 0-star hidden gems.",
        "badge_hu": "👑 #1 A NEXUSHUB FŐ AJÁNLÁSA",
        "badge_en": "👑 #1 NEXUSHUB FLAGSHIP PICK",
        "merit_boost": 1000
    },
    {
        "domain": "Hardware & Robotics Gem",
        "match_keys": ["esp32-wifi-drone", "drone"],
        "curator_note_hu": "Tökéletes példája annak, amikor egy apró mikrovezérlő komoly hardveres repülési fizikát kezel. Nincs szükség több százezres eszközre: böngészőből vezérelhető, azonnal építhető mérnöki gyöngyszem.",
        "curator_note_en": "A textbook example of raw engineering merit on a budget microchip. Full quadcopter flight physics controllable from any phone browser.",
        "badge_hu": "✍️ NEXUSHUB AJÁNLÁS: HARDVER KINCS",
        "badge_en": "✍️ NEXUSHUB PICK: HARDWARE GEM",
        "merit_boost": 850
    },
    {
        "domain": "Generative AI Video",
        "match_keys": ["sadtalker", "liveportrait", "animate", "video"],
        "curator_note_hu": "Az AI nem csupán szöveg: ezzel az eszközzel egyetlen fotóból és hangfájlból élő, lélegző beszélő karaktert animálhatunk. Rendkívül gyors és önállóan futtatható.",
        "curator_note_en": "AI beyond text: transforms a single still portrait and audio track into a photorealistic speaking animation in seconds.",
        "badge_hu": "✍️ NEXUSHUB AJÁNLÁS: GENERATÍV AI",
        "badge_en": "✍️ NEXUSHUB PICK: CREATIVE AI",
        "merit_boost": 800
    },
    {
        "domain": "Audio & Music Engineering",
        "match_keys": ["demucs", "audio", "stem", "voice"],
        "curator_note_hu": "Minden zenei alkotó álma: mesterséges intelligenciával izolálja az éneket, a dobot, a basszust és a hangszereket bármely hangfelvételből, professzionális stúdióminőségben.",
        "curator_note_en": "Every producer's holy grail: AI-powered stem separation that isolates vocals, drums, bass, and instruments with studio precision.",
        "badge_hu": "✍️ NEXUSHUB AJÁNLÁS: HANG & ZENE",
        "badge_en": "✍️ NEXUSHUB PICK: AUDIO TECH",
        "merit_boost": 780
    },
    {
        "domain": "Physical Computing & Smart Lighting",
        "match_keys": ["wled", "led", "flipper", "matrix"],
        "curator_note_hu": "A digitális kód és a fizikai világ lenyűgöző találkozása: azonnali zenei ritmusra reagáló szobai fényinstallációk készíthetők vele percek alatt.",
        "curator_note_en": "Where software meets physical lighting: sound-reactive ambient illumination and NeoPixel matrix magic made accessible to everyone.",
        "badge_hu": "✍️ NEXUSHUB AJÁNLÁS: MAKER & IOT",
        "badge_en": "✍️ NEXUSHUB PICK: MAKER & IOT",
        "merit_boost": 750
    }
]

def load_catalogue():
    if not os.path.exists(CATALOGUE_FILE):
        return {"items": [], "categories": []}
    with open(CATALOGUE_FILE, "r", encoding="utf-8") as f:
        return json.load(f)

def ask_gemini_curator(repo_data):
    """
    Calls Google Gemini Free API to review a repository like a bookshop curator.
    Generates bilingual curator commentary and merit evaluation.
    """
    if not GEMINI_API_KEY:
        return None
        
    url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-flash-latest:generateContent?key={GEMINI_API_KEY}"
    prompt = f"""
Te vagy a NexusHub nyílt forráskódú vizuális katalógus szigorú, de lelkes kurátora (mint egy igényes technikai könyvesbolt tulajdonosa, grezoo).
Értékeld ezt a projektet a működőképesség, kézzelfogható alkotói hasznosság és újdonságérték alapján.

Projekt adatai:
- Név: {repo_data.get('repo_name')}
- Cím: {repo_data.get('title')}
- Leírás: {repo_data.get('description')}
- Kategória: {repo_data.get('main_category')} / {repo_data.get('sub_category')}
- Van mozgó demó videó: {'Igen' if repo_data.get('has_video') else 'Nem'}
- Csillagok száma: {repo_data.get('stars', 0)}

Kérlek, válaszolj KIZÁRÓLAG egy érvényes JSON formátumban (semmi más szöveg):
{{
  "curator_note_hu": "1-2 mondatos személyes, frappáns ajánló magyarul, hogy miért kihagyhatatlan ez a projekt a felhasználónak",
  "curator_note_en": "1-2 sentences personal, punchy recommendation in English explaining why this project is a must-see",
  "badge_hu": "✍️ SZERZŐI AJÁNLÁS: [KATEGÓRIA]",
  "badge_en": "✍️ AUTHOR'S PICK: [CATEGORY]",
  "merit_score": 850
}}
"""
    payload = {
        "contents": [{"parts": [{"text": prompt}]}],
        "generationConfig": {"temperature": 0.3, "responseMimeType": "application/json"}
    }
    
    try:
        req = urllib.request.Request(
            url,
            data=json.dumps(payload).encode("utf-8"),
            headers={"Content-Type": "application/json"}
        )
        with urllib.request.urlopen(req, timeout=12) as response:
            res_data = json.loads(response.read().decode("utf-8"))
            text = res_data["candidates"][0]["content"]["parts"][0]["text"]
            return json.loads(text)
    except Exception as e:
        print(f"[Gemini API fallback] Could not query Gemini: {e}")
        return None

def curate_projects():
    data = load_catalogue()
    items = data.get("items", [])
    
    curated_list = []
    gemini_calls = 0
    gemini_failures = 0
    
    for item in items:
        repo = (item.get("repo_name") or item.get("title") or "").lower()
        tags = [t.lower() for t in item.get("tags", [])]
        
        # 1. Flagship always gets top spot
        if "grezoo/nexushub" in repo or "nexushub" in repo:
            flagship = dict(item)
            flagship["is_curated_pick"] = True
            flagship["curator_author"] = "grezoo"
            flagship["curator_note_hu"] = CURATOR_ARCHETYPES[0]["curator_note_hu"]
            flagship["curator_note_en"] = CURATOR_ARCHETYPES[0]["curator_note_en"]
            flagship["badge_hu"] = CURATOR_ARCHETYPES[0]["badge_hu"]
            flagship["badge_en"] = CURATOR_ARCHETYPES[0]["badge_en"]
            flagship["merit_score"] = 1000
            curated_list.append(flagship)
            continue
            
        # 2. Check if item has visual proof or high merit
        has_visual = item.get("has_video") or (item.get("stars", 0) <= 50)
        
        # Try Gemini API evaluation if key available and quota healthy
        gemini_result = None
        if GEMINI_API_KEY and has_visual and len(curated_list) < 8 and gemini_calls < 5 and gemini_failures < 2:
            gemini_calls += 1
            gemini_result = ask_gemini_curator(item)
            if not gemini_result:
                gemini_failures += 1
            
        if gemini_result:
            curated_item = dict(item)
            curated_item["is_curated_pick"] = True
            curated_item["curator_author"] = "grezoo (AI Assisted)"
            curated_item["curator_note_hu"] = gemini_result.get("curator_note_hu")
            curated_item["curator_note_en"] = gemini_result.get("curator_note_en")
            curated_item["badge_hu"] = gemini_result.get("badge_hu")
            curated_item["badge_en"] = gemini_result.get("badge_en")
            curated_item["merit_score"] = gemini_result.get("merit_score", 750)
            curated_list.append(curated_item)
        else:
            # Fallback to curated archetypes
            for arch in CURATOR_ARCHETYPES[1:]:
                if any(k in repo or any(k in t for t in tags) for k in arch["match_keys"]):
                    curated_item = dict(item)
                    curated_item["is_curated_pick"] = True
                    curated_item["curator_author"] = "grezoo"
                    curated_item["curator_note_hu"] = arch["curator_note_hu"]
                    curated_item["curator_note_en"] = arch["curator_note_en"]
                    curated_item["badge_hu"] = arch["badge_hu"]
                    curated_item["badge_en"] = arch["badge_en"]
                    curated_item["merit_score"] = arch["merit_boost"] + (100 if item.get("has_video") else 0)
                    curated_list.append(curated_item)
                    break

    # Sort by curator merit score
    curated_list.sort(key=lambda x: x.get("merit_score", 0), reverse=True)
    
    output = {
        "title": "Author's Curated Shelf / A Szerző Ajánlata (grezoo)",
        "description": "Bookshop-style editorial selection chosen personally by grezoo based on functioning proof, real-world utility, and independent craftsmanship.",
        "curator": "grezoo",
        "curator_contact": "grezoo@gmail.com",
        "curator_engine": "Gemini 1.5 Flash + Bookshop Merit Rules",
        "donation_url": "https://revolut.me/grezoo",
        "last_curated": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "picks": curated_list
    }
    
    with open(CURATED_FILE, "w", encoding="utf-8") as f:
        json.dump(output, f, ensure_ascii=False, indent=2)
        
    print(f"[OK] Curated {len(curated_list)} projects into '{CURATED_FILE}' successfully!")
    return output

if __name__ == "__main__":
    curate_projects()
