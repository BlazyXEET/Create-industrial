# Enable or remove the 3D Welder model (no code changes required)

The Welder's item model is **cosmetic only**. Welding, selections, multiblock
assembly, Shift+right-click unwelding, and networking live in Java and are not
changed by choosing a different item model.

## Easiest: disable 3D in an installed game, without rebuilding

Install the optional **CreateIndustrial-Welder-2D-Override-Resource-Pack.zip**:

1. Place the ZIP into Minecraft's `resourcepacks` folder.
2. Enable the pack in Options > Resource Packs. Put it ABOVE other packs that
   modify Create: Industrial's Welder.
3. To restore the original 3D Welder, simply disable the pack.

This changes only the appearance of `createindustrial:welder` and does not
require modifying an installed JAR or deleting model files.

## Easiest for mod developers: double-click the selector script

From the extracted `Source` folder on Windows:

- Double-click **`USE-2D-WELDER.cmd`** to use a simple flat item icon.
- Double-click **`USE-3D-WELDER.cmd`** to restore the orange 37-part 3D model.

Both require Python 3, which is already required for the offline tests and
GitHub publishing helper.

Equivalent commands:

```powershell
python tools/switch_welder_model.py 2d
python tools/switch_welder_model.py 3d
python tools/switch_welder_model.py status
```

Rebuild the JAR after switching. The mode becomes part of the new JAR's assets.
The resource pack is a simpler option for an already installed JAR.

## No Python? Edit ONE line

Open this file:

`src/main/resources/assets/createindustrial/models/item/welder.json`

For **3D**:

```json
{ "parent": "createindustrial:item/welder_3d" }
```

For **2D**:

```json
{ "parent": "createindustrial:item/welder_2d" }
```

Only the `parent` value matters. Leave all Java, registry, and gameplay files
alone. Do not delete `welder.json` itself, because Minecraft uses that path to
find the Welder item appearance.

## Replacing the Welder model with a new one

- Replace or regenerate **`models/item/welder_3d.json`** for the 3D option.
- Replace **`textures/item/welder_flat.png`** for the flat icon.
- The Blender-importable orange GLB is `art/welder/welder-orange-reference.glb`. The earlier teal model is backed up separately.
- You can always revert to the teal V23 appearance with the switch script.

The active orange model is rebuilt by `tools/generate_welder_orange.py`, which writes
`welder_3d.json` without changing the selected mode. The older V23 generator now
writes only `welder_v23_teal.json`, so it cannot restore teal by accident.

## Verification

```powershell
python tools/verify_welder_model_switch.py
python tools/verify_resources.py
python tools/run_offline_checks.py
.\gradlew.bat clean build runGameTestServer
```

The Python checks validate JSON, sprite dimensions, and reversible selection.
Only an actual successful Gradle build and running the Minecraft client can
establish whether rendering and welding work in the game.
