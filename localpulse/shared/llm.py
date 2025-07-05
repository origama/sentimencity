from __future__ import annotations

import requests

from .models import LLMConfig


class LLMClient:
    def __init__(self, cfg: LLMConfig) -> None:
        self.cfg = cfg

    def sentiment(self, text: str) -> float:
        payload = {
            "model": self.cfg.model,
            "prompt": f"Sentiment score between -1 and 1 for: {text}",
        }
        resp = requests.post(f"{self.cfg.base_url}/v1/chat/completions", json=payload, timeout=30)
        resp.raise_for_status()
        content = resp.json()
        # Very naive parsing
        try:
            return float(content.get("choices", [{}])[0].get("message", {}).get("content", 0))
        except Exception:  # pragma: no cover - guard parsing issues
            return 0.0
