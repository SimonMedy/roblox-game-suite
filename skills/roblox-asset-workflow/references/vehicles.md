# Vehicles, machines, modular equipment

Apply only when the task involves a vehicle or mechanical assembly.

## Form and design

- Establish the silhouette and wheelbase before microdetails. Match supplied reference angles and dimensions; invent only what is hidden or intentionally open to interpretation.
- Preserve approved design; inspect side/front/rear/top, wheel arches, hood, glass, underbody, seams, lights and spoilers. Prioritize readability at actual gameplay scale.
- Build independent geometry for anything the player or game may replace, animate, tint or illuminate. Keep fixed decorative elements merged only when beneficial for performance.

## Suggested hierarchy (adapt, do not enforce)

```text
VehicleRoot
  Body_Paintable
  Body_Trim
  Glass
  Wheel_FL | Wheel_FR | Wheel_RL | Wheel_RR
  Light_Front_L | Light_Front_R
  Light_Rear_L  | Light_Rear_R
  Interior
  Spoiler (optional replaceable part)
  Mount_Spoiler | Mount_Boost (attachment locators)
```

- **Wheels:** four independently addressable objects. Locate their origins at actual wheel rotation centers; preserve consistent vehicle-local axes. Separate tire/rim/caliper when customization demands it.
- **Cosmetics:** preserve paintable zones, trim/glass/light separation, stable UVs and clear attachment mounts. Swappable parts need compatible transforms and named connection points.
- **Materials:** use Blender materials as editable sources and bake supported PBR textures for Roblox when necessary. Do not rely on Blender-only shader nodes transferring to Roblox.
- **Physics:** an artist's mesh does not define gameplay hitboxes by default. Only the host integration agent with project context should bind visual models to physics.
- **Variants:** align HQ / GAME / optional MOBILE at the same dimensions, root orientation, wheel centers and mount positions. Share compatible skin UVs where practical.

## Subsurf fit and seam QA

- **Fit to evaluated GAME surface, not the control cage:** place/raycast trims, window seals, DRLs and light housings against the evaluated post-Subsurf mesh using Blender's dependency graph (`evaluated_get(depsgraph)`), at the exact GAME modifier/subdivision settings. Inspect in the same coordinate space and recheck exported geometry: smoothing can move the surface enough to create floating or intersecting parts.
- **Avoid T-junctions on continuous Subsurf patch seams:** match corresponding seam vertices/edges one-to-one before welding; `remove_doubles` alone cannot fix 4-to-1 edge topology. Inspect unexpected *internal* open boundaries (for example via BMesh `edge.is_boundary`) on surfaces intended to be joined; independent body panels, vents and deliberate open rims need not share vertices.

## Macro micro-joint pass (on GAME geometry)

Shoot close-ups of all six high-risk areas, not only global three-quarter views:

1. Outer corners of headlamps and taillamps, including lenses and DRLs.
2. Front-lip and rocker ends at wheel arches; check for under-door z-bleed.
3. Lower wheel-arch liners and flat floor: no stray flaps hanging below curved fender edges.
4. Upper/lower fender vents and sharp quarter-window seal tips: no miter spikes.
5. Mirrors from **above and below**: no floating LED strips, stalks or arms.
6. Bumper-to-diffuser seams, exhaust/boost surrounds and reflector fit.

## Intentional cavities and mounts

- **Boost/exhaust/intake openings:** create a genuine recessed cavity with a continuous closed rim/collar and a dark inner chamber or backstop; do not fake an open nozzle with a flat disc or leave an unintended view into empty space. For small *cosmetic* tilt angles, prefer baking the tilt into mesh vertices so exported object rotations remain clean; keep `Mount_*` orientation consistent with actual VFX/particle direction (identity rotation only when it is correct), and verify in Roblox Studio.

## Internal magenta leak test (enclosed vehicles)

- Temporarily make the car interior intensely magenta/emissive or place bright magenta lights inside, darken exterior lighting, and inspect opaque-window seams, A/C pillars, skirts, wheel arches and diffuser from multiple outside angles. Unexpected magenta bleeding through panels reveals possible micro-gaps or flipped faces.
- **Avoid false positives:** keep magenta emitters/test boxes strictly inside the wheel-arch liner enclosures and underfloor cavities; light protruding into an open wheel arch can masquerade as a panel leak.
- Distinguish deliberate vents/transparency from defects. Repeat on **GAME subdivision/export-equivalent geometry**; remove test lights/materials before delivery. This helps find leaks but cannot guarantee complete watertightness.

Before handoff: provide a component inventory and identify which parts are swappable, tintable, emissive, or fixed.
