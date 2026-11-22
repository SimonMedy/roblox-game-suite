# Roblox Asset Workflow — suite copy (v3.2.0)

**A specialized skill for polished, editable Roblox assets.** This self-contained module is derived from [SimonMedy/roblox-asset-workflow v3.2.0](https://github.com/SimonMedy/roblox-asset-workflow/releases/tag/v3.2.0).

## Install

```bash
npx skills add SimonMedy/roblox-game-suite --skill roblox-asset-workflow
```

The original standalone skill is also available independently via `npx skills add SimonMedy/roblox-asset-workflow`. Tool access (Blender, MCP, Roblox Studio) is separate.

## Scope

- Blender modeling, vehicles, props and modular environments, UVs/skins, HQ / GAME / optional MOBILE.
- Rarity and art direction, native Roblox VFX handoff and audio/SFX handoff, loaded as needed.
- 20,000 triangles per individual standard Roblox mesh is an import constraint, **not** a performance benchmark.
- Read-only audits, GAME export inspection, honest `PASS/FAIL/UNVERIFIED` reporting.

## Verify

From this skill directory:

```bash
python scripts/validate_skill.py
python -m unittest discover -s tests -v
blender -b asset.blend --python scripts/audit_blender.py -- --collection Vehicle_GAME --output asset-audit.json
python scripts/audit_glb.py path/to/Vehicle_GAME.glb --strict --output reports/glb-audit.json
```

These scripts cannot certify actual Roblox Studio import or runtime rendering. This module is copied for independent installation; keep future upstream fixes synchronized deliberately.

See [CHANGELOG](CHANGELOG.md) and [LICENSE](LICENSE).
