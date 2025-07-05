from __future__ import annotations

import asyncio
import os

import aiohttp
import typer

from shared import db, llm, models, utils

app = typer.Typer()


async def analyse_once(config: models.Config) -> None:
    db.init_db()
    conn = db.get_connection()
    row = conn.execute(
        "SELECT id, link FROM articles WHERE fetched=0 LIMIT 1"
    ).fetchone()
    if not row:
        return
    article_id, link = row
    async with aiohttp.ClientSession() as session:
        async with session.get(link) as resp:
            text = await resp.text()
    client = llm.LLMClient(config.llm)
    score = client.sentiment(text[:4096])
    conn.execute(
        "UPDATE articles SET fetched=1, analysed=1, sentiment=? WHERE id=?",
        (score, article_id),
    )


@app.command()
def main(once: bool = False) -> None:
    config = utils.load_config()
    concurrency = int(os.getenv("ANALYSIS_CONCURRENCY", "1"))
    async def worker() -> None:
        while True:
            await analyse_once(config)
            await asyncio.sleep(config.scheduler.analysis_interval_minutes * 60)
    if once:
        asyncio.run(analyse_once(config))
    else:
        async def runner() -> None:
            tasks = [asyncio.create_task(worker()) for _ in range(concurrency)]
            await asyncio.gather(*tasks)

        asyncio.run(runner())


if __name__ == "__main__":
    app()
