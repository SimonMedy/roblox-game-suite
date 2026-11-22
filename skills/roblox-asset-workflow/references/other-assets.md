# Props, interactive objects, characters and rigs

- Make a model's purpose clear at intended gameplay scale. Preserve its visual identity while preparing functional components for interaction and replacement.
- For a prop: separate hinges, doors, switches, handles, animated pieces and cosmetic inserts **only if** they need independent behavior. Place origins at the intended mechanical pivot.
- For characters or avatars: confirm whether the target is an ordinary game character, skinned rig or marketplace/avatar item. **Avatar/UGC rules can be stricter than the general 20k/mesh limit.** Look up the relevant Roblox specification before proceeding.
- For a rig: stable skeleton naming, sensible bone hierarchy/weights and skinning tests through intended poses; export only supported features. Blender shape keys, custom shaders and every modifier do not transfer automatically.
- Check animations and material appearance *after Roblox import*, not just in Blender. Keep source and rig editable for corrections.
- For items reused extensively: test many instances together and use shared materials and textures.
