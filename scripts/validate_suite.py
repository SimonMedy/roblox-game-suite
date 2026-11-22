#!/usr/bin/env python3
"""Validate all self-contained Agent Skills; no third-party dependencies."""
from __future__ import annotations

import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
EXPECTED = {"roblox-asset-workflow", "roblox-vfx-audio", "roblox-game-director"}
NAME = re.compile(r"[a-z0-9]+(?:-[a-z0-9]+)*\Z")
FRONTMATTER = re.compile(r"\A---\r?\n(.*?)\r?\n---\r?\n", re.S)
LINK = re.compile(r"\]\(([^)]+)\)")


def validate(root: Path = ROOT, expected: set[str] | None = None) -> list[str]:
    expected = EXPECTED if expected is None else expected
    errors = []
    skills = root / "skills"
    actual = {f.parent.name for f in skills.glob("*/SKILL.md")}
    if actual != expected:
        errors.append(f"Expected skill names {sorted(expected)}; found {sorted(actual)}")
    for file in root.rglob("SKILL.md"):
        if file.parent.parent != skills:
            errors.append(f"Unexpected nested SKILL.md: {file.relative_to(root)}")
    for name in sorted(actual):
        folder = skills / name
        entry = folder / "SKILL.md"
        text = entry.read_text(encoding="utf-8")
        match = FRONTMATTER.match(text)
        if not match:
            errors.append(f"{name}: missing YAML frontmatter")
            continue
        fields = {}
        for line in match.group(1).splitlines():
            if ":" not in line:
                errors.append(f"{name}: invalid frontmatter line {line!r}")
                continue
            key, value = line.split(":", 1)
            fields[key.strip()] = value.strip().strip('"\'')
        if fields.get("name") != name or not NAME.fullmatch(name) or len(name) > 64:
            errors.append(f"{name}: metadata name invalid or differs from folder")
        if not 1 <= len(fields.get("description", "")) <= 1024:
            errors.append(f"{name}: description empty or too long")
        if len(fields.get("compatibility", "")) > 500:
            errors.append(f"{name}: compatibility too long")
        if len(text.splitlines()) > 500:
            errors.append(f"{name}: excessive SKILL.md length")
        for target in LINK.findall(text):
            target = target.split("#", 1)[0]
            if not target or "://" in target or target.startswith("mailto:"):
                continue
            candidate = (folder / target).resolve()
            if not candidate.is_relative_to(folder.resolve()) or not candidate.is_file():
                errors.append(f"{name}: missing or unsafe local reference {target}")
    if not (root / "LICENSE").is_file():
        errors.append("Missing LICENSE")
    for rel in ("README.md", "README_FR.md", "CHANGELOG.md"):
        if not (root / rel).is_file():
            errors.append(f"Missing {rel}")
    asset = skills / "roblox-asset-workflow"
    for rel in ("scripts/audit_blender.py", "scripts/audit_glb.py", "scripts/validate_skill.py",
                "tests/test_audit_glb.py", "references/roblox-export.md", "references/vehicles.md"):
        if not (asset / rel).is_file():
            errors.append(f"Missing asset component: {rel}")
    for file in root.rglob("*.md"):
        if "\ufffd" in file.read_text(encoding="utf-8"):
            errors.append(f"Replacement character in {file.relative_to(root)}")
    return errors


if __name__ == "__main__":
    problems = validate()
    if problems:
        for problem in problems:
            print("FAIL:", problem)
        sys.exit(1)
    print(f"Suite OK: {len(EXPECTED)} discoverable skills, safe relative references, bundled asset tools.")
