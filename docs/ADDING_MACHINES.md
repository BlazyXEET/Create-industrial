# Add another weldable multiblock (V24 extension API)

The Welder does not know furnace classes. **Do not change `WelderItem`,
`WelderActions`, the click packet, or the renderer to add a machine.**
Register one `MachineDefinition` with `MachineRegistry.register(...)` during
mod initialization. The registry automatically handles matching, welding,
unwelding, safe controller searches, outline rendering, and player permissions.

## Easiest path: `PatternMachineDefinition`

`PatternMachineDefinition` now handles rectangular patterns, all four horizontal
rotations, searches for controllers from machine parts, required-air checks,
visual diagnostics, selection bounds, and outline members. A 3x5 pattern is
supported just as well as 3x3; the geometry does not assume a square footprint.

Define **bottom-to-top** Y layers. Each layer is a String array ordered from
north to south when the machine faces **south**. Pattern footprints must have
odd width/depth and **exactly one controller token**. `.` represents required
air; other characters represent block types.

```java
private static final VoxelPattern SHAPE = VoxelPattern.of(
    new String[] { "BBB", "BCB", "BBB" },
    new String[] { "BBB", "B.B", "BBB" },
    new String[] { "BBB", "BBB", "BBB" }
);
```

Make a machine-specific definition (illustrative: register your own controller
and casing blocks before using their references):

```java
public final class KilnDefinition extends PatternMachineDefinition {
    public KilnDefinition() {
        super(ResourceLocation.fromNamespaceAndPath("createindustrial", "kiln"),
            SHAPE, 'C', '.', Map.of(
                'B', s -> s.is(ModBlocks.FIRECLAY_BRICKS.get()),
                'C', s -> s.is(MyBlocks.KILN_CONTROLLER.get())
            ));
    }

    @Override protected Direction facing(Level level, BlockPos controller) {
        return level.getBlockState(controller).getValue(MyControllerBlock.FACING);
    }

    @Override public boolean isAssembled(BlockState state) {
        return state.getValue(MyControllerBlock.ASSEMBLED);
    }

    @Override public void setAssembled(ServerLevel level, BlockPos controller, boolean assembled) {
        BlockState old = level.getBlockState(controller);
        if (isController(old)) {
            level.setBlock(controller, old.setValue(MyControllerBlock.ASSEMBLED, assembled), 3);
            level.invalidateCapabilities(controller);
        }
    }

    @Override public void onAssembled(ServerLevel level, BlockPos controller) {
        // Notify the controller entity; schedule processing, invalidate caches.
    }

    @Override public void onDisassembled(ServerLevel level, BlockPos controller) {
        // Stop processing, invalidate cached handlers, retain stored contents.
    }
}
```

Finally, register exactly once, early in normal mod initialization:

```java
MachineRegistry.register(new KilnDefinition());
```

`MyBlocks` / `MyControllerBlock` in the snippet are **example names**. You must
create/register those classes and their blockstate properties; this is an
extension template, not another machine already added to the mod.

## Machines with special structures

For open hearths, optional casing blocks, molten rendering surfaces, legacy
world-data migration, or unusual controller searches, implement `MachineDefinition`
directly or subclass `PatternMachineDefinition` and override the appropriate
checks. The small and large blast furnaces intentionally retain their existing
specialized `BlastFurnaceMultiblock` implementation; replacing their matcher
would risk losing legacy world/surface behavior.

## Safety contract for every new definition

1. `id()` is globally unique; `searchRadius()` must be 1..12.
2. `controllerCandidates` never force-loads a chunk.
3. `isController` only matches controllers of this type.
4. `containsMember` must include its controller and every welded casing.
5. `matches` must check all required blocks AND required empty spaces.
6. `setAssembled` must persist the new state on the server.
7. `onAssembled` / `onDisassembled` must synchronize, invalidate capabilities,
   and preserve inventories, fluids, and existing blocks appropriately.
8. Controller on-remove or scheduled verification must disassemble when the
   structure breaks; never let a destroyed structure continue processing.
9. All orientations, save/reload, multiplayer and permission behavior require
   real Minecraft testing before a release.
10. Add pure geometry tests (see `tests/PatternGeometryTest.java`) and in-game
    GameTests for the new machine; **offline passing is not proof of gameplay**.

## Scope of this focused build

The Welder, Fireclay Bricks and Blast Furnace Hatch remain the only items
shown in the project's focused creative tab. Other legacy registries are left
in place for existing-world compatibility, not exposed as new features.
