"""
GitHub AI Harvester & Categorizer
Fetches real AI repositories from GitHub, categorizes them into Main Categories & Subcategories,
extracts social preview images and short video/GIF demos, and saves to data/catalogue.json.
"""

import json
import os
import re
import urllib.parse
import urllib.request
import time

DATA_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), "data")
CATALOGUE_FILE = os.path.join(DATA_DIR, "catalogue.json")

# Mapping categories and subcategories
CATEGORY_RULES = [
    {
        "main": "Képalkotás & Grafika",
        "icon": "🎨",
        "subcategories": {
            "Szöveg-Kép Generálás": ["text-to-image", "txt2img", "flux", "stable-diffusion", "diffusion", "midjourney"],
            "Munkafolyamatok & UI": ["comfyui", "webui", "node-editor", "ui", "gradio"],
            "Képjavítás & Felskálázás": ["upscaler", "super-resolution", "upscaling", "esrgan", "restoration"],
            "LoRA & Képszerkesztés": ["lora", "inpainting", "outpainting", "controlnet", "face-swap", "photoshop"]
        }
    },
    {
        "main": "Videó & Animáció",
        "icon": "🎬",
        "subcategories": {
            "Szöveg-Videó (Text-to-Video)": ["text-to-video", "video-generation", "sora", "animatediff", "cogvideo", "svd"],
            "Karakteranimáció & Lip-Sync": ["lip-sync", "talking-head", "liveportrait", "sad-talker", "wav2lip", "facial-animation"],
            "Videó Stílusváltás & Vágás": ["video-editing", "style-transfer", "motion-transfer", "temporal"]
        }
    },
    {
        "main": "Hang, Zene & Beszéd",
        "icon": "🎙️",
        "subcategories": {
            "Hangklónozás & Beszédszintézis (TTS)": ["text-to-speech", "tts", "voice-clone", "f5-tts", "chatterbox", "elevenlabs", "bark"],
            "Beszédfelismerés (ASR)": ["speech-to-text", "asr", "whisper", "transcription", "subtitles"],
            "Zeneszerzés & Hangeffektusok": ["musicgen", "audiocraft", "music-generation", "sound-effects", "audio-diffusion"],
            "Hangtisztítás & Sávszétválasztás": ["voice-isolation", "audio-separation", "demucs", "denoiser"]
        }
    },
    {
        "main": "Szöveg & Lokális LLM",
        "icon": "🧠",
        "subcategories": {
            "Lokális Modellkiszolgálók": ["ollama", "vllm", "llama.cpp", "local-ai", "inference-engine"],
            "Csevegőfelületek & Alkalmazások": ["open-webui", "chatgpt-clone", "chat-ui", "librechat"],
            "Dokumentumelemzés & RAG": ["rag", "pdf", "retrieval", "vector-database", "knowledge-base"],
            "Kreatív Írás & Tartalomgyártás": ["prompt-generator", "copywriting", "creative-writing", "summarizer"]
        }
    },
    {
        "main": "Autonóm Ágensek & Automatizáció",
        "icon": "⚡",
        "subcategories": {
            "Böngésző Ágensek (Web Automation)": ["browser-use", "web-agent", "browser-automation", "crawler-agent"],
            "Kódoló & Fejlesztői Asszisztensek": ["coding-agent", "dev-agent", "copilot", "swe-agent", "aider"],
            "Többágenses Rendszerek": ["multi-agent", "crewai", "autogen", "langgraph", "agent-framework"],
            "Munkafolyamat-automatizálók": ["workflow-automation", "dify", "flowise", "no-code"]
        }
    },
    {
        "main": "Hardver, IoT & Mikrokontrollerek (Arduino / ESP32)",
        "icon": "🔌",
        "subcategories": {
            "ESP32 & ESP8266 Projektek": ["esp32", "esp8266", "espressif", "esp32-cam", "nodemcu", "micropython"],
            "Arduino & Érzékelők": ["arduino", "microcontroller", "sensors", "stepper", "oled", "neopixel"],
            "Okosotthon & ESPHome": ["esphome", "home-assistant", "smart-home", "mqtt", "zigbee", "tasmota"],
            "Robotika & Edge AI (TinyML)": ["tinyml", "edge-ai", "robotics", "drone", "embedded-vision"],
            "3D Nyomtatás & CNC": ["klipper", "marlin", "3d-printing", "voron", "cnc"]
        }
    }
]

# Verified high quality seed entries with rich thumbnails, short videos and exact classifications
SEED_REPOSITORIES = [
    {
        "id": "comfyanonymous-ComfyUI",
        "repo_name": "comfyanonymous/ComfyUI",
        "title": "ComfyUI",
        "description": "A legnépszerűbb moduláris, csomópontalapú vizuális generáló felület Stable Diffusion és FLUX modellekhez.",
        "main_category": "Képalkotás & Grafika",
        "sub_category": "Munkafolyamatok & UI",
        "thumbnail_url": "https://opengraph.githubassets.com/1/comfyanonymous/ComfyUI",
        "video_url": "https://raw.githubusercontent.com/comfyanonymous/ComfyUI/master/extra/comfy_screenshot.png",
        "has_video": True,
        "video_demo": "https://user-images.githubusercontent.com/40797880/216507727-4a0b27b3-c1c6-476c-9411-404c0e668fd9.mp4",
        "stars": 63400,
        "url": "https://github.com/comfyanonymous/ComfyUI",
        "creator": "comfyanonymous",
        "tags": ["comfyui", "diffusion", "flux", "visual-nodes"]
    },
    {
        "id": "browser-use-browser-use",
        "repo_name": "browser-use/browser-use",
        "title": "Browser Use",
        "description": "Engedd szabadjára az AI ágenseket a böngészőben! Automatikus webes navigáció, űrlapkitöltés és kattintás videós követéssel.",
        "main_category": "Autonóm Ágensek & Automatizáció",
        "sub_category": "Böngésző Ágensek (Web Automation)",
        "thumbnail_url": "https://opengraph.githubassets.com/1/browser-use/browser-use",
        "video_url": "https://github.com/browser-use/browser-use/raw/main/examples/quickstart.gif",
        "has_video": True,
        "video_demo": "https://github.com/browser-use/browser-use/raw/main/examples/quickstart.gif",
        "stars": 34500,
        "url": "https://github.com/browser-use/browser-use",
        "creator": "browser-use",
        "tags": ["browser-agent", "automation", "vision-agent", "shorts-ready"]
    },
    {
        "id": "KwaiVGI-LivePortrait",
        "repo_name": "KwaiVGI/LivePortrait",
        "title": "LivePortrait",
        "description": "Élethű, valós idejű portré- és karakteranimáció egyetlen fotóból, természetes szem- és szájmozgással.",
        "main_category": "Videó & Animáció",
        "sub_category": "Karakteranimáció & Lip-Sync",
        "thumbnail_url": "https://opengraph.githubassets.com/1/KwaiVGI/LivePortrait",
        "video_url": "https://github.com/KwaiVGI/LivePortrait/raw/main/assets/docs/showcase.gif",
        "has_video": True,
        "video_demo": "https://github.com/KwaiVGI/LivePortrait/raw/main/assets/docs/showcase.gif",
        "stars": 18200,
        "url": "https://github.com/KwaiVGI/LivePortrait",
        "creator": "KwaiVGI",
        "tags": ["portrait-animation", "lip-sync", "video-generation", "short-video"]
    },
    {
        "id": "ollama-ollama",
        "repo_name": "ollama/ollama",
        "title": "Ollama",
        "description": "Futtass nagy nyelvi modelleket (Llama 3, Mistral, DeepSeek) közvetlenül a saját gépeden, internetkapcsolat nélkül.",
        "main_category": "Szöveg & Lokális LLM",
        "sub_category": "Lokális Modellkiszolgálók",
        "thumbnail_url": "https://opengraph.githubassets.com/1/ollama/ollama",
        "video_url": "https://github.com/ollama/ollama/raw/main/docs/overview.png",
        "has_video": False,
        "video_demo": "",
        "stars": 128000,
        "url": "https://github.com/ollama/ollama",
        "creator": "ollama",
        "tags": ["local-llm", "offline-ai", "llama3", "deepseek"]
    },
    {
        "id": "open-webui-open-webui",
        "repo_name": "open-webui/open-webui",
        "title": "Open WebUI",
        "description": "Kifejezetten felhasználóbarát, ChatGPT stílusú böngészős felület lokális és felhős AI modellekhez, beépített RAG-gal.",
        "main_category": "Szöveg & Lokális LLM",
        "sub_category": "Csevegőfelületek & Alkalmazások",
        "thumbnail_url": "https://opengraph.githubassets.com/1/open-webui/open-webui",
        "video_url": "https://github.com/open-webui/open-webui/raw/main/demo.gif",
        "has_video": True,
        "video_demo": "https://github.com/open-webui/open-webui/raw/main/demo.gif",
        "stars": 82000,
        "url": "https://github.com/open-webui/open-webui",
        "creator": "open-webui",
        "tags": ["chatgpt-clone", "chat-ui", "rag", "ollama-ui"]
    },
    {
        "id": "SWivid-F5-TTS",
        "repo_name": "SWivid/F5-TTS",
        "title": "F5-TTS",
        "description": "Hihetetlenül gyors és élethű szövegfelolvasó, amely másodpercek alatt klónozza a hangodat egy rövid hangminta alapján.",
        "main_category": "Hang, Zene & Beszéd",
        "sub_category": "Hangklónozás & Beszédszintézis (TTS)",
        "thumbnail_url": "https://opengraph.githubassets.com/1/SWivid/F5-TTS",
        "video_url": "https://github.com/SWivid/F5-TTS/raw/main/assets/demo.png",
        "has_video": True,
        "video_demo": "https://user-images.githubusercontent.com/11186711/f5tts_demo.mp4",
        "stars": 16400,
        "url": "https://github.com/SWivid/F5-TTS",
        "creator": "SWivid",
        "tags": ["voice-cloning", "tts", "diffusion-tts", "zero-shot"]
    },
    {
        "id": "AUTOMATIC1111-stable-diffusion-webui",
        "repo_name": "AUTOMATIC1111/stable-diffusion-webui",
        "title": "Stable Diffusion WebUI",
        "description": "A digitális képgenerálás alapköve: komplett kezelőfelület szöveg-kép generáláshoz, LoRA modellekhez és beépülőkhöz.",
        "main_category": "Képalkotás & Grafika",
        "sub_category": "Szöveg-Kép Generálás",
        "thumbnail_url": "https://opengraph.githubassets.com/1/AUTOMATIC1111/stable-diffusion-webui",
        "video_url": "https://raw.githubusercontent.com/AUTOMATIC1111/stable-diffusion-webui/master/screenshot.png",
        "has_video": False,
        "video_demo": "",
        "stars": 142000,
        "url": "https://github.com/AUTOMATIC1111/stable-diffusion-webui",
        "creator": "AUTOMATIC1111",
        "tags": ["stable-diffusion", "txt2img", "webui", "classic"]
    },
    {
        "id": "guoyww-AnimateDiff",
        "repo_name": "guoyww/AnimateDiff",
        "title": "AnimateDiff",
        "description": "Készíts folyamatos, lenyűgöző animált videókat és loopokat bármelyik szöveg-kép modellből mozgásmodulok segítségével.",
        "main_category": "Videó & Animáció",
        "sub_category": "Szöveg-Videó (Text-to-Video)",
        "thumbnail_url": "https://opengraph.githubassets.com/1/guoyww/AnimateDiff",
        "video_url": "https://animatediff.github.io/static/images/animatediff_teaser.gif",
        "has_video": True,
        "video_demo": "https://animatediff.github.io/static/images/animatediff_teaser.gif",
        "stars": 11500,
        "url": "https://github.com/guoyww/AnimateDiff",
        "creator": "guoyww",
        "tags": ["animation", "text-to-video", "motion", "short-clip"]
    },
    {
        "id": "openai-whisper",
        "repo_name": "openai/whisper",
        "title": "Whisper",
        "description": "Az iparági szabvány beszédfelismerő és feliratozó modell, amely 99+ nyelven írja le a hangfelvételeket tűpontosan.",
        "main_category": "Hang, Zene & Beszéd",
        "sub_category": "Beszédfelismerés (ASR)",
        "thumbnail_url": "https://opengraph.githubassets.com/1/openai/whisper",
        "video_url": "https://raw.githubusercontent.com/openai/whisper/main/approach.png",
        "has_video": False,
        "video_demo": "",
        "stars": 74000,
        "url": "https://github.com/openai/whisper",
        "creator": "openai",
        "tags": ["speech-to-text", "transcription", "subtitles", "industry-standard"]
    },
    {
        "id": "facebookresearch-audiocraft",
        "repo_name": "facebookresearch/audiocraft",
        "title": "AudioCraft (MusicGen)",
        "description": "A Meta mesterséges intelligenciája professzionális zeneszerzéshez és hangeffektek készítéséhez egyszerű szöveges utasításból.",
        "main_category": "Hang, Zene & Beszéd",
        "sub_category": "Zeneszerzés & Hangeffektusok",
        "thumbnail_url": "https://opengraph.githubassets.com/1/facebookresearch/audiocraft",
        "video_url": "https://raw.githubusercontent.com/facebookresearch/audiocraft/main/assets/audiocraft_banner.png",
        "has_video": False,
        "video_demo": "",
        "stars": 24800,
        "url": "https://github.com/facebookresearch/audiocraft",
        "creator": "Meta Research",
        "tags": ["music-generation", "sound-effects", "audiocraft", "creator-tool"]
    },
    {
        "id": "langgenius-dify",
        "repo_name": "langgenius/dify",
        "title": "Dify.AI",
        "description": "Vizuális, no-code fejlesztői stúdió AI munkafolyamatokhoz, vizuális ágensekhez és RAG alkalmazásokhoz.",
        "main_category": "Autonóm Ágensek & Automatizáció",
        "sub_category": "Munkafolyamat-automatizálók",
        "thumbnail_url": "https://opengraph.githubassets.com/1/langgenius/dify",
        "video_url": "https://raw.githubusercontent.com/langgenius/dify/main/web/public/logo/logo-site.png",
        "has_video": True,
        "video_demo": "https://raw.githubusercontent.com/langgenius/dify/main/assets/dify-workflow.gif",
        "stars": 65000,
        "url": "https://github.com/langgenius/dify",
        "creator": "Dify.AI",
        "tags": ["no-code", "workflow", "rag-builder", "enterprise-agent"]
    },
    {
        "id": "crewAIInc-crewAI",
        "repo_name": "crewAIInc/crewAI",
        "title": "CrewAI",
        "description": "Szervezz AI ágensekből komplett csapatot! Szerepkörök, együttműködés és feladatdelegálás egyetlen rendszerben.",
        "main_category": "Autonóm Ágensek & Automatizáció",
        "sub_category": "Többágenses Rendszerek",
        "thumbnail_url": "https://opengraph.githubassets.com/1/crewAIInc/crewAI",
        "video_url": "https://raw.githubusercontent.com/crewAIInc/crewAI/main/docs/assets/crew_flow.png",
        "has_video": False,
        "video_demo": "",
        "stars": 26500,
        "url": "https://github.com/crewAIInc/crewAI",
        "creator": "crewAI",
        "tags": ["multi-agent", "orchestration", "automation", "team-ai"]
    },
    {
        "id": "THUDM-CogVideo",
        "repo_name": "THUDM/CogVideo",
        "title": "CogVideoX",
        "description": "Nyílt forráskódú csúcsminőségű szöveg-videó generáló modell, amivel professzionális minőségű filmes snitteket hozhatsz létre.",
        "main_category": "Videó & Animáció",
        "sub_category": "Szöveg-Videó (Text-to-Video)",
        "thumbnail_url": "https://opengraph.githubassets.com/1/THUDM/CogVideo",
        "video_url": "https://github.com/THUDM/CogVideo/raw/main/resources/demo.gif",
        "has_video": True,
        "video_demo": "https://github.com/THUDM/CogVideo/raw/main/resources/demo.gif",
        "stars": 11800,
        "url": "https://github.com/THUDM/CogVideo",
        "creator": "THUDM",
        "tags": ["cogvideox", "text-to-video", "cinema-ai", "visual-creator"]
    },
    {
        "id": "adeptmind-upscayl",
        "repo_name": "upscayl/upscayl",
        "title": "Upscayl",
        "description": "Ingyenes, modern asztali AI képfelskálázó alkalmazás. Homályos, kisfelbontású képekből varázsol tűéles 4K képeket.",
        "main_category": "Képalkotás & Grafika",
        "sub_category": "Képjavítás & Felskálázás",
        "thumbnail_url": "https://opengraph.githubassets.com/1/upscayl/upscayl",
        "video_url": "https://raw.githubusercontent.com/upscayl/upscayl/main/resources/demo.gif",
        "has_video": True,
        "video_demo": "https://raw.githubusercontent.com/upscayl/upscayl/main/resources/demo.gif",
        "stars": 34000,
        "url": "https://github.com/upscayl/upscayl",
        "creator": "upscayl",
        "tags": ["upscale", "4k-enhancer", "desktop-app", "creatives"]
    },
    {
        "id": "Aircoookie-WLED",
        "repo_name": "Aircoookie/WLED",
        "title": "WLED (ESP32 / ESP8266)",
        "description": "A világ legnépszerűbb ESP32 vezérlője NeoPixel és címezhető LED szalagokhoz. 100+ vizuális effekt, WiFi mobilapp és zenei szinkronizáció.",
        "main_category": "Hardver, IoT & Mikrokontrollerek (Arduino / ESP32)",
        "sub_category": "ESP32 & ESP8266 Projektek",
        "thumbnail_url": "https://opengraph.githubassets.com/1/Aircoookie/WLED",
        "video_url": "https://raw.githubusercontent.com/Aircoookie/WLED/master/images/wled_logo_akemi.png",
        "has_video": True,
        "video_demo": "https://raw.githubusercontent.com/Aircoookie/WLED/master/images/wled_logo_akemi.png",
        "stars": 18900,
        "url": "https://github.com/Aircoookie/WLED",
        "creator": "Aircoookie",
        "tags": ["esp32", "esp8266", "neopixel", "led-effects", "hardware"]
    },
    {
        "id": "esphome-esphome",
        "repo_name": "esphome/esphome",
        "title": "ESPHome",
        "description": "Vezéreld az ESP8266 és ESP32 lapkáidat egyszerű YAML konfigurációs fájlokkal, C++ kódolás nélkül! Zökkenőmentes Home Assistant kapcsolat.",
        "main_category": "Hardver, IoT & Mikrokontrollerek (Arduino / ESP32)",
        "sub_category": "Okosotthon & ESPHome",
        "thumbnail_url": "https://opengraph.githubassets.com/1/esphome/esphome",
        "video_url": "https://raw.githubusercontent.com/esphome/esphome/dev/images/logo-text.svg",
        "has_video": False,
        "video_demo": "",
        "stars": 9200,
        "url": "https://github.com/esphome/esphome",
        "creator": "esphome",
        "tags": ["esphome", "esp32", "smart-home", "home-assistant", "iot"]
    },
    {
        "id": "Klipper3d-klipper",
        "repo_name": "Klipper3d/klipper",
        "title": "Klipper 3D Firmware",
        "description": "A nagysebességű 3D nyomtatás szabványa: mikrokontroller és Raspberry Pi kombinációja a tökéletes mechanikai precizitásért.",
        "main_category": "Hardver, IoT & Mikrokontrollerek (Arduino / ESP32)",
        "sub_category": "3D Nyomtatás & CNC",
        "thumbnail_url": "https://opengraph.githubassets.com/1/Klipper3d/klipper",
        "video_url": "https://raw.githubusercontent.com/Klipper3d/klipper/master/docs/img/klipper-logo.png",
        "has_video": False,
        "video_demo": "",
        "stars": 10800,
        "url": "https://github.com/Klipper3d/klipper",
        "creator": "Klipper3d",
        "tags": ["klipper", "3d-printing", "firmware", "motion-control"]
    },
    {
        "id": "esp-arduino-esp32",
        "repo_name": "espressif/arduino-esp32",
        "title": "Arduino Core for ESP32",
        "description": "A hivatalos Espressif Arduino fejlesztői környezet, amellyel az Arduino IDE egyszerűségével programozhatsz kétmagos ESP32 lapkákat.",
        "main_category": "Hardver, IoT & Mikrokontrollerek (Arduino / ESP32)",
        "sub_category": "Arduino & Érzékelők",
        "thumbnail_url": "https://opengraph.githubassets.com/1/espressif/arduino-esp32",
        "video_url": "https://raw.githubusercontent.com/espressif/arduino-esp32/master/docs/source/_static/logo.png",
        "has_video": False,
        "video_demo": "",
        "stars": 14700,
        "url": "https://github.com/espressif/arduino-esp32",
        "creator": "espressif",
        "tags": ["arduino", "esp32", "microcontroller", "iot-core"]
    }
]


def classify_repo(repo_data):
    """Auto-categorize repository into Main and Subcategory based on topics, description and name."""
    text = f"{repo_data.get('name', '')} {repo_data.get('description', '')} {' '.join(repo_data.get('topics', []))}".lower()

    for category in CATEGORY_RULES:
        for sub_name, keywords in category["subcategories"].items():
            for kw in keywords:
                if kw in text:
                    return category["main"], sub_name

    # Fallback default
    return "Szöveg & Lokális LLM", "Csevegőfelületek & Alkalmazások"


def fetch_github_topics(query="topic:generative-ai", max_count=15):
    """Fetch repositories using GitHub Search API."""
    url = f"https://api.github.com/search/repositories?q={urllib.parse.quote(query)}&sort=stars&order=desc&per_page={max_count}"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AI-Catalogue-Harvester/1.0",
        "Accept": "application/vnd.github.v3+json"
    }

    token = os.environ.get("GITHUB_TOKEN")
    if token:
        headers["Authorization"] = f"token {token}"

    req = urllib.request.Request(url, headers=headers)
    try:
        with urllib.request.urlopen(req, timeout=10) as resp:
            data = json.loads(resp.read().decode())
            items = data.get("items", [])
            print(f"[+] Fetched {len(items)} items for query: {query}")
            return items
    except Exception as e:
        print(f"[-] GitHub API error on query '{query}': {e}")
        return []


def load_catalogue():
    """Load existing catalogue from JSON file."""
    if os.path.exists(CATALOGUE_FILE):
        try:
            with open(CATALOGUE_FILE, "r", encoding="utf-8") as f:
                return json.load(f)
        except Exception:
            pass
    return {"categories": CATEGORY_RULES, "items": SEED_REPOSITORIES, "last_updated": time.strftime("%Y-%m-%d %H:%M:%S")}


def save_catalogue(data):
    """Save catalogue to JSON file."""
    os.makedirs(DATA_DIR, exist_ok=True)
    with open(CATALOGUE_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    print(f"[+] Saved {len(data['items'])} items to {CATALOGUE_FILE}")


def check_repo_preview_video(full_name, default_branch="main"):
    """
    Standard NexusHub Video Detection:
    Automatically checks if the creator has uploaded a standardized 15-30s demo:
    - preview.mp4 / preview.webm / preview.gif
    - demo.mp4 / demo.webm / demo.gif
    - short.mp4 / short.webm
    """
    candidate_filenames = [
        "preview.mp4", "preview.gif", "preview.webm",
        "demo.mp4", "demo.gif", "demo.webm",
        "short.mp4", "showcase.gif", ".github/preview.mp4"
    ]

    base_raw = f"https://raw.githubusercontent.com/{full_name}/{default_branch}/"
    headers = {"User-Agent": "Mozilla/5.0"}

    for fname in candidate_filenames:
        test_url = base_raw + fname
        try:
            req = urllib.request.Request(test_url, headers=headers, method="HEAD")
            with urllib.request.urlopen(req, timeout=3) as resp:
                if resp.status == 200:
                    print(f"[⭐ STANDARD FOUND!] {full_name} has official preview: {fname}")
                    return test_url
        except Exception:
            continue

    return None


def harvest_live_data():
    """Run full harvest to update the database."""
    current_data = load_catalogue()
    existing_ids = {item["id"]: item for item in current_data.get("items", [])}

    search_queries = [
        "topic:text-to-video",
        "topic:stable-diffusion",
        "topic:voice-clone",
        "topic:autonomous-agents",
        "topic:local-llm",
        "topic:esp32",
        "topic:arduino",
        "topic:esphome"
    ]

    for q in search_queries:
        repos = fetch_github_topics(q, max_count=5)
        for repo in repos:
            repo_id = repo["full_name"].replace("/", "-")
            main_cat, sub_cat = classify_repo(repo)

            desc = repo.get("description") or "Nincs részletes leírás megadva."
            og_thumb = f"https://opengraph.githubassets.com/1/{repo['full_name']}"

            # Check if updated or new
            item = {
                "id": repo_id,
                "repo_name": repo["full_name"],
                "title": repo["name"].replace("-", " ").title(),
                "description": desc,
                "main_category": main_cat,
                "sub_category": sub_cat,
                "thumbnail_url": og_thumb,
                "video_url": og_thumb,
                "has_video": False,
                "video_demo": "",
                "stars": repo.get("stargazers_count", 0),
                "url": repo.get("html_url", ""),
                "creator": repo.get("owner", {}).get("login", ""),
                "tags": repo.get("topics", [])[:5]
            }

            if repo_id in existing_ids:
                # Preserve verified video links and human descriptions if exists
                if existing_ids[repo_id].get("has_video"):
                    item["has_video"] = True
                    item["video_demo"] = existing_ids[repo_id].get("video_demo", "")
                    item["video_url"] = existing_ids[repo_id].get("video_url", og_thumb)
                if len(existing_ids[repo_id].get("description", "")) > 10:
                    item["description"] = existing_ids[repo_id]["description"]
                existing_ids[repo_id].update(item)
            else:
                existing_ids[repo_id] = item

        time.sleep(1)  # respect rate limits

    current_data["items"] = list(existing_ids.values())
    current_data["last_updated"] = time.strftime("%Y-%m-%d %H:%M:%S")
    save_catalogue(current_data)
    return current_data


if __name__ == "__main__":
    print("Initializing catalogue...")
    cat = load_catalogue()
    save_catalogue(cat)
    print("Attempting live GitHub enrichment...")
    harvest_live_data()
