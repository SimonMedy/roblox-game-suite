# Asset module provenance and maintenance

This module contains the exact v3.2.0 Agent Skill core, eight references, Python scripts and tests from `SimonMedy/roblox-asset-workflow` (the original repository). The module's README documents installation from the suite rather than the standalone project.

Before syncing a newer standalone version:

1. Review the upstream release, its changelog, permissions and all changed files.
2. Copy the updated core, scripts, tests and referenced files into this module without breaking relative paths.
3. Refresh `upstream/asset-v3.2.0.json` into an appropriately renamed versioned manifest (and the snapshot validator) after reviewing each file's Git blob hash.
4. Run suite validation, asset validation, all tests and the skills CLI discovery check. Test actual Blender/Studio workflows separately.
5. Commit on the suite's permanent `develop` branch; open a PR to `main` and merge only after required checks pass. Never delete either repository.

If the suite-specific skills overlap with asset guidance, retain independent installability but avoid conflicting rules. Game Suite's VFX/audio skill may specialize beyond the asset module's original references; do not silently rewrite historical upstream content.
