package net.createindustrialteam.createindustrial.items;

/** Offline rules for two-click selections; no NeoForge classpath required. */
public final class SelectionPolicyTest {
    private static void check(boolean condition, String description) {
        if (!condition) throw new AssertionError(description);
    }
    public static void main(String[] args) {
        check(SelectionPolicy.isFresh(0, 0), "first tick");
        check(SelectionPolicy.isFresh(100, 100 + SelectionPolicy.MAX_AGE_TICKS), "end of timeout");
        check(!SelectionPolicy.isFresh(100, 100 + SelectionPolicy.MAX_AGE_TICKS + 1), "selection expiry");
        check(!SelectionPolicy.isFresh(101, 100), "time rewind / reload");
        check(!SelectionPolicy.isFresh(-1, 0), "untrusted negative time");
        check(SelectionPolicy.withinBounds(15, 0, 0, 16, 24), "max axis span");
        check(!SelectionPolicy.withinBounds(16, 0, 0, 16, 24), "oversized axis");
        check(!SelectionPolicy.withinBounds(0, 0, 0, 16, 24), "same block cannot be both corners");
        check(SelectionPolicy.withinBounds(15, 15, 0, 16, 24), "2D diagonal");
        check(!SelectionPolicy.withinBounds(15, 15, 15, 16, 24), "too long 3D diagonal");
        check(!SelectionPolicy.withinBounds(Integer.MAX_VALUE, 0, 0, 16, 24), "overflow safe");
        check(!SelectionPolicy.withinBounds(1, 1, 1, 0, 24), "invalid config");
        System.out.println("PASS: timed selections, axis bounds, diagonal reach, overflow checks");
    }
}
