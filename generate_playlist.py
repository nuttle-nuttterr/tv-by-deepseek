#!/usr/bin/env python3
import requests
import re
import json
import datetime
import os
import shutil
import concurrent.futures

# ==========================================
# HARDCODED WORKING CHANNELS (paste your full list here)
# ==========================================
HARDCODED_WORKING_M3U = """#EXTM3U
#EXTINF:-1 tvg-logo="https://v3img.voot.com/resizeMedium,w_450,h_253/v3Storage/assets/ct-1644165913136.jpg" group-title="Tamil GEC",Colors Tamil
https://get.perfecttv.net/dash2.mpd?username=vip_sgnep6z9&password=dBlA1nxq&channel=colortamil

#EXTINF:-1 tvg-logo="https://raw.githubusercontent.com/amazeyourself/tamil-local-iptv/refs/heads/main/logos/MakkalpaniTV.png" group-title="Tamil GEC",Makkal TV
https://play.applelive.in/mapatv/mapatv.m3u8

# ... (all your other working channels) ...
"""

# ==========================================
# SOURCES & SETTINGS
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

CATEGORY_ORDER = [
    "Tamil GEC", "Tamil Movies", "Tamil News", "Tamil Comedy",
    "Tamil Music", "Tamil Infotainment", "Tamil Spiritual", "Tamil Kids",
    "English GEC", "English Movies", "English National News",
    "English International News", "English Business News", "English Infotainment",
    "English Lifestyle", "English Kids", "Sports",
    "local channels", "Tamil Local Channels", "tamil iptv channels"
]

# (Include your CATEGORIES_MAP and FLAT_CATEGORIES building from the original script)

# ==========================================
# HELPER FUNCTIONS (all of them from your original script)
# ==========================================
def clean_name(name):
    name = re.sub(r'\s*\[.*?\]\s*', '', name)
    name = re.sub(r'\s*\(.*?\)\s*', '', name)
    name = re.sub(r'\b(HD|SD|FHD|4K|UHD|HDR|Dolby|1080p|720p|Premium|Plus|IN|UK)\b', '', name, flags=re.I)
    return ' '.join(name.split()).strip()

def is_blocked(name):
    if not name:
        return True
    n = name.lower()
    return any(lang in n for lang in BLOCKED_KEYWORDS)

def get_category_and_name(name):
    # your original implementation
    pass

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
    try:
        resp = requests.head(url, allow_redirects=True, timeout=5)
        return resp.url
    except:
        return url

def validate_stream(url, cat):
    # your full validation logic
    pass

def process_channel(item, resolved_urls_global):
    # your full processing logic
    pass

# ==========================================
# MAIN FUNCTION (the hybrid version)
# ==========================================
def main():
    print("Starting merged builder – guaranteed channels + fresh scraping...")
    # ... (the rest of the merged main function)

if __name__ == "__main__":
    main()
