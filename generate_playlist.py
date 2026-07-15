#!/usr/bin/env python3
import requests
import re
import json
import datetime
import os
import shutil
import concurrent.futures

# ==========================================
# 1. HARDCODED WORKING CHANNELS (your proven list)
# ==========================================
HARDCODED_WORKING_M3U = """#EXTM3U
#EXTINF:-1 tvg-logo="https://v3img.voot.com/resizeMedium,w_450,h_253/v3Storage/assets/ct-1644165913136.jpg" group-title="Tamil GEC",Colors Tamil
https://get.perfecttv.net/dash2.mpd?username=vip_sgnep6z9&password=dBlA1nxq&channel=colortamil

#EXTINF:-1 tvg-logo="https://raw.githubusercontent.com/amazeyourself/tamil-local-iptv/refs/heads/main/logos/MakkalpaniTV.png" group-title="Tamil GEC",Makkal TV
https://play.applelive.in/mapatv/mapatv.m3u8

#EXTINF:-1 tvg-logo="https://jiotv.catchup.cdn.jio.com/dare_images/images/Polimer_TV.png" group-title="Tamil GEC",Polimer TV
https://cdn-2.pishow.tv/live/1241/master.m3u8

#EXTINF:-1 tvg-logo="https://jiotv.catchup.cdn.jio.com/dare_images/images/Sun_TV_HD.png" group-title="Tamil GEC",Sun TV
https://livestream2.sunnxt.com/19ee29194c4d4fc286c3e697362e60cd/SunTVHDB_IN_index.mpd

#EXTINF:-1 tvg-logo="https://play-lh.googleusercontent.com/RrIUDazd9z6EZaRewzOa9tjeJELR5qT2eJkukFRvRRIe1Odo4nJEjkguxwHVM1_SAty7=w480-h960-rw" group-title="Tamil GEC",Vasanth TV
https://play.applelive.in/vasanthtv/vasanthtv.m3u8

#EXTINF:-1 tvg-logo="https://jiotv.catchup.cdn.jio.com/dare_images/images/Vendhar_TV.png" group-title="Tamil GEC",Vendhar TV
https://cdn-3.pishow.tv/live/1271/master.m3u8

#EXTINF:-1 tvg-logo="https://jiotv.catchup.cdn.jio.com/dare_images/images/KTV_HD.png" group-title="Tamil Movies",KTV
https://livestream.sunnxt.com/6ae70edd4c1440379f5311e8fbddc7c1/KTVB_IN_index.mpd

#EXTINF:-1 tvg-logo="https://jiotv.catchup.cdn.jio.com/dare_images/images/Malai_Murasu.png" group-title="Tamil Movies",Murasu
https://segment.yuppcdn.net/050522/murasu/playlist.m3u8

#EXTINF:-1 tvg-logo="https://jiotv.catchup.cdn.jio.com/dare_images/images/News7_Tamil.png" group-title="Tamil News",News7 Tamil
https://segment.yuppcdn.net/240122/news7/playlist.m3u8

#EXTINF:-1 tvg-logo="https://jiotv.catchup.cdn.jio.com/dare_images/images/Polimer_News.png" group-title="Tamil News",Polimer News
https://segment.yuppcdn.net/110322/polimernews/playlist.m3u8

#EXTINF:-1 tvg-logo="https://tamilwebcast.com/TV-Logos/PuthiyaThalaimurai.png" group-title="Tamil News",Puthiya Thalaimurai
https://segment.yuppcdn.net/240122/puthiya/playlist.m3u8

#EXTINF:-1 tvg-logo="https://jiotv.catchup.cdn.jio.com/dare_images/images/Thanti_One.png" group-title="Tamil News",Thanthi TV
https://cdn-3.pishow.tv/live/1612/master.m3u8

#EXTINF:-1 tvg-logo="https://jiotv.catchup.cdn.jio.com/dare_images/images/Adithya_TV.png" group-title="Tamil Comedy",Adithya TV
https://livestream.sunnxt.com/4d0eb3cde30247ada4ade679fdfbaf86/AdithyaTVB_IN_index.mpd

#EXTINF:-1 tvg-logo="https://tamilwebcast.com/TV-Logos/isaiaruvi.jpeg" group-title="Tamil Music",Isaiaruvi
https://segment.yuppcdn.net/140622/isaiaruvi/playlist.m3u8

#EXTINF:-1 tvg-logo="https://jiotv.catchup.cdn.jio.com/dare_images/images/Sun_Music_HD.png" group-title="Tamil Music",Sun Music
https://livestream.sunnxt.com/d434796d90fa4dc9b7ecfacedbe683f1/SunMusicHDB_IN_index.mpd

#EXTINF:-1 tvg-logo="https://jiotv.catchup.cdn.jio.com/dare_images/images/Sun_Life.png" group-title="Tamil Infotainment",Sun Life
https://livestream.sunnxt.com/6b79451f54284b3fb680fd717ee008dc/SunLifeB_IN_index.mpd

#EXTINF:-1 tvg-logo="https://jiotv.catchup.cdn.jio.com/dare_images/images/Angel_TV_HD.png" group-title="Tamil Spiritual",Angel TV
https://cdn-7.pishow.tv/live/453/master.m3u8

#EXTINF:-1 tvg-logo="https://jiotv.catchup.cdn.jio.com/dare_images/images/Madha_TV.png" group-title="Tamil Spiritual",Madha TV
https://cdn-3.pishow.tv/live/1265/master.m3u8

#EXTINF:-1 tvg-logo="https://jiotv.catchup.cdn.jio.com/dare_images/images/Sri_Sankara.png" group-title="Tamil Spiritual",Sri Sankara TV
https://cdn-3.pishow.tv/live/1135/master.m3u8

#EXTINF:-1 tvg-logo="https://jiotv.catchup.cdn.jio.com/dare_images/images/Vaanavil_TV.png" group-title="Tamil Spiritual",Vaanavil
https://get.perfecttv.net/dash2.mpd?channel=vaanavil&username=vip_level7&password=vip_level7

#EXTINF:-1 tvg-logo="https://jiotv.catchup.cdn.jio.com/dare_images/images/Velicham_Tv.png" group-title="Tamil Spiritual",Velicham TV
https://play.applelive.in/nithyavelichamtv/nithyavelichamtv.m3u8

#EXTINF:-1 tvg-logo="https://jiotv.catchup.cdn.jio.com/dare_images/images/Chutti_TV.png" group-title="Tamil Kids",Chutti TV
https://livestream.sunnxt.com/3ed29d5b01b546eaa05d184cd87535f1/ChuttiTVB_IN_index.mpd

#EXTINF:-1 tvg-logo="https://www.ashokadigital.net/_next/image?url=https%3A%2F%2Flivetv.ashokadigital.net%2Fupload%2Flogo%2F1756798791_Logo_00341.png&w=1920&q=75" group-title="English Movies",WB
https://stitcher-ipv4.pluto.tv/v2/stitch/embed/hls/channel/5f4d86f519358a00072b978e/master.m3u8?deviceType=samsung-tvplus&deviceMake=samsung&deviceModel=samsung&deviceVersion=unknown&appVersion=unknown&deviceLat=0&deviceLon=0&deviceDNT=%7BTARGETOPT%7D&deviceId=%7BPSID%7D&advertisingId=%7BPSID%7D&us_privacy=1YNY&samsung_app_domain=%7BAPP_DOMAIN%7D&samsung_app_name=%7BAPP_NAME%7D&profileLimit=&profileFloor=&embedPartner=samsung-tvplus&masterJWTPassthrough=1&authToken=eyJhbGciOiJIUzI1NiIsImtpZCI6ImI2YzVkMmFlLTIzODgtNDg3Ny1hMTM1LTFiN2RhZDJkYjMxYSIsInR5cCI6IkpXVCJ9.eyJwYXJ0bmVyIjoic2Ftc3VuZ3R2cGx1cyIsImZlYXR1cmVzIjp7Im11bHRpUG9kQWRzIjp7ImNvaG9ydCI6IiIsImVuYWJsZWQiOnRydWV9LCJzdGl0Y2hlckhsc05nIjp7ImRlbXV4ZWRBdWRpbyI6ImppdCJ9LCJzdGl0Y2hlclBhcnRuZXJTaG93U2xhdGUiOnsiZW5hYmxlZCI6dHJ1ZX19LCJpc3MiOiJzZXJ2aWNlLXBhcnRuZXItYXV0aC5wbHV0by50diIsInN1YiI6InByaTp2MTpwbHV0bzpkZXZpY2VzOmMyRnRjM1Z1WjNSMmNHeDFjdz09IiwiYXVkIjoiKi5wbHV0by50diIsImV4cCI6MTc4NDEzNjQ0OSwiaWF0IjoxNzg0MDUwMDQ5LCJqdGkiOiJkMDNkZGViYi1mODk0LTRiYzYtYmQzNS03OTk2Yzk2ODFhZTIifQ.TGJm4yDDww4N-RdKkorRyOhA3JmqWEGhsIN3cciY0JA

#EXTINF:-1 tvg-logo="https://akamaividz2.zee5.com/image/upload/w_auto,h_396,c_scale,f_webp,q_auto:eco/resources/0-101-10z5588214/list/1170x658withlogofbf8f188fa714b538ff5dd8cb80e3bb5.jpg" group-title="English National News",India Today
https://livehub-voidnet.onrender.com/cluster/streamcore/in/INDIATODAY_StreamOrchestrator.m3u8

#EXTINF:-1 tvg-logo="https://jiotv.catchup.cdn.jio.com/dare_images/images/Mirror_Now.png" group-title="English National News",Mirror Now
https://d1rc86nwwc9fag.cloudfront.net/v1/vglive-sk-310426/main.m3u8?hdnts=st=1784076817~exp=1784098417~acl=!*/v1/vglive-sk-310426/*!/payload/yupptvott_5_-1_3b6f5839-0b53-aa06-7a80-023047a6357c_US_172.208.127.81_yuppfast_2_channel_213_-1/*~data=yupptvott_5_-1_3b6f5839-0b53-aa06-7a80-023047a6357c_US_172.208.127.81_yuppfast_2_channel_213_-1~hmac=0a16229d66c49b24cdfe76df8b66d2d80b032ba2c3261d9398075eda66b531cd&ads.network_name=yuppfast&ads.app_store_url=&ads.app_bundle=&ads.content_livestream=1&ads.content_genre=NEWS&ads.channel_name=MirrorNow&ads.language=ENG&ads.user=0

#EXTINF:-1 tvg-logo="https://jiotv.catchup.cdn.jio.com/dare_images/images/NDTV_24x7.png" group-title="English National News",NDTV 24x7
https://d1rc86nwwc9fag.cloudfront.net/vglive-sk-227286/v1/0194a671d8dd1ebd416a3e0a8a4524/0194a67abb941ebd47043cd206ba4f/main.m3u8?hdnts=st=1784076817~exp=1784098417~acl=!*/vglive-sk-227286/v1/0194a671d8dd1ebd416a3e0a8a4524/0194a67abb941ebd47043cd206ba4f/*!/payload/yupptvott_5_-1_3b6f5839-0b53-aa06-7a80-023047a6357c_US_172.208.127.81_yuppfast_2_channel_1_-1/*~data=yupptvott_5_-1_3b6f5839-0b53-aa06-7a80-023047a6357c_US_172.208.127.81_yuppfast_2_channel_1_-1~hmac=f087b27a16e2058da775c69fc9de63dcd11d049ddb28bee57f321164e90d48c9&ads.network_name=yuppfast&ads.app_store_url=&ads.app_bundle=&ads.content_livestream=1&ads.content_genre=NEWS&ads.channel_name=NDTV24x7&ads.language=ENG&ads.user=0

#EXTINF:-1 tvg-logo="https://jiotv.catchup.cdn.jio.com/dare_images/images/Republic_TV.png" group-title="English National News",Republic TV
https://cdn-2.pishow.tv/live/271/master.m3u8

#EXTINF:-1 tvg-logo="https://jiotv.catchup.cdn.jio.com/dare_images/images/AL_Jazeera.png" group-title="English International News",Al Jazeera English
https://live-hls-apps-aje-fa.getaj.net/AJE/index.m3u8

#EXTINF:-1 tvg-logo="https://xstreamcp-assets-msp.streamready.in/assets/LIVETV/LIVECHANNEL/LIVETV_LIVETVCHANNEL_BBC_NEWS/images/LOGO_HD/image.png" group-title="English International News",BBC News
https://vs-cmaf-push-ww-live.akamaized.net/x=4/i=urn:bbc:pips:service:bbc_news_channel_hd/hevc_iptv_mse_v0.mpd

#EXTINF:-1 tvg-logo="https://jiotv.catchup.cdn.jio.com/dare_images/images/CNN.png" group-title="English International News",CNN International
https://viewmedia7219.bozztv.com/wmedia/viewmedia100/web_014/Stream/playlist.m3u8

#EXTINF:-1 tvg-logo="https://jiotv.catchup.cdn.jio.com/dare_images/images/NDTV_Profit.png" group-title="English Business News",NDTV Profit
https://yuppnimrestreammum.akamaized.net/181224/smil:ndtvprofit.smil/playlist.m3u8?ads.channel=204&ads.content_custom_1_param=FAST&ads.user=2&ads.content_custom_3_param=YuppFastIndia&hdnts=st=1784076819~exp=1784098419~acl=!*/181224/smil:ndtvprofit.smil/*!/payload/yupptvott_5_-1_3b6f5839-0b53-aa06-7a80-023047a6357c_US_172.208.127.81_yuppfast_2_channel_3_-1/*~data=yupptvott_5_-1_3b6f5839-0b53-aa06-7a80-023047a6357c_US_172.208.127.81_yuppfast_2_channel_3_-1~hmac=155ea1a6432a070b9679a548b5d6fffa3c3e7719361e48347b78197881f88eb0&ads.network_name=yuppfast&ads.app_store_url=&ads.app_bundle=&ads.content_livestream=1&ads.content_genre=NEWS&ads.channel_name=NDTVProfit&ads.language=ENG&ads.user=0

#EXTINF:-1 tvg-logo="https://vmfm.github.io/tamilvmtv/image/Animal_Planet.png" group-title="English Infotainment",Animal Planet
https://vodzong.mjunoon.tv:8087/streamtest/Animal-Planet-158-3/playlist.m3u8

#EXTINF:-1 tvg-logo="https://d229kpbsb5jevy.cloudfront.net/yuppfast/content/common/channel/logos/mxzyyw.png" group-title="English Lifestyle",Goodtimes
https://d2gvyg6lvauoko.cloudfront.net/230226/ndtvgoodtimes/playlist.m3u8?ads.channel=205&ads.content_custom_1_param=FAST&ads.user=2?ads.channel=205&ads.content_custom_1_param=FAST&ads.user=2&ads.content_custom_3_param=YuppFastIndia&hdnts=st=1784076820~exp=1784098420~acl=!*/230226/ndtvgoodtimes/*!/payload/yupptvott_5_-1_3b6f5839-0b53-aa06-7a80-023047a6357c_US_172.208.127.81_yuppfast_2_channel_4_-1/*~data=yupptvott_5_-1_3b6f5839-0b53-aa06-7a80-023047a6357c_US_172.208.127.81_yuppfast_2_channel_4_-1~hmac=8ac1a9698d686133c3b1bd12bfb40feee515e9e8ae53a125dbe43600c32a79ac&ads.network_name=yuppfast&ads.app_store_url=&ads.app_bundle=&ads.content_livestream=1&ads.content_genre=LIFESTYLE&ads.channel_name=NDTVGoodTimes&ads.language=ENG&ads.user=0

#EXTINF:-1 tvg-logo="https://jiotv.catchup.cdn.jio.com/dare_images/images/Ten_HD.png" group-title="Sports",Sony Sports Ten 1
https://raw.githubusercontent.com/Jatin-0-7/intro/main/intro_playlist0.ts

#EXTINF:-1 tvg-logo="https://jiotv.catchup.cdn.jio.com/dare_images/images/Six_HD.png" group-title="Sports",Sony Sports Ten 5
https://files.catbox.moe/uizjo7.mp4

#EXTINF:-1 tvg-logo="https://jiotvimages.cdn.jio.com/dare_images/images/sanaplus.png" group-title="local channels",Sana
https://galaxyott.live/hls/sanaplus.m3u8

#EXTINF:-1 tvg-logo="https://jiotvimages.cdn.jio.com/dare_images/images/sanatv.png" group-title="local channels",Sana TV
https://galaxyott.live/hls/sanatv.m3u8

... (include the rest of your Tamil Local Channels list – I truncated to fit here, but paste the full list)
"""

# ==========================================
# 2. SOURCES & BLOCKLIST (unchanged)
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

# ... (rest of the helper functions – clean_name, is_blocked, get_category_and_name, parse_m3u, parse_json, resolve_url, validate_stream, process_channel – remain exactly as in your original script)

def main():
    print("Starting merged builder – guaranteed channels + fresh scraping...")

    # -------------------------------------------------
    # PHASE A: Load hardcoded working channels (always)
    # -------------------------------------------------
    print("Loading hardcoded working channels...")
    from io import StringIO
    hardcoded_channels = {}  # proper_name -> {category, logo, urls}
    seen_urls_global = set()

    # Parse the hardcoded M3U string
    for name, logo, url, cat in parse_m3u(HARDCODED_WORKING_M3U):
        url = url.strip()
        if not url.startswith("http") or url in seen_urls_global:
            continue
        seen_urls_global.add(url)
        if is_blocked(name):
            continue
        cat = cat if cat else "tamil iptv channels"
        proper_name = clean_name(name) or name
        if proper_name not in hardcoded_channels:
            hardcoded_channels[proper_name] = {'category': cat, 'logo': logo, 'urls': [url]}
        else:
            hardcoded_channels[proper_name]['urls'].append(url)

    # -------------------------------------------------
    # PHASE B: Scrape remote sources
    # -------------------------------------------------
    grouped_channels = dict(hardcoded_channels)  # start with guaranteed ones
    print("Scraping remote sources...")
    for src_url in SOURCES:
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
                        proper_name = clean_name(name) or name
                    else:
                        continue
                if proper_name not in grouped_channels:
                    grouped_channels[proper_name] = {'category': cat, 'logo': logo, 'urls': []}
                grouped_channels[proper_name]['urls'].append(url)
                if not grouped_channels[proper_name]['logo'] and logo:
                    grouped_channels[proper_name]['logo'] = logo
        except Exception as e:
            print(f"  Error fetching {src_url}: {e}")

    # -------------------------------------------------
    # PHASE C: Validate (only scraped entries, not hardcoded ones)
    # -------------------------------------------------
    print(f"Total unique channel names: {len(grouped_channels)}. Validating scraped links...")
    # Separate channels that came from scraping (not in hardcoded)
    scraped_channels = {k: v for k, v in grouped_channels.items() if k not in hardcoded_channels}
    # Hardcoded channels are considered pre-validated; we still need to deduplicate them by resolved URL later
    final_channels = {cat: [] for cat in CATEGORY_ORDER}
    resolved_urls_global = set()

    # First, add hardcoded channels directly (they're guaranteed to work)
    for proper_name, data in hardcoded_channels.items():
        cat = data['category']
        logo = data['logo']
        # pick the first URL (there's only one per hardcoded entry anyway)
        url = data['urls'][0]
        # Check if this URL (after resolving) is already used
        final_url = resolve_url(url)
        if final_url in resolved_urls_global:
            continue
        resolved_urls_global.add(final_url)
        if cat not in final_channels:
            final_channels[cat] = []
        final_channels[cat].append((proper_name, logo, url))

    # Then validate scraped channels
    with concurrent.futures.ThreadPoolExecutor(max_workers=50) as executor:
        items = list(scraped_channels.items())
        future_to_item = {executor.submit(process_channel, item, resolved_urls_global): item for item in items}
        for future in concurrent.futures.as_completed(future_to_item):
            res = future.result()
            if res:
                cat, proper_name, logo, url = res
                if cat not in final_channels:
                    final_channels[cat] = []
                final_channels[cat].append((proper_name, logo, url))

    # -------------------------------------------------
    # PHASE D: Write output
    # -------------------------------------------------
    OUTPUT_FILE = "master_playlist.m3u"
    BACKUP_FILE = "playlist_backup.m3u"

    # Count total channels
    total_added = sum(len(v) for v in final_channels.values())
    if total_added == 0:
        print("⚠️ No channels found. Restoring backup.")
        if os.path.exists(BACKUP_FILE):
            shutil.copy2(BACKUP_FILE, OUTPUT_FILE)
        return

    # Sort channels within each category A-Z
    for cat in final_channels:
        final_channels[cat].sort(key=lambda x: x[0].lower())

    with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
        f.write("#EXTM3U\n")
        for cat in CATEGORY_ORDER:
            if cat in final_channels and final_channels[cat]:
                f.write(f"\n# --- {cat} ---\n")
                for display_name, logo, url in final_channels[cat]:
                    f.write(f'#EXTINF:-1 tvg-name="{display_name}" tvg-logo="{logo}" group-title="{cat}",{display_name}\n{url}\n')
        # Catch-all for unexpected categories
        for cat in sorted(final_channels.keys()):
            if cat not in CATEGORY_ORDER and final_channels[cat]:
                f.write(f"\n# --- {cat} ---\n")
                for display_name, logo, url in final_channels[cat]:
                    f.write(f'#EXTINF:-1 tvg-name="{display_name}" tvg-logo="{logo}" group-title="{cat}",{display_name}\n{url}\n')

    shutil.copy2(OUTPUT_FILE, BACKUP_FILE)
    print(f"\n✅ SUCCESS! Total Working Channels: {total_added} (hardcoded + scraped)")

    # README update (same as before)
    # ...

if __name__ == "__main__":
    main()
