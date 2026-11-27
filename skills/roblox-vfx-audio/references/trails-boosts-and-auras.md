# Trails, boost continuity and entity auras — Studio QA

Load when building motion trails, volumetric boosts or ball/character auras. These are **testable patterns**, not mandatory implementations or fixed presets. SideRush findings are agent-reported; unavailable local screenshots/code and claimed pixel-perfect measurements are not independently verified here.

## UV direction: test before reauthoring

- `Beam` and `Trail` use surface/ribbon texturing. Do **not** assume that the horizontal orientation of the authored image maps to travel direction; the appearance depends on UV mapping, attachment order, camera and `TextureMode`/`TextureLength`.
- In Studio, start with an asymmetric **U/V diagnostic texture**: a labeled arrow along each texture axis, distinctive start/end colors, and a non-square marker. Apply it separately to `Beam` and `Trail`; inspect the live ribbon with motion, attachment reversal and different camera views. Capture proof of which source axis runs along the length and which across width. Rotate/repack the artwork **only after** the mapping is confirmed.
- Check each supported `TextureMode` against documented `TextureLength` behavior and the intended repeat/stretch pattern. Inspect for horizontal stripes, repeated square tiles, stretched ellipses, inverted gradients and seams. Never hardcode one TextureLength for every asset.

## High-speed boost and exhaust continuity

- Test exhaust during high speed, variable `dt`, aerial drift, fast camera pans and abrupt stops. A world-attached `Trail` plus separate nozzle `ParticleEmitter` can create an unintended **fork/V-shaped silhouette** or disconnected puffs when paths diverge.
- Choose coherent attachment space and visual ownership. If discrete particles leave gaps at high speed, consider **distance-based substeps**: interpolate positions between previous/current nozzle transforms and emit at bounded spacing, with a capped per-step budget. Clamp large frame gaps, handle teleports/spawns and reset previous transforms on release. Avoid assuming an arbitrary fixed count of interpolation samples solves every speed.
- Real-time ribbon geometry and particles can be combined, but inspect their relationship during turns; reducing a fork may require changing the art layout or one layer, not adding more particles.
- For authored volume boosts, test silhouettes on daylight and dark maps using intentional key/rim light, visible internal shadow and controlled color/opacity. Cycles `Principled Volume`, `LightEmission` and nozzle roll are **artistic choices**, not universal numeric recipes. Validate imported alpha, contrast and client overdraw.

## Entity / ball aura layering

- A hybrid aura can use subtle `Highlight` to preserve the subject silhouette, camera-facing `HaloSprite`/GUI elements for readability, and controlled `PointLight`, meshes, seams or particles for depth. Prioritize readability of the actual ball or character; check Bloom enabled/disabled, daylight, mobile and accessibility. Do not prescribe one `FillTransparency` or `LightInfluence` for every game.
- For world-space `BillboardGui`, test `Adornee` rotation, parent transforms and camera position **both at screen center and corners**. If rotation causes unwanted drift, compare an independently positioned, non-rotating anchor against direct attachment, while preserving the actual target world position. Do **not** claim all rotating `BasePart` adornments are intrinsically broken or that one anchor guarantees subpixel error.
- Define which visual cue supersedes/interrupts previous cues for repeated effects. Prevent stale `Highlight`/trails/billboards; pool when useful, detach idle callbacks and reset every layer on release.

## Studio acceptance

- Check all asset references (nil/blank/missing), effect visibility, UV direction and texture readiness; then run rapid repeated cues, spawn/despawn, camera pans, high-speed movement and target rotation.
- After effects expire, assert **no leaked active billboard, highlight or trail**, but also visually inspect for stutters and artifacts. Instance counts and script assertions are not GPU/render validation.
- Report separately: **PASS Studio**, **PASS actual device**, **FAIL** with screenshot or reproduction steps, or **UNVERIFIED**. Preserve measured conditions (device, refresh rate, scene, graphics mode and load).

Roblox references: https://create.roblox.com/docs/reference/engine/classes/Trail · https://create.roblox.com/docs/reference/engine/classes/Beam · https://create.roblox.com/docs/reference/engine/classes/Highlight · https://create.roblox.com/docs/reference/engine/classes/BillboardGui
