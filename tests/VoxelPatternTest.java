package net.createindustrialteam.createindustrial.multiblock;

/** Offline regression suite for the reusable multi-machine blueprint format. */
public final class VoxelPatternTest {
    private static void expectFailure(Runnable code) {
        try { code.run(); } catch (IllegalArgumentException expected) { return; }
        throw new AssertionError("Expected an invalid blueprint to be rejected");
    }

    public static void main(String[] args) {
        VoxelPattern furnace = BlastFurnaceLayout.pattern();
        if (furnace.width() != 3 || furnace.depth() != 3 || furnace.height() != 4
                || furnace.count('B') != 29 || furnace.count('H') != 1 || furnace.count('.') != 6) {
            throw new AssertionError("Blast Furnace dimensions or block counts changed");
        }
        var offsets = furnace.controllerOffsets('H', '.');
        if (offsets.isEmpty() || offsets.size() >= 4 * 30) {
            throw new AssertionError("Controller search offsets are not deduplicated");
        }
        if (!offsets.contains(new VoxelPattern.Offset(0, 0, 0))) {
            throw new AssertionError("Hatch is not a candidate for itself");
        }
        expectFailure(() -> furnace.controllerOffsets('B', '.')); // 29 bricks, not one controller
        expectFailure(() -> furnace.controllerOffsets('.', '.'));
        int[][] machineFacings = {{0, 1}, {1, 0}, {0, -1}, {-1, 0}};
        for (int[] facing : machineFacings) {
            for (int y = 0; y < furnace.height(); y++) {
                for (int x = -1; x <= 1; x++) {
                    for (int z = -1; z <= 1; z++) {
                        if (furnace.at(x, y, z, facing[0], facing[1]) == '.') continue;
                        var offset = new VoxelPattern.Offset(facing[0] - x, 1 - y, facing[1] - z);
                        if (!offsets.contains(offset)) {
                            throw new AssertionError("Missing possible hatch position for a machine member: " + offset);
                        }
                    }
                }
            }
        }
        VoxelPattern rectangular = VoxelPattern.of(
                new String[] {"..C", "...", "...", "...", "M.."});
        if (rectangular.width() != 3 || rectangular.depth() != 5
                || rectangular.count('C') != 1 || rectangular.controllerOffsets('C', '.').isEmpty()) {
            throw new AssertionError("Rectangular machine patterns are unsupported");
        }
        // A member at local (-1,+2) must locate the controller at (+1,-2),
        // including when the pattern rotates and swaps its world axes.
        if (!rectangular.controllerOffsets('C', '.').contains(new VoxelPattern.Offset(2, 0, -4))
                || !rectangular.controllerOffsets('C', '.').contains(new VoxelPattern.Offset(-4, 0, -2))) {
            throw new AssertionError("Rectangular candidate controller search failed");
        }
        VoxelPattern asymmetric = VoxelPattern.of(new String[]{"N..", "...", "..S"});
        int[][] directions = {{0, 1}, {1, 0}, {0, -1}, {-1, 0}};
        for (int[] dir : directions) {
            int dx = dir[0], dz = dir[1];
            // Local SE corner is world (dz + dx, -dx + dz).
            if (asymmetric.at(dz + dx, 0, dz - dx, dx, dz) != 'S') {
                throw new AssertionError("SE corner did not rotate with the machine");
            }
            if (asymmetric.at(-dz - dx, 0, dx - dz, dx, dz) != 'N') {
                throw new AssertionError("NW corner did not rotate with the machine");
            }
            if (furnace.count('B') != 29) throw new AssertionError("Data mutated");
        }
        expectFailure(() -> VoxelPattern.of(new String[]{"BB"}));
        expectFailure(() -> VoxelPattern.of(new String[]{"BBB", "B.B"}));
        expectFailure(() -> VoxelPattern.of(new String[]{"BBB", "B B", "BBB"}));
        expectFailure(() -> furnace.at(99, 0, 0, 0, 1));
        expectFailure(() -> furnace.at(0, -1, 0, 0, 1));
        expectFailure(() -> furnace.at(0, 0, 0, 1, 1));
        System.out.println("PASS: declarative pattern, 29+1 furnace, all rotations, invalid patterns");
    }
}
