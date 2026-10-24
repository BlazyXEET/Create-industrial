# Welder model sources

**Default model: orange reference design (V24).** This uses the user's Oct 24 orange-and-black Welder screenshots as the target silhouette: bright orange rectangular grip, graphite top, pale steel left-facing welding tip, and black rear lever. The actual in-game model is `src/main/resources/assets/createindustrial/models/item/welder_3d.json`.

## Editing / generating

- `python tools/generate_welder_orange.py` rebuilds the 3D Minecraft JSON and the 12 original 16x16 material PNGs, and optionally exports `art/welder/welder-orange-reference.glb` for editing in Blender. No Blender installation is needed to run the exporter; the GLB can be imported into Blender.
- `python tools/make_welder_flat_icon.py` restores the **exact supplied 16x16 icon**, from `reference-welder-icon-16x16.png`.
- `welder.json` selects 3D or 2D; **do not delete it**. On Windows use `USE-3D-WELDER.cmd` or `USE-2D-WELDER.cmd`. Java/gameplay behavior is unchanged by model switching.
- `python tools/make_welder_orange_3d_pack.py` packages the orange look as a cosmetic resource pack for an existing installed mod.
- `welder-v23-create-industrial.glb`, `welder-teal-v7.glb` and `models/item/welder_v23_teal.json` remain archival material. `python tools/generate_welder_v23.py` regenerates only the archived teal model, never the new default.

The GLB is an editable model reference, **not a Minecraft JAR**. Minecraft uses item JSON and its actual 16x16 PNGs. Inspect first-/third-person transforms in Minecraft before declaring the hold pose finalized.
