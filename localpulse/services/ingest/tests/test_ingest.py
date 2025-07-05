from pathlib import Path
from typing import Any
import asyncio

from shared import db, models
from services.ingest.main import ingest_once

class DummyFeed:
    def __init__(self) -> None:
        self.feed = {"title": "dummy"}
        self.entries = [{"id": "1", "link": "http://a", "title": "t"}]

async def fake_fetch(*args: object, **kwargs: object) -> DummyFeed:
    return DummyFeed()


def test_ingest(tmp_path: Path, monkeypatch: Any) -> None:
    db.DB_PATH = tmp_path / "test.db"
    db.SCHEMA = Path(__file__).resolve().parents[3] / 'shared' / 'schema.sql'
    opml_file = tmp_path / "c.opml"
    opml_file.write_text('<opml><body><outline xmlUrl="http://x"/></body></opml>')
    config = models.Config(
        llm=models.LLMConfig(base_url="", model=""),
        cities=[models.CityConfig(name="C", opml=str(opml_file))],
        scheduler=models.SchedulerConfig(ingest_interval_minutes=1, analysis_interval_minutes=1, metrics_time="00:00", site_time="00:00"),
    )
    monkeypatch.setattr("services.ingest.main.fetch_feed", fake_fetch)
    asyncio.run(ingest_once(config))
    conn = db.get_connection()
    assert conn.execute("SELECT COUNT(*) FROM feeds").fetchone()[0] == 1
    assert conn.execute("SELECT COUNT(*) FROM articles").fetchone()[0] == 1
