#!/usr/bin/env python3
"""Dependency-free structural checks for this Agent Skill repository."""
from __future__ import annotations

import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
LIMIT = 20_000


def check() -> list[str]:
    errors: list[str] = []
    skill_path = ROOT / "SKILL.md"
    if not skill_path.is_file():
        return ["Missing root SKILL.md"]
    content = skill_path.read_text(encoding="utf-8")
    match = re.match(r"\A---\n(?P<header>.*?)\n---\n", content, re.DOTALL)
    if not match:
        return ["SKILL.md must begin with YAML frontmatter surrounded by ---"]
    header = match.group("header")
    fields: dict[str, str] = {}
    for line in header.splitlines():
        if ":" not in line:
            errors.append(f"Invalid frontmatter line: {line!r}")
            continue
        key, value = line.split(":", 1)
        fields[key.strip()] = value.strip()

    name = fields.get("name", "")
    if not re.fullmatch(r"[a-z0-9]+(?:-[a-z0-9]+)*", name) or len(name) > 64:
        errors.append("Invalid Agent Skills name")
    if name != "roblox-asset-workflow":
        errors.append("Unexpected skill name; update package layout if renaming")
    description = fields.get("description", "")
    if not description or len(description) > 1024:
        errors.append("description must be nonempty and <=1024 characters")
    if len(fields.get("compatibility", "")) > 500:
        errors.append("compatibility must be <=500 characters")
    if len(content.splitlines()) > 500:
        errors.append("SKILL.md exceeds suggested 500-line limit")
    if not re.search(r"20,?000 triangles", content, re.IGNORECASE):
        errors.append("Missing explicit 20,000-triangle-per-mesh rule")
    if not all(token in content for token in ("HQ", "GAME", "MOBILE", "UV", "PART")):
        errors.append("Required quality/cosmetic/profile concepts missing")

    for path_string in re.findall(r"\]\((references/[^)#]+)\)", content):
        if not (ROOT / path_string).is_file():
            errors.append(f"Broken reference: {path_string}")
    for filename in ("README.md", "README_FR.md", "LICENSE", "CHANGELOG.md"):
        if not (ROOT / filename).is_file():
            errors.append(f"Missing required file: {filename}")
    for path in [*ROOT.rglob("*.md"), *ROOT.rglob("*.py")]:
        if "/.git/" in path.as_posix():
            continue
        text = path.read_text(encoding="utf-8")
        if "\ufffd" in text:
            errors.append(f"Replacement characters in {path.relative_to(ROOT)}")
    if LIMIT != 20_000:
        errors.append("Incorrect documented Roblox mesh limit")
    return errors


if __name__ == "__main__":
    issues = check()
    if issues:
        print("Skill validation FAILED:")
        for issue in issues:
            print(" -", issue)
        sys.exit(1)
    print("Skill structure OK (metadata, references, docs, core constraints).")
