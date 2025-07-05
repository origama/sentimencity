from __future__ import annotations

import shutil
from pathlib import Path
import os

from staticjinja import Site  # type: ignore[attr-defined]
import typer


app = typer.Typer()


def build_site(config_path: Path = Path("config.yml")) -> None:
    templates = Path("html_template")
    public = Path("public")
    Site.make_site(searchpath=str(templates), outpath=str(public)).render()
    deploy = Path(os.getenv("DEPLOY_DIR", ""))
    if deploy:
        shutil.copytree(public, deploy, dirs_exist_ok=True)


@app.command()
def main(once: bool = False) -> None:
    build_site()


if __name__ == "__main__":
    app()
