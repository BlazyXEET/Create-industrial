# Welder + Multiblock Stabilization Edition

This development focus exposes only the Welder, Fireclay Bricks and Blast Furnace Hatch in the creative tab. The remaining V22 registries and resources are intentionally retained for existing world compatibility; they are not the focus of this build.

## Controls
- Right-click any valid completed furnace casing/controller with the Welder to assemble.
- Shift-right-click a formed furnace member to unweld.
- Shift-left-click with the main-hand Welder is an alternative unweld input.
- Shift-right-click air clears a selection.
- Alt-right-click targets a free air cell for two-corner selection.

## Assembly
- Small furnace: 3x3x4, with optional central brick in the lower hearth.
- Large furnace: 5x5x7 using the source blueprint in `LargeBlastFurnaceLayout.java`.
- One selection may assemble at most one furnace, to avoid unintended mass-welding.
- Case/hatch assembly uses all four horizontal orientations.

## Verification
Run `python3 tools/run_offline_checks.py` and `./gradlew clean build runGameTestServer` from Source (on Windows use `gradlew.bat`). Offline checks do not establish Minecraft gameplay correctness.

## Push to GitHub
Use `git add -A`, `git commit -m "Focus Create Industrial on welder and reliable furnace multiblocks"`, and `git push -u origin <new-branch>` on your own checked-out branch. Do not force-push GitHub main or overwrite newer work.
