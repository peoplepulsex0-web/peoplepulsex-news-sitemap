import requests, os, html
from datetime import datetime, timedelta
import xml.etree.ElementTree as ET

RSS_URL = "https://www.peoplepulsex.com/feeds/posts/default?alt=rss"
OUTPUT_DIR = "public"
OUTPUT_FILE = os.path.join(OUTPUT_DIR, "news-sitemap.xml")

os.makedirs(OUTPUT_DIR, exist_ok=True)

print("🔄 Fetching RSS feed...")
r = requests.get(RSS_URL)
if r.status_code != 200:
    print("❌ Failed to fetch RSS:", r.status_code)
    exit(1)

root = ET.fromstring(r.content)
channel = root.find("channel")

now = datetime.utcnow()

news_sitemap = """<?xml version="1.0" encoding="UTF-8"?>
<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9"
 xmlns:news="http://www.google.com/schemas/sitemap-news/0.9">
"""

for item in channel.findall("item"):
    try:
        title = html.escape(item.find("title").text)
        link = html.escape(item.find("link").text)
        pub = datetime.strptime(item.find("pubDate").text, "%a, %d %b %Y %H:%M:%S %z")
        # تحويل إلى UTC بدون المنطقة الزمنية
        pub = pub.astimezone(tz=None).replace(tzinfo=None)
        if now - pub > timedelta(days=2):
            continue
    except Exception:
        continue

    news_sitemap += f"""
<url>
  <loc>{link}</loc>
  <news:news>
    <news:publication>
      <news:name>PeoplePulseX</news:name>
      <news:language>en</news:language>
    </news:publication>
    <news:publication_date>{pub.strftime("%Y-%m-%dT%H:%M:%S")}Z</news:publication_date>
    <news:title>{title}</news:title>
  </news:news>
</url>"""

news_sitemap += "\n</urlset>"

with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
    f.write(news_sitemap)

print("✅ تم إنشاء news-sitemap.xml بنجاح!")
