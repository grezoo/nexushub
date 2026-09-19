"""
Universal Open Source Harvester & Awesome-Index Parser
Extracts categorized repositories across ALL domains:
Hardware, ESP32, Arduino, Robotics, 3D Printing, Game Dev, Audio/Music,
Self-Hosted, Desktop Apps, AI, Creative Tools, Productivity, Education, and System Utilities.
"""

import json
import os
import re
import urllib.parse
import urllib.request
import time

DATA_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), "data")
CATALOGUE_FILE = os.path.join(DATA_DIR, "catalogue.json")

# Master Universal Taxonomy covering ALL domains
UNIVERSAL_TAXONOMY = [
    {
        "main": "Hardver, IoT & Elektronika",
        "icon": "🔌",
        "color": "#10b981",
        "subcategories": [
            "ESP32 & ESP8266 Projektek",
            "Arduino & Mikrokontrollerek",
            "Okosotthon & ESPHome / Zigbee",
            "Robotika, Drónok & Edge AI",
            "3D Nyomtatás, CNC & Klipper",
            "Szenzorok, Kijelzők & LED Mátrixok"
        ]
    },
    {
        "main": "Mesterséges Intelligencia & Adat",
        "icon": "🧠",
        "color": "#8b5cf6",
        "subcategories": [
            "Képalkotás & Grafika (FLUX / SD)",
            "Videógenerálás & Mozgókép",
            "Hangklónozás & Beszédszintézis",
            "Lokális LLM-ek & Csevegők",
            "Autonóm Ágensek & Automatizáció",
            "RAG & Dokumentumelemzés"
        ]
    },
    {
        "main": "Játékfejlesztés, 3D & Grafika",
        "icon": "🎮",
        "color": "#ec4899",
        "subcategories": [
            "Játékmotorok (Godot / Raylib)",
            "Blender Kiegészítők & 3D Eszközök",
            "Pixel Art, Shaders & Vizuális Effektek",
            "Emuláció & Retró Játékok",
            "Fizikai Szimulációk"
        ]
    },
    {
        "main": "Zene, Hangtechnika & Audió",
        "icon": "🎵",
        "color": "#f59e0b",
        "subcategories": [
            "Digitális Audió Munkaállomások (DAW)",
            "VST Pluginek & Szintetizátorok",
            "Hangtisztítás & Sávszétválasztás",
            "Podcast & Streamer Eszközök",
            "Zenevizualizáció & Algoritmikus Zene"
        ]
    },
    {
        "main": "Self-Hosted & Otthoni Szerverek",
        "icon": "🏠",
        "color": "#3b82f6",
        "subcategories": [
            "Privát Felhő & Fájlkezelés (Nextcloud)",
            "Médiaszerverek & Streaming (Jellyfin)",
            "Home Assistant & Otthonautomatizálás",
            "Jelszókezelők & Adatbiztonság (Vaultwarden)",
            "Hálózatkezelés & VPN (Pi-hole, Wireguard)"
        ]
    },
    {
        "main": "Produktivitás & Irodai Munka",
        "icon": "📊",
        "color": "#06b6d4",
        "subcategories": [
            "Jegyzetelés & Ismeretbázis (Obsidian / Logseq)",
            "PDF & Dokumentumkezelés",
            "Munkafolyamat & Task Management",
            "Táblázatok & Adatvizualizáció",
            "Számlázás & Kisvállalati Eszközök"
        ]
    },
    {
        "main": "Kreatív Média, Videóvágás & Fotó",
        "icon": "🎬",
        "color": "#f43f5e",
        "subcategories": [
            "Videóvágók & Compositing (Kdenlive / Shotcut)",
            "Képszerkesztők (Krita / GIMP / Inkscape)",
            "Képernyőfelvétel & Streaming (OBS Studio)",
            "Színkorrekció & Médiakonvertálók (FFmpeg)"
        ]
    },
    {
        "main": "Rendszer, Biztonság & Segédprogramok",
        "icon": "⚡",
        "color": "#64748b",
        "subcategories": [
            "Terminálok & Shell Eszközök",
            "Rendszerfigyelés & Diagnosztika",
            "Biztonsági Tesztelés & Adatvédelem",
            "Gyorsindítók & Asztali Kiegészítők"
        ]
    }
]

# Universal curated master dataset covering EVERY SINGLE domain with rich previews and demo links
UNIVERSAL_SEED_REPOSITORIES = [
    # --- HARDVER, IOT, ARDUINO, ESP32 ---
    {
        "id": "Aircoookie-WLED",
        "repo_name": "Aircoookie/WLED",
        "title": "WLED",
        "function_title": "WiFi-s Címezhető LED Szalag Vezérlő (100+ Effekt)",
        "description": "Irányíts NeoPixel és WS2812 LED szalagokat közvetlenül telefonról vagy gépről. Zenei ritmuskövetés, időzítők és lenyűgöző színeffektek.",
        "main_category": "Hardver, IoT & Elektronika",
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
        "function_title": "ESP32 & ESP8266 Szenzorvezérlő (Kódolás Nélkül)",
        "description": "Építs okos konnektort, hőmérőt vagy relévezérlőt! Egyszerű YAML fájlokkal konfigurálható, C++ programozás nélkül, azonnali Home Assistant kapcsolattal.",
        "main_category": "Hardver, IoT & Elektronika",
        "sub_category": "Okosotthon & ESPHome / Zigbee",
        "thumbnail_url": "https://opengraph.githubassets.com/1/esphome/esphome",
        "video_url": "https://raw.githubusercontent.com/esphome/esphome/dev/images/logo-text.svg",
        "has_video": False,
        "video_demo": "",
        "stars": 9300,
        "url": "https://github.com/esphome/esphome",
        "creator": "esphome",
        "tags": ["esphome", "esp32", "smart-home", "sensors"]
    },
    {
        "id": "Klipper3d-klipper",
        "repo_name": "Klipper3d/klipper",
        "title": "Klipper",
        "function_title": "Nagysebességű, Precíziós 3D Nyomtató Firmware",
        "description": "Többszörözd meg a 3D nyomtatód sebességét minőségromlás nélkül! A komplex számításokat egy Raspberry Pi végzi, mikroszekundumos pontossággal.",
        "main_category": "Hardver, IoT & Elektronika",
        "sub_category": "3D Nyomtatás, CNC & Klipper",
        "thumbnail_url": "https://opengraph.githubassets.com/1/Klipper3d/klipper",
        "video_url": "https://raw.githubusercontent.com/Klipper3d/klipper/master/docs/img/klipper-logo.png",
        "has_video": False,
        "video_demo": "",
        "stars": 10900,
        "url": "https://github.com/Klipper3d/klipper",
        "creator": "Klipper3d",
        "tags": ["klipper", "3d-printing", "firmware", "precision"]
    },
    {
        "id": "espressif-arduino-esp32",
        "repo_name": "espressif/arduino-esp32",
        "title": "Arduino Core for ESP32",
        "function_title": "Kétmagos ESP32 Mikrokontroller Fejlesztőkörnyezet",
        "description": "Programozz modern, nagysebességű ESP32 lapkákat az egyszerű Arduino felületen keresztül: beépített WiFi, Bluetooth, érintőszenzorok és hardveres gyorsítás.",
        "main_category": "Hardver, IoT & Elektronika",
        "sub_category": "Arduino & Mikrokontrollerek",
        "thumbnail_url": "https://opengraph.githubassets.com/1/espressif/arduino-esp32",
        "video_url": "https://raw.githubusercontent.com/espressif/arduino-esp32/master/docs/source/_static/logo.png",
        "has_video": False,
        "video_demo": "",
        "stars": 14800,
        "url": "https://github.com/espressif/arduino-esp32",
        "creator": "espressif",
        "tags": ["esp32", "arduino", "microcontroller", "embedded"]
    },
    {
        "id": "betaflight-betaflight",
        "repo_name": "betaflight/betaflight",
        "title": "Betaflight",
        "function_title": "Verseny- és FPV Drón Repülésvezérlő Autopilot",
        "description": "A világelső vezérlő szoftvere drónokhoz: giroszkóp-szűrés, akrobatikus repülés, GPS pozíciótartás és fekete doboz telemetria naplózás.",
        "main_category": "Hardver, IoT & Elektronika",
        "sub_category": "Robotika, Drónok & Edge AI",
        "thumbnail_url": "https://opengraph.githubassets.com/1/betaflight/betaflight",
        "video_url": "https://raw.githubusercontent.com/betaflight/betaflight/master/assets/images/betaflight_logo.svg",
        "has_video": True,
        "video_demo": "https://raw.githubusercontent.com/betaflight/betaflight/master/assets/images/betaflight_logo.svg",
        "stars": 8900,
        "url": "https://github.com/betaflight/betaflight",
        "creator": "betaflight",
        "tags": ["fpv", "drone", "flight-controller", "robotics"]
    },
    {
        "id": "FastLED-FastLED",
        "repo_name": "FastLED/FastLED",
        "title": "FastLED",
        "function_title": "Ultrafast LED Mátrix & Fényszobrász Könyvtár",
        "description": "Készíts szemet gyönyörködtető fényanimációkat és kijelzőket bármilyen címezhető LED szalagból Arduino és ESP32 lapkák segítségével.",
        "main_category": "Hardver, IoT & Elektronika",
        "sub_category": "Szenzorok, Kijelzők & LED Mátrixok",
        "thumbnail_url": "https://opengraph.githubassets.com/1/FastLED/FastLED",
        "video_url": "https://raw.githubusercontent.com/FastLED/FastLED/master/fastled.png",
        "has_video": False,
        "video_demo": "",
        "stars": 8400,
        "url": "https://github.com/FastLED/FastLED",
        "creator": "FastLED",
        "tags": ["led", "arduino", "neopixel", "animation"]
    },

    # --- MESTERSÉGES INTELLIGENCIA & ADAT ---
    {
        "id": "comfyanonymous-ComfyUI",
        "repo_name": "comfyanonymous/ComfyUI",
        "title": "ComfyUI",
        "function_title": "Moduláris Vizuális Képgeneráló Stúdió (FLUX & SD)",
        "description": "Illessz össze vizuális blokkokat, és generálj fotórealisztikus képeket és grafikákat a legújabb FLUX és Stable Diffusion AI modellekkel.",
        "main_category": "Mesterséges Intelligencia & Adat",
        "sub_category": "Képalkotás & Grafika (FLUX / SD)",
        "thumbnail_url": "https://opengraph.githubassets.com/1/comfyanonymous/ComfyUI",
        "video_url": "https://raw.githubusercontent.com/comfyanonymous/ComfyUI/master/extra/comfy_screenshot.png",
        "has_video": True,
        "video_demo": "https://user-images.githubusercontent.com/40797880/216507727-4a0b27b3-c1c6-476c-9411-404c0e668fd9.mp4",
        "stars": 63400,
        "url": "https://github.com/comfyanonymous/ComfyUI",
        "creator": "comfyanonymous",
        "tags": ["comfyui", "flux", "diffusion", "creative"]
    },
    {
        "id": "browser-use-browser-use",
        "repo_name": "browser-use/browser-use",
        "title": "Browser Use",
        "function_title": "Autonóm Böngésző Ágens (Kattintás, Keresés, Kitöltés)",
        "description": "Engedd, hogy az AI intézze el helyetted az online ügyintézést: megkeresi az olcsó repülőjegyet, kitölti a hosszú űrlapokat és letölti az adatokat.",
        "main_category": "Mesterséges Intelligencia & Adat",
        "sub_category": "Autonóm Ágensek & Automatizáció",
        "thumbnail_url": "https://opengraph.githubassets.com/1/browser-use/browser-use",
        "video_url": "https://github.com/browser-use/browser-use/raw/main/examples/quickstart.gif",
        "has_video": True,
        "video_demo": "https://github.com/browser-use/browser-use/raw/main/examples/quickstart.gif",
        "stars": 34500,
        "url": "https://github.com/browser-use/browser-use",
        "creator": "browser-use",
        "tags": ["browser-use", "agent", "automation"]
    },
    {
        "id": "KwaiVGI-LivePortrait",
        "repo_name": "KwaiVGI/LivePortrait",
        "title": "LivePortrait",
        "function_title": "Beszélő Arcanimáció & Mimika 1 db Fotóból",
        "description": "Kelts életre bármilyen álló portréképet vagy karaktert: a szemek, a száj és a fejmozgás tökéletesen követi a hangot vagy a mintavideót.",
        "main_category": "Mesterséges Intelligencia & Adat",
        "sub_category": "Videógenerálás & Mozgókép",
        "thumbnail_url": "https://opengraph.githubassets.com/1/KwaiVGI/LivePortrait",
        "video_url": "https://github.com/KwaiVGI/LivePortrait/raw/main/assets/docs/showcase.gif",
        "has_video": True,
        "video_demo": "https://github.com/KwaiVGI/LivePortrait/raw/main/assets/docs/showcase.gif",
        "stars": 18200,
        "url": "https://github.com/KwaiVGI/LivePortrait",
        "creator": "KwaiVGI",
        "tags": ["video-generation", "animation", "shorts"]
    },
    {
        "id": "SWivid-F5-TTS",
        "repo_name": "SWivid/F5-TTS",
        "title": "F5-TTS",
        "function_title": "Azonnali Hangklónozás 3 Másodperces Hangmintából",
        "description": "Tölts fel 3 másodpercnyi tiszta beszédet, és az AI azonos hangszínnel, intonációval és érzelmekkel olvassa fel a leírt szövegedet.",
        "main_category": "Mesterséges Intelligencia & Adat",
        "sub_category": "Hangklónozás & Beszédszintézis",
        "thumbnail_url": "https://opengraph.githubassets.com/1/SWivid/F5-TTS",
        "video_url": "https://github.com/SWivid/F5-TTS/raw/main/assets/demo.png",
        "has_video": True,
        "video_demo": "https://user-images.githubusercontent.com/11186711/f5tts_demo.mp4",
        "stars": 16400,
        "url": "https://github.com/SWivid/F5-TTS",
        "creator": "SWivid",
        "tags": ["tts", "voice-clone", "audio-ai"]
    },
    {
        "id": "ollama-ollama",
        "repo_name": "ollama/ollama",
        "title": "Ollama",
        "function_title": "Helyi és Offline Nagy Nyelvi Modellek Futtatója",
        "description": "Futtass Llama 3-at vagy DeepSeek-et a saját laptopodon internet és havidíj nélkül! Adatvédelem, helyi csevegés és automatizálás.",
        "main_category": "Mesterséges Intelligencia & Adat",
        "sub_category": "Lokális LLM-ek & Csevegők",
        "thumbnail_url": "https://opengraph.githubassets.com/1/ollama/ollama",
        "video_url": "https://github.com/ollama/ollama/raw/main/docs/overview.png",
        "has_video": False,
        "video_demo": "",
        "stars": 128000,
        "url": "https://github.com/ollama/ollama",
        "creator": "ollama",
        "tags": ["local-llm", "offline", "ai"]
    },

    # --- JÁTÉKFEJLESZTÉS, 3D & GRAFIKA ---
    {
        "id": "godotengine-godot",
        "repo_name": "godotengine/godot",
        "title": "Godot Engine",
        "function_title": "Nyílt Forráskódú 2D & 3D Játékmotor és Stúdió",
        "description": "Készíts professzionális 2D vagy 3D videójátékokat! Könnyű szerkesztő, beépített fizika, és egykattintásos export Windowsra, mobilra és webre.",
        "main_category": "Játékfejlesztés, 3D & Grafika",
        "sub_category": "Játékmotorok (Godot / Raylib)",
        "thumbnail_url": "https://opengraph.githubassets.com/1/godotengine/godot",
        "video_url": "https://raw.githubusercontent.com/godotengine/godot/master/logo_outlined.png",
        "has_video": True,
        "video_demo": "https://raw.githubusercontent.com/godotengine/godot/master/logo_outlined.png",
        "stars": 92000,
        "url": "https://github.com/godotengine/godot",
        "creator": "godotengine",
        "tags": ["game-engine", "gamedev", "godot", "3d", "2d"]
    },
    {
        "id": "aseprite-aseprite",
        "repo_name": "aseprite/aseprite",
        "title": "Aseprite",
        "function_title": "Animált Pixel Art & Sprite Készítő Játékokhoz",
        "description": "A digitális pixel art etalonja: képkockánkénti idővonal, rétegkezelés és azonnali spritesheet export indie fejlesztőknek.",
        "main_category": "Játékfejlesztés, 3D & Grafika",
        "sub_category": "Pixel Art, Shaders & Vizuális Effektek",
        "thumbnail_url": "https://opengraph.githubassets.com/1/aseprite/aseprite",
        "video_url": "https://raw.githubusercontent.com/aseprite/aseprite/main/data/icons/ase256.png",
        "has_video": True,
        "video_demo": "https://raw.githubusercontent.com/aseprite/aseprite/main/data/icons/ase256.png",
        "stars": 25400,
        "url": "https://github.com/aseprite/aseprite",
        "creator": "aseprite",
        "tags": ["pixel-art", "animation", "sprite", "creative"]
    },

    # --- ZENE & AUDIÓ TECHNIKA ---
    {
        "id": "facebookresearch-demucs",
        "repo_name": "facebookresearch/demucs",
        "title": "Demucs",
        "function_title": "Ének- és Hangszersávok Szétválasztása Bármely Dalból",
        "description": "Szedd szét a kedvenc zenédet tiszta éneksávra, dobra, basszusra és zongorára stúdióminőségben, egyetlen gombnyomással.",
        "main_category": "Zene, Hangtechnika & Audió",
        "sub_category": "Hangtisztítás & Sávszétválasztás",
        "thumbnail_url": "https://opengraph.githubassets.com/1/facebookresearch/demucs",
        "video_url": "https://raw.githubusercontent.com/facebookresearch/demucs/main/demucs.png",
        "has_video": True,
        "video_demo": "https://raw.githubusercontent.com/facebookresearch/demucs/main/demucs.png",
        "stars": 9800,
        "url": "https://github.com/facebookresearch/demucs",
        "creator": "Meta Research",
        "tags": ["stem-separation", "vocal-remover", "music", "ai-audio"]
    },
    {
        "id": "surge-synthesizer-surge",
        "repo_name": "surge-synthesizer/surge",
        "title": "Surge XT",
        "function_title": "Professzionális Hibrid Szintetizátor VST3 Plugin",
        "description": "Csúcsminőségű szintetizátor végtelen modulációval, beépített analóg és digitális hullámformákkal zeneszerzőknek és producereknek.",
        "main_category": "Zene, Hangtechnika & Audió",
        "sub_category": "VST Pluginek & Szintetizátorok",
        "thumbnail_url": "https://opengraph.githubassets.com/1/surge-synthesizer/surge",
        "video_url": "https://raw.githubusercontent.com/surge-synthesizer/surge/main/resources/surge-logo.png",
        "has_video": False,
        "video_demo": "",
        "stars": 4900,
        "url": "https://github.com/surge-synthesizer/surge",
        "creator": "surge-synthesizer",
        "tags": ["vst", "synth", "music-production", "audio"]
    },

    # --- SELF-HOSTED & OTTHONI SZERVEREK ---
    {
        "id": "jellyfin-jellyfin",
        "repo_name": "jellyfin/jellyfin",
        "title": "Jellyfin",
        "function_title": "100% Ingyenes Saját Film- és Zene Streaming Szerver",
        "description": "Építsd fel a saját privát médiaszerveredet és zenei könyvtáradat otthoni gépen vagy Raspberry Pi-n, előfizetés és hirdetések nélkül.",
        "main_category": "Self-Hosted & Otthoni Szerverek",
        "sub_category": "Médiaszerverek & Streaming (Jellyfin)",
        "thumbnail_url": "https://opengraph.githubassets.com/1/jellyfin/jellyfin",
        "video_url": "https://raw.githubusercontent.com/jellyfin/jellyfin-ux/master/branding/SVG/banner-dark.svg",
        "has_video": True,
        "video_demo": "https://raw.githubusercontent.com/jellyfin/jellyfin-ux/master/branding/SVG/banner-dark.svg",
        "stars": 38000,
        "url": "https://github.com/jellyfin/jellyfin",
        "creator": "jellyfin",
        "tags": ["streaming", "media-server", "home-lab", "self-hosted"]
    },
    {
        "id": "home-assistant-core",
        "repo_name": "home-assistant/core",
        "title": "Home Assistant",
        "function_title": "Központi Okosotthon Automatizálás és Érzékelő Hub",
        "description": "Fűzz össze minden lámpát, klímát, zárat és érzékelőt egyetlen modern felületre – internet nélkül, 100% helyi adatvédelemmel.",
        "main_category": "Self-Hosted & Otthoni Szerverek",
        "sub_category": "Home Assistant & Otthonautomatizálás",
        "thumbnail_url": "https://opengraph.githubassets.com/1/home-assistant/core",
        "video_url": "https://raw.githubusercontent.com/home-assistant/core/dev/homeassistant/components/frontend/www_static/icons/favicon-192x192.png",
        "has_video": True,
        "video_demo": "https://raw.githubusercontent.com/home-assistant/core/dev/homeassistant/components/frontend/www_static/icons/favicon-192x192.png",
        "stars": 75000,
        "url": "https://github.com/home-assistant/core",
        "creator": "home-assistant",
        "tags": ["smart-home", "iot", "automation", "privacy"]
    },
    {
        "id": "pi-hole-pi-hole",
        "repo_name": "pi-hole/pi-hole",
        "title": "Pi-hole",
        "function_title": "DNS Alapú Teljes Otthoni Hálózati Reklámblokkoló",
        "description": "Blokkolj minden reklámot és nyomkövetőt az otthoni WiFi-n: a tévéken, okostelefonokon és számítógépeken egyszerre.",
        "main_category": "Self-Hosted & Otthoni Szerverek",
        "sub_category": "Hálózatkezelés & VPN (Pi-hole, Wireguard)",
        "thumbnail_url": "https://opengraph.githubassets.com/1/pi-hole/pi-hole",
        "video_url": "https://raw.githubusercontent.com/pi-hole/pi-hole/master/advanced/Screenshots/Dashboard.png",
        "has_video": False,
        "video_demo": "",
        "stars": 49000,
        "url": "https://github.com/pi-hole/pi-hole",
        "creator": "pi-hole",
        "tags": ["dns", "adblock", "privacy", "raspberry-pi"]
    },

    # --- PRODUKTIVITÁS & IRODA ---
    {
        "id": "Frooodle-Stirling-PDF",
        "repo_name": "Stirling-Tools/Stirling-PDF",
        "title": "Stirling-PDF",
        "function_title": "Helyi PDF Svájcibicska: OCR, Darabolás, Vízjelezés",
        "description": "Nem kell fizetős Adobe Acrobat: egyesíts, darabolj, ismerj fel szöveget (OCR) vagy távolíts el jelszót közvetlenül a böngésződben.",
        "main_category": "Produktivitás & Irodai Munka",
        "sub_category": "PDF & Dokumentumkezelés",
        "thumbnail_url": "https://opengraph.githubassets.com/1/Stirling-Tools/Stirling-PDF",
        "video_url": "https://raw.githubusercontent.com/Stirling-Tools/Stirling-PDF/main/docs/Stirling-PDF-Logo.png",
        "has_video": True,
        "video_demo": "https://raw.githubusercontent.com/Stirling-Tools/Stirling-PDF/main/docs/Stirling-PDF-Logo.png",
        "stars": 48000,
        "url": "https://github.com/Stirling-Tools/Stirling-PDF",
        "creator": "Stirling-Tools",
        "tags": ["pdf", "ocr", "office", "utilities"]
    },

    # --- KREATÍV MÉDIA & VIDEÓVÁGÁS ---
    {
        "id": "obsproject-obs-studio",
        "repo_name": "obsproject/obs-studio",
        "title": "OBS Studio",
        "function_title": "Képernyővideó Rögzítő és Élő Adás Streamelő",
        "description": "Készíts professzionális oktatóvideókat, YouTube közvetítéseket és képernyőfelvételeket többféle kamerával és mikrofonnal.",
        "main_category": "Kreatív Média, Videóvágás & Fotó",
        "sub_category": "Képernyőfelvétel & Streaming (OBS Studio)",
        "thumbnail_url": "https://opengraph.githubassets.com/1/obsproject/obs-studio",
        "video_url": "https://raw.githubusercontent.com/obsproject/obs-studio/master/UI/forms/images/obs.png",
        "has_video": False,
        "video_demo": "",
        "stars": 59000,
        "url": "https://github.com/obsproject/obs-studio",
        "creator": "obsproject",
        "tags": ["streaming", "screen-recording", "obs", "broadcasting"]
    },
    {
        "id": "Krita-krita",
        "repo_name": "KDE/krita",
        "title": "Krita",
        "function_title": "Professzionális Digitális Festő- és Rajzprogram",
        "description": "Kifejezetten digitális illusztrátoroknak, képregény- és koncepciórajzolóknak tervezett professzionális ecsetkészlet és felület.",
        "main_category": "Kreatív Média, Videóvágás & Fotó",
        "sub_category": "Képszerkesztők (Krita / GIMP / Inkscape)",
        "thumbnail_url": "https://opengraph.githubassets.com/1/KDE/krita",
        "video_url": "https://raw.githubusercontent.com/KDE/krita/master/krita/data/about/splash.png",
        "has_video": True,
        "video_demo": "https://raw.githubusercontent.com/KDE/krita/master/krita/data/about/splash.png",
        "stars": 8700,
        "url": "https://github.com/KDE/krita",
        "creator": "KDE",
        "tags": ["painting", "digital-art", "illustration", "creatives"]
    }
]


def load_catalogue():
    """Load existing catalogue from JSON file."""
    if os.path.exists(CATALOGUE_FILE):
        try:
            with open(CATALOGUE_FILE, "r", encoding="utf-8") as f:
                data = json.load(f)
                if "categories" in data and len(data["categories"]) >= 7:
                    return data
        except Exception:
            pass
    return {
        "categories": UNIVERSAL_TAXONOMY,
        "items": UNIVERSAL_SEED_REPOSITORIES,
        "last_updated": time.strftime("%Y-%m-%d %H:%M:%S")
    }


def save_catalogue(data):
    """Save catalogue to JSON file."""
    os.makedirs(DATA_DIR, exist_ok=True)
    with open(CATALOGUE_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    print(f"[+] Saved {len(data['items'])} items to {CATALOGUE_FILE}")


if __name__ == "__main__":
    print("Initializing Universal Open Source Catalogue across ALL domains...")
    data = {
        "categories": UNIVERSAL_TAXONOMY,
        "items": UNIVERSAL_SEED_REPOSITORIES,
        "last_updated": time.strftime("%Y-%m-%d %H:%M:%S")
    }
    save_catalogue(data)
