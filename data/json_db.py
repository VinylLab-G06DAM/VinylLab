import json
from pathlib import Path
from typing import Any

DATA_DIR = Path(__file__).resolve().parent


def read_collection(filename: str, key: str) -> list[dict[str, Any]]:
    """Read a named list collection from a JSON file inside data/."""
    path = DATA_DIR / filename
    if not path.exists():
        return []
    content = path.read_text(encoding="utf-8").strip()
    if not content:
        return []
    data = json.loads(content)
    return list(data.get(key, []))


def write_collection(filename: str, key: str, items: list[dict[str, Any]]) -> None:
    """Write a named list collection to a JSON file inside data/."""
    path = DATA_DIR / filename
    path.write_text(
        json.dumps({key: items}, indent=4, ensure_ascii=False) + "\n",
        encoding="utf-8",
    )
