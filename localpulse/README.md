# LocalPulse

LocalPulse monitors city-specific news feeds, analyzes article sentiment via a local LLM,
computes daily metrics, and publishes a static site with the results.

## Quick Start

```bash
# install dependencies
poetry install

# copy and edit configuration
cp config.yml.example config.yml

# build and run the full stack
docker-compose up --build
```

### Running with Docker

Ensure you have Docker and Docker Compose installed. After copying
`config.yml.example` to `config.yml` you can start the complete system with:

```bash
docker-compose up --build
```

This command builds the service images and launches a small stack made up of
SQLite, an Ollama LLM container and the four LocalPulse services. Data will be
stored in the `data/` directory and the generated site will appear in
`public/`. Stop the services with <kbd>Ctrl+C</kbd> and remove the containers
with `docker-compose down` when you are done.

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
