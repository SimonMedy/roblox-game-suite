---
name: roblox-vfx-audio
description: Design, prototype and validate Roblox-native visual effects and game audio for auras, boosts, abilities, trails, impact bursts and cosmetic rarity. Use for ParticleEmitter, Beam, Trail, flipbooks, emissive effects, sound cues and mobile VFX optimization.
license: MIT
compatibility: Requires Roblox Studio access for in-engine validation. Blender and image/audio tooling optional.
---

# Roblox VFX & Audio

**Aim:** recognizable art direction, readable motion and clear sound without unnecessary visual/audio noise. Use only supported Roblox components; no imaginary custom shaders or unverified performance claims.

## Load relevant references

- Particles, Beam/Trail, flipbook sprites, emission, performance: [references/vfx-roblox.md](references/vfx-roblox.md)
- SFX, music, cue layering and mix: [references/audio-sfx.md](references/audio-sfx.md)

## Delivery loop

1. Identify camera, gameplay states, user controls, target devices, rarity identity and collision/competitive constraints.
2. Define readable silhouette, timing and sound signature; build one hero effect before making a set. Reuse `roblox-asset-workflow` for involved 3D meshes/UVs where installed.
3. Implement with Roblox-native emitters/geometry and authorized audio; connect effect timing to **actual** client/server state rather than inventing APIs.
4. Inspect real motion in Studio if accessible: alpha edges, flipbook timing, occlusion, overbright Bloom and audibility, then multi-player/mobile performance. Add reduced effects without losing identity.
5. Deliver sources, trigger/state map, attachment hierarchy, visual and audio evidence, measured costs if available, and `PASS/FAIL/UNVERIFIED` for tests. Never report unrun Studio/device checks as successful.
