from keep_alive import keep_alive
keep_alive()
import discord
import feedparser
import asyncio
import schedule
import time
import os
keep_alive()

TOKEN = os.getenv("BOT_TOKEN")
keep_alive()

intents = discord.Intents.default()
client = discord.Client(intents=intents)

# Replace with your actual channel IDs
ANIME_CHANNEL_ID = 1383440564569112636
MANGA_CHANNEL_ID = 1383441099561107528

ANIME_FEED = "https://www.animenewsnetwork.com/all/rss.xml"
MANGA_FEED = "https://www.animenewsnetwork.com/news/category/manga/.rss"

posted_anime = set()
posted_manga = set()

async def post_news():
    anime_channel = client.get_channel(ANIME_CHANNEL_ID)
    manga_channel = client.get_channel(MANGA_CHANNEL_ID)

    anime_feed = feedparser.parse(ANIME_FEED)
    manga_feed = feedparser.parse(MANGA_FEED)

    for entry in anime_feed.entries[:3]:
        if entry.link not in posted_anime:
            await anime_channel.send(f"📺 **Anime News:** {entry.title}\n🔗 {entry.link}")
            posted_anime.add(entry.link)

    for entry in manga_feed.entries[:3]:
        if entry.link not in posted_manga:
            await manga_channel.send(f"📖 **Manga News:** {entry.title}\n🔗 {entry.link}")
            posted_manga.add(entry.link)

async def scheduler():
    while True:
        schedule.run_pending()
        await asyncio.sleep(30)

@client.event
async def on_ready():
    print(f'✅ Logged in as {client.user}')
    schedule.every(6).hours.do(asyncio.create_task, post_news())
    await post_news()
    await scheduler()

client.run(TOKEN)
