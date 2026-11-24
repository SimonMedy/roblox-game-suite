# Changelog

## 0.1.6 — 2026-11-24

- Incorporated SideRush Voidstorm v2 Studio-PC feedback into native VFX QA: calibrate `LightEmission`/Bloom across bright and dark arenas; `0.45` is project evidence, never a universal setting.
- Added Studio MCP/Open Cloud upload-directory permission and eventual asset availability checks, without promising a fixed CDN delay.
- Clarified performance reports: compare frame times and tails under representative load; identical capped FPS does not prove zero overhead. Mobile/online multiplayer remain unverified in the reported SideRush test.
- Kept Garage/ViewportFrame fallback, both VFX references, compact skill routing and other specialists unchanged.

## 0.1.5 — 2026-11-24

- Added an in-project SideRush lesson: Garage/shop `ViewportFrame` previews must not assume `ParticleEmitter`/`Beam`/`Trail` render like Workspace VFX; use a time-driven GUI atlas preview (`ImageLabel.ImageRectSize`/`ImageRectOffset`) where appropriate.
- Require separate Garage and gameplay playback checks, plus honest `UNVERIFIED` labeling before real Studio tests. No changes to the standalone asset skill or the experimental Blender baking pipeline.

## 0.1.4 — 2026-11-24

- Added a compact pipeline selection guide in `roblox-vfx-audio/SKILL.md`: native/3D for reactive or multi-angle effects, baked flipbooks for short camera-facing bursts, hybrid for layered results.
- Noted that side-on 2.5D views favor predictable flipbook framing but do not guarantee mobile FPS; preserved two separate lazy-loaded references, existing QA and all other skills.

## 0.1.3 — 2026-11-24

- Added lessons reported from a real Blender Voidstorm 4×4 flipbook prototype: controlled Transparent/Emission shader mixing, premultiplied-alpha downsampling and noise-range/erosion checks; kept these as conditional guidance, not universal rules.
- Clarified that `ParticleEmitter` **OneShot ignores `FlipbookFramerate`** and plays over `Lifetime`; real Studio playback, multiplayer and mobile performance remain `UNVERIFIED`.
- Marked Blender-side prototype as externally reported rather than independently reproduced. No changes to other skills or audit code.

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
