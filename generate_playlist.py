#!/usr/bin/env python3
import requests
import re
import json
import datetime
import os
import shutil
import concurrent.futures
from urllib.parse import urlparse

# ==========================================
# 1. USER'S CUSTOM HARDCODED CHANNELS
# (same as before – kept unchanged)
# ==========================================
USER_CUSTOM_CHANNELS = """
#EXTINF:-1 group-title="local channels",Sana TV
https://galaxyott.live/hls/sanatv.m3u8
#EXTINF:-1 group-title="local channels",Sana Plus
https://galaxyott.live/hls/sanaplus.m3u8
... (truncated for brevity – paste your full list)
"""

# ==========================================
# 2. SOURCES & BLOCKLIST (same as before)
# ==========================================
SOURCES = [
    "https://raw.githubusercontent.com/Vmfm/tamilvmtv/main/live/channels.m3u",
    "https://raw.githubusercontent.com/Vmfm/tamilvmtv/main/live/jio.m3u",
    "https://raw.githubusercontent.com/Tamilwebcast/Tamilwebcast.github.io/main/TWCIPTV.m3u",
    "https://raw.githubusercontent.com/PraveenBojja83/praveentv/main/resource/channels.json",
    "https://raw.githubusercontent.com/Indiblog/india-iptv/main/output/india_iptv.m3u",
    "https://raw.githubusercontent.com/Indiblog/india-iptv/main/output/india_general.m3u",
    "https://raw.githubusercontent.com/amazeyourself/m3u/main/jtv.m3u",
    "https://raw.githubusercontent.com/amazeyourself/m3u/main/pishow.m3u",
    "https://raw.githubusercontent.com/amazeyourself/m3u/main/yupptvfast.m3u",
    "https://raw.githubusercontent.com/amazeyourself/m3u/main/tangotv.m3u",
    "https://raw.githubusercontent.com/amazeyourself/m3u/main/ashokadigital.m3u",
    "https://raw.githubusercontent.com/amazeyourself/m3u/main/neotv.m3u",
    "https://raw.githubusercontent.com/amazeyourself/tamil-local-iptv/refs/heads/main/channels.m3u",
    "https://iptv-org.github.io/iptv/languages/tam.m3u",
    "https://iptv-org.github.io/iptv/languages/eng.m3u"
]

LOCAL_SOURCES = [
    "https://raw.githubusercontent.com/Vmfm/tamilvmtv/main/live/channels.m3u",
    "https://raw.githubusercontent.com/amazeyourself/m3u/main/ashokadigital.m3u",
    "https://raw.githubusercontent.com/amazeyourself/tamil-local-iptv/refs/heads/main/channels.m3u"
]

BLOCKED_KEYWORDS = [
    "hindi", "telugu", "malayalam", "kannada", "marathi", "bengali", "bangla",
    "gujarati", "punjabi", "odia", "assamese", "urdu", "bhojpuri",
    "spanish", "french", "german", "italian", "portuguese", "russian",
    "chinese", "japanese", "korean", "arabic", "indonesian", "nepali"
]

# ==========================================
# 3. ENHANCED CATEGORY MAPPING (more keywords)
# ==========================================
CATEGORY_ORDER = [
    "Tamil GEC", "Tamil Movies", "Tamil News", "Tamil Comedy",
    "Tamil Music", "Tamil Infotainment", "Tamil Spiritual", "Tamil Kids",
    "English GEC", "English Movies", "English National News",
    "English International News", "English Business News", "English Infotainment",
    "English Lifestyle", "English Kids", "Sports",
    "local channels", "Tamil Local Channels", "tamil iptv channels"
]

CATEGORIES_MAP = {
    "Tamil GEC": {
        "Sun TV": ["sun tv", "suntv"], "Star Vijay": ["star vijay", "vijay tv"],
        "Zee Tamil": ["zee tamil", "zeetamil"], "Colors Tamil": ["colors tamil"],
        "Kalaignar TV": ["kalaignar tv", "kalaignar"], "Jaya TV": ["jaya tv"],
        "Raj TV": ["raj tv"], "Polimer TV": ["polimer tv"],
        "Makkal TV": ["makkal tv", "makkal"], "Vasanth TV": ["vasanth tv", "vasanth"],
        "Puthuyugam TV": ["puthuyugam tv", "puthuyugam"], "Mega TV": ["mega tv"],
        "Captain TV": ["captain tv"], "Vendhar TV": ["vendhar tv", "vendhar"]
    },
    "Tamil Movies": {
        "KTV": ["ktv"], "Star Vijay Super": ["star vijay super", "vijay super"],
        "Zee Thirai": ["zee thirai"], "J Movie": ["j movie", "jaya movie"],
        "Raj Digital Plus": ["raj digital plus"], "Murasu": ["murasu"],
        "Mega 24": ["mega 24"], "Sun Action": ["sun action"],
        "Tamil Movies": ["tamil movies", "tamil movie"]
    },
    "Tamil News": {
        "Sun News": ["sun news"], "Puthiya Thalaimurai": ["puthiya thalaimurai"],
        "Thanthi TV": ["thanthi tv", "thanthi"], "News18 Tamil Nadu": ["news18 tamil", "news 18 tamil"],
        "Polimer News": ["polimer news"], "News7 Tamil": ["news7 tamil", "news 7 tamil", "news 7"],
        "Sathiyam TV": ["sathiyam tv", "sathiyam"], "News J": ["news j", "newsj"],
        "Jaya Plus": ["jaya plus"], "Kalaignar Seithigal": ["kalaignar seithigal"],
        "Raj News Tamil": ["raj news tamil", "raj news"], "Captain News": ["captain news"]
    },
    "Tamil Comedy": {
        "Adithya TV": ["adithya tv", "adithya"], "Sirippoli": ["sirippoli"]
    },
    "Tamil Music": {
        "Sun Music": ["sun music"], "Star Vijay Music": ["star vijay music", "vijay music"],
        "Isaiaruvi": ["isaiaruvi", "isai aruvi"], "Jaya Max": ["jaya max"],
        "Raj Musix Tamil": ["raj musix tamil", "raj musix"], "Mega Musiq": ["mega musiq", "mega music"]
    },
    "Tamil Infotainment": {
        "Sun Life": ["sun life"], "Discovery Tamil": ["discovery tamil", "discovery channel tamil"],
        "Nat Geo Tamil": ["nat geo tamil", "national geographic tamil"],
        "Sony BBC Earth Tamil": ["sony bbc earth tamil", "bbc earth tamil"]
    },
    "Tamil Spiritual": {
        "Madha TV": ["madha tv"], "Angel TV": ["angel tv"],
        "Nambikkai TV": ["nambikkai tv", "nambikkai"], "Vaanavil": ["vaanavil"],
        "Jothi TV": ["jothi tv"], "Velicham TV": ["velicham tv"],
        "Sri Sankara TV": ["sri sankara tv", "sankara tv", "sri sankara"]
    },
    "Tamil Kids": {
        "Chutti TV": ["chutti tv"], "ETV Bal Bharat Tamil": ["etv bal bharat tamil", "bal bharat tamil"],
        "Cartoon Network Tamil": ["cartoon network tamil", "cn tamil"], "Pogo Tamil": ["pogo tamil"],
        "Discovery Kids Tamil": ["discovery kids tamil"], "Sony Yay Tamil": ["sony yay tamil"],
        "Nick Tamil": ["nick tamil", "nickelodeon tamil"], "Disney Channel Tamil": ["disney channel tamil", "disney tamil"],
        "Kochu TV": ["kochu tv"]
    },
    "English GEC": {
        "Zee Cafe": ["zee cafe"], "Colors Infinity": ["colors infinity"],
        "Comedy Central": ["comedy central"], "Disney International HD": ["disney international"]
    },
    "English Movies": {
        "Star Movies Select": ["star movies select"], "Star Movies": ["star movies"],
        "Sony PIX": ["sony pix"], "Movies Now": ["movies now"], "MNX": ["mnx"], "MN+": ["mn+"],
        "&flix": ["&flix", "andflix"], "&prive HD": ["&prive hd", "&prive", "andprive"],
        "Romedy Now": ["romedy now"], "HBO": ["hbo"], "WB": ["wb"]
    },
    "English National News": {
        "Times Now": ["times now"], "Republic TV": ["republic tv"],
        "CNN-News18": ["cnn-news18", "cnn news18"], "India Today": ["india today"],
        "NDTV 24x7": ["ndtv 24x7"], "NewsX": ["newsx"],
        "Mirror Now": ["mirror now"], "WION": ["wion"]
    },
    "English International News": {
        "BBC News": ["bbc news"], "CNN International": ["cnn international", "cnn"],
        "Al Jazeera English": ["al jazeera english", "al jazeera"],
        "RT (Russia Today)": ["rt russia today", "russia today", "rt news"]
    },
    "English Business News": {
        "CNBC-TV18": ["cnbc-tv18", "cnbc tv18"], "ET Now": ["et now"],
        "NDTV Profit": ["ndtv profit"]
    },
    "English Infotainment": {
        "Discovery Channel": ["discovery channel", "discovery"], "National Geographic": ["national geographic", "nat geo"],
        "History TV18": ["history tv18", "history"], "Animal Planet": ["animal planet"],
        "Sony BBC Earth": ["sony bbc earth", "bbc earth"]
    },
    "English Lifestyle": {
        "TLC": ["tlc"], "Travelxp": ["travelxp"], "Goodtimes": ["goodtimes"]
    },
    "English Kids": {
        "Cartoon Network": ["cartoon network"], "Nickelodeon": ["nickelodeon", "nick"],
        "Pogo": ["pogo"], "Disney Channel": ["disney channel"], "Disney Junior": ["disney junior"],
        "Sonic": ["sonic"], "Super Hungama": ["super hungama"], "Discovery Kids": ["discovery kids"],
        "BabyTV": ["babytv"]
    },
    "Sports": {
        "Star Sports 1 Tamil": ["star sports 1 tamil", "star sports tamil"],
        "Star Sports 1": ["star sports 1"], "Star Sports 2": ["star sports 2"],
        "Star Sports Select 1": ["star sports select 1"], "Star Sports Select 2": ["star sports select 2"],
        "Sony Sports Ten 1": ["sony sports ten 1", "sony ten 1"],
        "Sony Sports Ten 2": ["sony sports ten 2", "sony ten 2"],
        "Sony Sports Ten 5": ["sony sports ten 5", "sony ten 5"],
        "Eurosport": ["eurosport"], "Sports18 - 1": ["sports18 - 1", "sports18", "sports 18"]
    }
}

# Build flat list sorted by keyword length (longest first)
FLAT_CATEGORIES = []
for cat, channels in CATEGORIES_MAP.items():
    for proper_name, keywords in channels.items():
        for kw in keywords:
            FLAT_CATEGORIES.append((len(kw), kw, proper_name, cat))
FLAT_CATEGORIES.sort(reverse=True, key=lambda x: x[0])

# ==========================================
# 4. HELPER FUNCTIONS (enhanced)
# ==========================================

def clean_name(name):
    """Remove tags, brackets, resolution markers, and extra whitespace."""
    # Remove [..] and (..)
    name = re.sub(r'\s*\[.*?\]\s*', '', name)
    name = re.sub(r'\s*\(.*?\)\s*', '', name)
    # Remove common resolution/quality tags
    name = re.sub(r'\b(HD|SD|FHD|4K|UHD|HDR|Dolby|1080p|720p|Premium|Plus|IN|UK)\b', '', name, flags=re.I)
    # Remove extra spaces
    return ' '.join(name.split()).strip()

def is_blocked(name):
    if not name:
        return True
    n = name.lower()
    return any(lang in n for lang in BLOCKED_KEYWORDS)

def get_category_and_name(name):
    if is_blocked(name):
        return None, None
    # First, clean the name to strip resolution tags
    cleaned = clean_name(name)
    # If cleaned is empty, fallback to original
    if not cleaned:
        cleaned = name
    n = cleaned.lower()
    # Longest‑keyword match
    for _, kw, proper_name, cat in FLAT_CATEGORIES:
        if kw in n:
            return cat, proper_name
    return None, None

def parse_m3u(content):
    channels = []
    lines = content.splitlines()
    current_name, current_logo, current_cat = None, "", None
    for line in lines:
        line = line.strip()
        if line.startswith("#EXTINF:"):
            logos = re.findall(r'tvg-logo="(.*?)"', line)
            current_logo = logos[0] if logos else ""
            cats = re.findall(r'group-title="(.*?)"', line)
            current_cat = cats[0] if cats else None
            current_name = line.rsplit(',', 1)[1].strip() if ',' in line else None
        elif line and not line.startswith("#") and current_name:
            channels.append((current_name, current_logo, line, current_cat))
            current_name, current_cat = None, None
    return channels

def parse_json(content):
    channels = []
    try:
        data = json.loads(content)
        items = data if isinstance(data, list) else data.get('channels', data.get('streams', data.get('data', [])))
        for item in items:
            name = item.get('name') or item.get('title') or item.get('channel_name')
            url = item.get('url') or item.get('stream') or item.get('link') or item.get('channel_url')
            logo = item.get('logo') or item.get('icon') or item.get('stream_icon') or ""
            if name and url:
                channels.append((name, logo, url, None))
    except Exception:
        pass
    return channels

def resolve_url(url):
    """Follow redirects and return the final URL."""
    try:
        resp = requests.head(url, allow_redirects=True, timeout=5)
        return resp.url
    except:
        return url

def validate_stream(url, cat):
    """
    Enhanced validation:
    - Follow redirects and get final URL.
    - For .m3u8: download playlist, parse, check it contains valid segment URLs.
    - For others: check Content‑Type and first 1500 bytes for HTML/JSON.
    Returns (True, final_url) if valid, else (False, None).
    """
    timeout_val = 5.0 if "local" in cat.lower() else 8.0
    headers = {'User-Agent': 'VLC/3.0.9 LibVLC/3.0.9', 'Accept': '*/*'}

    try:
        # First, do a GET with stream=True and follow redirects
        resp = requests.get(url, headers=headers, timeout=timeout_val, stream=True, allow_redirects=True)
        final_url = resp.url

        if resp.status_code != 200:
            return False, None

        # Check Content‑Type
        ctype = resp.headers.get('Content-Type', '').lower()

        # If it's a .m3u8 or mpegurl, we need to parse the playlist
        if '.m3u8' in final_url.lower() or 'mpegurl' in ctype:
            # Read the whole playlist (usually small)
            content = resp.raw.read(8192).decode('utf-8', errors='ignore')
            if not content:
                return False, None
            # Look for #EXTM3U and at least one segment line
            if '#EXTM3U' not in content.upper():
                return False, None
            # Check if there's a segment URL (not just a comment)
            lines = content.splitlines()
            segment_found = False
            for line in lines:
                line = line.strip()
                if line and not line.startswith('#') and ('http' in line or line.startswith('/')):
                    # Might be a segment URL
                    segment_found = True
                    break
            if not segment_found:
                # Sometimes the playlist is a master playlist with variants; we can still accept it.
                # But if it has no segments at all, it's likely broken.
                # We'll accept if it contains #EXT-X-STREAM-INF or #EXT-X-MEDIA
                if '#EXT-X-STREAM-INF' not in content.upper() and '#EXT-X-MEDIA' not in content.upper():
                    return False, None
            # Also reject if the playlist itself contains HTML
            if '<html' in content.lower() or '<body' in content.lower():
                return False, None
            return True, final_url

        # For non‑m3u8 streams: check content type and first bytes
        if 'text/html' in ctype:
            return False, None
        if 'application/json' in ctype:
            return False, None

        # Read first 1500 bytes to check for HTML disguised as 200 OK
        chunk = resp.raw.read(1500)
        if not chunk:
            return False, None
        text_chunk = chunk.decode('utf-8', errors='ignore').lower()
        if '<html' in text_chunk or '<body' in text_chunk or '<!doctype' in text_chunk:
            return False, None
        # Also if it's empty or too small (like < 100 bytes)
        if len(chunk) < 100 and not text_chunk.startswith('#'):
            return False, None

        return True, final_url

    except Exception:
        return False, None

def process_channel(item, resolved_urls_global):
    """
    For a given proper_name and its list of URLs, test each URL.
    Returns (cat, proper_name, logo, final_url) if a valid stream is found,
    and adds the final_url to the global set to avoid duplicates.
    """
    proper_name, data = item
    cat = data['category']
    logo = data['logo']

    # We'll iterate over a copy of the URLs list
    for url in data['urls']:
        valid, final_url = validate_stream(url, cat)
        if valid:
            # Check if this final URL was already used for another channel
            if final_url in resolved_urls_global:
                # Duplicate stream – skip
                continue
            resolved_urls_global.add(final_url)
            return (cat, proper_name, logo, final_url)
    return None

# ==========================================
# 5. MAIN EXECUTION
# ==========================================
def main():
    print("Starting Ultimate Deduplication, Ordered, & Strict Validation Builder...")

    grouped_channels = {}
    seen_urls_global = set()

    # --- 1. CUSTOM CHANNELS ---
    print("\nGathering User Custom Channels...")
    custom_parsed = parse_m3u(USER_CUSTOM_CHANNELS)
    for name, logo, url, custom_cat in custom_parsed:
        url = url.strip()
        if not url.startswith("http") or url in seen_urls_global:
            continue
        seen_urls_global.add(url)
        if is_blocked(name):
            continue
        cat = custom_cat if custom_cat else "tamil iptv channels"
        proper_name = clean_name(name)
        if not proper_name:
            proper_name = name
        if proper_name not in grouped_channels:
            grouped_channels[proper_name] = {'category': cat, 'logo': logo, 'urls': []}
        grouped_channels[proper_name]['urls'].append(url)

    # --- 2. REMOTE SOURCES ---
    for src_url in SOURCES:
        print(f"Scraping: {src_url}")
        try:
            resp = requests.get(src_url, timeout=15)
            resp.raise_for_status()
            parsed = parse_json(resp.text) if src_url.endswith('.json') else parse_m3u(resp.text)
            for name, logo, url, _ in parsed:
                url = url.strip()
                if not url.startswith("http") or url in seen_urls_global:
                    continue
                seen_urls_global.add(url)
                if is_blocked(name):
                    continue
                cat, proper_name = get_category_and_name(name)
                if not cat:
                    if src_url in LOCAL_SOURCES:
                        cat = "Tamil Local Channels"
                        proper_name = clean_name(name)
                        if not proper_name:
                            proper_name = name
                    else:
                        continue
                if proper_name not in grouped_channels:
                    grouped_channels[proper_name] = {'category': cat, 'logo': logo, 'urls': []}
                grouped_channels[proper_name]['urls'].append(url)
                if not grouped_channels[proper_name]['logo'] and logo:
                    grouped_channels[proper_name]['logo'] = logo
        except Exception as e:
            print(f"  Error fetching {src_url}: {e}")

    print(f"\n-> Extracted {len(grouped_channels)} unique channels. Testing backups to find 1 working link per channel...")

    # --- 3. MULTITHREADED VALIDATION (with global resolved‑URL dedup) ---
    final_channels = {cat: [] for cat in CATEGORY_ORDER}
    resolved_urls_global = set()
    total_added = 0

    with concurrent.futures.ThreadPoolExecutor(max_workers=50) as executor:
        # Prepare list of items
        items = list(grouped_channels.items())
        future_to_item = {executor.submit(process_channel, item, resolved_urls_global): item for item in items}
        for future in concurrent.futures.as_completed(future_to_item):
            res = future.result()
            if res:
                cat, proper_name, logo, final_url = res
                if cat not in final_channels:
                    final_channels[cat] = []
                final_channels[cat].append((proper_name, logo, final_url))
                total_added += 1

    # --- 4. BACKUP & FILE GENERATION (unchanged) ---
    OUTPUT_FILE = "master_playlist.m3u"
    BACKUP_FILE = "playlist_backup.m3u"

    if total_added == 0:
        print("⚠️ No playable streams found. Restoring previous playlist.")
        if os.path.exists(BACKUP_FILE):
            shutil.copy2(BACKUP_FILE, OUTPUT_FILE)
        return

    print("\nWriting master_playlist.m3u in perfect category order...")
    with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
        f.write("#EXTM3U\n")
        f.write("#PLAYLIST:Checked by CODECS.COM M3U Checker\n")
        for cat in CATEGORY_ORDER:
            if cat in final_channels and final_channels[cat]:
                channels = final_channels[cat]
                channels.sort(key=lambda x: x[0].lower())
                f.write(f"\n# --- {cat} ---\n")
                for display_name, logo, url in channels:
                    f.write(f'#EXTINF:-1 tvg-name="{display_name}" tvg-logo="{logo}" group-title="{cat}",{display_name}\n{url}\n')
        # Catch‑all for any custom categories
        for cat in sorted(final_channels.keys()):
            if cat not in CATEGORY_ORDER and final_channels[cat]:
                channels = final_channels[cat]
                channels.sort(key=lambda x: x[0].lower())
                f.write(f"\n# --- {cat} ---\n")
                for display_name, logo, url in channels:
                    f.write(f'#EXTINF:-1 tvg-name="{display_name}" tvg-logo="{logo}" group-title="{cat}",{display_name}\n{url}\n')

    shutil.copy2(OUTPUT_FILE, BACKUP_FILE)
    print(f"\n✅ SUCCESS! Total Working Unique Channels: {total_added}")

    # README update
    timestamp = datetime.datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S UTC")
    with open("README.md", "w", encoding="utf-8") as f:
        f.write("# Tamil & English IPTV Playlist\n\n")
        f.write("This playlist is automatically checked, perfectly categorized, A-Z sorted, completely deduplicated (1 link per channel), and updated every 6 hours.\n\n")
        f.write(f"**Total LIVE Channels:** {total_added}\n**Last Updated:** {timestamp}\n\n")
        f.write("## 📥 Playlist URL\n")
        f.write("Use the **Copy button** in the top right corner of the box below. Paste it directly into your IPTV Player:\n\n")
        f.write("```text\n")
        f.write("https://raw.githubusercontent.com/nuttle-nuttterr/tv-by-deepseek/main/master_playlist.m3u\n")
        f.write("```\n\n")
        f.write("## 📊 Channel Breakdown\n| Category | Count |\n|---|---|\n")
        for cat in CATEGORY_ORDER:
            if cat in final_channels and final_channels[cat]:
                f.write(f"| {cat} | {len(final_channels[cat])} |\n")

if __name__ == "__main__":
    main()
