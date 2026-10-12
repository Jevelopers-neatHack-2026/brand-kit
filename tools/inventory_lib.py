"""Shared helpers for the BK-01 checks. Standard library only (Python 3.9+)."""
from __future__ import annotations

import os
import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
INVENTORY = "inventory/brand-inventory.json"


def list_files(root: Path) -> list[str]:
    """Tracked plus untracked-unignored files via git; falls back to a filesystem walk outside a git work tree."""
    try:
        out = subprocess.run(["git", "-C", str(root), "ls-files", "-z", "--cached", "--others", "--exclude-standard"], check=True,
                             capture_output=True, text=True).stdout
        files = [f for f in out.split("\0") if f]
        return sorted(f for f in set(files) if (root / f).is_file())
    except (subprocess.CalledProcessError, FileNotFoundError):
        found = []
        for dirpath, dirnames, filenames in os.walk(root):
            dirnames[:] = [d for d in dirnames if d not in (".git", "__pycache__")]
            for name in filenames:
                found.append(os.path.relpath(os.path.join(dirpath, name), root))
        return sorted(f.replace(os.sep, "/") for f in found)
