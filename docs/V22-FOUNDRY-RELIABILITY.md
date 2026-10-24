# V22 in-game furnace / Welder regression checklist

This document is a test plan, not a record of tests already completed.

| Case | Setup and action | Expected result |
| --- | --- | --- |
| Unformed controller | Place hatch but do not finish/weld furnace; attach vanilla hopper and Create funnel/pipe | No shared machine item or molten-fluid capability |
| Form small furnace | Build 3×3×4 with 29 original bricks; right-click any casing with Welder | Assembled, no new port blocks |
| Form hollow small | Omit optional center hearth fireclay; assemble and reassemble | Accepted without filling the empty space |
| Form large furnace | Build supplied 5×5×7 blueprint, all four orientations | Formed shape matches exactly, including open foundation row |
| Welder undo | Shift + right-click or Shift + left-click assembled brick | Weld removed, bricks remain, stored molten and items stay on hatch |
| Empty/hot chamber undo | Alt + Shift + right-click air / Shift + right-click molten surface | Weld removed without orphaned surface blocks |
| Hot molten check | Put molten metal in formed furnace; wait five minutes | Furnace remains assembled; molten pool stays within chamber |
| Item simulate | Simulate funnel insert into any face | Correct acceptance count, no inventory changes |
| Item execute | Insert raw ore, coal, valid flux from separate faces | Same backing storage; only output ingots can be extracted |
| Hopper isolation | Unweld; retry vanilla hopper | No continued access while unformed |
| Cached handler | Hold Java IItemHandler/IFluidHandler reference; unweld or replace hatch | Old references cannot change/drop/create contents |
| Fluid simulate | Simulate filtered pipe fill/extraction | No quantity changes |
| Fluid execute | Fill molten copper, reject iron mixing, drain precise amounts | Fluid conserved; no cross-metal mixing |
| Reassembly | Unweld with stored inventory and molten metal; reweld | Storage unchanged, new/old capabilities read shared tank |
| Steel refining | Superheated Create Mixer/Basin with 576 mB pig iron + calcite + 2 iron nuggets | 576 mB steel + 144 mB slag; no Steel Converter needed |
| Legacy saves | Load copied V18 world with old ports; let controller update | Port blocks become fireclay; saved inventory/tanks survive |
| Multiplayer | Two players simultaneously weld/unweld/pipe transfer | No duplication, desync, invisible extra actions or unauthorized edits |
| Visuals | Inspect stone/deepslate ores, generated raw items, ingots and active furnace | Crisp 16×16 art with no missing textures or wrong orientation |

## Build commands

```
python3 tools/run_offline_checks.py
./gradlew clean build runGameTestServer
./gradlew runClient -PassetAudit
```

Windows: substitute `gradlew.bat` for `./gradlew`. Keep build and crash logs if any test fails. The game is not verified from Java syntax parsing alone.
