package net.createindustrialteam.createindustrial.multiblock;

/** Exact user-supplied seven-layer factory blueprint, checked without Minecraft. */
public final class LargeBlastFurnaceLayoutTest {
    private static final String[][] ROWS = {
            {".....", "BBBBB", "BBBBB", "BBBBB", "BBBBB"},
            {"BBBBB", "B...B", "B...B", "B...B", "BBCBB"},
            {".BBB.", "B...B", "B...B", "B...B", ".BBB."},
            {".BBB.", "B...B", "B...B", "B...B", ".BBB."},
            {".....", ".BBB.", ".B.B.", ".BBB.", "....."},
            {".....", "..B..", ".B.B.", "..B..", "....."},
            {".....", "..B..", ".B.B.", "..B..", "....."}
    };
    public static void main(String[] args) {
        VoxelPattern p = LargeBlastFurnaceLayout.pattern();
        if (p.width() != 5 || p.depth() != 5 || p.height() != 7 || p.count('B') != 75
                || p.count('C') != 1 || p.count('I') != 0 || p.count('O') != 0
                || p.count('F') != 0 || p.count('G') != 0 || p.count('.') != 99)
            throw new AssertionError("Seven-layer blueprint counts changed");
        if (p.count('B') + p.count('C') + p.count('.') != 175)
            throw new AssertionError("Invalid large volume");
        for (int y = 0; y < 7; y++) for (int z = 0; z < 5; z++) for (int x = 0; x < 5; x++) {
            if (p.at(x-2,y,z-2,0,1) != ROWS[y][z].charAt(x))
                throw new AssertionError("Layer mismatch " + y + ":" + z + ":" + x);
        }
        int[][] fronts = {{0,1},{1,0},{0,-1},{-1,0}};
        for (int[] front : fronts) {
            int fx = front[0], fz = front[1];
            // All four previous layer-2 IO positions are now plain fireclay.
            for (int z=-2; z<=2; z++) for (int x=-2; x<=2; x++) {
                char cell = p.at(fz*x+fx*z,1,-fx*x+fz*z,fx,fz);
                if (cell=='I' || cell=='O' || cell=='F' || cell=='G')
                    throw new AssertionError("Port token appeared in a plain brick layer");
            }
            for (int z=-2; z<=2; z++) for (int x=-2; x<=2; x++) {
                char cell = p.at(fz*x+fx*z,2,-fx*x+fz*z,fx,fz);
                if (cell=='I' || cell=='O' || cell=='F' || cell=='G')
                    throw new AssertionError("Port token appeared in layer 3");
            }
            if (p.at(2*fx,1,2*fz,fx,fz) != 'C')
                throw new AssertionError("controller not on front");
        }
        var candidates = p.controllerOffsets('C','.');
        if (!candidates.contains(new VoxelPattern.Offset(0,0,0)) || candidates.size() < 80)
            throw new AssertionError("Missing big controller candidates");
        System.out.println("PASS: V20 seamless large furnace, no port tokens, all four rotations");
    }
}
