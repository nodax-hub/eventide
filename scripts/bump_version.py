from __future__ import annotations

import datetime as dt
import subprocess
import sys
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PYPROJECT = ROOT / "pyproject.toml"


def get_latest_tag() -> str | None:
    try:
        tag = subprocess.check_output(
            ["git", "describe", "--tags", "--abbrev=0"],
            stderr=subprocess.DEVNULL,
            text=True,
        ).strip()
        return tag
    except subprocess.CalledProcessError:
        return None


def parse_version(tag: str) -> tuple[int, int, int]:
    """
    vYYYY.M.PATCH
    """
    m = re.fullmatch(r"v(\d{4})\.(\d{1,2})\.(\d+)", tag)
    if not m:
        raise ValueError(f"Invalid tag format: {tag}")
    return int(m[1]), int(m[2]), int(m[3])


def next_version() -> str:
    today = dt.date.today()
    y, m = today.year, today.month

    tag = get_latest_tag()
    if tag is None:
        return f"{y}.{m}.0"

    ty, tm, patch = parse_version(tag)

    if (ty, tm) == (y, m):
        patch += 1
    else:
        patch = 0

    return f"{y}.{m}.{patch}"


def update_pyproject(version: str) -> None:
    text = PYPROJECT.read_text(encoding="utf-8")

    new_text, n = re.subn(
        r'version\s*=\s*"[^\"]+"',
        f'version = "{version}"',
        text,
        count=1,
    )

    if n != 1:
        raise RuntimeError("Failed to update version in pyproject.toml")

    PYPROJECT.write_text(new_text, encoding="utf-8")


def main() -> None:
    version = next_version()
    update_pyproject(version)
    print(version)


if __name__ == "__main__":
    main()