from __future__ import annotations

import asyncio
import time
from pathlib import Path

import aiohttp
import feedparser
import opml
import typer

from shared import db, models, utils

app = typer.Typer()


async def fetch_feed(session: aiohttp.ClientSession, url: str) -> feedparser.FeedParserDict:
    async with session.get(url) as resp:
        text = await resp.text()
    return feedparser.parse(text)


async def ingest_once(config: models.Config) -> None:
    db.init_db()
    conn = db.get_connection()
    async with aiohttp.ClientSession() as session:
        for city in config.cities:
            outline: opml.OPML = opml.parse(Path(city.opml))
            for o in outline:
                url = o.xmlUrl
                parsed = await fetch_feed(session, url)
                conn.execute(
                    "INSERT OR IGNORE INTO feeds(city, title, url) VALUES(?,?,?)",
                    (city.name, parsed.feed.get("title", url), url),
                )
                feed_id = conn.execute(
                    "SELECT id FROM feeds WHERE url=?", (url,)
                ).fetchone()[0]
                for entry in parsed.entries:
                    conn.execute(
                        "INSERT OR IGNORE INTO articles(feed_id, guid, title, link, published)"
                        " VALUES(?,?,?,?,?)",
                        (
                            feed_id,
                            entry.get("id", entry.get("link")),
                            entry.get("title"),
                            entry.get("link"),
                            entry.get("published"),
                        ),
                    )


@app.command()
def main(once: bool = False) -> None:
    config = utils.load_config()
    if once:
        asyncio.run(ingest_once(config))
    else:
        interval = config.scheduler.ingest_interval_minutes * 60
        while True:
            asyncio.run(ingest_once(config))
            time.sleep(interval)


if __name__ == "__main__":
    app()
