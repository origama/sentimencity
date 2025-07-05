from shared import db, models
from services.metrics_builder.main import build_metrics
from pathlib import Path

def test_build_metrics(tmp_path: Path, monkeypatch: object) -> None:
    db.DB_PATH = tmp_path / "test.db"
    db.SCHEMA = Path(__file__).resolve().parents[3] / 'shared' / "schema.sql"
    db.init_db()
    conn = db.get_connection()
    conn.execute("INSERT INTO feeds(city, url) VALUES('X', 'u')")
    feed_id = conn.execute("SELECT id FROM feeds").fetchone()[0]
    conn.execute("INSERT INTO articles(feed_id, guid, link, sentiment, analysed) VALUES(?,?,?,?,1)", (feed_id, 'g', 'l', 0.5))
    config = models.Config(llm=models.LLMConfig(base_url='', model=''), cities=[], scheduler=models.SchedulerConfig(ingest_interval_minutes=1, analysis_interval_minutes=1, metrics_time='00:00', site_time='00:00'))
    build_metrics(config)
    rows = conn.execute("SELECT * FROM city_metrics").fetchall()
    assert rows
