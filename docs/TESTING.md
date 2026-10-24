# V13 — Minecraft acceptance tests

Minecraft 1.21.1, NeoForge 21.1.257, Create 6.0.10-280, JDK 21. Back up your world first and install only one createindustrial JAR.

1. Use `BUILD_TEST_JAR.bat` (14 Minecraft GameTests). The alternative `BUILD_ONLY_WITHOUT_GAMETESTS.bat` deliberately creates an unverified build and labels it accordingly.
2. Form the small 3x3x4 furnace. Check that it forms **two ports** (item input on left at second layer, fluid output on right at third layer). The other two side bricks must remain Fireclay Bricks. Feed raw copper and coal through its item port; pump out molten copper using a Create fluid pipe. Check that it offers no item-output capability on its hatch or sides.
3. Form the big 5x5x7 furnace using `BLUEPRINTS.md` and Fireclay Bricks at the four port-symbol cells. Check that it forms **four ports** (all four ports at layer 2; layer 3 has no ports), correctly facing outward. Connect Create funnels to the item faces and pipes/pumps to the fluid faces. Feed raw metal and coal, export molten fluid, test molten input, and extract an ingot from item output.
4. Test both sizes at all four orientations. When built, the scale property on the hatch must be `small` or `large` respectively. After unwelding, every port must return to a brick; reassemble and break a casing or hatch to confirm no orphaned ports remain.
5. Holding the blue Welder should show gold/yellow edges around *all nearby assembled* industrial machines in loaded chunks, even without aiming at one. Sneak-right-click to clear an assembly; right-click a completed machine to assemble it. Selected boxes spark on completion; no chat popups.
6. Run heating and smoke tests, goggles tooltips, a player touching molten metal (Survival vs Creative), save/reload after welding, and two-player multiplayer assembly/automation. The GameTest server alone cannot certify visuals or multiplayer.

If there is a failure, upload `BUILD_LOG.txt`, `GAMETEST_LOG.txt`, and your Minecraft client's `logs/latest.log`.
