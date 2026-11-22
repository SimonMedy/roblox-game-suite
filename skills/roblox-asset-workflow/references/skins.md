# Skins, color customization, paint masks and animation

Prepare assets for future cosmetics **without requiring a complete customization system now**.

## In Blender

1. UV-unwrap paintable surfaces deliberately: consistent texel density, low-distortion patches, seams off prominent areas. Keep editable texture layers and a UV template when useful.
2. Keep paint, glass, trim and light zones addressable by material or mesh **when functionally necessary**; prefer neutral paint-friendly albedo and primary/secondary tint masks.
3. Keep original artwork separate from baked texture maps. Bake Blender-only shaders to Roblox-supported maps; preserve UV interfaces between versions.

## In Roblox (game integration is separate)

- **Live paint:** use `SurfaceAppearance.Color` on a suitable ColorMap, or `SurfaceAppearance.AlphaMode = Enum.AlphaMode.TintMask` with ColorMap alpha for selective tint. Validate actual tint and unaffected glass/trim in client.
- **Static liveries:** provide UV-aligned ColorMaps/variants with cross-panel seam continuity. Keep the original templates editable.
- **PBR finish:** verify metalness, roughness, normal and albedo after Studio import; Blender shader graphs do not transfer wholesale.

## Native emission on UV-mapped meshes

- `SurfaceAppearance.EmissiveMaskContent` is a pre-authored grayscale mask; Roblox uses its **red channel** for intensity. Its map content is protected by **PluginSecurity**: configure in Studio/authorized tooling, use preconfigured `SurfaceAppearance` variants, or investigate `AssetService:CreateSurfaceAppearanceAsync` with its actual permissions and content requirements. Do **not** assign the map content from an ordinary runtime script.
- `EmissiveStrength` and `EmissiveTint` **are runtime-scriptable**: animate a **fixed** mask's intensity/tint across `Idle → Move → Boost`, without necessarily adding a separate `Neon` mesh. These properties do **not** scroll the mask; no guaranteed draw-call count.
- Emission is modulated by the ColorMap/albedo: keep intended tintable emissive zones light/neutral. Avoid strength values that clip to white; review actual lighting, Bloom, color fidelity and mobile output.

## Choose motion by effect, not by trick

- **Pulsing/recoloring accents on a fixed UV pattern:** preconfigured `SurfaceAppearance` emissive mask plus script-controlled strength/tint.
- **Scrolling energy lines:** `Beam.TextureSpeed`, a `Trail`, or dedicated animated geometry along the intended path.
- **Moving mechanical/energy parts:** separately animated 3D meshes with correct pivots.
- **Full-body flowing galaxy/waves:** no arbitrary custom shader support; prototype on the actual curved car with performance measurement and a static fallback. `EditableImage`-based updates need a permissions/performance check.
- **Avoid the wrong mapping:** a `Texture` instance's `OffsetStudsU/V` animates tiled surface textures; it does **not** animate the Blender UV atlas used by `MeshPart.TextureID` / `SurfaceAppearance`. Do not rely on it for seam-aligned, scrolling custom car liveries.

## QA and handoff

Test two paint colors, a cross-panel livery, UV checker and emissive `Idle/Boost` states at match-camera distance and in close-up. Inspect stretch, color clipping, seams and unaffected glass/trim. For moving patterns, validate one measured prototype before scaling; deliver a static fallback.

Report which masks, materials and effects are **prepared**, **implemented in Studio**, or **tested on target clients**.

Sources:
- https://create.roblox.com/docs/reference/engine/classes/SurfaceAppearance
- https://create.roblox.com/docs/reference/engine/classes/AssetService
- https://create.roblox.com/docs/art/modeling/surface-appearance
- https://create.roblox.com/docs/parts/textures-decals
