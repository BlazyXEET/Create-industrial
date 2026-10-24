package net.createindustrialteam.createindustrial.multiblock;

import java.util.HashSet;
import java.util.List;

/** Undo target must be able to find its controller from casing OR molten air cell. */
public final class FurnaceControllerOffsetsTest {
    private static void check(boolean value, String message) {
        if (!value) throw new AssertionError(message);
    }
    public static void main(String[] args) {
        for (boolean large : new boolean[]{false,true}) {
            List<VoxelPattern.Offset> all=FurnaceControllerOffsets.forScale(large);
            check(all.size()==new HashSet<>(all).size(), "duplicate candidate offsets");
            int radius=large?1:0, frontOffset=large?2:1;
            int[] heights=large?new int[]{1}:new int[]{1,2};
            for (int[] f : new int[][]{{0,1},{1,0},{0,-1},{-1,0}})
                for (int y : heights) for (int x=-radius;x<=radius;x++) for(int z=-radius;z<=radius;z++) {
                    var controllerOffset=new VoxelPattern.Offset(f[0]*frontOffset-x,1-y,
                            f[1]*frontOffset-z);
                    check(all.contains(controllerOffset), "missing chamber click candidate: "+controllerOffset);
                }
            List<VoxelPattern.Offset> structural=large
                    ? LargeBlastFurnaceLayout.controllerOffsets():BlastFurnaceLayout.controllerOffsets();
            check(all.containsAll(structural), "lost structural controller candidate");
        }
        System.out.println("PASS: all four rotations; molten/core weld removal offsets");
    }
}
