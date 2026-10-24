# V20 design and QA guide — simple Create integration

## Design goals

A blast furnace should look like a furnace, not a cluster of color-coded plugs.
Both sizes now require only refractory bricks and one controller hatch. Every
formed structural brick exposes the same item/fluid handlers on every side; this
works with NeoForge capability-based Create inventory and pipe integration. No
extra connector block, optional direction, GUI port toggle or machine-specific
item-transport interface is necessary.

## Automation rules

- Four virtual item capability slots, mapped to input / fuel / flux / output.
- Input accepts foundry recipes only; fuel accepts supported solid fuel; flux
  accepts only blast-furnace-flux tag items. Output cannot accept items.
- Extraction is output-only. When hot, the handler can form a single ingot from
  enough molten metal and hand it to an extracting Create funnel/chute.
- Item simulation does not write to inventories or cast a physical ingot.
- The controller exposes the same underlying inventory and molten/slag tanks on
  any face; every formed casing delegates to the controller.
- Fluid input accepts compatible registered molten metals up to tank capacity.
  Fluid extraction can drain metal or slag; fluid requests choose a type.
- Simulated fill/drain must not modify fluid amounts.
- No capability is exposed by loose bricks or a disassembled hatch.
- Capability caches are invalidated for all structure members on assembly and
  disassembly. Shared/colliding casing ownership returns no adapter, not a random
  controller inventory. No chunk is force-loaded during ownership lookup.

## Why existing registry IDs remain

Simply unregistering `createindustrial:laser_printer` or
`createindustrial:industrial_port` corrupts references to placed blocks in old
worlds. These block IDs are retained for data compatibility but have no new
BlockItems/recipes and cannot be crafted or selected from the new creative tab.
An assembled old furnace converts existing port positions into fireclay casing
when verified on the server. Never claim registry compatibility implies that
all saves have been fully migrated: back up before test upgrades.

## Steel progression

Iron ore + fuel + flux + forced draft → molten pig iron in the blast furnace.
Mix 576 mB pig iron, 1 calcite, 2 iron nuggets in a superheated Create Basin.
Extract 576 mB steel and 144 mB slag separately, then cast an ingot. This is a
playable abstraction of oxidizing/carbon-adjusting pig iron, not exact chemistry.

## Texture and model principles

Every mod texture is an editable 16×16 RGBA PNG. Ore veins are drawn as irregular
mineral patches embedded in the rock surface, with separate stone/deepslate
shading. Ingots, nuggets, raw ore, crushed ore and powders use vanilla-style
flat `minecraft:item/generated` sprites. Metal storage blocks do not have
industrial machine-face textures. No AI image output is used as game textures.
Run `python3 tools/generate_v20_textures.py` to regenerate the entire texture set
without changing non-art data. The full materials generator calls it last.

## Real Minecraft test checklist — NOT YET EXECUTED

1. `./gradlew clean build`; client load check for missing sprites and models.
2. `./gradlew runGameTestServer`; fix any failing recipes/API methods.
3. Form small and large furnaces in all four orientations, all with brick casing.
4. Place funnels/chutes on side, top, bottom and hatch; feed valid ore, fuel, flux.
5. Use smart chutes/filters to take finished ingots; check one 144 mB ingot per
   144 mB drained from molten inventory, not from mere simulation.
6. Connect Create fluid pipes and pumps to any side, verify molten fill and drain
   on the same tank and no duplicate fluid from multiple parallel outputs.
7. Check both sizes, chunk unloading/reloading, server restart and save restore.
8. Convert V18 world copy containing port blocks; inspect material conservation.
9. Unweld/break casing and make sure capabilities disappear immediately.
10. Dedicated server and two-player multiplayer visual/logic smoke tests.

## Known blockers

The build environment lacks the cached Gradle distribution and could not fetch
it from `services.gradle.org`. Offline JavaParser logic and resource integrity
checks passed; actual NeoForge classpath compilation and runtime behavior are not
claimed to have passed.
