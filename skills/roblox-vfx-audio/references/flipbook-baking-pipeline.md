# 3D → flipbook bake (Blender / Niagara → Roblox)

**Evidence:** a Voidstorm 4×4 RGBA prototype was reportedly rendered and inspected in Blender 5.2 by an external agent (16 frames, 1024² sheet). The source scripts and Roblox playback have **not been independently verified here**. Treat Blender-side steps as *tested once, per report*; Studio, multiplayer and mobile as **UNVERIFIED**. Use for baked, camera-facing explosions/impacts/smoke; use native `Beam`/`Trail`/`MeshPart`/emission for multi-angle or reactive effects. See [native VFX](vfx-roblox.md).

## One hero-effect workflow

1. **Art and motion:** inspect authorized references for timing and silhouette; create original art. Flash/hard cuts, three-tone shading and erosion are style choices, not defaults. Decide camera, one-shot vs loop, and gameplay scale.
2. **Author:** prefer Blender MCP / `bpy` / EEVEE where available; Niagara Flipbook Baker is optional. Keep editable `.blend`, scripts, seeds and settings. Bake/cache simulations when arbitrary frame evaluation would change results.
3. **Render transparent RGBA:** fix camera, lighting, framing and color management; inspect both straight and premultiplied alpha on black, white and representative game backgrounds. For transparent/bright effects, a controlled `Mix Shader(Transparent BSDF, Emission)` with explicit opacity worked in the reported Voidstorm test; **do not** assume this node recipe handles all additive/Bloom effects. Check color fringes, clipping and glow. A black/white dual-matte is only a conditional fallback, not universal.
4. **Frames and erosion:** sample deterministically with stable pivots/crop. Inspect occupancy/opacity for **every** frame; evaluate the actual procedural noise range before mapping it to erosion thresholds (normalize/remap when useful). Skip a warm-up frame only if polluted. For loops, favor a periodic source and test seam continuity; blend ends only if visually correct.
5. **Pack:** resize RGB in **premultiplied-alpha space**, then safely unpremultiply if exporting straight-alpha PNG (avoid dark fringes at translucent edges). Verify zero unintended border alpha and test black/white/sky composites. `Grid4x4`=16 cells or `Grid8x8`=64; on a 1024² sheet, each cell is 256² or 128² respectively. Choose based on visual detail, playback duration and device memory—not frame count alone.
6. **Studio playback:** import as `ParticleEmitter.Texture`; test `FlipbookLayout`, `FlipbookMode`, alpha, world size, camera angle and floor contact. **In `OneShot`, `FlipbookFramerate` is ignored**: playback spans particle `Lifetime`; use a fixed lifetime for consistent pacing (16 frames over ~0.73 s ≈ 22 frames/s average). For looping/ping-pong modes, follow their documented framerate behavior/caps; do not assume multiple sheets auto-chain. Measure Bloom, transparent overdraw, frame time, texture memory and concurrent players/mobile; provide an appropriate native/reduced fallback.

## PASS / FAIL / UNVERIFIED

- **PASS (Blender only):** reproducible rendered frames/sheet, good alpha/edges and timing documented, with source and QA previews. A single reported example supports the *technique*, not guaranteed render speed or universal shader settings.
- **FAIL:** square/black fringes, premature empty frames, abrupt unintended loop, broken frame ordering, sprite clipping, wrong scale, unreadable gameplay or unsuitable flatness from off-angle views; correct and rerender.
- **UNVERIFIED:** Roblox Studio playback, real client/device performance, multiplayer, or any other unrun checks. Only mark a full production pipeline validated after observed in-engine playback and applicable performance checks.

Docs: https://create.roblox.com/docs/reference/engine/classes/ParticleEmitter · https://docs.blender.org/manual/en/latest/render/cycles/render_settings/film.html · https://dev.epicgames.com/documentation/en-us/unreal-engine/niagara-flipbook-baker-quick-start-guide-in-unreal-engine
