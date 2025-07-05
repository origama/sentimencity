from pathlib import Path

from .. import db


def test_init_db(tmp_path: Path) -> None:
    orig = db.DB_PATH
    db.DB_PATH = tmp_path / "test.db"
    try:
        db.init_db()
        assert db.DB_PATH.exists()
    finally:
        db.DB_PATH = orig
