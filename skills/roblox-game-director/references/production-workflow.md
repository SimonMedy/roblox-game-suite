# Playable vertical slice: production and acceptance

## Brief and design

Define the core fun hypothesis, user actions, failure/success loop, expected camera and game modes. Identify must-have vs later features, player-facing differentiators, technical dependencies and the existing game state. Prefer one concrete playable demonstration over speculative content volume.

## Deliverable and interface map

Record owners and interfaces per feature: `Input → authoritative gameplay state → visuals → audio → persistence if applicable`. Cosmetics must not change physics/competitive hitboxes. Use stable named attachment points and feature state contracts (`Idle`, `Move`, `Boost`, `Impact`) only where those states actually exist. Coordinate required client/server boundaries; don't trust client-provided rewards, purchases, speed or hits without server validation.

## Gate by evidence

- **Gameplay:** player controls, objective/feedback and multiplayer correctness; no accidental existing mechanic changes.
- **Art:** silhouette, rarity tier/collection identity, gameplay-distance readability, GAME export and UV/material correctness.
- **Effects:** emission, alpha edges, flipbook loops, occlusion and competition readability; clean performance at expected concurrency.
- **Audio:** intelligible critical cues, attack/loop/release, comfortable mix and correct licensing.
- **Quality:** client/server logs, tested devices, expected number of equipped players, performance delta from baseline and regression checks.

Use `PASS` only for observed verification, `FAIL` for reproducible defects and `UNVERIFIED` when Roblox Studio/client access or target devices are unavailable. A preflight script is not an import, and a single preview is not a multiplayer benchmark. Never fabricate FPS, draw calls, memory or test outcomes.

## Completion and iteration

For every slice, report artifact links, screenshots/previews where available, implementation vs concept status, remaining integration tasks, local tests, real Studio/device checks, known issues and what may be expanded next. Stop and request approval before altering protected gameplay mechanics, monetization rules or other consequential user decisions.
