from __future__ import annotations

from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent


def safe_path(raw_path: str, root: str = str(PROJECT_ROOT)) -> Path:
    base = Path(root).resolve()
    candidate = (base / raw_path).resolve() if not Path(raw_path).is_absolute() else Path(raw_path).resolve()
    try:
        candidate.relative_to(base)
    except ValueError as exc:
        raise ValueError(f"Path escapes project root: {raw_path}") from exc
    return candidate


def read_file(file_path: str, start: int | None = None, end: int | None = None) -> dict[str, object]:
    path = safe_path(file_path)
    if not path.exists() or not path.is_file():
        raise FileNotFoundError(f"File not found: {file_path}")

    text = path.read_text(encoding="utf-8")
    lines = text.splitlines()
    if start is not None or end is not None:
        start_i = max(0, int(start or 0))
        end_i = len(lines) if end is None else min(len(lines), int(end))
        output = "\n".join(lines[start_i:end_i])
        return {"path": str(path.relative_to(PROJECT_ROOT)), "content": output, "start": start_i, "end": end_i}

    return {"path": str(path.relative_to(PROJECT_ROOT)), "content": text}


def write_file(file_path: str, content: str) -> dict[str, str]:
    path = safe_path(file_path)
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content, encoding="utf-8")
    return {"path": str(path.relative_to(PROJECT_ROOT)), "status": "written"}


def list_dir(dir_path: str = ".", include_hidden: bool = False) -> list[str]:
    path = safe_path(dir_path)
    if not path.exists() or not path.is_dir():
        raise FileNotFoundError(f"Directory not found: {dir_path}")
    items: list[str] = []
    for child in sorted(path.iterdir()):
        if not include_hidden and child.name.startswith("."):
            continue
        rel = str(child.relative_to(PROJECT_ROOT))
        items.append(rel)
    return items
