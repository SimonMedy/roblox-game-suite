# Roblox export and performance rules

Authoritative baseline: https://create.roblox.com/docs/art/modeling/specifications , https://create.roblox.com/docs/art/modeling/texture-specifications , and https://create.roblox.com/docs/studio/importer . Recheck when the platform changes.

## Required checks

1. **20,000 triangles maximum per individual imported mesh**, not per full model; avatar/UGC may impose stricter limits. Count after evaluated modifiers/triangulation; optimize deliberately. Splitting into materials/primitives can change imported object boundaries, so inspect **actual imported MeshParts** too.
2. Geometry: consistent axes, scale and origin; outward normals, no stray objects, stable naming and shading. Check non-manifold only where the design should be closed. Non-unit object scale is a review warning, not a guarantee of failure.
3. **Customizable parts: prefer one material per independently addressable mesh.** A Blender object with multiple materials may become multiple glTF primitives or be split during import; do not depend on importer-generated names or exact splits. Deliberately separate parts with stable names/pivots, or bake compatible regions into an atlas when independent control is unnecessary. Verify the resulting Studio hierarchy.
4. **UVs:** Roblox's texture specs call for a UV set in `[0,1]` for SurfaceAppearance. Check actual exported UV0 and cross-panel skin seams. UVs outside the range can be intentional for tiling elsewhere, but should trigger review; do not silently mark livery-ready.
5. Export `.glb`/`.gltf`/`.fbx` as appropriate; pack supported textures or deliver referenced files, and retain hierarchy/swappable parts. Blender shader graphs and glTF material extensions are not automatically guaranteed to import faithfully. Normal maps need Roblox-compatible tangent-space convention.
6. **GAME visual QA:** render/inspect the **actual export-equivalent geometry at the exact GAME subdivision/modifier settings**; check close-up panel/glass/joint fit after lowering HQ subdivision. Reimport the exported file, then verify in Roblox Studio/client when available. HQ beauty renders alone do not certify GAME.
7. Performance: record total and max per-mesh triangles, mesh/material/texture counts, repeated instances and resolutions. Measure frame time in a representative Roblox scene; the triangle ceiling does not guarantee FPS.

## Blender → glTF → Roblox pitfalls

- **Emission/LED:** a Blender emissive shader or `KHR_materials_emissive_strength` extension might not reproduce identically on import. Roblox has `SurfaceAppearance` emissive controls/maps; set up and test supported emissive properties in Studio. `Neon` on a separately addressable LED is one visual option, **not** mandatory.
- **Axes, forward and size:** Blender and Roblox use different coordinate/up conventions. Check export axis transforms, units and imported orientation/size against a test object in Studio; validate wheel rotation and `LookVector`. Do not hardcode one universal `-Y`/`-Z`/meters-to-studs rule across FBX and glTF settings.
- **UV0 and textures:** make intended livery UVs `[0,1]`, inspect alpha/paint masks, check actual color/normal/roughness/metalness appearance, and ensure textures are embedded or supplied. External texture paths can break when files move.
- **glTF primitives/extensions:** glTF supports multiple primitives per mesh and optional extensions. Review material splits and extension names; *flag for import testing*, do not declare a specific extension unsupported without a verified platform test.
- **Blender MCP viewport hygiene:** after Cycles/batch renders in a live Blender session, restore the user's interactive 3D Viewport to its prior workable shading (or `MATERIAL`/`SOLID`) with overlays on; never leave it stuck in Cycles `RENDERED` unintentionally.

## Output profiles (avoid unnecessary duplicates)

- `HQ`: non-destructive editable Blender master, high resolution/complexity as needed; preserve modifiers, separate components, scripts and source textures. Not necessarily import-ready.
- `GAME`: Roblox export under the per-mesh budget, geometry/detail appropriate at gameplay distance, stable pivots and cosmetics/UVs. Inspect macro shots using these exact settings.
- `MOBILE`: optional lower-cost variation; optimize textures, materials, transparency and hidden faces as well as triangles; keep roots/mounts consistent. Custom GAME/MOBILE switching requires game code; Roblox automatic LOD is a different feature.

## Visual & gameplay Pass / Fail gate

Check **the requested asset in context** at match-camera distance, side-by-side with its rarity lineup where relevant, then inspect close-up. Record `PASS`, `FAIL` or `UNVERIFIED` for each applicable criterion; fix confirmed failures before calling the asset finished.

- **FAIL:** silhouette/effect is unreadable, visually noisy, obscures the ball, clashes with the game's camera, or a requested rarity lacks a recognizable identity. Low-tier items should feel finished, not artificially degraded.
- **FAIL:** visible square sprite edges, broken flipbook transitions or distracting transparent overdraw; inspect actual motion/backgrounds, not just a static concept image.
- **FAIL:** UV distortion, paint seams, emissive-mask stretch or glow blown out to near-white at the intended lighting/Bloom.
- **FAIL:** cosmetics alter established collision, gameplay mechanics or mount function without authorization.
- **UNVERIFIED:** Studio import, concurrent equipped players or mobile/device performance not tested. State exact gaps; never claim production-ready multiplayer/mobile performance from an isolated render. Test a representative scene with the expected player count (e.g. 6–8 only when relevant), not an invented official Roblox cap.
- **PASS:** only when relevant visible checks and available integration tests actually succeed. Deliver evidence (GAME screenshots/captures, import/audit results, test environment) and a concise unresolved-check list.

## Optional read-only audits

Choose the relevant export collection rather than counting the studio cyclorama:

```bash
blender -b PATH_TO_ASSET.blend --python scripts/audit_blender.py -- --collection Vehicle_GAME --output asset-audit.json
python scripts/audit_glb.py path/to/Vehicle_GAME.glb --output glb-audit.json
```

Blender audit excludes hidden meshes by default (`--include-hidden` overrides) and warns for non-unit scale, multi-material objects, UVs outside `[0,1]`, and mesh triangle limits. The Python-only GLB preflight checks primitives, UV0 data, external images and extensions. **Neither script validates actual Studio import, names, appearance, pivots or performance; always verify in Roblox.**

Further docs:
- https://create.roblox.com/docs/onboarding/artists
- https://create.roblox.com/docs/art/modeling/surface-appearance
- https://create.roblox.com/docs/art/blender
