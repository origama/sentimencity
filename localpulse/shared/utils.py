from __future__ import annotations

import yaml
from pathlib import Path

from .models import Config


def load_config(path: Path | str = "config.yml") -> Config:
    data = yaml.safe_load(Path(path).read_text())
    return Config.model_validate(data)
