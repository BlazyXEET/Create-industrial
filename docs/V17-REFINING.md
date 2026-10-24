> **Historical V17 documentation:** Laser Printer recipes are retired in V20; follow [V20 instructions](V20-SEAMLESS-FOUNDRY.md) for current gameplay and automation.

# V17 processing and automation

Minecraft 1.21.1 · NeoForge 21.1.257 · Create 6.0.10-280 · Java 21.

All crushing, washing, mixing, compacting, pressing and cutting below are native
Create recipes. Use Crushing Wheels, an Encased Fan blowing through water,+a Mechanical Mixer over a Basin, a Mechanical Press, and an upward-facing
Mechanical Saw as appropriate. Heated means a fueled Blaze Burner below the
Basin. The Laser Printer is a working machine. The steel converter is deprecated in V19.

## Silicon

| Input | Process | Output |
|---|---|---|
| 1 sand | Heated basin mixing | 10% chance of 1 impure silicon powder |
| 1 impure silicon powder | Fan washing | 1 pure silicon powder, 0–2 iron nuggets, 20% chance of 1 aluminium nugget |
| 1 pure silicon powder + 250 mB water | Heated basin compacting | 1 silicon crystal |
| 1 silicon crystal | Mechanical Saw | 8 silicon wafers |
| 1 silicon wafer | Laser Printer | 1 printed silicon wafer |
| 1 printed silicon wafer | Mechanical Saw | 8 silicon chips |

The sand is consumed even when its 10% roll fails. The two possible iron nuggets
each have an independent 50% roll. Washing always preserves one pure silicon
powder. A crystal ultimately yields 64 chips, as requested. These are gameplay
recipes, rather than a literal semiconductor manufacturing simulation.

The Laser Printer accepts Create rotation on its left/right shaft ends.
Supply at least 64 RPM; either rotation direction works. Work rate is 1 / 2 / 4
at 64 / 128 / 256 RPM, capped at 4. A wafer requires 120 work units: 6 / 3 / 1.5
seconds at those speeds. Stress impact is 8 SU per RPM. No extra printing
consumable is required after crafting the machine.

Feed wafers using a funnel or hopper on the top or back; extract printed wafers
from the front or bottom. Right-click with a wafer to insert one, and empty-hand
right-click to collect output. A redstone signal pauses work. A full output
pauses without consuming another wafer. Progress and inventory are saved.
The visible shaft rotates and the front laser lights while working.

## Bauxite and aluminium

| Input | Process | Output |
|---|---|---|
| 1 raw bauxite (`raw_aluminium`) or 1 bauxite ore block | Crushing Wheels | 2–4 bauxite powder |
| 1 bauxite powder | Fan washing | 1–2 alumina powder, 40% chance of 1 iron nugget, 5% chance of 1 impure silicon powder |
| 1 alumina powder | Heated basin compacting | 1 aluminium ingot |
| 1 aluminium ingot | Mechanical Press | 1 aluminium sheet |
| 2 aluminium sheets + 1 iron nugget | Crafting, vertical | 1 turbine blade |
| 4 aluminium sheets, square | Crafting | 1 Create white windmill sail |
| 4 turbine blades around 1 iron nugget | Crafting | 4 Create white windmill sails |

Bauxite crushing guarantees two powder, with two independent 50% bonus rolls.
Washing guarantees one alumina, with a 50% second alumina roll. A raw aluminium
block unpacks to nine raw bauxite before processing, so storage cannot multiply
the ore. Stone/deepslate bauxite share the same processing recipe yields.

The sails are Create's functional windmill sails: place them on a contraption
driven by a Windmill Bearing. Turbine blades are usable crafting components for
those sails. A separate turbine generator block is not included in this build.

Legacy `crushed_raw_aluminium` still washes into alumina powder. Legacy
`alumina_dust` converts 1:1 into alumina powder. Direct bauxite smelting and the
old charcoal reduction recipe are removed. A slow renewable route remains:
heated mixing of four clay balls and 250 mB water gives one alumina powder.

Heated pressing of alumina follows the requested game recipe. Real aluminium
production needs electrolysis; this recipe is intentionally simplified.

## Fireclay and refractory bricks

Mine a natural Fireclay block with a shovel for four fireclay balls. Silk Touch
returns the block. Fortune does not multiply this reversible storage material.
Four balls also craft back into one Fireclay block.

Smelt or blast each fireclay ball into one fireclay brick. Craft four bricks in a
square into one Fireclay Bricks block. The existing tier-one large blast furnace
uses these blocks; its 5×5×7 layout and independent Welder assembly are preserved.

Natural deposits check actual terrain:

- River deposits replace dirt, clay, sand or gravel beside river-biome water,
  allowing low banks up to two blocks above the water. Covered ground is skipped.
- Underground deposits replace natural stone/deepslate directly beside coal ore,
  leaving the coal itself in place. Searches are bounded and do not force chunks.

New natural deposits appear in newly generated chunks. Existing worlds also have
a renewable route: mix four clay balls, one gravel and 250 mB water into four
fireclay balls. Furnace and fan smelting can automate the brick stage.

## Steel: legacy air-blown refining (V17/V18 worlds only)

The blast furnace makes **carbon-rich pig iron** from raw iron with fuel, forced
air and flux. Steelmaking then removes carbon and impurities in a separate
refining vessel. This follows the two-stage distinction in industrial iron and
steel production; adding more charcoal is not the refining step.

The old Air-Blown Steel Converter represents a basic Bessemer/Thomas-style
process: its shaft-driven blower supplies oxygen from air, and basic flux helps
collect impurities into slag. It is not a pure-oxygen BOF simulation.

For one batch, pipe **576 mB molten pig iron** into the back, and supply **one
calcite or Create limestone** through a top/back item inlet. Place a **superheated
Blaze Burner below**, provide **64 RPM or more** on either side shaft, and leave
the block above the front pipe connection clear for the air outlet. The burner
is a gameplay requirement for maintaining process heat; real oxidation also
generates heat.

After 600 work units, the converter produces **576 mB molten steel** and **144 mB
molten slag**. Processing takes 30 / 15 / 7.5 seconds at 64 / 128 / 256 RPM. Stress
impact is 16 SU per RPM. A redstone signal pauses the machine. It cannot process
ordinary molten iron, accept charcoal as flux, or make steel in a cold vessel.

The front/bottom fluid output exposes separate steel and slag tanks. Use filtered
Create pipes to separate them. Its pig-iron/steel tanks each hold 2304 mB; the slag
tank holds 576 mB. Both outputs must have room before a batch starts or advances.
Blocked outputs and interrupted power/heat pause the batch without spending its
inputs. A lost input resets that batch's work. Tanks and progress survive saving.

Use the existing Create basin casting recipes to solidify steel and slag. The
iron-plus-charcoal and pig-iron-plus-calcite mixing shortcuts are removed. Cast
pig iron can be remelted in the blast furnace if needed. The complete production
line supports Create funnels, pumps, filters and shaft power without a GUI.

Sources for the process distinction:
[American Iron and Steel Institute — Steel Production](https://www.steel.org/steel-technology/steel-production/)
and [World Steel Association — What is steel?](https://worldsteel.org/about-steel/what-is%20steel/).
Fixed batch ratios, heat thresholds, carbon removal, and slag quantities are
balanced game abstractions; the mod does not calculate chemical equilibrium.

## Artwork and verification

The six natural ore families have distinct mineral silhouettes and separate
stone/deepslate sprites. Storage blocks use painted metallic highlights. Those
highlights work in vanilla rendering; no reflection shader is required. Uranium
and plutonium metals do not glow unnaturally. The V18 Blender scene contains block models for all six
ore families, all three manufactured families, and both machine bodies.
All material inventory items are flat pixel-art PNGs, with no ingot, nugget, raw,
or crushed-item meshes.
Minecraft loads the corresponding cuboid JSON models, not the `.blend` file.

Regenerate assets with `python tools/generate_materials.py` (Pillow required).
Run `python tools/run_offline_checks.py`, then `./gradlew clean build
runGameTestServer`. Run `./gradlew build runClient -PassetAudit` for the optional
client model/texture audit and an actual Minecraft-rendered asset sheet.
See the packaged verification report for the checks run on the delivered JAR.

> **V19:** New steel refining uses a superheated Mechanical Mixer and Basin. See `docs/V19-ART-AND-STEEL.md`. The legacy converter remains registered solely for world compatibility, but is no longer craftable or displayed in the creative tab.
