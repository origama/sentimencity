PRAGMA journal_mode=WAL;

CREATE TABLE IF NOT EXISTS feeds (
  id INTEGER PRIMARY KEY,
  city TEXT NOT NULL,
  title TEXT,
  url TEXT UNIQUE,
  etag TEXT,
  last_checked TIMESTAMP
);

CREATE TABLE IF NOT EXISTS articles (
  id INTEGER PRIMARY KEY,
  feed_id INTEGER REFERENCES feeds(id),
  guid TEXT UNIQUE,
  title TEXT,
  link TEXT,
  published TIMESTAMP,
  fetched BOOLEAN DEFAULT 0,
  analysed BOOLEAN DEFAULT 0,
  sentiment REAL,
  raw_json TEXT
);

CREATE INDEX IF NOT EXISTS idx_articles_status
  ON articles(analysed, fetched);

CREATE TABLE IF NOT EXISTS city_metrics (
  city TEXT,
  date DATE,
  metric TEXT,
  value REAL,
  PRIMARY KEY (city, date, metric)
);
