> **Historical V19 documentation:** The Laser Printer and dedicated furnace ports are retired in V20. Consult [current V20 documentation](V20-SEAMLESS-FOUNDRY.md).

# Create: Industrial V19 — Pixel Art, Laser Printer & Basin Steel

**Status:** source-only development changes applied to the V18 baseline. Minecraft runtime, Blender scene save, and a full Gradle JAR build still need verification in a configured development environment. This is not a release claim.

**Targets:** Minecraft Java 1.21.1 · NeoForge 21.1.257 · Create 6.0.10-280 · Java 21.

## What's changed

- Reauthored all 124 existing source PNG textures as restrained, 16×16 RGBA Minecraft pixel art; added 11 new block textures required by the model update. Total: 135.
- Materials keep flat inventory sprites (`minecraft:item/generated`), not custom 3D item meshes. Metal ingots, nuggets, crushed ores, raw ores, silicon, and powders have distinct silhouettes and controlled color ramps. No generated images are used as texture sources.
- Machine casing, brass accents, ore faces, concrete, firebrick, industrial ports, and molten fluids have consistent palettes. All blocks remain Minecraft-scale.
- Laser Printer uses 28 individually authored cuboids, a sealed roof (no black hole), an optical head, a recessed glass front, rails, a wafer stage, Create-style brass details, venting, and matching side shaft collars. Active state has a luminous emitter/focus texture. Existing recipes, Create power and input/output logic are retained.
- Blender-compatible editable GLB is `art/laser_printer/laser-printer-v19.glb`. The shared geometry source lives in `art/laser_printer/geometry.json`. In Blender, run `art/laser_printer/build_in_blender.py` to generate `laser-printer-v19.blend` and textured `laser-printer-v19-textured.glb`; Blender was unavailable in the source-generation environment, so this output is not pre-rendered or labeled as a tested `.blend` file.
- Steel Converter is **retired from new gameplay**. It has no crafting recipe and is not displayed in the creative tab. Its block ID, block entity, legacy fluids and existing world save behavior are intentionally retained so old saves don't lose those blocks. A separate future world migration could eliminate the legacy classes entirely after an explicit migration strategy is in place.

## Steel — superheated Create Basin refining

This deliberately simplified **basic oxygen steelmaking** gameplay abstraction uses the existing blast furnace to make carbon-rich pig iron and a mechanically mixed superheated basin to remove excess carbon/impurities with flux and recycled iron. Create's mixing process stands in for oxygen/air agitation; it does **not** simulate real dissolved oxygen chemistry or oxygen mass flow.

Set up a powered **Mechanical Mixer** above a **Basin** with a **superheated Blaze Burner** below it. Supply:

| Input | Amount | Purpose |
|---|---:|---|
| Molten pig iron from Blast Furnace | 576 mB | Carbon-rich base metal (equivalent to 4 ingots at 144 mB each) |
| Calcite | 1 | Limestone/calcium-carbonate flux |
| Iron nuggets | 2 | Scrap iron/dilution material |

Outputs:

| Output | Amount | Further processing |
|---|---:|---|
| Molten steel | 576 mB | Compact in a Create Basin/Press: 144 mB → 1 steel ingot |
| Molten slag | 144 mB | Existing slag-casting recipe |

The recipe is `src/main/resources/data/createindustrial/recipe/mixing/steel_refining.json`. Cold or merely heated Basin mixing must not perform the recipe. **No new Steel Converter block is required.** Complete the processing chain with Create item and fluid automation and filtered fluid outputs. Route steel/slag out of the Basin with a filtered drain or appropriately separate storage to avoid blockages. The recipe uses Create's own mixing serializer and the existing molten metal fluids.

### Game balance and realism constraints

- Pig iron is made through iron reduction with carbon; steelmaking should *remove or control* carbon instead of producing steel merely by adding charcoal to iron.
- Actual blast/basic-oxygen steelmaking typically uses controlled oxygen input and flux and produces slag. Create's Mixer is a stylized abstraction, not a simulation of a BOF.
- Existing cast-iron and steel recipes, item tags, and machine progression remain compatible.
- Avoid introducing a new oxygen system until it has actual gameplay use and isn't just a pointless extra ingredient.

## Maintenance

The new source of truth is:

```text
python3 tools/generate_v19_textures.py
python3 tools/generate_laser_printer.py
python3 tools/run_offline_checks.py
```

`tools/generate_refining.py` now reruns the V19 art/model generation and restores the basin recipe; it does not resurrect converter crafting. `tools/generate_clean_art.py` is retained only for backwards-compatibility but delegates direct runs to V19.

In an online Minecraft development environment:

```text
./gradlew clean build runGameTestServer
./gradlew runClient -PassetAudit
```

On Windows use `gradlew.bat` instead of `./gradlew`. Then verify shaft animation, side connection, model face/collision consistency, real Laser Printer item insertion/extraction, steel/slag fluid output separation, game reloads, dedicated server loading and multiplayer. These checks **were not run here** because the Gradle distribution/dependencies and Blender executable were unavailable. This package contains *source*, not an unverified newly compiled JAR.
