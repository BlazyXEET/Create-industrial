package net.createindustrialteam.createindustrial.multiblock;

import java.util.HashMap;
import java.util.Map;

/** Runs the same production matcher used against Minecraft block states. */
public final class BlastFurnaceBehaviorTest {
    private static int assertions;
    private static void check(boolean condition, String label) {
        assertions++;
        if (!condition) throw new AssertionError(label);
    }
    private static String key(int x,int y,int z) { return x+","+y+","+z; }
    public static void main(String[] args) {
        for (int[] facing : new int[][]{{0,1},{1,0},{0,-1},{-1,0}}) {
            int fx=facing[0], fz=facing[1];
            Map<String,BlastFurnaceLayout.Seen> cells = new HashMap<>();
            for (int y=0;y<4;y++) for (int z=-1;z<=1;z++) for (int x=-1;x<=1;x++) {
                cells.put(key(x,y,z), switch(BlastFurnaceLayout.at(x,y,z,fx,fz)) {
                    case FIRECLAY -> BlastFurnaceLayout.Seen.FIRECLAY;
                    case HATCH -> BlastFurnaceLayout.Seen.HATCH;
                    case AIR -> BlastFurnaceLayout.Seen.AIR;
                });
            }
            BlastFurnaceLayout.Sampler sample = (x,y,z)->cells.get(key(x,y,z));
            check(BlastFurnaceLayout.scan(fx,fz,false,sample).valid(),"classic 29-brick shape");
            cells.put(key(0,1,0),BlastFurnaceLayout.Seen.AIR);
            check(BlastFurnaceLayout.scan(fx,fz,false,sample).valid(),"open lower core");
            for (var entry : new HashMap<>(cells).entrySet()) {
                if (entry.getValue()!=BlastFurnaceLayout.Seen.FIRECLAY) continue;
                cells.put(entry.getKey(),BlastFurnaceLayout.Seen.AIR);
                var result=BlastFurnaceLayout.scan(fx,fz,false,sample);
                check(!result.valid() && result.missing().size()==1,"each required brick is checked: "+entry.getKey());
                cells.put(entry.getKey(),entry.getValue());
            }
            cells.put(key(0,2,0),BlastFurnaceLayout.Seen.OTHER);
            check(BlastFurnaceLayout.scan(fx,fz,false,sample).obstructed().size()==1,"blocked chimney");
            cells.put(key(0,2,0),BlastFurnaceLayout.Seen.AIR);
            cells.put(key(0,1,0),BlastFurnaceLayout.Seen.MOLTEN);
            check(!BlastFurnaceLayout.scan(fx,fz,false,sample).valid(),"unowned molten block must not form");
            check(BlastFurnaceLayout.scan(fx,fz,true,sample).valid(),"formed molten tank");
            cells.put(key(0,1,0),BlastFurnaceLayout.Seen.AIR);
            cells.put(key(1,3,1),BlastFurnaceLayout.Seen.FIRECLAY);
            check(!BlastFurnaceLayout.scan(fx,fz,false,sample).valid(),"no extra corner towers");
            cells.put(key(1,3,1),BlastFurnaceLayout.Seen.AIR);
            cells.put(key(0,0,0),BlastFurnaceLayout.Seen.UNLOADED);
            var unloaded=BlastFurnaceLayout.scan(fx,fz,false,sample);
            check(!unloaded.loaded() && !unloaded.valid(),"unloaded is not a valid machine");
        }
        System.out.println("PASS: "+assertions+" production furnace-matcher assertions");
    }
}
