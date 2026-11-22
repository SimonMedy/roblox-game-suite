#!/usr/bin/env python3
"""Check the imported asset skill against the exact pinned upstream Git blobs."""
from __future__ import annotations

import hashlib
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def check(root: Path = ROOT) -> list[str]:
    manifest = json.loads((root / "upstream/asset-v3.2.0.json").read_text(encoding="utf-8"))
    asset = root / "skills/roblox-asset-workflow"
    issues = []
    for relative, expected in manifest["files"].items():
        file = asset / relative
        if not file.is_file():
            issues.append(f"Missing asset source: {relative}")
            continue
        raw = file.read_bytes()
        git_blob = hashlib.sha1(b"blob " + str(len(raw)).encode() + b"\0" + raw).hexdigest()
        if git_blob != expected:
            issues.append(f"Asset source differs from pinned {manifest['tag']}: {relative}")
    return issues


if __name__ == "__main__":
    issues = check()
    if issues:
        for issue in issues:
            print("FAIL:", issue)
        sys.exit(1)
    print("Asset source matches pinned v3.2.0 (13 core/reference/script/test blobs).")
