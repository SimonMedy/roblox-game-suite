# Environments, maps, modular architecture

- Start with proportionally correct blockout and target camera(s); preserve gameplay routes, silhouettes and any locked map dimensions.
- Prefer reusable modules for walls, trims, beams, stadium parts, terrain edges, lights and decorations; use shared materials and trim sheets where practical.
- Author curves and joining surfaces deliberately to avoid seams, floating geometry, flipped faces, z-fighting and messy intersections. Not every open surface should be sealed: determine whether it is intentional.
- Separate decorative geometry from collision/navigation volumes when a host game's physics is already defined. Never replace physics with prettier mesh without permission.
- Design composition, lighting, distance layers and readable landmarks before adding microdetail. Spend geometry/texture budgets where the camera can see them.
- Test repeated modules in a representative assembled scene, with actual camera distance, brightness and mobile targets; check draw calls, texture memory and transparency costs, not only polygon counts.
- Provide modular source pieces, naming guide, transform/orientation conventions, export(s), previews, and list of intentional open edges.
