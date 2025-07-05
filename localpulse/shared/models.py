from __future__ import annotations

from datetime import datetime
from typing import List

from pydantic import BaseModel


class LLMConfig(BaseModel):
    base_url: str
    model: str


class CityConfig(BaseModel):
    name: str
    opml: str


class SchedulerConfig(BaseModel):
    ingest_interval_minutes: int
    analysis_interval_minutes: int
    metrics_time: str
    site_time: str


class Config(BaseModel):
    llm: LLMConfig
    cities: List[CityConfig]
    scheduler: SchedulerConfig


class Feed(BaseModel):
    id: int | None = None
    city: str
    title: str | None = None
    url: str
    etag: str | None = None
    last_checked: datetime | None = None


class Article(BaseModel):
    id: int | None = None
    feed_id: int
    guid: str
    title: str | None = None
    link: str
    published: datetime | None = None
    fetched: bool = False
    analysed: bool = False
    sentiment: float | None = None
    raw_json: str | None = None


class CityMetric(BaseModel):
    city: str
    date: datetime
    metric: str
    value: float
