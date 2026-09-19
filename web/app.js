/**
 * NexusHub — Universal Open Source & AI Visual Catalogue
 * Full Bilingual Support (English default & Hungarian toggle).
 * Handles live search, category/subcategory hierarchy, hidden gems merit sorting,
 * video preview modal, view switching, and community project submissions.
 */

let currentLang = localStorage.getItem("nexushub_lang") || "en";

const I18N = {
  en: {
    searchPlaceholder: "Search projects, functions, tags... (e.g. flux, esp32, whisper)",
    hiddenGemsBtn: "💎 Hidden Gems",
    shortDemosBtn: "▶ Short Demos",
    submitBtn: "+ Submit Project",
    manifestoPill: "💡 THE NEW ERA OF GITHUB",
    heroTitle: "Don't browse code names. <br><span class=\"gradient-text\">See the function and the solution!</span>",
    manifestoText: "<strong>The AI revolution fundamentally transformed GitHub's user base.</strong> Alongside traditional coders, millions of mainstream content creators, hardware makers, designers, and entrepreneurs have arrived. The legacy GitHub search was never built for them — <em>NexusHub is:</em> replacing cryptic acronyms with <strong>plain human functions, 15-second working video demos, and 0-star hidden gems</strong> discovered purely on merit.",
    statProjects: "projects in catalogue",
    statDemos: "video / animated demos",
    statUpdated: "Updated:",
    statNow: "Just now",
    allCategories: "All Categories",
    subcategoriesLabel: "Subcategories:",
    allSubcategories: "All subcategories",
    exploreAllTitle: "Explore All Open Source & AI Projects",
    hiddenGemsSectionTitle: "💎 Hidden Gems & Independent Projects",
    projectsFound: "projects found",
    sortLabel: "Sort by:",
    sortGems: "💎 Hidden Gems first (Merit & Proof)",
    sortStars: "⭐ Most Stars (Popularity)",
    sortName: "🔤 Alphabetical",
    viewGrid: "⊞ Grid",
    viewShelves: "☰ Shelves",
    functionLabel: "FUNCTION:",
    openGithub: "Open GitHub ↗",
    demoBadge: "▶ 15s DEMO",
    gemBadge: "💎 GEM",
    noProjectsFoundTitle: "No projects match your current filters",
    noProjectsFoundSubtitle: "Try clearing your search, removing video filter, or submit a new gem!",
    hiddenGemsShelfTitle: "💎 Fresh Discoveries & Hidden Gems (0-100 ⭐)",
    modalTechnicalRepo: "Technical Repo:",
    modalAuthor: "Author:",
    modalOpenGithub: "Open GitHub Repository ↗",
    modalCopyLink: "🔗 Copy Link",
    modalCopied: "✅ Copied!",
    submitModalBadge: "FOR INDEPENDENT CREATORS",
    submitModalTitle: "💎 Submit a Hidden Gem!",
    submitModalDesc: "Whether it's your own 0-star Arduino controller, an ESP32 maker project, or an AI workflow — if it works and has visual proof, it belongs here!",
    submitLabelRepo: "GitHub Repo URL (Required):",
    submitLabelTitle: "Project Title:",
    submitLabelCategory: "Primary Category:",
    submitLabelDemo: "15-30s Demo Video / GIF Link (Recommended):",
    submitLabelDesc: "One-sentence function summary (What does it do?):",
    submitBtnText: "🚀 Publish to Catalogue Immediately",
    submitSuccessAlert: "🎉 Congratulations! Your project has been added to NexusHub's Hidden Gems!",
    footerMission: "A function-first, video-powered open-source search engine adapted to the transformed user demographic of the AI era.",
    footerConceptBadge: "💡 ORIGINAL CONCEPT & INTELLECTUAL PROPERTY",
    footerConceptText: "Created by <strong>grezoo</strong> (<a href=\"mailto:grezoo@gmail.com\" class=\"author-email-link\">grezoo@gmail.com</a>). The visual, function-first open-source discovery paradigm, video-first shelves, and the star-independent <strong>'Hidden Gems'</strong> engine are the original intellectual creation of <strong>grezoo</strong>.",
    footerCopyright: "© 2026 NexusHub by grezoo. All rights reserved.",
    footerDonationLabel: "SUPPORT THE CREATOR",
    footerDonateBtn: "💳 Support via Revolut (@grezoo)",
    footerDonationSubtext: "Revolut Tag: <strong>@grezoo</strong> | Direct & secure creator support",
    standardTitle: "Are you an Open Source Creator? Upload a preview.mp4 or preview.gif!",
    standardDesc: "Place a 15-30s demo named <strong>preview.mp4</strong> or <strong>preview.gif</strong> in your repo root. NexusHub automatically detects it, plays it directly on your card, highlights your project on the homepage, and grants the <strong>▶ Verified Short Demo</strong> badge!",
    standardBtn: "Copy README Badge",
    standardCopied: "✅ Badge Copied!"
  },
  hu: {
    searchPlaceholder: "Keresés projektek, funkciók, tagek között... (pl. flux, esp32, whisper)",
    hiddenGemsBtn: "💎 Rejtett Kincsek",
    shortDemosBtn: "▶ Csak Short Demók",
    submitBtn: "+ Projekt Beküldése",
    manifestoPill: "💡 A GITHUB ÚJ KORSZAKA",
    heroTitle: "Ne kódneveket böngéssz. <br><span class=\"gradient-text\">Lásd a funkciót és a megoldást!</span>",
    manifestoText: "<strong>Az AI forradalma alapjaiban változtatta meg a GitHub felhasználói táborát.</strong> A kódolók mellett megjelentek a mainstream tartalomkészítők, elektronikai alkotók, dizájnerek és vállalkozók milliói. A régi GitHub-kereső nem nekik készült — <em>a NexusHub viszont igen:</em> a technikai betűszavak helyett <strong>emberi funkciókat, 15 másodperces működő videós demókat és a 0 csillagos rejtett kincseket</strong> hozza felszínre.",
    statProjects: "projekt a katalógusban",
    statDemos: "videós / animált demó",
    statUpdated: "Frissítve:",
    statNow: "Most",
    allCategories: "Összes Kategória",
    subcategoriesLabel: "Alcsoportok:",
    allSubcategories: "Összes alcsoport",
    exploreAllTitle: "Összes Nyílt Forráskódú & AI Projekt",
    hiddenGemsSectionTitle: "💎 Rejtett Kincsek & Független Projektek",
    projectsFound: "projekt találat",
    sortLabel: "Rendezés:",
    sortGems: "💎 Rejtett Kincsek előre (Merit & Proof)",
    sortStars: "⭐ Legtöbb csillag (Népszerűség)",
    sortName: "🔤 ABC sorrend",
    viewGrid: "⊞ Rács",
    viewShelves: "☰ Polcok",
    functionLabel: "FUNKCIÓ:",
    openGithub: "GitHub Megnyitása ↗",
    demoBadge: "▶ 15s DEMÓ",
    gemBadge: "💎 KINCS",
    noProjectsFoundTitle: "Nem található projekt a kiválasztott szűrőkkel",
    noProjectsFoundSubtitle: "Kapcsold ki a szűrőket, vagy ajánlj egy új kincset a '+ Projekt Beküldése' gombbal!",
    hiddenGemsShelfTitle: "💎 Friss Felfedezések & Rejtett Kincsek (0-100 ⭐)",
    modalTechnicalRepo: "Technikai Repó:",
    modalAuthor: "Szerző:",
    modalOpenGithub: "Ugrás a GitHub Repóra ↗",
    modalCopyLink: "🔗 Link Másolása",
    modalCopied: "✅ Másolva!",
    submitModalBadge: "FÜGGETLEN ALKOTÓKNAK",
    submitModalTitle: "💎 Ajánlj egy Kincset!",
    submitModalDesc: "Legyen az egy 0 csillagos saját Arduino vezérlőd, ESP32 projekted vagy AI fejlesztésed – ha működik és van bizonyítékod, itt a helye!",
    submitLabelRepo: "GitHub Repó URL (Kötelező):",
    submitLabelTitle: "Projekt Címe:",
    submitLabelCategory: "Főcsoport:",
    submitLabelDemo: "15-30s Demó Videó / GIF Link (Ajánlott):",
    submitLabelDesc: "1 mondatos leírás (Mit csinál?):",
    submitBtnText: "🚀 Azonnali Közzététel a Katalógusban",
    submitSuccessAlert: "🎉 Gratulálunk! A projekt azonnal bekerült a NexusHub katalógusba a Rejtett Kincsek közé!",
    footerMission: "Az AI-korszak megváltozott felhasználói igényeihez igazított, funkció- és videóalapú nyílt forráskódú keresőmotor.",
    footerConceptBadge: "💡 EREDETI KONCEPCIÓ & SZELLEMI TULAJDON",
    footerConceptText: "Megalkotta: <strong>grezoo</strong> (<a href=\"mailto:grezoo@gmail.com\" class=\"author-email-link\">grezoo@gmail.com</a>). A mainstream és videóalapú nyílt forráskódú katalógus, a funkcióközpontú címrendszer és a csillagfüggetlen <strong>'Rejtett Kincsek'</strong> felfedező logikája <strong>grezoo</strong> szellemi terméke.",
    footerCopyright: "© 2026 NexusHub by grezoo. Minden jog fenntartva.",
    footerDonationLabel: "TÁMOGASD AZ ALKOTÓT",
    footerDonateBtn: "💳 Támogatás Revoluton (@grezoo)",
    footerDonationSubtext: "Revolut Tag: <strong>@grezoo</strong> | Közvetlen készítői támogatás",
    standardTitle: "Nyílt forráskódú alkotó vagy? Tölts fel egy preview.mp4 vagy preview.gif fájlt!",
    standardDesc: "Helyezz el egy 15-30 másodperces demót <strong>preview.mp4</strong> vagy <strong>preview.gif</strong> néven a repód gyökerében. A NexusHub automatikusan felismeri, közvetlenül a kártyádon játssza le, előresorolja a kezdőlapon, és megkapod a <strong>▶ Ellenőrzött Short Demó</strong> jelvényt!",
    standardBtn: "README Jelvény Másolása",
    standardCopied: "✅ Jelvény Másolva!"
  }
};

// Bilingual Category Translations
const CATEGORY_TRANSLATIONS = {
  "Hardver, IoT & Elektronika": { en: "Hardware, IoT & Electronics", hu: "Hardver, IoT & Elektronika", icon: "🔌" },
  "Mesterséges Intelligencia & Adat": { en: "Artificial Intelligence & Data", hu: "Mesterséges Intelligencia & Adat", icon: "🧠" },
  "Játékfejlesztés, 3D & Grafika": { en: "Game Dev, 3D & Graphics", hu: "Játékfejlesztés, 3D & Grafika", icon: "🎮" },
  "Zene, Hangtechnika & Audió": { en: "Music & Audio Tech", hu: "Zene, Hangtechnika & Audió", icon: "🎵" },
  "Self-Hosted & Otthoni Szerverek": { en: "Self-Hosted & Home Labs", hu: "Self-Hosted & Otthoni Szerverek", icon: "🏠" },
  "Produktivitás & Irodai Munka": { en: "Productivity & Office", hu: "Produktivitás & Irodai Munka", icon: "📊" },
  "Kreatív Média, Videóvágás & Fotó": { en: "Creative Media & Video", hu: "Kreatív Média, Videóvágás & Fotó", icon: "🎬" },
  "Rendszer, Biztonság & Segédprogramok": { en: "System, Security & Utilities", hu: "Rendszer, Biztonság & Segédprogramok", icon: "⚡" }
};

// English Translations for Seed Functions
const FUNCTION_TRANSLATIONS_EN = {
  "WiFi-s Címezhető LED Szalag Vezérlő (100+ Effekt)": "WiFi Addressable LED Strip Controller (100+ Effects)",
  "ESP32 & ESP8266 Szenzorvezérlő (Kódolás Nélkül)": "ESP32 & ESP8266 Sensor Controller (No-Code YAML)",
  "Nagysebességű, Precíziós 3D Nyomtató Firmware": "High-Speed, Precision 3D Printer Firmware",
  "Kétmagos ESP32 Mikrokontroller Fejlesztőkörnyezet": "Dual-Core ESP32 Microcontroller Arduino Core",
  "Verseny- és FPV Drón Repülésvezérlő Autopilot": "Racing & FPV Drone Flight Controller Autopilot",
  "Ultrafast LED Mátrix & Fényszobrász Könyvtár": "Ultrafast LED Matrix & Light-Art Animation Library",
  "Moduláris Vizuális Képgeneráló Stúdió (FLUX & SD)": "Modular Visual Image Generation Studio (FLUX & SD)",
  "Autonóm Böngésző Ágens (Kattintás, Keresés, Kitöltés)": "Autonomous Browser Agent (Click, Search, Fill)",
  "Beszélő Arcanimáció & Mimika 1 db Fotóból": "Talking Face Animation & Lip-Sync from 1 Photo",
  "Azonnali Hangklónozás 3 Másodperces Hangmintából": "Instant Voice Cloning from 3-Second Audio Sample",
  "Helyi és Offline Nagy Nyelvi Modellek Futtatója": "Run Local & Offline Large Language Models (LLMs)",
  "Nyílt Forráskódú 2D & 3D Játékmotor és Stúdió": "Open-Source 2D & 3D Game Engine & Studio",
  "Animált Pixel Art & Sprite Készítő Játékokhoz": "Animated Pixel Art & Sprite Editor for Game Dev",
  "Ének- és Hangszersávok Szétválasztása Bármely Dalból": "AI Vocal & Stem Separation from Any Music Track",
  "Professzionális Hibrid Szintetizátor VST3 Plugin": "Professional Hybrid Synthesizer VST3 Plugin",
  "100% Ingyenes Saját Film- és Zene Streaming Szerver": "100% Free Self-Hosted Media & Music Streaming",
  "Központi Okosotthon Automatizálás és Érzékelő Hub": "Central Smart Home Automation & Sensor Hub",
  "DNS Alapú Teljes Otthoni Hálózati Reklámblokkoló": "Network-Wide DNS Ad & Tracker Blocker",
  "Helyi PDF Svájcibicska: OCR, Darabolás, Vízjelezés": "Local PDF Swiss-Army Knife: OCR, Split, Watermark",
  "Képernyővideó Rögzítő és Élő Adás Streamelő": "Screen Recording & Live Streaming Studio",
  "Professzionális Digitális Festő- és Rajzprogram": "Professional Digital Painting & Concept Art Studio",
  "ESP32 WiFi Micro-Drón Vezérlő": "ESP32 WiFi Micro-Drone Controller & Web Remote",
  "Magyar Hangszintézis Modell (TTS)": "High-Quality Neural Hungarian Speech Synthesizer"
};

let catalogueData = {
  categories: [],
  items: [],
  last_updated: ""
};

let currentMainCat = "all";
let currentSubCat = "all";
let onlyVideosFilter = false;
let onlyGemsFilter = false;
let currentSort = "gems";
let searchQuery = "";
let currentViewMode = "grid";

// DOM Elements
const searchInput = document.getElementById("searchInput");
const onlyVideoBtn = document.getElementById("onlyVideoBtn");
const hiddenGemsBtn = document.getElementById("hiddenGemsBtn");
const submitRepoBtn = document.getElementById("submitRepoBtn");
const sortSelect = document.getElementById("sortSelect");
const mainCategoriesContainer = document.getElementById("mainCategoriesContainer");
const subCategoriesContainer = document.getElementById("subCategoriesContainer");
const subCategoriesBar = document.getElementById("subCategoriesBar");
const cardsGrid = document.getElementById("cardsGrid");
const shelvesContainer = document.getElementById("shelvesContainer");
const viewGridBtn = document.getElementById("viewGridBtn");
const viewShelfBtn = document.getElementById("viewShelfBtn");
const currentSectionTitle = document.getElementById("currentSectionTitle");
const itemsFoundText = document.getElementById("itemsFoundText");
const totalCountEl = document.getElementById("totalCount");
const videoCountEl = document.getElementById("videoCount");
const lastUpdatedEl = document.getElementById("lastUpdated");
const langEnBtn = document.getElementById("langEnBtn");
const langHuBtn = document.getElementById("langHuBtn");

// Detail Modal Elements
const detailModal = document.getElementById("detailModal");
const modalCloseBtn = document.getElementById("modalCloseBtn");
const modalMediaContainer = document.getElementById("modalMediaContainer");
const modalCategory = document.getElementById("modalCategory");
const modalSubCategory = document.getElementById("modalSubCategory");
const modalStars = document.getElementById("modalStars");
const modalTitle = document.getElementById("modalTitle");
const modalCreator = document.getElementById("modalCreator");
const modalDesc = document.getElementById("modalDesc");
const modalTags = document.getElementById("modalTags");
const modalGithubLink = document.getElementById("modalGithubLink");
const copyUrlBtn = document.getElementById("copyUrlBtn");

// Submit Modal Elements
const submitModal = document.getElementById("submitModal");
const submitModalCloseBtn = document.getElementById("submitModalCloseBtn");
const submitForm = document.getElementById("submitForm");

// Apply Language strings to Static DOM
function applyLanguage() {
  const t = I18N[currentLang];

  // Active button styling
  langEnBtn.classList.toggle("active", currentLang === "en");
  langHuBtn.classList.toggle("active", currentLang === "hu");

  // Search input
  searchInput.placeholder = t.searchPlaceholder;

  // Header buttons
  hiddenGemsBtn.querySelector("span").textContent = t.hiddenGemsBtn;
  onlyVideoBtn.querySelector("span:last-child").textContent = t.shortDemosBtn;
  submitRepoBtn.querySelector("span").textContent = t.submitBtn;

  // Hero & Manifesto
  const manifestoPill = document.querySelector(".manifesto-pill");
  if (manifestoPill) manifestoPill.textContent = t.manifestoPill;

  const heroTitle = document.querySelector(".hero-title");
  if (heroTitle) heroTitle.innerHTML = t.heroTitle;

  const manifestoText = document.querySelector(".manifesto-text");
  if (manifestoText) manifestoText.innerHTML = t.manifestoText;

  // Stats labels
  const statItems = document.querySelectorAll(".hero-stats .stat-item");
  if (statItems.length >= 3) {
    statItems[0].innerHTML = `<span class="stat-number" id="totalCount">${totalCountEl.textContent}</span> ${t.statProjects}`;
    statItems[1].innerHTML = `<span class="stat-number" id="videoCount">${videoCountEl.textContent}</span> ${t.statDemos}`;
    statItems[2].innerHTML = `${t.statUpdated} <span id="lastUpdated">${lastUpdatedEl.textContent}</span>`;
  }

  // Sort labels
  const sortLabel = document.querySelector(".sort-label");
  if (sortLabel) sortLabel.textContent = t.sortLabel;

  if (sortSelect && sortSelect.options.length >= 3) {
    sortSelect.options[0].textContent = t.sortGems;
    sortSelect.options[1].textContent = t.sortStars;
    sortSelect.options[2].textContent = t.sortName;
  }

  // View buttons
  if (viewGridBtn) viewGridBtn.textContent = t.viewGrid;
  if (viewShelfBtn) viewShelfBtn.textContent = t.viewShelves;

  // Standard Creator Banner
  const standardTitle = document.querySelector(".standard-title");
  if (standardTitle) standardTitle.textContent = t.standardTitle;

  const standardDesc = document.querySelector(".standard-desc");
  if (standardDesc) standardDesc.innerHTML = t.standardDesc;

  const showBadgeGuideBtn = document.getElementById("showBadgeGuideBtn");
  if (showBadgeGuideBtn) showBadgeGuideBtn.textContent = t.standardBtn;

  // Subcategories label
  const subLabel = document.querySelector(".sub-label");
  if (subLabel) subLabel.textContent = t.subcategoriesLabel;

  // Footer elements
  const footerMission = document.querySelector(".footer-mission");
  if (footerMission) footerMission.textContent = t.footerMission;

  const conceptBadge = document.querySelector(".concept-badge");
  if (conceptBadge) conceptBadge.textContent = t.footerConceptBadge;

  const conceptText = document.querySelector(".concept-text");
  if (conceptText) conceptText.innerHTML = t.footerConceptText;

  const copyrightYear = document.querySelector(".copyright-year");
  if (copyrightYear) copyrightYear.textContent = t.footerCopyright;

  const donationLabel = document.querySelector(".donation-label");
  if (donationLabel) donationLabel.textContent = t.footerDonationLabel;

  const donateBtn = document.getElementById("donateBtn");
  if (donateBtn) donateBtn.querySelector("span:last-child").textContent = t.footerDonateBtn;

  const donationSubtext = document.querySelector(".donation-subtext");
  if (donationSubtext) donationSubtext.textContent = t.footerDonationSubtext;

  // Re-render categories and items in current language
  renderMainCategories();
  renderSubCategories();
  renderItems();
}

// Set active language
function setLanguage(lang) {
  currentLang = lang;
  localStorage.setItem("nexushub_lang", lang);
  applyLanguage();
}

// Get translated category name
function getCategoryName(rawName) {
  if (CATEGORY_TRANSLATIONS[rawName]) {
    return CATEGORY_TRANSLATIONS[rawName][currentLang] || rawName;
  }
  return rawName;
}

// Get translated function title for card
function getItemFunctionTitle(item) {
  const huTitle = item.function_title || item.title;
  if (currentLang === "en") {
    return FUNCTION_TRANSLATIONS_EN[huTitle] || item.title_en || huTitle;
  }
  return huTitle;
}

// Initialize application
async function init() {
  try {
    const res = await fetch("/api/catalogue");
    catalogueData = await res.json();
  } catch (err) {
    try {
      const res = await fetch("../data/catalogue.json");
      catalogueData = await res.json();
    } catch (e) {
      console.error("Failed to load catalogue:", e);
    }
  }

  ensureSampleGems();
  updateStats();
  applyLanguage();
  setupEventListeners();
}

// Pinned Flagship Reference Project demonstrating the standard
const PINNED_SHOWCASE_ITEM = {
  id: "nexushub-official-standard",
  is_pinned: true,
  repo_name: "grezoo/nexushub",
  title: "NexusHub — Open Source Streaming Library",
  function_title: "Netflix-stílusú Vizuális Felfedező a Nyílt Forráskódhoz",
  title_en: "Visual Streaming & Netflix-Style Discovery for Open Source",
  description: "Böngéssz a nyílt forráskódú eszközök, hardverek és AI projektek között úgy, mint egy streaming platformon: képes kártyák, 15 mp-es élő videók és azonnali kipróbálás kódböngészés helyett.",
  description_en: "Browse open-source tools, hardware, and AI like a streaming service: visual cards, live 15-second video previews, and merit-based discovery instead of reading code.",
  main_category: "Rendszer, Biztonság & Segédprogramok",
  sub_category: "Vizuális Streaming & Katalógus",
  thumbnail_url: "netflix_showcase.svg",
  video_url: "netflix_showcase.svg",
  has_video: true,
  video_demo: "netflix_showcase.svg",
  stars: 100,
  url: "https://github.com/grezoo/nexushub",
  creator: "grezoo",
  tags: ["netflix-ui", "open-source-discovery", "visual-cards", "hidden-gems"]
};

// Ensure 0-50 star hidden gems exist in seed and pin the flagship showcase
function ensureSampleGems() {
  const gems = [
    PINNED_SHOWCASE_ITEM,
    {
      id: "maker-esp32-drone-fc",
      repo_name: "open-maker/esp32-wifi-drone",
      title: "ESP32 WiFi Micro-Drón Vezérlő",
      function_title: "ESP32 WiFi Micro-Drón Vezérlő",
      description: "Egyetlen ESP32-vel és MPU6050 giroszkóppal működő ultrakönnyű minidrón teljes szoftvere, böngészős távirányítással.",
      main_category: "Hardver, IoT & Elektronika",
      sub_category: "Robotika, Drónok & Edge AI",
      thumbnail_url: "https://opengraph.githubassets.com/1/open-maker/esp32-wifi-drone",
      video_url: "https://images.unsplash.com/photo-1527977966376-1c8408f9f108?w=800&auto=format&fit=crop&q=60",
      has_video: true,
      video_demo: "https://images.unsplash.com/photo-1527977966376-1c8408f9f108?w=800&auto=format&fit=crop&q=60",
      stars: 4,
      url: "https://github.com/espressif/arduino-esp32",
      creator: "open-maker",
      tags: ["esp32", "drone", "flight-control", "hidden-gem"]
    },
    {
      id: "solo-ai-voice-hu",
      repo_name: "hungarian-ai/magyar-hang-tts",
      title: "Magyar Hangszintézis Modell (TTS)",
      function_title: "Magyar Hangszintézis Modell (TTS)",
      description: "Tiszta magyar kiejtésre és intonációra tanított könnyűsúlyú hangklónozó modell Raspberry Pi-re és mobilra.",
      main_category: "Mesterséges Intelligencia & Adat",
      sub_category: "Hangklónozás & Beszédszintézis",
      thumbnail_url: "https://opengraph.githubassets.com/1/hungarian-ai/magyar-hang-tts",
      video_url: "https://images.unsplash.com/photo-1590602847861-f357a9332bbc?w=800&auto=format&fit=crop&q=60",
      has_video: true,
      video_demo: "https://images.unsplash.com/photo-1590602847861-f357a9332bbc?w=800&auto=format&fit=crop&q=60",
      stars: 9,
      url: "https://github.com/SWivid/F5-TTS",
      creator: "hungarian-ai",
      tags: ["hungarian", "tts", "voice-clone", "garage-project"]
    }
  ];

  gems.forEach(g => {
    if (!catalogueData.items.some(i => i.id === g.id)) {
      catalogueData.items.unshift(g);
    }
  });
}

// Update Hero Stats
function updateStats() {
  const t = I18N[currentLang];
  const total = catalogueData.items.length;
  const withVideo = catalogueData.items.filter(i => i.has_video).length;
  totalCountEl.textContent = total;
  videoCountEl.textContent = withVideo;
  lastUpdatedEl.textContent = catalogueData.last_updated || t.statNow;
}

// Render Main Categories navigation
function renderMainCategories() {
  const t = I18N[currentLang];
  mainCategoriesContainer.innerHTML = "";

  // 'All' button
  const allBtn = document.createElement("button");
  allBtn.className = `cat-btn ${currentMainCat === "all" ? "active" : ""}`;
  allBtn.innerHTML = `<span>🌐</span><span>${t.allCategories}</span>`;
  allBtn.onclick = () => selectMainCategory("all");
  mainCategoriesContainer.appendChild(allBtn);

  catalogueData.categories.forEach(cat => {
    const btn = document.createElement("button");
    btn.className = `cat-btn ${currentMainCat === cat.main ? "active" : ""}`;
    const translatedName = getCategoryName(cat.main);
    btn.innerHTML = `<span>${cat.icon || "📁"}</span><span>${translatedName}</span>`;
    btn.onclick = () => selectMainCategory(cat.main);
    mainCategoriesContainer.appendChild(btn);
  });
}

// Select Main Category
function selectMainCategory(catName) {
  currentMainCat = catName;
  currentSubCat = "all";
  renderMainCategories();
  renderSubCategories();
  renderItems();
}

// Render Subcategories
function renderSubCategories() {
  const t = I18N[currentLang];
  subCategoriesContainer.innerHTML = "";

  if (currentMainCat === "all") {
    subCategoriesBar.style.display = "none";
    return;
  }

  subCategoriesBar.style.display = "flex";
  const catObj = catalogueData.categories.find(c => c.main === currentMainCat);
  if (!catObj) return;

  // 'All subcategories' button
  const allSubBtn = document.createElement("button");
  allSubBtn.className = `sub-btn ${currentSubCat === "all" ? "active" : ""}`;
  allSubBtn.textContent = t.allSubcategories;
  allSubBtn.onclick = () => {
    currentSubCat = "all";
    renderSubCategories();
    renderItems();
  };
  subCategoriesContainer.appendChild(allSubBtn);

  const subList = Array.isArray(catObj.subcategories) 
    ? catObj.subcategories 
    : Object.keys(catObj.subcategories || {});

  subList.forEach(subName => {
    const btn = document.createElement("button");
    btn.className = `sub-btn ${currentSubCat === subName ? "active" : ""}`;
    btn.textContent = subName;
    btn.onclick = () => {
      currentSubCat = subName;
      renderSubCategories();
      renderItems();
    };
    subCategoriesContainer.appendChild(btn);
  });
}

// Filter and sort items based on active criteria
function getFilteredAndSortedItems() {
  let list = catalogueData.items.filter(item => {
    if (currentMainCat !== "all" && item.main_category !== currentMainCat) return false;
    if (currentSubCat !== "all" && item.sub_category !== currentSubCat) return false;
    if (onlyVideosFilter && !item.has_video) return false;
    if (onlyGemsFilter && (item.stars || 0) > 100) return false;

    if (searchQuery.trim() !== "") {
      const q = searchQuery.toLowerCase();
      const matchTitle = (item.title || "").toLowerCase().includes(q);
      const matchFunc = (item.function_title || "").toLowerCase().includes(q);
      const matchDesc = (item.description || "").toLowerCase().includes(q);
      const matchRepo = (item.repo_name || "").toLowerCase().includes(q);
      const matchTags = (item.tags || []).some(t => t.toLowerCase().includes(q));
      if (!matchTitle && !matchFunc && !matchDesc && !matchRepo && !matchTags) {
        return false;
      }
    }
    return true;
  });

  // Sorting
  if (currentSort === "gems") {
    list.sort((a, b) => {
      if (a.is_pinned) return -1;
      if (b.is_pinned) return 1;
      const aScore = (a.has_video ? 1000 : 0) - (a.stars || 0);
      const bScore = (b.has_video ? 1000 : 0) - (b.stars || 0);
      return bScore - aScore;
    });
  } else if (currentSort === "stars") {
    list.sort((a, b) => {
      if (a.is_pinned) return -1;
      if (b.is_pinned) return 1;
      return (b.stars || 0) - (a.stars || 0);
    });
  } else if (currentSort === "name") {
    list.sort((a, b) => {
      if (a.is_pinned) return -1;
      if (b.is_pinned) return 1;
      return (a.title || "").localeCompare(b.title || "");
    });
  }

  // Double check pinned item is first
  const pinnedIdx = list.findIndex(i => i.is_pinned);
  if (pinnedIdx > 0) {
    const [pinned] = list.splice(pinnedIdx, 1);
    list.unshift(pinned);
  }

  return list;
}

// Render items into Grid or Shelf view
function renderItems() {
  const t = I18N[currentLang];
  const filtered = getFilteredAndSortedItems();

  currentSectionTitle.textContent = onlyGemsFilter 
    ? t.hiddenGemsSectionTitle
    : currentMainCat === "all" 
      ? t.exploreAllTitle
      : `${getCategoryName(currentMainCat)} ${currentSubCat !== "all" ? "› " + currentSubCat : ""}`;
  
  itemsFoundText.textContent = `${filtered.length} ${t.projectsFound}`;

  if (currentViewMode === "grid") {
    cardsGrid.style.display = "grid";
    shelvesContainer.style.display = "none";
    renderGridView(filtered);
  } else {
    cardsGrid.style.display = "none";
    shelvesContainer.style.display = "block";
    renderShelfView(filtered);
  }
}

// Render Grid View
function renderGridView(items) {
  const t = I18N[currentLang];
  cardsGrid.innerHTML = "";

  if (items.length === 0) {
    cardsGrid.innerHTML = `
      <div style="grid-column: 1 / -1; text-align: center; padding: 60px 20px; color: var(--text-dim);">
        <div style="font-size: 48px; margin-bottom: 12px;">💎</div>
        <h3>${t.noProjectsFoundTitle}</h3>
        <p style="margin-top: 8px;">${t.noProjectsFoundSubtitle}</p>
      </div>
    `;
    return;
  }

  items.forEach(item => {
    cardsGrid.appendChild(createCardElement(item));
  });
}

// Render Shelf View
function renderShelfView(items) {
  const t = I18N[currentLang];
  shelvesContainer.innerHTML = "";

  if (items.length === 0) {
    shelvesContainer.innerHTML = `
      <div style="text-align: center; padding: 60px 20px; color: var(--text-dim);">
        <h3>${t.noProjectsFoundTitle}</h3>
      </div>
    `;
    return;
  }

  // If in 'all' view, feature a dedicated Hidden Gems shelf on top
  if (currentMainCat === "all" && !onlyGemsFilter) {
    const gems = items.filter(i => (i.stars || 0) <= 100);
    if (gems.length > 0) {
      const gemShelf = document.createElement("div");
      gemShelf.className = "shelf";
      gemShelf.innerHTML = `
        <h3 class="shelf-title" style="color: #34d399;">
          <span>${t.hiddenGemsShelfTitle}</span>
          <span style="font-size: 13px; color: var(--text-dim); font-weight: normal;">(${gems.length})</span>
        </h3>
        <div class="shelf-rail"></div>
      `;
      const rail = gemShelf.querySelector(".shelf-rail");
      gems.forEach(g => rail.appendChild(createCardElement(g)));
      shelvesContainer.appendChild(gemShelf);
    }
  }

  // Group items by category or subcategory
  const groupKey = currentMainCat === "all" ? "main_category" : "sub_category";
  const groups = {};

  items.forEach(item => {
    const key = item[groupKey] || "Other";
    if (!groups[key]) groups[key] = [];
    groups[key].push(item);
  });

  Object.entries(groups).forEach(([groupName, groupItems]) => {
    const shelf = document.createElement("div");
    shelf.className = "shelf";

    const displayGroupName = currentMainCat === "all" ? getCategoryName(groupName) : groupName;

    const title = document.createElement("h3");
    title.className = "shelf-title";
    title.innerHTML = `<span>${displayGroupName}</span> <span style="font-size: 13px; color: var(--text-dim); font-weight: normal;">(${groupItems.length})</span>`;
    shelf.appendChild(title);

    const rail = document.createElement("div");
    rail.className = "shelf-rail";

    groupItems.forEach(item => {
      rail.appendChild(createCardElement(item));
    });

    shelf.appendChild(rail);
    shelvesContainer.appendChild(shelf);
  });
}

// Create a single interactive Card DOM element with DIRECT INLINE VIDEO PLAYBACK
function createCardElement(item) {
  const t = I18N[currentLang];
  const card = document.createElement("div");
  card.className = "card" + (item.is_pinned ? " card-pinned" : "");
  card.onclick = (e) => {
    if (e.target.closest(".card-btn")) return;
    openDetailModal(item);
  };

  const isGem = (item.stars || 0) <= 50 && !item.is_pinned;
  const starsFormatted = item.stars >= 1000 
    ? (item.stars / 1000).toFixed(1) + "k" 
    : (item.stars || 0);

  const thumbUrl = item.thumbnail_url || `https://opengraph.githubassets.com/1/${item.repo_name}`;
  const functionTitle = getItemFunctionTitle(item);
  const technicalRepo = item.repo_name || item.title;

  // Direct video or image markup
  let mediaMarkup = "";
  const hasMp4 = item.has_video && item.video_demo && item.video_demo.endsWith(".mp4");
  const isGif = item.video_demo && (item.video_demo.endsWith(".gif") || item.video_demo.includes("giphy.com"));

  if (hasMp4) {
    mediaMarkup = `
      <video class="card-video" src="${item.video_demo}" muted loop playsinline preload="metadata" poster="${thumbUrl}"></video>
      <img src="${thumbUrl}" alt="${functionTitle}" class="card-img card-poster-fallback" loading="lazy" onerror="this.src='https://opengraph.githubassets.com/1/${item.repo_name}'">
    `;
  } else if (isGif) {
    mediaMarkup = `
      <img src="${item.video_demo}" alt="${functionTitle}" class="card-img" loading="lazy" onerror="this.src='${thumbUrl}'">
    `;
  } else {
    mediaMarkup = `
      <img src="${thumbUrl}" alt="${functionTitle}" class="card-img" loading="lazy" onerror="this.src='https://opengraph.githubassets.com/1/${item.repo_name}'">
    `;
  }

  const pinnedBadge = currentLang === "en" ? "📌 PINNED SHOWCASE" : "📌 HIVATALOS MINTA";

  card.innerHTML = `
    <div class="card-media">
      ${mediaMarkup}
      <div class="card-media-overlay"></div>
      ${item.is_pinned ? `<div class="badge-pinned">${pinnedBadge}</div>` : ''}
      ${isGem ? `<div class="badge-gem">${t.gemBadge}</div>` : ''}
      ${item.has_video ? `<div class="badge-video">${t.demoBadge}</div>` : ''}
      <div class="badge-function-tag">${item.sub_category || getCategoryName(item.main_category)}</div>
    </div>
    <div class="card-body">
      <div class="card-function-lead">
        <span class="function-label">${t.functionLabel}</span>
        <h3 class="card-title">${functionTitle}</h3>
      </div>
      
      <div class="card-tech-meta">
        <span class="card-tech-name">📦 ${technicalRepo}</span>
        <span class="card-stars">⭐ ${starsFormatted}</span>
      </div>

      <p class="card-desc">${item.description}</p>
      
      <div class="card-footer">
        <span class="card-creator">👤 ${item.creator || technicalRepo.split("/")[0]}</span>
        <a href="${item.url}" target="_blank" rel="noopener noreferrer" class="card-btn">${t.openGithub}</a>
      </div>
    </div>
  `;

  // Hover video auto-play & pause logic for silky smooth performance
  if (hasMp4) {
    const videoEl = card.querySelector(".card-video");
    const posterEl = card.querySelector(".card-poster-fallback");

    card.addEventListener("mouseenter", () => {
      if (videoEl) {
        videoEl.style.opacity = "1";
        if (posterEl) posterEl.style.opacity = "0";
        videoEl.play().catch(() => {});
      }
    });

    card.addEventListener("mouseleave", () => {
      if (videoEl) {
        videoEl.pause();
        videoEl.currentTime = 0;
        videoEl.style.opacity = "0";
        if (posterEl) posterEl.style.opacity = "1";
      }
    });
  }

  return card;
}

// Open Detail / Video Preview Modal
function openDetailModal(item) {
  const t = I18N[currentLang];
  const functionTitle = getItemFunctionTitle(item);
  modalTitle.textContent = functionTitle;
  modalCategory.textContent = getCategoryName(item.main_category);
  modalSubCategory.textContent = item.sub_category;
  modalStars.textContent = `⭐ ${(item.stars || 0).toLocaleString()}`;
  modalCreator.innerHTML = `${t.modalTechnicalRepo} <strong>${item.repo_name}</strong> | ${t.modalAuthor} <strong>${item.creator || item.repo_name.split("/")[0]}</strong>`;
  modalDesc.textContent = item.description;
  modalGithubLink.href = item.url;
  modalGithubLink.querySelector("span").textContent = t.modalOpenGithub;
  copyUrlBtn.textContent = t.modalCopyLink;

  // Media preview
  modalMediaContainer.innerHTML = "";
  if (item.has_video && item.video_demo && item.video_demo.endsWith(".mp4")) {
    const video = document.createElement("video");
    video.src = item.video_demo;
    video.controls = true;
    video.autoplay = true;
    video.loop = true;
    video.playsInline = true;
    modalMediaContainer.appendChild(video);
  } else {
    const img = document.createElement("img");
    img.src = item.video_demo || item.thumbnail_url || `https://opengraph.githubassets.com/1/${item.repo_name}`;
    img.alt = item.title;
    modalMediaContainer.appendChild(img);
  }

  // Tags
  modalTags.innerHTML = "";
  (item.tags || []).forEach(tag => {
    const pill = document.createElement("span");
    pill.className = "tag-pill";
    pill.textContent = `#${tag}`;
    modalTags.appendChild(pill);
  });

  // Copy link
  copyUrlBtn.onclick = () => {
    navigator.clipboard.writeText(item.url);
    copyUrlBtn.textContent = t.modalCopied;
    setTimeout(() => { copyUrlBtn.textContent = t.modalCopyLink; }, 1800);
  };

  detailModal.classList.add("active");
  document.body.style.overflow = "hidden";
}

// Close Modals
function closeModal() {
  detailModal.classList.remove("active");
  submitModal.classList.remove("active");
  modalMediaContainer.innerHTML = "";
  document.body.style.overflow = "";
}

// Event Listeners Setup
function setupEventListeners() {
  // Language switcher buttons
  langEnBtn.addEventListener("click", () => setLanguage("en"));
  langHuBtn.addEventListener("click", () => setLanguage("hu"));

  // Search input
  searchInput.addEventListener("input", (e) => {
    searchQuery = e.target.value;
    renderItems();
  });

  // Keyboard shortcut '/' to focus search
  window.addEventListener("keydown", (e) => {
    if (e.key === "/" && document.activeElement !== searchInput) {
      e.preventDefault();
      searchInput.focus();
    }
    if (e.key === "Escape") {
      closeModal();
    }
  });

  // Toggle Video Only
  onlyVideoBtn.addEventListener("click", () => {
    onlyVideosFilter = !onlyVideosFilter;
    onlyVideoBtn.classList.toggle("active", onlyVideosFilter);
    renderItems();
  });

  // Toggle Hidden Gems
  hiddenGemsBtn.addEventListener("click", () => {
    onlyGemsFilter = !onlyGemsFilter;
    hiddenGemsBtn.classList.toggle("active", onlyGemsFilter);
    renderItems();
  });

  // Sort change
  sortSelect.addEventListener("change", (e) => {
    currentSort = e.target.value;
    renderItems();
  });

  // View Switchers
  viewGridBtn.addEventListener("click", () => {
    currentViewMode = "grid";
    viewGridBtn.classList.add("active");
    viewShelfBtn.classList.remove("active");
    renderItems();
  });

  viewShelfBtn.addEventListener("click", () => {
    currentViewMode = "shelf";
    viewShelfBtn.classList.add("active");
    viewGridBtn.classList.remove("active");
    renderItems();
  });

  // Modal close events
  modalCloseBtn.addEventListener("click", closeModal);
  detailModal.addEventListener("click", (e) => {
    if (e.target === detailModal) closeModal();
  });

  // Creator Standard Badge copy button
  const showBadgeGuideBtn = document.getElementById("showBadgeGuideBtn");
  if (showBadgeGuideBtn) {
    showBadgeGuideBtn.addEventListener("click", () => {
      const t = I18N[currentLang];
      const badgeCode = `[![NexusHub 15s Demo](https://img.shields.io/badge/NexusHub-15s_Demo_Verified-ec4899?style=for-the-badge&logo=youtube)](http://localhost:8765)`;
      navigator.clipboard.writeText(badgeCode);
      showBadgeGuideBtn.textContent = t.standardCopied;
      setTimeout(() => {
        showBadgeGuideBtn.textContent = t.standardBtn;
      }, 2000);
    });
  }

  // Submit Modal Open & Close
  submitRepoBtn.addEventListener("click", () => {
    submitModal.classList.add("active");
    document.body.style.overflow = "hidden";
  });
  submitModalCloseBtn.addEventListener("click", closeModal);
  submitModal.addEventListener("click", (e) => {
    if (e.target === submitModal) closeModal();
  });

  // Handle Form Submission for 0-Star Projects
  submitForm.addEventListener("submit", async (e) => {
    e.preventDefault();
    const t = I18N[currentLang];
    const repoUrl = document.getElementById("submitRepoUrl").value.trim();
    const title = document.getElementById("submitTitle").value.trim();
    const category = document.getElementById("submitCategory").value;
    const demoUrl = document.getElementById("submitDemoUrl").value.trim();
    const desc = document.getElementById("submitDesc").value.trim();

    let repoName = repoUrl.replace("https://github.com/", "").replace(/\/$/, "");
    if (!repoName.includes("/")) repoName = `creator/${title.toLowerCase().replace(/\s+/g, "-")}`;

    const newProject = {
      id: "submitted-" + Date.now(),
      repo_name: repoName,
      title: title,
      function_title: title,
      description: desc,
      main_category: category,
      sub_category: currentLang === "en" ? "Community Discoveries" : "Közösségi Felfedezések",
      thumbnail_url: demoUrl || `https://opengraph.githubassets.com/1/${repoName}`,
      video_url: demoUrl,
      has_video: Boolean(demoUrl),
      video_demo: demoUrl,
      stars: 1,
      url: repoUrl,
      creator: repoName.split("/")[0],
      tags: ["community-submission", "hidden-gem"]
    };

    catalogueData.items.unshift(newProject);
    updateStats();
    renderItems();

    try {
      await fetch("/api/submit", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(newProject)
      });
    } catch (err) {
      console.warn("Could not save to backend:", err);
    }

    submitForm.reset();
    closeModal();
    alert(t.submitSuccessAlert);
  });
}

// Launch
init();
