package net.createindustrialteam.createindustrial.multiblock;

/** Offline test; java-only, no Minecraft classpath required. */
public final class BlastFurnaceLayoutTest {
    public static void main(String[] args) {
        int[][] directions = {{0,1},{0,-1},{1,0},{-1,0}};
        for (int[] d : directions) {
            int bricks = 0;
            int hatches = 0;
            int air = 0;
            for (int y=0; y<4; y++) {
                for (int x=-1; x<=1; x++) {
                    for (int z=-1; z<=1; z++) {
                        var cell = BlastFurnaceLayout.at(x,y,z,d[0],d[1]);
                        switch (cell) {
                            case FIRECLAY -> bricks++;
                            case HATCH -> hatches++;
                            case AIR -> air++;
                        }
                        if (y==3 && ((Math.abs(x)+Math.abs(z)==1)
                                != (cell==BlastFurnaceLayout.Cell.FIRECLAY)))
                            throw new AssertionError("Wrong top cardinal layout");
                        if (y==2 && ((x==0 && z==0) != (cell==BlastFurnaceLayout.Cell.AIR)))
                            throw new AssertionError("Chamber is not hollow");
                        if (y==1 && ((x==d[0] && z==d[1]) != (cell==BlastFurnaceLayout.Cell.HATCH)))
                            throw new AssertionError("Hatch is not on the outer front face");
                    }
                }
            }
            if (bricks!=29 || hatches!=1 || air!=6)
                throw new AssertionError("Wrong block count: " + bricks + "/" + hatches + "/" + air);
        }
        System.out.println("PASS: four rotations; 29 fireclay, 1 hatch, 6 air; hollow chamber; cardinal top pattern");
    }
}
