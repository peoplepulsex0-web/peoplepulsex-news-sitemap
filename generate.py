import xml.etree.ElementTree as ET
from datetime import datetime, timedelta
import html, os, urllib.request

# إنشاء مجلد public لحفظ الناتج
os.makedirs("public", exist_ok=True)

# تحميل RSS من موقعك
urllib.request.urlretrieve("https://www.peoplepulsex.com/rss.xml", "public/rss.xml")

rss = ET.parse("public/rss.xml")
root = rss.getroot()
items = root.findall(".//item")
now = datetime.utcnow()

news_sitemap = '''<?xml version="1.0" encoding="UTF-8"?>
<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9"
 xmlns:news="http://www.google.com/schemas/sitemap-news/0.9">
'''

for item in items:
    title = html.escape(item.findtext("title", ""))
    link = html.escape(item.findtext("link", ""))
    pubDate = item.findtext("pubDate", "")
    if not pubDate:
        continue
    try:
        pub = datetime.strptime(pubDate, "%a, %d %b %Y %H:%M:%S %z").replace(tzinfo=None)
    except:
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
open("public/news-sitemap.xml", "w", encoding="utf-8").write(news_sitemap)
