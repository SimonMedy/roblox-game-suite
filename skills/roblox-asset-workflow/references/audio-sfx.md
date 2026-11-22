# Game audio and SFX (supporting asset workflow)

An asset/code agent can design cues, generate or process simple synthetic layers (e.g. Python DSP), edit loops and specify Roblox audio integration; this does **not** replace skilled music composition, sound design or in-game mixing. Use licensed/original audio only; verify upload permissions.

- **Three-phase events:** clear `Attack` transient → click-free `Loop` (zero crossing/crossfade) → smooth `Release`. For boosts, test activation, sustained use, interruption and stop in Studio.
- **Variation:** bounded randomized pitch/volume and multiple samples reduce repetition; preserve cue recognition and avoid volume spikes.
- **Hierarchy:** protect essential competition cues (ball, impacts, boost status, UI) above cosmetic flourishes. Higher rarities may have memorable sonic signatures, not simply louder audio.
- **Spatial mix:** choose 2D UI or positional 3D playback intentionally; check attenuation, overlapping players, clipping, accessibility, mobile speakers and consistent loudness.
- **Music:** use only if it benefits the scene, keep gameplay cues intelligible and respect licensing. Never claim to have composed or tested a track without a real artifact.
- **Handoff:** provide source/licensing, formats, cue naming, trigger/state map, loop points, gain/pitch ranges and what was actually auditioned in Roblox.

Docs: https://create.roblox.com/docs/sound and https://create.roblox.com/docs/reference/engine/classes/Sound
