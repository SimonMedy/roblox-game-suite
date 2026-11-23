# Changelog

## 0.1.2 — 2026-11-23

- Added an **experimental**, lazy-loaded Blender/Unreal-to-Roblox flipbook baking reference under `roblox-vfx-audio` (one hero-effect trial; real Studio verification still required).
- Documented transparent RGBA/alpha pitfalls, deterministic frames and loops, 4×4 vs 8×8 resolution, Roblox playback limitations, mobile/performance checks and native 3D fallbacks.
- Kept Niagara optional, Blender preferred when accessible, and the existing native VFX, asset and director rules unchanged; no untested results claimed.

## 0.1.1 — 2026-11-22

- Added lazy-loaded director reference for character, item and environment animation, game cameras, MVP podiums and cinematics.
- Documented purposeful motion, delta-time-safe smoothing, coherent scene timelines, rig versus procedural animation and interruption-safe cleanup.
- Added visual and integration `PASS/FAIL/UNVERIFIED` criteria; pacing and tools are guidance, not invented Roblox engine limits.
- No new placeholder skill, no changes to existing assets, VFX/audio guidance, or Python audit tools.

## 0.1.0 — 2026-11-22

- Established a standalone multi-skill Agent Skills suite with three independent skills: `roblox-game-director`, `roblox-asset-workflow` and `roblox-vfx-audio`.
- Included the existing v3.2.0 asset-production guidance and audit tools without replacing the original repository; added portable suite discovery/structure tests and CI.
- Added a lightweight production director for vertical slices, task coordination and honest end-to-end acceptance.
- Created a VFX/audio specialist based on the native Roblox effects and sound design guidance, with no claim of studio/device validation.
- Deferred gameplay/Luau/UI skills until real tested implementations exist; no empty placeholder skills.
