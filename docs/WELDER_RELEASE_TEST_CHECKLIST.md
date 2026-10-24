# Manual Minecraft validation checklist (not executed in this environment)

Before installing: back up the world. Run Minecraft 1.21.1 with the NeoForge/Create versions in gradle.properties.

1. New creative tab: only Welder, Fireclay Bricks, Blast Furnace Hatch.
2. Build the small 3x3x4 furnace in each direction; right-click any structural fireclay block using Welder. Hatch must indicate assembled.
3. Test hollow and solid optional-hearth layouts.
4. Shift-right-click and Shift-left-click the formed structure separately; each must remove the assembly state, preserve bricks, and allow rewelding.
5. Build and weld 5x5x7 large furnace in all four rotations using docs/V17-FOUNDRY.md and LargeBlastFurnaceLayout.java.
6. Break a casing, reload the world, reassemble, and check all item/fluid storage stays conserved.
7. Stand behind solid wall and try to use the Welder through it; must not work.
8. Test two players and a dedicated server; reject unauthorized interactions.
9. Test two full furnaces inside the same selection bounds; the weld attempt must be refused, not assemble both.
10. Run ./gradlew clean build runGameTestServer. Record any failed test output. Do not call this release verified until completed.

Legacy content is still registered to protect older save data; it is hidden from the creative tab, not removed from the registry. No JAR in this package is a newly verified build.
