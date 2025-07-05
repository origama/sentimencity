# LocalPulse

LocalPulse monitors city-specific news feeds, analyzes article sentiment via a local LLM,
computes daily metrics, and publishes a static site with the results.

## Quick Start

```bash
# install dependencies
poetry install --no-root

# copy and edit configuration
cp config.yml.example config.yml

# run all services with Docker
docker-compose up --build
```

Each service can also be run manually:

```bash
poetry run python -m services.ingest --once
poetry run python -m services.analysis_worker --once
poetry run python -m services.metrics_builder --once
poetry run python -m services.site_builder --once
```

## Tests

```bash
poetry run pytest --cov
```

Open `htmlcov/index.html` to view coverage.

## FAQ

**How do I switch to another LLM runtime?**
Edit `config.yml` to point `llm.base_url` to a compatible OpenAI-style API.
