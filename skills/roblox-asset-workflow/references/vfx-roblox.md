# Roblox VFX: readable, authored, measured

Use for boosts, auras, trails, impact bursts, powers and rarity signatures. Aim for clear visual intent, controlled timing and in-game readability—not particle quantity.

## Build a readable stack

- **Anchor:** a darker shape or contrast layer; `ParticleEmitter.LightEmission = 0` can preserve dark tones.
- **Core:** a restrained bright focal element; `LightEmission = 1` can yield a luminous/additive look, but tune for the game's Bloom and lighting.
- **Detail:** a few secondary sparks/arcs/debris; use negative space so the ball, car outline and scene remain visible.
- **Timing:** explicit onset/peak/dissipation using `NumberSequence` / `ColorSequence` for size, transparency and color. Avoid a constant bright cloud.

These are **design starting points**, not required values or Roblox performance caps.

## Native building blocks

- `ParticleEmitter`: sprites, burst effects and flipbooks (`Grid2x2`, `Grid4x4`, `Grid8x8`, or supported custom layouts).
- `Beam`: path-bound animated energy; `TextureSpeed` scrolls along its attachments.
- `Trail`: motion streaks; verify trail lifetime, width, attachment alignment and motion.
- `MeshPart`: rings, arcs, cones, swirling cores or rigid geometry; use local pivots and test shading/materials.
- `SurfaceAppearance`: fixed emissive masks with scriptable tint/strength (see [skins](skins.md)).
- Hybrid 3D meshes are **not automatically cheaper** than particles. Geometry, transparency, draw calls, render order and updates all matter.

## Sprite and flipbook pipeline

- Generative images may help **explore** shape language; reconstruct, edit and validate sprites rather than shipping raw AI artifacts as final textures.
- Deliver genuine RGBA alpha, no opaque rectangular background or unintended color fringes. Fade outer pixels to alpha 0 for soft sprites; keep deliberately hard edges only where intended.
- Author neutral white/grayscale color for tintable effects driven by `ColorSequence`; keep color artwork only when deliberate.
- Align frames on an exact grid using deterministic tools (Python or Blender orthographic renders); match cell size, pivots and margins, verify playback timing and seamless loop **if looped**.
- Test against bright/dark backgrounds at the actual camera scale; watch for square borders, jump cuts, banding and overbright clipping.

## Real-game performance

- Profile **representative concurrent equipped players**, e.g. 6–8 vehicles if that matches the game's expected player count (example, **not a Roblox limit**).
- Evaluate frame times, transparent overdraw, draw calls, particle lifetime/rate, stacked transparencies and texture memory on target clients. Compare against a baseline in Studio and on mobile where possible.
- Define a MOBILE variant with fewer overlapping transparent layers/particles while preserving signature silhouette, color and timing; avoid unnecessary fast flashing.
- Visual QA: inspect Idle/Move/Boost/Impact, front/back/side, camera occlusion, motion and simultaneous effects. Mark unrun Studio/device tests explicitly.

Docs:
- https://create.roblox.com/docs/reference/engine/classes/ParticleEmitter
- https://create.roblox.com/docs/reference/engine/classes/Beam
- https://create.roblox.com/docs/reference/engine/classes/Trail
- https://create.roblox.com/docs/art/modeling/surface-appearance
