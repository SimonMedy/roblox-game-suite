# Cinematics, animation and camera direction

Use for MVP podiums, intros, replays, item reveals, characters, animated props and environmental sequences. Coordinate with asset, VFX/audio, gameplay and UI specialists when available; preserve the game's mechanics and competitive readability. **A camera screenshot cannot validate motion.**

## Motion language

- Choose intentional motion: anticipation → action/impact → optional overshoot → settle. Use eased timing, arcs/splines or damped springs where they improve weight; linear motion and `TweenService` are valid for deliberate simple moves. Avoid generic constant-speed camera tours.
- For per-frame procedural animation, use elapsed `dt` (e.g. `alpha = 1 - math.exp(-response * dt)` for exponential smoothing, with sensible bounds). Never use a constant interpolation fraction per rendered frame and assume equal behavior at 30/60/120 FPS.
- Curved camera paths, damped look-at and subtle secondary movement can add life; keep camera shake/noise optional, slight and accessibility-aware. Prevent clipping, motion sickness and poor subject framing.

## Shot design: MVP example (adapt to game)

- **Reveal:** quick readable wide/low-angle establishing shot; communicate stadium and podium scale.
- **Hero:** focused shot of winning vehicle/avatar, deliberate FOV/framing and optional restrained depth of field. Narrowing FOV changes perspective; it is **not** optical compression by itself without camera repositioning.
- **Peak → settle:** celebration pose/vehicle movement, synchronized VFX/audio and clear name/score UI with negative space. Avoid hiding the winning asset or ball/gameplay cues.
- A ~4–6 s sequence is an **example pacing target**, not a Roblox rule. Adapt to game flow; make it skippable or provide reduced-motion options when appropriate. Test different screen aspect ratios, mobile safe areas and UI scale.

## One timeline, clear ownership

- Coordinate camera, rig tracks, lights, VFX, SFX and UI using **one local scene timeline** with named markers (`Start`, `Reveal`, `Peak`, `Settle`) and elapsed-time state; use event markers from `AnimationTrack` when rig animation timing is authoritative.
- Avoid independent drifting `task.wait` chains. Use shared monotonic scene time, idempotent transitions and guard against replay/late asset loading; exact same-frame audio/visual synchronization is **not guaranteed**. Verify audiovisual timing in Studio.
- Server decides authoritative match results, MVP selection and allowed cosmetic data; clients present camera/UI and local-only effects. Validate network messages and permissions; replicate only gameplay state/events that genuinely need replication. Local presentation must not award points or change physics.

## Animate with the right tool

- **Blender via Blender MCP** when available: complex 3D rigs, mechanical keyframe animation and authoring/editing intricate character motions. Verify rig/export/import compatibility; Blender motion is not automatically a playable R15 `AnimationTrack`.
- **Roblox Studio and Studio MCP:** rig/Animation Editor, `Animator:LoadAnimation` and `AnimationTrack` for imported or authored compatible rigs (R15 and custom rigs); preview all key poses, transitions, priorities, contact and loops. For difficult dance/acrobatic motion, use suitably licensed motion references/capture and retarget/clean rather than inventing untested Euler-angle sequences.
- **Client-side Luau:** procedural camera, suspension, springy accessories, arena lights and other local presentation. Use render-step updates only for visible camera/per-frame work; other timing may use appropriate simulation/update loops. Prefer Studio's `Animator` to stacking tweens on animated joints. Verify `Motor6D.Transform` timing/ownership if used.
- **3D environment:** animate only intended moving pieces; keep collisions, server-owned interactions and navigation independent of decorative animation. For complex set pieces, use appropriate rigs/constraints or keyframes rather than hundreds of unrelated tweens.

## MVP lifecycle and cleanup

- Use dedicated visual clones/stand-ins for podium cars/avatars so a winner disconnecting does not destroy the scene. Handle unavailable cosmetics/assets with safe defaults; clone only authorized content.
- Before taking camera control, preserve `CameraType`, `CameraSubject`, `FieldOfView` and any camera controller/GUI state actually touched. Track locally created post-effects/lighting overrides and previous values. Restore via one **idempotent cleanup** on completion, skip, character respawn, disconnect, new round or error; disconnect event listeners, unbind render callbacks, stop tracks and destroy clones.
- If modifying shared `Lighting`, design reversible and isolated effects; local-only post-processing is preferable where appropriate, and changes must not leak to other players or subsequent rounds. Avoid fighting the default camera scripts.

## Cinematic PASS / FAIL / UNVERIFIED

- **FAIL:** unintentional robotic motion or refresh-rate-dependent smoothing; camera clips scenery/crops hero, UI hides focal point, excessive shake/flashing, missed audio/VFX beats, or broken screen framing.
- **FAIL:** R15/custom rig foot sliding, joint twisting, broken contacts/loops, poor retargeting; visuals alter authoritative gameplay; podium breaks on disconnect, skip or respawn; camera/post-effects/UI/callbacks are not restored.
- **UNVERIFIED:** any motion, timing, Studio integration, mobile layout, accessibility, disconnect or multiplayer test not actually performed. Screenshots and static previews alone are insufficient.
- **PASS:** only after real playback, interruptions/cleanup, target-camera/aspect-ratio review and applicable multiplayer/device checks. Deliver clip or capture, tested conditions and outstanding issues.

Official APIs: https://create.roblox.com/docs/reference/engine/classes/Animator · https://create.roblox.com/docs/reference/engine/classes/RunService · https://create.roblox.com/docs/workspace/camera · https://create.roblox.com/docs/animation
