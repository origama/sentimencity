from pathlib import Path

from .. import utils


def test_load_config(tmp_path: Path) -> None:
    cfg = tmp_path / "cfg.yml"
    cfg.write_text("llm:\n  base_url: http://x\n  model: m\ncities: []\nscheduler:\n  ingest_interval_minutes: 1\n  analysis_interval_minutes: 1\n  metrics_time: '00:00'\n  site_time: '00:00'\n")
    conf = utils.load_config(cfg)
    assert conf.llm.model == "m"
