from __future__ import annotations

from datetime import date
import json

from pathlib import Path
import pandas as pd
import typer

from shared import db, models, utils

app = typer.Typer()


def build_metrics(config: models.Config) -> None:
    db.init_db()
    conn = db.get_connection()
    df = pd.read_sql_query(
        "SELECT feeds.city, sentiment, datetime(published) as published FROM articles JOIN feeds ON feeds.id = articles.feed_id WHERE analysed=1",
        conn,
    )
    if df.empty:
        return
    today = date.today().isoformat()
    for city, g in df.groupby("city"):
        hsi = g["sentiment"].mean()
        spread = g["sentiment"].std()
        conn.execute(
            "INSERT OR REPLACE INTO city_metrics(city, date, metric, value) VALUES(?,?,?,?)",
            (city, today, "hsi", hsi),
        )
        conn.execute(
            "INSERT OR REPLACE INTO city_metrics(city, date, metric, value) VALUES(?,?,?,?)",
            (city, today, "polarity_spread", spread),
        )
        # placeholders
        conn.execute(
            "INSERT OR REPLACE INTO city_metrics(city, date, metric, value) VALUES(?,?,?,?)",
            (city, today, "crime_intensity", 0.0),
        )
        conn.execute(
            "INSERT OR REPLACE INTO city_metrics(city, date, metric, value) VALUES(?,?,?,?)",
            (city, today, "tourist_sentiment", 0.0),
        )
        city_data = conn.execute(
            "SELECT date, value FROM city_metrics WHERE city=? AND metric='hsi' ORDER BY date",
            (city,),
        ).fetchall()
        out = {
            "city": city,
            "dates": [r[0] for r in city_data],
            "hsi": [r[1] for r in city_data],
        }
        Path("public/data").mkdir(parents=True, exist_ok=True)
        Path(f"public/data/{city}.json").write_text(json.dumps(out))


@app.command()
def main(once: bool = False) -> None:
    config = utils.load_config()
    if once:
        build_metrics(config)
    else:
        import time
        while True:
            build_metrics(config)
            time.sleep(24 * 3600)


if __name__ == "__main__":
    app()
