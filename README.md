# Roblox Game Suite

**A portable, progressive Agent Skills collection for building and verifying polished Roblox game experiences.** Skills are separate, discoverable modules; no oversized router prompt.

## Install

```bash
npx skills add SimonMedy/roblox-game-suite --skill '*'
```

Select individual skills through the installer, or target a specific one with `--skill roblox-asset-workflow` (replace with the desired skill name). Node.js and a compatible agent are required. **Blender, Blender MCP and Roblox Studio MCP are not installed by this package.** Agent-specific skill discovery and installation must be verified on the target client.

## Available skills

| Skill | Activate for | Status |
| --- | --- | --- |
| [`roblox-game-director`](skills/roblox-game-director/SKILL.md) | Product vision, playable vertical slices, coordination, handoff and cross-domain quality | Initial workflow; needs live game-production trials |
| [`roblox-asset-workflow`](skills/roblox-asset-workflow/SKILL.md) | Blender models, vehicles, UVs, cosmetics, skins, Roblox-ready exports, geometry audits | Based on standalone asset workflow **v3.2.0** |
| [`roblox-vfx-audio`](skills/roblox-vfx-audio/SKILL.md) | Roblox-native particles, auras, boosts, flipbooks and SFX | Initial focused workflow; needs Studio/device trials |

**Not yet included:** `roblox-gameplay-luau` or standalone UI/networking modules. They will be developed after real-world tests rather than populated with generic instructions. The director does not itself write, run, deploy or test an entire game without compatible tools.

## Production approach

1. Define playable core mechanics, player experience, performance targets and non-negotiables.
2. Produce **one playable vertical slice** instead of generating the entire feature list at once.
3. Use specialists as needed and preserve their local QA: geometry/import for assets; visuals/overdraw for VFX; source/licensing and mix for audio.
4. Integrate and test gameplay, state connections, camera readability, concurrent players and mobile targets. Report `PASS / FAIL / UNVERIFIED` truthfully.
5. Expand only after the slice demonstrates the intended quality. New subsystems should be informed by actual project failures, not filler documents.

For example, a Voidstorm wheel prototype needs the asset skill for mesh/UV/pivots, VFX skill for glow and particles, and the director for end-to-end acceptance (visual identity, boost-state handoff and match-camera checks). Cosmetics must not change existing vehicle physics unless expressly authorized.

## Provenance and updates

The asset specialist is copied/derived from [SimonMedy/roblox-asset-workflow v3.2.0](https://github.com/SimonMedy/roblox-asset-workflow/releases/tag/v3.2.0). The standalone repo remains the **source of truth for its specialized rules and audits**. The suite contains self-contained files for installation and runs checks for drift when updating; do not silently assume both repos are synchronized.

## Verify

```bash
python scripts/validate_suite.py
python -m unittest discover -s tests -v
python -m compileall -q scripts tests skills
```

GitHub Actions runs the same checks on `develop`, pull requests and `main`. This validates package structure and Python utilities, **not** installation in every agent, Blender/MCP operation, Roblox gameplay or device FPS.

MIT licensed; third-party art, music, models and trademarks are not relicensed. See [LICENSE](LICENSE) and [CHANGELOG](CHANGELOG.md).
