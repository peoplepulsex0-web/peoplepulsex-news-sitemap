import xml.etree.ElementTree as ET
from datetime import datetime, timedelta
import html, os, urllib.request

RSS_URL = "https://api.rss2json.com/v1/api.json?rss_url=https://www.peoplepulsex.com/feeds/posts/default?alt=rss"
OUTPUT_DIR = "public"
OUTPUT_FILE = os.path.join(OUTPUT_DIR, "news-sitemap.xml")

os.makedirs(OUTPUT_DIR, exist_ok=True)

try:
    urllib.request.urlretrieve(RSS_URL, os.path.join(OUTPUT_DIR, "rss.xml"))
except Exception as e:
    print("❌ فشل تحميل RSS:", e)
    exit(1)

rss = ET.parse(os.path.join(OUTPUT_DIR, "rss.xml"))
root = rss.getroot()

items = root.findall(".//item")
now = datetime.utcnow()

news_sitemap = """<?xml version="1.0" encoding="UTF-8"?>
<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9"
 xmlns:news="http://www.google.com/schemas/sitemap-news/0.9">
"""

for item in items:
    title = html.escape(item.findtext("title", ""))
    link = html.escape(item.findtext("link", ""))
    pubDate = item.findtext("pubDate", "")
    if not pubDate:
        continue
    try:
        pub = datetime.strptime(pubDate, "%a, %d %b %Y %H:%M:%S %z").replace(tzinfo=None)
    except Exception:
        continue
    if now - pub > timedelta(days=2):
        continue

    news_sitemap += f"""
<url>
  <loc>{link}</loc>
  <news:news>
    <news:publication>
      <news:name>PeoplePulseX</news:name>
      <news:language>en</news:language>
    </news:publication>
    <news:publication_date>{pub.isoformat()}</news:publication_date>
    <news:title>{title}</news:title>
  </news:news>
</url>"""

news_sitemap += "\n</urlset>"

with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
    f.write(news_sitemap)

print("✅ تم إنشاء news-sitemap.xml بنجاح!")
