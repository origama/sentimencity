from ..llm import LLMClient
from ..models import LLMConfig
from unittest.mock import patch
import requests


def test_sentiment_parsing()-> None:
    cfg = LLMConfig(base_url="http://x", model="m")
    client = LLMClient(cfg)
    with patch.object(requests, "post") as mock_post:
        mock_post.return_value.json.return_value = {"choices": [{"message": {"content": "0.1"}}]}
        mock_post.return_value.raise_for_status.return_value = None
        score = client.sentiment("hi")
    assert score == 0.1
