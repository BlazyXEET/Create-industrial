package net.createindustrialteam.createindustrial.multiblock;

import java.util.HashSet;
import java.util.Set;

/** Real executable JDK-only regression tests for the reusable multiblock geometry. */
public final class PatternGeometryTest {
    private static void check(boolean result, String message) {
        if (!result) throw new AssertionError(message);
    }

    public static void main(String[] args) {
        // A rectangular 3x5 pattern tests the difficult 90-degree swap, not just
        // square patterns for which rotation bugs are much harder to notice.
        VoxelPattern pattern = VoxelPattern.of(
            new String[]{"BBB", "B.B", "B.C", "B.B", "BBB"},
            new String[]{"...", ".B.", "...", ".B.", "..."}
        );
        PatternGeometry geometry = new PatternGeometry(pattern, 'C', '.');
        check(geometry.tokens().equals(Set.of('C','B','.')), "token inventory");
        check(geometry.searchRadius() == 2, "controller search radius");
        check(geometry.controllerOffsets().contains(new VoxelPattern.Offset(0,0,0)), "self candidate");
        for (int[] facing : new int[][]{{0,1},{1,0},{0,-1},{-1,0}}) {
            int controllerCount = 0;
            int nonAir = 0;
            Set<String> coords = new HashSet<>();
            Set<String> candidateOffsets = new HashSet<>();
            for (PatternGeometry.Cell cell : geometry.cells(facing[0], facing[1])) {
                String key = cell.x()+":"+cell.y()+":"+cell.z();
                check(coords.add(key), "duplicate rotated coordinate");
                if (cell.token() == 'C') {
                    controllerCount++;
                    check(cell.x()==0 && cell.y()==0 && cell.z()==0, "controller is origin");
                }
                if (cell.token() != '.') {
                    nonAir++;
                    candidateOffsets.add((-cell.x())+":"+(-cell.y())+":"+(-cell.z()));
                    check(geometry.contains(facing[0], facing[1],cell.x(),cell.y(),cell.z()),
                            "occupied member lost");
                } else check(!geometry.contains(facing[0], facing[1],cell.x(),cell.y(),cell.z()),
                        "air must not count as a structural member");
            }
            check(coords.size() == 30, "cell count");
            check(controllerCount == 1, "exactly one controller");
            check(nonAir == 14, "occupied count");
            PatternGeometry.Extents bounds = geometry.extents(facing[0], facing[1]);
            int spanX = bounds.maxX()-bounds.minX()+1;
            int spanZ = bounds.maxZ()-bounds.minZ()+1;
            check(spanX * spanZ == 15, "rotated rectangular footprint");
            if (facing[0] != 0) check(spanX==5 && spanZ==3, "east/west footprint");
            else check(spanX==3 && spanZ==5, "north/south footprint");
            check(bounds.minY()==0 && bounds.maxY()==1,"vertical extent");
            for (String offset : candidateOffsets) check(geometry.controllerOffsets().stream().anyMatch(
                o -> (o.x()+":"+o.y()+":"+o.z()).equals(offset)), "missing controller candidate");
        }
        check(!geometry.contains(0,1,100,0,100), "out-of-bounds member");
        for (int[] bad : new int[][]{{0,0},{1,1},{2,0}}) {
            try { geometry.cells(bad[0],bad[1]); throw new AssertionError("accepted invalid facing"); }
            catch (IllegalArgumentException expected) { /* pass */ }
        }
        for (char invalid : new char[]{'.','B','X'}) {
            try { new PatternGeometry(pattern, invalid, '.'); throw new AssertionError("invalid controller"); }
            catch (IllegalArgumentException expected) { /* pass */ }
        }
        System.out.println("PASS: pattern extension geometry, asymmetric rotations, controller candidates, and member lookup");
    }
}
