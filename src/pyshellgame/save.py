import json
from pathlib import Path


def default_save_path() -> Path:
    return Path.home() / ".pyshellgame" / "save.json"


def load_completed_challenges(path: Path) -> set[str]:
    if not path.exists():
        return set()
    data = json.loads(path.read_text())
    return set(data.get("completed_challenges", []))


def write_completed_challenges(path: Path, completed: set[str]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps({"completed_challenges": sorted(completed)}, indent=2))
