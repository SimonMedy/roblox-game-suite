---
name: roblox-asset-workflow
description: Create, refine, audit and export original game-ready 3D assets for Roblox using Blender or other available tools. Use for vehicles, props, modular environments, characters, UVs, materials, recolorable or animated cosmetics, optimization and Blender-to-Roblox handoff.
license: MIT
compatibility: Requires an asset creation tool (Blender recommended). Blender MCP and Roblox Studio MCP are optional integrations, not included.
---

# Roblox Asset Workflow

**Aim:** excellent art + editable master + reliable Roblox export. **Creative freedom by default.** Apply technical constraints only when relevant; never trade away an approved design simply to make the task easier.

## Compact contract

- `REF`: Treat user images as design constraints. Match identifiable proportions, volumes and details; resolve unseen angles coherently. For original briefs, invent freely. Never copy protected assets or branding without rights.
- `LOCK`: Preserve accepted silhouette, dimensions and finished regions through revisions; change only what the user requests or what is demonstrably broken.
- `PART`: Separate what must move, swap, tint, glow or animate. Name components and set sensible local pivots; do **not** split every fixed decorative detail.
- `UV`: Prepare usable UVs, editable textures and optional paint masks for future liveries. Never bake replaceable colors or cosmetics irreversibly into geometry.
- `CLEAN`: Inspect rendered output for gaps, shading artifacts, incorrect normals, clipping, z-fighting and unintended openings. Deliberate openings are valid. For enclosed vehicles, use an optional internal magenta light leak test; see vehicles reference.
- `SAFE`: Before destructive changes, preserve an editable snapshot. Retain approved versions, creation scripts and source textures. Prefer `assets/<name>/versions/v01...` plus `exports/<name>/` outside this skill repo; never overwrite the only copy.
- `RBX`: **20,000 triangles max per individual imported mesh**, not per entire asset. Leave margin; check each mesh **after modifiers/triangulation**, plus total triangles, mesh/material count and texture costs. This limit alone is **not** a performance target; avatar/UGC rules can be stricter.
- `VIS`: New models are visual-only unless the host project specifies otherwise. Never silently change established hitboxes, gameplay physics, animation controllers or scripts.
- `VERIFY`: Inspect the actual **GAME export geometry** at macro and gameplay scale, not only HQ; reimport where possible. Apply the export reference's Pass/Fail gate; report untested Roblox/device checks.

## Workflow

1. Read references, brief and existing scene; identify locked features, the intended camera, customisable regions and target platform. Make sensible assumptions when unspecified.
2. Build silhouette/large forms first, then connections, details, materials, UVs and attachment points. Prefer Blender via Blender MCP for authored 3D when available; never substitute crude Studio primitives merely for convenience. Use primitives for blockouts, collision or simple functional geometry. If unavailable, report the limitation and use alternatives only if quality holds; a skill does not install tools.
3. Check close-ups, side/front/rear/top, hidden angles and gameplay-scale renders. Iterate on real defects without redesigning approved work.
4. Preserve the **HQ** editable master. Produce **GAME** Roblox-ready export. Add a **MOBILE** variant only when useful or requested, with stable component names, pivots and skin interfaces across variants.
5. Validate `.glb`/`.gltf`/`.fbx` as appropriate: hierarchy, mesh budgets, transforms, UVs, normals, materials, texture references and retained swappable pieces. Reimport/test in Roblox Studio when available.
6. Deliver source, export(s), previews and a concise audit: changed items, unresolved issues, total and largest per-mesh triangle counts, materials/textures, cosmetic readiness and verified test environment. Never claim performance without measurements.

## Load only the relevant references

- Vehicle / machinery: [references/vehicles.md](references/vehicles.md)
- Surface skins, colors, animated appearances: [references/skins.md](references/skins.md)
- Environments / maps: [references/environments.md](references/environments.md)
- Props, rigs and character-like assets: [references/other-assets.md](references/other-assets.md)
- Cosmetic rarity / collection art direction: [references/rarity-and-art-direction.md](references/rarity-and-art-direction.md)
- Native VFX / flipbooks: [references/vfx-roblox.md](references/vfx-roblox.md)
- SFX / music handoff: [references/audio-sfx.md](references/audio-sfx.md)
- Export, optimization, profiles, import validation: [references/roblox-export.md](references/roblox-export.md)

## Optional shorthand

`REF=<images>; LOCK=<approved parts>; PART=<swappable parts>; SKIN=<none|static|animated>; CAM=<view>; PROFILE=<HQ|GAME|MOBILE|ALL>; EXPORT=<glb|fbx>`

Missing shorthand keys are open choices, **not** permission to skip quality checks. Keep status and final reports concise and truthful.
