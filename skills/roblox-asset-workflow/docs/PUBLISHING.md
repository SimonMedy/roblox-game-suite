# Asset module provenance and maintenance

This module preserves the **12 unchanged source/reference/audit/test files** from `SimonMedy/roblox-asset-workflow v3.2.0`. The suite has a documented local modification to `scripts/validate_skill.py`, making the redundant `README_FR.md` optional; `README.md` is also suite-specific.

Before syncing a newer standalone version:

1. Review the upstream release, changelog and changed files.
2. Copy the updated skill core, scripts, tests and references without breaking relative paths.
3. Update `upstream/asset-v3.2.0.json` (or a new version manifest) for **unchanged** files; record intended local overrides separately.
4. Run suite validation, asset validation, regression tests and skills CLI discovery. Verify Blender/Studio workflows separately.
5. Commit on the suite's permanent `develop` branch; open a PR to `main` and merge only after checks pass.

Do not claim local overrides are byte-for-byte identical to upstream. Keep both repositories installable.
