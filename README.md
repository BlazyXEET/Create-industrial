# Welder 3D Model Can Now Be Turned Off Easily

## Welder appearance — orange reference model

The latest Welder appearance is the user-supplied orange/graphite design, with a
matching exact 16x16 icon. All weld/unweld and multiblock code is unchanged.
Regenerate assets with `python tools/generate_welder_orange.py`. Switch the
model with `USE-2D-WELDER.cmd` or `USE-3D-WELDER.cmd`; see
`docs/WELDER_MODEL_SWITCH.md` and `CHANGELOG-V24-ORANGE-WELDER.md`.


Double-click **`USE-2D-WELDER.cmd`** to disable the 3D item model in the next
build, or **`USE-3D-WELDER.cmd`** to restore it. There is also a standalone 2D
resource pack for toggling the appearance in Minecraft without rebuilding.
Only the item model is changed; Welder and multiblock code is untouched.

- Guide: `docs/WELDER_MODEL_SWITCH.md`
- Changelog: `CHANGELOG-V24-WELDER-MODEL-TOGGLE.md`
- Command-line: `python tools/switch_welder_model.py 2d` (or `3d`)
- One-line JSON selector: `assets/createindustrial/models/item/welder.json`

---

# V24 - Welder GitHub-ready source and multiblock extension API

**Focus:** V23 Welder model + small/large weldable furnaces; legacy content
remains registered for world compatibility but is not expanded here.

- `GITHUB_UPLOAD_GUIDE.md`: step-by-step Windows publishing and tests.
- `Publish-Welder-To-GitHub.ps1`: safe new-branch script; never force-pushes.
- `docs/ADDING_MACHINES.md`: blueprint-based extension API for future weldable machines.
- `CHANGELOG-V24-WELDER.md`: exact changes and verification status.

**Status:** offline tests pass; full Gradle compilation and actual Minecraft
GameTests were unavailable in the authoring environment. Do not call this a
verified release until the script/CI tests and gameplay checks pass.

---

# Welder V23 model upgrade

See `CHANGELOG-WELDER-V23.md` and `art/welder/README.md` for the new 62-part handheld model, 16 pixel-art materials, and Blender-compatible textured GLB. Gameplay remains the Welder/multiblock-focused V22 baseline.

# Create: Industrial — V22 Foundry Reliability Development Source

**Status: SOURCE-ONLY UPDATE, NOT A COMPILED OR GAME-TESTED V22 JAR.**

Minecraft **1.21.1** · NeoForge **21.1.257** · Create **6.0.10-280** · Java **21** · Gradle wrapper included.

V22 builds on V20's portless foundries and Minecraft pixel art and V21's
Welder/multiblock fixes, with stronger machine automation, save-safety and
regression tests. No dedicated port or Laser Printer returns.

## What changed in V22

- Formed fireclay casing and hatch: same item and molten-fluid capabilities on **every** side. Unformed controllers now hide vanilla Hopper slots too.
- Cached Create item/fluid handlers are inert after **unwelding, hatch removal or chunk unload**, preventing stale transfers. Actual stored contents remain for reassembly.
- Unified bounded item/fluid transfer arithmetic; rejects wrong metal, invalid, full and negative requests. Fluid component identity is respected.
- Preserved Welder right-click assembly, Shift-right-click/Shift-left-click undo, all four rotations and saved molten contents. Obstructed blueprint cells now appear **red** in Welder outlines; missing cells remain gold.
- Lazy controller-offset iteration reduces temporary BlockPos allocations during frequent Create logistics lookups.
- Added two runtime GameTests and **640,011** independent Java conservation assertions. Added strict steel Basin/recipe consistency checks.
- The GitHub Actions workflow uploads the development JAR as a CI artifact **after** successful compilation, even if a subsequent GameTest fails. A failing test still fails CI.
- Complete details: `CHANGELOG-V22.md`, `INSTALL-V22.txt`, `docs/V22-FOUNDRY-RELIABILITY.md`.

## What changed in V21

- Small furnace: the true **28-brick hollow-hearth** configuration now matches
  in production code as well as the older 29-brick configuration.
- Both furnace sizes: their *own* molten-surface visuals are accepted by the
  formed-state validator. This prevents spontaneous unwelding after melting.
- Any valid assembled casing or controller supports **Shift + right-click** to
  undo the weld. When the Welder is in the main hand, **Shift + left-click**
  can also remove the weld. For an air cell inside the chamber, hold **Alt +
  Shift + right-click**. Removing a weld keeps the machine contents and bricks.
- Right-click a completed furnace block once to assemble; an old first-corner
  selection no longer interferes. Supports all four horizontal rotations.
- New pure-Java tests and Minecraft GameTests are included; the Minecraft
  GameTests could not be executed here due to unavailable Gradle distribution.
- Details: `CHANGELOG-V21.md` and `INSTALL-V21.txt`.


## What changed in V20

- **No more dedicated Item Input, Item Output, Fluid Input or Fluid Output ports.** Every exposed ordinary fireclay casing block and the furnace hatch now expose the SAME backing furnace item inventory and molten metal / slag tanks to NeoForge capabilities on **all six directions**. Place a Create funnel/chute or mechanical pipe/pump beside any exterior structural block; use Create filters or smart chutes for routing. The furnace enforces insertion/extraction rules on its four item slots.
- **No new Laser Printer.** Removed the crafting recipe, printing recipe serializer registration, creative-tab item, silicon-printing recipe, dependent chip-cutting recipe, drops and newly added Blender model. Old placed Laser Printer blocks remain registered but inactive for **existing-world compatibility**; they have no automation capability. Printed wafers and chips remain only as legacy item IDs and are excluded from creative.
- **Minecraft-native ore art.** All 135 existing textures are regenerated as original 16x16 RGBA pixel art with embedded irregular mineral clusters on stone and deepslate, flat 2D ingots/raw items/nuggets/powders, clean refractory bricks, restrained casings and Welder colors. No blurry upscaled screenshots, 3D ingot meshes or AI-generated images.
- **No new Steel Converter.** Steel uses the existing superheated Create Mechanical Mixer + Basin recipe: 576 mB molten pig iron + 1 calcite + 2 iron nuggets → 576 mB molten steel + 144 mB molten slag. Cast 144 mB steel to an ingot. The converter's old ID is retained for compatibility only.
- **Legacy worlds:** A loaded, already-assembled V18 furnace with original port blocks automatically migrates those blocks to matching fireclay on server verification; saved machine inventory and tanks remain on the controller. Old machine block and port IDs intentionally remain registered; please **back up your world before upgrading**.

## How the seamless item and fluid capability works

| Position | Item insertion | Item extraction | Fluid input | Fluid output |
| --- | --- | --- | --- | --- |
| Any **formed** furnace fireclay brick, any side | Ore (slot 0), fuel (slot 1), flux (slot 2) | Finished ingots (slot 3, auto-casting when hot) | Supported molten metal | Molten metal / slag |
| Formed furnace hatch, any side | Same shared slots | Same shared ingots | Same shared tank | Same shared tanks |
| Loose bricks or disassembled hatch | No shared furnace capability | None | None | None |

All accesses are server-owned and share one machine inventory/tank. Simulated insertion, extraction and transfer must not mutate state. Filtering which fluid goes down which branch is managed with Create's filterable drains/pipes/tanks as appropriate; this mod does not create special port blocks. The internal working chamber (air/molten surface) is not an exterior connection face. **Actual physical Create funnel and fluid pipe compatibility must still be proven in a running client/server.**

## Sources and instructions

- Java: `src/main/java/net/createindustrialteam/createindustrial/`
- Textures: `src/main/resources/assets/createindustrial/textures/` (135 original 16x16 PNGs)
- Ore and sprite generator: `tools/generate_v20_textures.py`
- Full material recipe/data regeneration: `tools/generate_materials.py` (automatically reapplies V20 art; will NOT recreate Laser Printer recipes)
- Capability adapters: `foundry/FurnaceConnections.java`, `FurnaceItemHandler.java`, `FurnaceFluidHandler.java`
- World migration / multiblock: `multiblock/BlastFurnaceMultiblock.java`, `multiblock/MachineRegistry.java`
- Detailed V20 notes: `docs/V20-SEAMLESS-FOUNDRY.md`

## Verify before installing

With a working JDK 21 and **network or cached Gradle dependencies**:

```shell
# Linux/macOS
./gradlew clean build runGameTestServer
./gradlew runClient -PassetAudit
python3 tools/run_offline_checks.py
# Windows
# gradlew.bat clean build runGameTestServer
```

**This V22 delivery passed only the reproducible offline checks.** The builder could not download the required Gradle wrapper distribution (DNS/`UnknownHostException`), so Java/NeoForge compilation, server GameTests, Create multiplayer transfers, actual rendered model/texture appearance, and producing a new V22 test JAR remain **unverified**. The older V18 JAR is NOT a valid V22 binary and must not be relabeled.

The separate optional V20 **resource pack** replaces only visuals on an existing V18/V19 installation. It does **not** remove its printer or ports or add any of the new automation logic. Test gameplay changes only after building the V22 source into a new mod JAR.
