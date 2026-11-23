# Experimental 3D → flipbook bake (Blender / Niagara → Roblox)

**Status: unproven in this suite.** Use only for effects that benefit from a baked, camera-facing sequence (stylized explosions, impacts, smoke, vortex detail); keep multi-angle waves, vehicle-attached forms and gameplay-reactive effects in native `Beam`/`Trail`/`MeshPart`/emission as needed. This is an **optional production route**, not a quality or performance guarantee. See [native VFX](vfx-roblox.md) for regular authoring and QA.

## One hero-effect trial

1. **Reference and design:** study authorized video/key frames for timing, volume, color and secondary layers; reconstruct original art, do not copy proprietary frames. Choose viewpoint, camera distance and intended `one-shot` vs loop. Hard cuts, three-tone cel shading and lumpy/eroded edges are *style options*, not mandatory.
2. **Author in Blender first when available:** Blender MCP / `bpy`, EEVEE, materials, geometry and particles/simulations as appropriate; Niagara Flipbook Baker is an alternative **if Unreal is already accessible and materially useful**. Automate frame-accurate capture only after the effect actually renders. Bake/cache simulation state when seeking frames would change its result; preserve source files and settings.
3. **Render RGBA:** fixed camera, lighting, scale, orthographic framing if suitable, transparent film and consistent color management. Inspect *straight vs premultiplied* alpha, RGB fringes and additive/emissive halos against both light and dark backgrounds; transparent film alone does not guarantee correct glow. If native transparency is unusable, controlled black/white matte reconstruction may help with ordinary alpha compositing, but is not a universal solution for additive/Bloom effects.
4. **Select frames:** use deterministic spacing and identical crop/pivot/margins. Discard an initial warm-up frame **only if contaminated**; for loops, prefer actual periodic animation or test a controlled boundary blend. Keep source frames editable. Check frame order, temporal aliasing, opacity and silhouette throughout motion.
5. **Pack and import:** arrange a supported `ParticleEmitter.FlipbookLayout` grid (`Grid4x4`=16, `Grid8x8`=64; other layouts when appropriate). At 1024², individual cells are 256² or 128² respectively: balance sharpness, duration, frame rate and texture memory. `FlipbookFramerate` has an engine-supported maximum of 30 FPS; check current docs. One-shot sequences longer than a sheet need a validated playback strategy, **not** an assumed automatic multi-sheet chain.
6. **Integrate in Studio:** verify `Size`/world-scale and floor contact empirically, brightness/Bloom, correct orientation as camera or object moves, seams, camera occlusion, effect timing, and interaction with 3D meshes/Beam/Trail. Profile transparency overdraw, frame time and memory with representative concurrent players/mobile. Flipbooks may be restricted on low-memory devices; provide a reduced/native fallback.

## Gate and evidence

- **PASS:** source scene + PNG frames/sheet exist, RGBA and spacing inspected on light/dark backgrounds, actual Roblox Studio playback and match-camera/multi-angle results checked; runtime/device performance passed when applicable.
- **FAIL:** square edges/halos, clipped geometry, frame-order or loop jump, visibly flat critical 3D effect, bad floor contact, unreadable gameplay, severe overdraw or lost visual identity on fallback.
- **UNVERIFIED:** any bake, Studio import, animation, mobile or multiplayer check not performed. Do **not** claim a working Blender/Niagara automated pipeline based only on this document.

Docs: https://docs.blender.org/manual/en/latest/render/cycles/render_settings/film.html · https://dev.epicgames.com/documentation/en-us/unreal-engine/niagara-flipbook-baker-quick-start-guide-in-unreal-engine · https://create.roblox.com/docs/reference/engine/classes/ParticleEmitter
