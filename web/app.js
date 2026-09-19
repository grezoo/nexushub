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
    vintageLabel: "📅 Vintage:",
    vintageAll: "All Years (Any)",
    vintage2025: "🚀 2025–2026 (New Wave)",
    vintage2021: "🏎️ 2021–2024 (Modern Mature)",
    vintage2015: "🏛️ 2015–2020 (Battle-Tested Classic)",
    vintageLegacy: "📼 Pre-2014 (Vintage / Legendary)",
    viewGrid: "⊞ Grid",
    viewShelves: "☰ Shelves",
    functionLabel: "FUNCTION:",
    openGithub: "Open GitHub ↗",
    demoBadge: "▶ 15s DEMO",
    gemBadge: "💎 GEM",
    originalBadge: "⭐ NEXUSHUB ORIGINAL",
    tryLiveBtn: "🚀 Try Live",
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
    standardCopied: "✅ Badge Copied!",
    sliderBadge: "✍️ NEXUSHUB CURATED PICKS",
    sliderTitle: "NexusHub Official Bookshop Showcase — Hand-Curated Open Source Gems",
    sliderCuratorLead: "✨ NexusHub Editorial Review:",
    sliderWatchDemo: "Watch Live Demo ▶",
    sliderOpenRepo: "Open GitHub ↗",
    loadMoreBtn: "⬇ Load More Projects",
    showingCount: "Showing"
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
    vintageLabel: "📅 Évjárat:",
    vintageAll: "Minden évjárat (Összes)",
    vintage2025: "🚀 2025–2026 (Új hullám)",
    vintage2021: "🏎️ 2021–2024 (Kiforrott, modern)",
    vintage2015: "🏛️ 2015–2020 (Időtlen klasszikus)",
    vintageLegacy: "📼 2014 előtt (Veterán / Oldtimer)",
    originalBadge: "⭐ NEXUSHUB SAJÁT FEJLESZTÉS",
    tryLiveBtn: "🚀 Kipróbálom",
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
    standardCopied: "✅ Jelvény Másolva!",
    sliderBadge: "✍️ A NEXUSHUB AJÁNLÁSA",
    sliderTitle: "NexusHub Könyvesbolti Kurátori Válogatás — Működő demók és rejtett kincsek",
    sliderCuratorLead: "✨ NexusHub Kurátori Indoklás:",
    sliderWatchDemo: "Demó Megtekintése ▶",
    sliderOpenRepo: "GitHub Megnyitása ↗",
    loadMoreBtn: "⬇ További Projektek Betöltése",
    showingCount: "Megjelenítve"
  }
};

const TRANSLATIONS = I18N;

// Bilingual Category Translations
const CATEGORY_TRANSLATIONS = {
  "Hardver, IoT & Elektronika": { en: "Hardware, IoT & Electronics", hu: "Hardver, IoT & Elektronika", icon: "🔌" },
  "Mesterséges Intelligencia & Adat": { en: "Artificial Intelligence & Data", hu: "Mesterséges Intelligencia & Adat", icon: "🧠" },
  "Pénzügy, Tőzsde & Kripto Elemzés": { en: "FinTech, Trading & Crypto Analytics", hu: "Pénzügy, Tőzsde & Kripto Elemzés", icon: "📈" },
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
let currentVintage = "all";
let searchQuery = "";
let currentViewMode = "grid";

// DOM Elements
const searchInput = document.getElementById("searchInput");
const onlyVideoBtn = document.getElementById("onlyVideoBtn");
const hiddenGemsBtn = document.getElementById("hiddenGemsBtn");
const submitRepoBtn = document.getElementById("submitRepoBtn");
const sortSelect = document.getElementById("sortSelect");
const sortLabel = document.getElementById("sortLabel");
const vintageSelect = document.getElementById("vintageSelect");
const vintageLabel = document.getElementById("vintageLabel");
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
  if (sortLabel) sortLabel.textContent = t.sortLabel;

  if (sortSelect && sortSelect.options.length >= 3) {
    sortSelect.options[0].textContent = t.sortGems;
    sortSelect.options[1].textContent = t.sortStars;
    sortSelect.options[2].textContent = t.sortName;
  }

  // Vintage labels
  if (vintageLabel) vintageLabel.textContent = t.vintageLabel;
  if (vintageSelect && vintageSelect.options.length >= 5) {
    vintageSelect.options[0].textContent = t.vintageAll;
    vintageSelect.options[1].textContent = t.vintage2025;
    vintageSelect.options[2].textContent = t.vintage2021;
    vintageSelect.options[3].textContent = t.vintage2015;
    vintageSelect.options[4].textContent = t.vintageLegacy;
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

  // Weekly slider headers
  const sliderBadgeText = document.getElementById("sliderBadgeText");
  if (sliderBadgeText) sliderBadgeText.textContent = t.sliderBadge;

  const sliderTitleText = document.getElementById("sliderTitleText");
  if (sliderTitleText) sliderTitleText.textContent = t.sliderTitle;

  // Re-render slider, categories and items in current language
  try {
    renderWeeklySlider();
  } catch (err) {
    console.error("Error rendering weekly slider:", err);
  }
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
  if (!item) return "";
  const huTitle = item.function_title || item.title || "";
  if (currentLang === "en") {
    return FUNCTION_TRANSLATIONS_EN[huTitle] || item.title_en || huTitle;
  }
  return huTitle;
}

// Get translated description for item
function getItemDescription(item) {
  if (!item) return "";
  if (currentLang === "en") {
    return item.description_en || item.desc_en || item.description || "";
  }
  return item.description || "";
}

// Escape HTML utility to prevent script injection or broken markup
function escapeHtml(str) {
  if (!str) return "";
  return String(str)
    .replace(/&/g, "&amp;")
    .replace(/</g, "&lt;")
    .replace(/>/g, "&gt;")
    .replace(/"/g, "&quot;")
    .replace(/'/g, "&#039;");
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

  await loadCuratedPicks();
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
  title: "NexusHub — Open Source Visual Catalogue",
  function_title: "Nyílt Forráskódú Vizuális Katalógus & Rövid Demó Kereső",
  title_en: "Visual Catalogue & Short-Demo Discovery for Open Source",
  description: "A nyílt forráskódú projektek élményalapú vizuális katalógusa. Valós működést bemutató 15-30 mp-es videós demókkal (preview.mp4 / preview.gif), funkció-központú kártyákkal és érdemalapú rangsorolással.",
  description_en: "A visual catalogue and short-demo discovery platform for open-source repositories. Featuring 15-30s real video demos (preview.mp4 / preview.gif), function-first cards, and merit-based discovery.",
  main_category: "Rendszer, Biztonság & Segédprogramok",
  sub_category: "Vizuális Katalógus & Rendszerező",
  thumbnail_url: "preview.gif",
  video_url: "preview.gif",
  has_video: true,
  video_demo: "preview.gif",
  stars: 100,
  url: "https://github.com/grezoo/nexushub",
  creator: "grezoo",
  tags: ["visual-catalogue", "open-source-discovery", "visual-cards", "hidden-gems"]
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
  currentGridLimit = 60;
  renderMainCategories();
  renderSubCategories();
  renderItems();

  setTimeout(() => {
    const activeBtn = mainCategoriesContainer.querySelector(".cat-btn.active");
    if (activeBtn) {
      activeBtn.scrollIntoView({ behavior: "smooth", block: "nearest", inline: "center" });
    }
  }, 50);
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
    currentGridLimit = 60;
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
      currentGridLimit = 60;
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

    // Vintage filtering
    if (currentVintage !== "all") {
      const y = item.year || 2024;
      if (currentVintage === "2025-2026" && y < 2025) return false;
      if (currentVintage === "2021-2024" && (y < 2021 || y > 2024)) return false;
      if (currentVintage === "2015-2020" && (y < 2015 || y > 2020)) return false;
      if (currentVintage === "legacy" && y >= 2015) return false;
    }

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

let currentGridLimit = 60;

// Render Grid View with Smart Batch Loading (Scales to 50,000+ items seamlessly)
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

  const batch = items.slice(0, currentGridLimit);
  batch.forEach(item => {
    cardsGrid.appendChild(createCardElement(item));
  });

  if (items.length > currentGridLimit) {
    const loadMoreWrapper = document.createElement("div");
    loadMoreWrapper.className = "load-more-wrapper";
    loadMoreWrapper.style.cssText = "grid-column: 1 / -1; display: flex; flex-direction: column; align-items: center; justify-content: center; padding: 40px 0 20px;";

    const info = document.createElement("p");
    info.style.cssText = "font-size: 13px; color: var(--text-dim); margin-bottom: 14px; font-weight: 500;";
    info.textContent = `${t.showingCount}: ${batch.length} / ${items.length} ${t.projectsFound}`;

    const btn = document.createElement("button");
    btn.className = "btn btn-primary";
    btn.style.cssText = "padding: 12px 36px; font-size: 14px; font-weight: 700; border-radius: 9999px; cursor: pointer; box-shadow: 0 4px 20px rgba(168, 85, 247, 0.35); transition: transform 0.2s ease;";
    btn.textContent = `${t.loadMoreBtn} (+60)`;
    btn.onclick = () => {
      currentGridLimit += 60;
      renderGridView(items);
    };

    loadMoreWrapper.appendChild(info);
    loadMoreWrapper.appendChild(btn);
    cardsGrid.appendChild(loadMoreWrapper);
  }
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

  // Direct moving video or image markup
  let mediaMarkup = "";
  const hasMp4 = item.has_video && item.video_demo && item.video_demo.endsWith(".mp4");
  const isGif = item.video_demo && (item.video_demo.endsWith(".gif") || item.video_demo.includes("giphy.com"));

  if (hasMp4) {
    mediaMarkup = `
      <video class="card-video" src="${item.video_demo}" autoplay muted loop playsinline poster="${thumbUrl}"></video>
      <img src="${thumbUrl}" alt="${functionTitle}" class="card-img card-poster-fallback" loading="lazy" onerror="this.onerror=null; this.src='https://opengraph.githubassets.com/1/${item.repo_name}'">
    `;
  } else if (isGif || (item.thumbnail_url && item.thumbnail_url.endsWith(".gif"))) {
    const gifSrc = item.video_demo && item.video_demo.endsWith(".gif") ? item.video_demo : item.thumbnail_url;
    mediaMarkup = `
      <img src="${gifSrc}" alt="${functionTitle}" class="card-img card-moving-media" loading="eager" onerror="this.onerror=null; this.src='${thumbUrl}'">
    `;
  } else {
    mediaMarkup = `
      <img src="${thumbUrl}" alt="${functionTitle}" class="card-img" loading="lazy" onerror="this.onerror=null; this.src='https://opengraph.githubassets.com/1/${item.repo_name}'">
    `;
  }

  const pinnedBadge = currentLang === "en" ? "📌 PINNED SHOWCASE" : "📌 HIVATALOS MINTA";

  const isOriginal = item.is_pinned || (item.repo_name && item.repo_name.includes("nexushub"));
  const isVintageLegacy = (item.year || 2024) < 2015;

  card.innerHTML = `
    <div class="card-media">
      ${mediaMarkup}
      <div class="card-media-overlay"></div>
      ${isOriginal ? `<div class="badge-pinned">${t.originalBadge}</div>` : ''}
      ${isGem ? `<div class="badge-gem">${t.gemBadge}</div>` : ''}
      ${isVintageLegacy ? `<div class="badge-vintage">📼 ${item.year}</div>` : ''}
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
        <span class="card-year">📅 ${item.year || 2024}</span>
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
    currentGridLimit = 60;
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
    currentGridLimit = 60;
    renderItems();
  });

  // Toggle Hidden Gems
  hiddenGemsBtn.addEventListener("click", () => {
    onlyGemsFilter = !onlyGemsFilter;
    hiddenGemsBtn.classList.toggle("active", onlyGemsFilter);
    currentGridLimit = 60;
    renderItems();
  });

  // Sort change
  sortSelect.addEventListener("change", (e) => {
    currentSort = e.target.value;
    currentGridLimit = 60;
    renderItems();
  });

  // Vintage change
  if (vintageSelect) {
    vintageSelect.addEventListener("change", (e) => {
      currentVintage = e.target.value;
      currentGridLimit = 60;
      renderItems();
    });
  }

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

  // Category sliding strip buttons & wheel event handlers
  const catNavPrevBtn = document.getElementById("catNavPrevBtn");
  const catNavNextBtn = document.getElementById("catNavNextBtn");
  if (catNavPrevBtn && catNavNextBtn && mainCategoriesContainer) {
    catNavPrevBtn.addEventListener("click", () => {
      mainCategoriesContainer.scrollBy({ left: -240, behavior: "smooth" });
    });
    catNavNextBtn.addEventListener("click", () => {
      mainCategoriesContainer.scrollBy({ left: 240, behavior: "smooth" });
    });
    mainCategoriesContainer.addEventListener("wheel", (e) => {
      if (e.deltaY !== 0) {
        e.preventDefault();
        mainCategoriesContainer.scrollLeft += e.deltaY;
      }
    }, { passive: false });
  }

  // Subcategory sliding strip buttons & wheel event handlers
  const subNavPrevBtn = document.getElementById("subNavPrevBtn");
  const subNavNextBtn = document.getElementById("subNavNextBtn");
  if (subNavPrevBtn && subNavNextBtn && subCategoriesContainer) {
    subNavPrevBtn.addEventListener("click", () => {
      subCategoriesContainer.scrollBy({ left: -200, behavior: "smooth" });
    });
    subNavNextBtn.addEventListener("click", () => {
      subCategoriesContainer.scrollBy({ left: 200, behavior: "smooth" });
    });
    subCategoriesContainer.addEventListener("wheel", (e) => {
      if (e.deltaY !== 0) {
        e.preventDefault();
        subCategoriesContainer.scrollLeft += e.deltaY;
      }
    }, { passive: false });
  }

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
      const badgeCode = `[![NexusHub 15s Demo](https://img.shields.io/badge/NexusHub-15s_Demo_Verified-ec4899?style=for-the-badge&logo=youtube)](https://gitcatalog.onrender.com)`;
      navigator.clipboard.writeText(badgeCode);
      showBadgeGuideBtn.textContent = t.standardCopied;
      setTimeout(() => {
        showBadgeGuideBtn.textContent = t.standardBtn;
      }, 2000);
    });
  }

  // Submit Modal Open & Close with Anti-Bot Time Trap
  let submitModalOpenedAt = 0;

  submitRepoBtn.addEventListener("click", () => {
    submitModalOpenedAt = Date.now();
    const statusMsg = document.getElementById("submitStatusMsg");
    if (statusMsg) statusMsg.style.display = "none";
    submitModal.classList.add("active");
    document.body.style.overflow = "hidden";
  });
  submitModalCloseBtn.addEventListener("click", closeModal);
  submitModal.addEventListener("click", (e) => {
    if (e.target === submitModal) closeModal();
  });

  // Handle Quality-Gated Form Submission with Anti-Spam
  submitForm.addEventListener("submit", async (e) => {
    e.preventDefault();
    const t = I18N[currentLang];
    const repoUrl = document.getElementById("submitRepoUrl").value.trim();
    const title = document.getElementById("submitTitle").value.trim();
    const category = document.getElementById("submitCategory").value;
    const demoUrl = document.getElementById("submitDemoUrl").value.trim();
    const desc = document.getElementById("submitDesc").value.trim();
    const hp = document.getElementById("submitHoneypot") ? document.getElementById("submitHoneypot").value : "";
    const statusMsg = document.getElementById("submitStatusMsg");
    const btn = document.getElementById("submitBtnMain") || submitForm.querySelector("button[type='submit']");

    const elapsedSec = (Date.now() - submitModalOpenedAt) / 1000;

    // UI Loading state
    if (btn) {
      btn.disabled = true;
      btn.textContent = currentLang === "en" ? "⏳ Running Quality Gate..." : "⏳ Minőségellenőrzés folyamatban...";
    }
    if (statusMsg) {
      statusMsg.style.display = "block";
      statusMsg.style.background = "rgba(168, 85, 247, 0.15)";
      statusMsg.style.border = "1px solid rgba(168, 85, 247, 0.4)";
      statusMsg.style.color = "#c084fc";
      statusMsg.textContent = currentLang === "en"
        ? "Verifying repository existence, public README, and media integrity on GitHub..."
        : "GitHub repó létezésének, publikus README fájljának és médiájának ellenőrzése...";
    }

    const payload = {
      url: repoUrl,
      title: title,
      main_category: category,
      video_demo: demoUrl,
      description: desc,
      website_hp: hp,
      client_elapsed_sec: elapsedSec
    };

    try {
      const res = await fetch("/api/submit", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(payload)
      });
      const data = await res.json();

      if (res.status !== 200 || data.status === "error") {
        if (statusMsg) {
          statusMsg.style.background = "rgba(239, 68, 68, 0.15)";
          statusMsg.style.border = "1px solid rgba(239, 68, 68, 0.4)";
          statusMsg.style.color = "#f87171";
          statusMsg.innerHTML = `❌ <strong>${currentLang === "en" ? "Submission Rejected:" : "Minőségellenőrzés sikertelen:"}</strong> ${escapeHtml(data.error || "Hiba történt.")}`;
        }
        if (btn) {
          btn.disabled = false;
          btn.textContent = currentLang === "en" ? "🚀 Verify & Publish" : "🚀 Minőségellenőrzés & Közzététel";
        }
        return;
      }

      // Success
      if (statusMsg) {
        statusMsg.style.background = "rgba(34, 197, 94, 0.15)";
        statusMsg.style.border = "1px solid rgba(34, 197, 94, 0.4)";
        statusMsg.style.color = "#4ade80";
        statusMsg.innerHTML = `✅ <strong>${currentLang === "en" ? "Quality Verified!" : "Minőségellenőrzés sikeres!"}</strong> ${data.message || ""}`;
      }

      if (data.item) {
        catalogueData.items.unshift(data.item);
        updateStats();
        currentGridLimit = 60;
        renderItems();
      }

      setTimeout(() => {
        submitForm.reset();
        if (statusMsg) statusMsg.style.display = "none";
        if (btn) {
          btn.disabled = false;
          btn.textContent = currentLang === "en" ? "🚀 Verify & Publish" : "🚀 Minőségellenőrzés & Közzététel";
        }
        closeModal();
      }, 1800);

    } catch (err) {
      if (statusMsg) {
        statusMsg.style.background = "rgba(239, 68, 68, 0.15)";
        statusMsg.style.border = "1px solid rgba(239, 68, 68, 0.4)";
        statusMsg.style.color = "#f87171";
        statusMsg.innerHTML = `❌ Hálózati hiba: ${escapeHtml(String(err))}`;
      }
      if (btn) {
        btn.disabled = false;
        btn.textContent = currentLang === "en" ? "🚀 Verify & Publish" : "🚀 Minőségellenőrzés & Közzététel";
      }
    }
  });

  // Initialize weekly top slider events
  setupWeeklySliderEvents();
}

// ==========================================
// WEEKLY TOP SLIDER LOGIC
// ==========================================
let currentSlideIndex = 0;
let sliderAutoplayTimer = null;
let curatedPicksData = null;

async function loadCuratedPicks() {
  try {
    const res = await fetch("/api/curated");
    curatedPicksData = await res.json();
  } catch (err) {
    try {
      const res = await fetch("../data/curated_picks.json");
      curatedPicksData = await res.json();
    } catch (e) {
      console.warn("Could not load curated picks:", e);
    }
  }
}

function getWeeklyTopItems() {
  if (curatedPicksData && curatedPicksData.picks && curatedPicksData.picks.length > 0) {
    return curatedPicksData.picks;
  }

  const topPicks = [
    {
      ...PINNED_SHOWCASE_ITEM,
      badge_hu: "👑 #1 A SZERZŐ KÖNYVESBOLTI AJÁNLÁSA",
      badge_en: "👑 #1 AUTHOR'S FLAGSHIP PICK (GREZOO)",
      curator_note_hu: "A vizuális nyílt forráskód forradalma: kódnevek helyett működő 15-30 mp-es demókkal, funkció-címekkel és rejtett kincsekkel.",
      curator_note_en: "The visual revolution of open source: replacing code-centric browsing with dynamic 15-30s demos and merit-first discovery."
    }
  ];

  if (catalogueData && catalogueData.items) {
    const drone = catalogueData.items.find(i => i.repo_name && i.repo_name.includes("esp32-wifi-drone"));
    if (drone) {
      topPicks.push({
        ...drone,
        badge_hu: "✍️ SZERZŐI AJÁNLÁS: HARDVER KINCS",
        badge_en: "✍️ AUTHOR'S PICK: HARDWARE GEM",
        curator_note_hu: "Mérnöki remekmű apró mikrovezérlőn: valódi repülési fizika és okostelefonos távirányítás kódolás nélkül.",
        curator_note_en: "A triumph of hardware engineering: full flight mechanics on a tiny ESP32 chip controlled via mobile browser."
      });
    }

    const aiVideo = catalogueData.items.find(i => (i.tags && i.tags.includes("sadtalker")) || (i.repo_name && i.repo_name.includes("SadTalker")));
    if (aiVideo) {
      topPicks.push({
        ...aiVideo,
        badge_hu: "✍️ SZERZŐI AJÁNLÁS: GENERATÍV AI",
        badge_en: "✍️ AUTHOR'S PICK: CREATIVE AI",
        curator_note_hu: "Bármilyen állóképből és hangból másodpercek alatt beszélő videót készít közvetlenül böngészőből.",
        curator_note_en: "Transforms static portraits into lifelike speaking characters using voice files in seconds."
      });
    }

    const demucs = catalogueData.items.find(i => i.repo_name && i.repo_name.includes("demucs"));
    if (demucs) {
      topPicks.push({
        ...demucs,
        badge_hu: "✍️ SZERZŐI AJÁNLÁS: HANG & ZENE",
        badge_en: "✍️ AUTHOR'S PICK: AUDIO TECH",
        curator_note_hu: "Professzionális sávbontó stúdió: izolálja a hangsávokat (ének, dob, gitár) bármely dalból.",
        curator_note_en: "Studio-grade stem separation that isolates vocals, drums, and instruments with AI precision."
      });
    }
  }

  return topPicks;
}

function renderWeeklySlider() {
  const track = document.getElementById("sliderTrack");
  const indicators = document.getElementById("sliderIndicators");
  if (!track || !indicators) return;

  const items = getWeeklyTopItems();
  const t = I18N[currentLang];

  track.innerHTML = items.map((item, idx) => {
    const title = getItemFunctionTitle(item);
    const desc = getItemDescription(item);
    const catName = getCategoryName(item.main_category);
    const rankLabel = currentLang === "en" ? (item.badge_en || item.rank_label_en || `#${idx + 1} AUTHOR'S PICK`) : (item.badge_hu || item.rank_label_hu || `#${idx + 1} SZERZŐI AJÁNLÁS`);
    const curatorNote = currentLang === "en" ? (item.curator_note_en || desc) : (item.curator_note_hu || desc);
    const mediaSrc = item.thumbnail_url || `https://opengraph.githubassets.com/1/${item.repo_name}`;
    const hasMp4 = item.has_video && item.video_demo && item.video_demo.endsWith(".mp4");
    const isGif = (item.video_demo && item.video_demo.endsWith(".gif")) || (item.thumbnail_url && item.thumbnail_url.endsWith(".gif"));

    let sliderMediaMarkup = "";
    if (hasMp4) {
      sliderMediaMarkup = `<video class="slide-media" src="${item.video_demo}" autoplay muted loop playsinline poster="${mediaSrc}"></video>`;
    } else if (isGif) {
      const gifSrc = item.video_demo && item.video_demo.endsWith(".gif") ? item.video_demo : item.thumbnail_url;
      sliderMediaMarkup = `<img src="${gifSrc}" alt="${escapeHtml(title)}" class="slide-media" loading="eager" />`;
    } else {
      sliderMediaMarkup = `<img src="${mediaSrc}" alt="${escapeHtml(title)}" class="slide-media" loading="lazy" />`;
    }

    return `
      <div class="slider-slide" data-slide-index="${idx}">
        <div class="slide-media-wrapper" onclick="openDetailModalById('${item.id || item.repo_name}')">
          ${sliderMediaMarkup}
          <div class="slide-play-overlay">
            <div class="slide-play-btn">▶</div>
          </div>
        </div>
        <div class="slide-content">
          <div class="slide-meta-row">
            <span class="slide-rank-badge">${rankLabel}</span>
            <span class="slide-category-badge">${escapeHtml(catName)}</span>
            ${item.has_video ? `<span class="slide-gem-badge">${t.demoBadge}</span>` : ""}
            ${item.stars <= 100 ? `<span class="slide-gem-badge">${t.gemBadge}</span>` : ""}
          </div>
          <h3 class="slide-title">${escapeHtml(title)}</h3>
          <div class="slide-repo-author">
            📦 <strong>${escapeHtml(item.repo_name)}</strong> • ${t.modalAuthor} ${escapeHtml(item.creator || "grezoo")}
          </div>

          <!-- Bookshop-style Author's Curator Recommendation Box -->
          <div class="slide-curator-box">
            <div class="curator-box-header">
              <span class="curator-seal">🎖️</span>
              <span class="curator-header-title">${t.sliderCuratorLead}</span>
            </div>
            <p class="curator-note-text">„${escapeHtml(curatorNote)}”</p>
          </div>

          <div class="slide-actions">
            <button class="btn btn-primary" onclick="openDetailModalById('${item.id || item.repo_name}')">
              ${t.sliderWatchDemo}
            </button>
            <a href="${item.url}" target="_blank" rel="noopener noreferrer" class="btn btn-secondary">
              ${t.sliderOpenRepo}
            </a>
          </div>
        </div>
      </div>
    `;
  }).join("");

  indicators.innerHTML = items.map((_, idx) => `
    <button class="slider-dot ${idx === currentSlideIndex ? 'active' : ''}" data-index="${idx}" aria-label="Slide ${idx + 1}"></button>
  `).join("");

  goToSlide(currentSlideIndex, false);
}

function goToSlide(index, animate = true) {
  const track = document.getElementById("sliderTrack");
  const dots = document.querySelectorAll(".slider-dot");
  const items = getWeeklyTopItems();
  if (!track || items.length === 0) return;

  if (index < 0) {
    currentSlideIndex = items.length - 1;
  } else if (index >= items.length) {
    currentSlideIndex = 0;
  } else {
    currentSlideIndex = index;
  }

  track.style.transition = animate ? "transform 0.45s cubic-bezier(0.25, 1, 0.5, 1)" : "none";
  track.style.transform = `translateX(-${currentSlideIndex * 100}%)`;

  dots.forEach((dot, idx) => {
    dot.classList.toggle("active", idx === currentSlideIndex);
  });
}

function setupWeeklySliderEvents() {
  const prevBtn = document.getElementById("sliderPrevBtn");
  const nextBtn = document.getElementById("sliderNextBtn");
  const trackContainer = document.getElementById("sliderTrackContainer");
  const indicators = document.getElementById("sliderIndicators");

  if (prevBtn) {
    prevBtn.addEventListener("click", () => {
      goToSlide(currentSlideIndex - 1);
      restartAutoplay();
    });
  }

  if (nextBtn) {
    nextBtn.addEventListener("click", () => {
      goToSlide(currentSlideIndex + 1);
      restartAutoplay();
    });
  }

  if (indicators) {
    indicators.addEventListener("click", (e) => {
      if (e.target.classList.contains("slider-dot")) {
        const idx = parseInt(e.target.dataset.index, 10);
        goToSlide(idx);
        restartAutoplay();
      }
    });
  }

  // Pause on hover
  if (trackContainer) {
    trackContainer.addEventListener("mouseenter", () => clearInterval(sliderAutoplayTimer));
    trackContainer.addEventListener("mouseleave", () => startAutoplay());
  }

  startAutoplay();
}

function startAutoplay() {
  clearInterval(sliderAutoplayTimer);
  sliderAutoplayTimer = setInterval(() => {
    goToSlide(currentSlideIndex + 1);
  }, 7000);
}

function restartAutoplay() {
  startAutoplay();
}

// Helper to open modal from slider item
window.openDetailModalById = function(idOrRepo) {
  const items = getWeeklyTopItems();
  let found = items.find(i => i.id === idOrRepo || i.repo_name === idOrRepo);
  if (!found && catalogueData && catalogueData.items) {
    found = catalogueData.items.find(i => i.id === idOrRepo || i.repo_name === idOrRepo);
  }
  if (found) {
    openDetailModal(found);
  }
};

// Launch
init();
