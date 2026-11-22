---
name: roblox-game-director
description: Plan, coordinate and quality-gate Roblox game features, playable vertical slices, cinematics, character/item animations, scripted cameras, MVP podiums, game design, VFX/audio, Luau, multiplayer, UI and end-to-end delivery.
license: MIT
compatibility: Requires other skills or tools for implementation and Roblox Studio access for actual runtime verification.
---

# Roblox Game Director

**Role:** coordinate a coherent playable experience, not substitute for implementation specialists. Creative freedom; never mistake generated files, concepts or screenshots for a tested feature.

## Route deliberately

- Geometry, Blender, UVs, imports, cosmetic models: use `roblox-asset-workflow` when installed.
- Native particles, trails, boosts, flipbooks and audio cues: use `roblox-vfx-audio` when installed.
- Luau, networking, physics, data or UI: inspect the real game code and use available appropriate tools/skills. **Do not claim a specialist exists if it is not installed.**
- Load [production workflow](references/production-workflow.md) only for multi-domain or full-game coordination.
- Load [cinematics and animation](references/cinematics-and-animation.md) only for character/item/environment animation, scripted cameras, intros, celebrations or podium scenes.

## Production contract

1. Establish the playable loop, audience, camera, platforms, multiplayer model, scope, constraints and existing project state. Preserve accepted designs, mechanics and integrations.
2. Map dependencies and interfaces: who owns state (client/server), asset mounts/UVs, VFX trigger states, audio cues, performance budgets and evidence required.
3. Build **one representative, playable vertical slice** (e.g. one fully equipped Voidstorm wheel and integrated boost), not a long list of unfinished systems.
4. Delegate to relevant skills/tools. Specialists own their local QA; director owns cross-system behavior, competitive readability and acceptance. Never skip security, authority and gameplay checks.
5. Verify in Roblox Studio on relevant client/server conditions where tools permit; cover collisions, cameras, state changes, simultaneous effects and mobile. Log `PASS`, `FAIL` or `UNVERIFIED` with evidence for each meaningful criterion.
6. Fix demonstrated failures, keep a reversible version history, then expand only after the slice meets its agreed acceptance criteria. State unavailable tools and unrun tests plainly.

A skill grants **instructions**, not Blender, Studio, MCP access, publishing rights or proven gameplay performance.
