package net.createindustrialteam.createindustrial.multiblock;

import net.createindustrialteam.createindustrial.multiblock.FurnaceCellMatcher.Material;

/** Exercise the exact per-cell matcher used by the server to keep structures formed. */
public final class FurnaceCellMatcherTest {
    private static int assertions;
    private static void check(boolean value, String message) {
        assertions++;
        if (!value) throw new AssertionError(message);
    }
    private static char small(int x, int y, int z, int fx, int fz) {
        return switch (BlastFurnaceLayout.at(x,y,z,fx,fz)) {
            case AIR -> '.';
            case FIRECLAY -> 'B';
            case HATCH -> 'C';
        };
    }
    private static Material normal(char code) {
        return switch (code) {
            case '.' -> Material.AIR;
            case 'B' -> Material.FIRECLAY;
            case 'C' -> Material.HATCH;
            default -> Material.OTHER;
        };
    }
    public static void main(String[] args) {
        for (int[] f : new int[][]{{0,1}, {1,0}, {0,-1}, {-1,0}}) {
            for (boolean large : new boolean[]{false, true}) {
                int radius=large?2:1, height=large?7:4;
                for (int y=0; y<height; y++) for (int x=-radius;x<=radius;x++)
                    for (int z=-radius;z<=radius;z++) {
                        char cell=large ? LargeBlastFurnaceLayout.at(x,y,z,f[0],f[1])
                                : small(x,y,z,f[0],f[1]);
                        check(FurnaceCellMatcher.matches(large,x,y,z,cell,false,normal(cell)),
                                "unformed proper block must match");
                        check(FurnaceCellMatcher.matches(large,x,y,z,cell,true,normal(cell)),
                                "formed proper block must match");
                        check(!FurnaceCellMatcher.matches(large,x,y,z,cell,false,Material.OWNED_MOLTEN),
                                "cannot assemble out of leftover surface blocks");
                        boolean chamber = FurnaceCellMatcher.isChamberCell(large,x,y,z);
                        check(FurnaceCellMatcher.matches(large,x,y,z,cell,true,Material.OWNED_MOLTEN)==chamber,
                                "molten visual must only be allowed in furnace chamber");
                        if (!chamber && cell == 'B')
                            check(!FurnaceCellMatcher.matches(large,x,y,z,cell,true,Material.AIR),
                                    "removing a wall must break assembly");
                    }
                if (!large) {
                    check(FurnaceCellMatcher.matches(false,0,1,0,'B',false,Material.AIR),
                            "hollow hearth must assemble");
                    check(FurnaceCellMatcher.matches(false,0,1,0,'B',true,Material.AIR),
                            "hollow hearth must remain assembled");
                    check(!FurnaceCellMatcher.matches(false,0,1,0,'B',false,Material.OTHER),
                            "obstructed hearth must fail");
                }
            }
        }
        System.out.println("PASS: "+assertions+" real furnace-cell matcher assertions");
    }
}
