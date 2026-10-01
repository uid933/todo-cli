"""JSON file persistence."""

import json
from pathlib import Path

DEFAULT_PATH = Path("todos.json")


def load(path=DEFAULT_PATH):
    path = Path(path)
    if not path.exists():
        return []
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except json.JSONDecodeError as e:
        raise ValueError(f"{path} 不是有效的 JSON: {e}") from e


def save(todos, path=DEFAULT_PATH):
    Path(path).write_text(
        json.dumps(todos, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )
