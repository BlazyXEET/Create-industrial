package net.createindustrialteam.createindustrial.foundry;

import java.util.Random;

/** Executable invariant tests, with no NeoForge/Gradle dependency. */
public final class FurnaceTransferRulesTest {
    private static long cases;
    private static void check(boolean good, String message) {
        cases++;
        if (!good) throw new AssertionError(message);
    }
    public static void main(String[] ignored) {
        check(FurnaceTransferRules.accepted(0, 64, 64, true) == 64, "full stack insertion");
        check(FurnaceTransferRules.accepted(63, 64, 64, true) == 1, "near-full stack");
        check(FurnaceTransferRules.accepted(64, 1, 64, true) == 0, "full inventory");
        check(FurnaceTransferRules.accepted(65, 1, 64, true) == 0, "invalid existing stack");
        check(FurnaceTransferRules.accepted(0, Integer.MAX_VALUE, 64, true) == 64, "unbounded request");
        check(FurnaceTransferRules.accepted(Integer.MIN_VALUE, 100, 64, true) == 0, "corrupted store");
        check(FurnaceTransferRules.accepted(0, -100, 64, true) == 0, "negative input");
        check(FurnaceTransferRules.accepted(0, 100, 64, false) == 0, "mixed metal/item type");
        check(FurnaceTransferRules.extracted(144, 9999) == 144, "bounded extraction");
        check(FurnaceTransferRules.extracted(144, -1) == 0, "negative extraction");
        check(FurnaceTransferRules.extracted(Integer.MAX_VALUE, Integer.MAX_VALUE) == Integer.MAX_VALUE, "maximum values");
        Random random = new Random(0xF0A22);
        for (int i = 0; i < 160_000; i++) {
            int capacity = random.nextInt(12000) + 1;
            int stored = random.nextInt(capacity + 1);
            int offered = random.nextInt(30000);
            boolean compatible = random.nextBoolean();
            int accepted = FurnaceTransferRules.accepted(stored, offered, capacity, compatible);
            check(accepted >= 0 && accepted <= offered && (long) stored + accepted <= capacity,
                    "insertion overflow: " + i);
            check(compatible || accepted == 0, "mixed fluid accepted");
            check(accepted == FurnaceTransferRules.accepted(stored, offered, capacity, compatible),
                    "nondeterministic simulation");
            int requested = random.nextInt(30000);
            int extracted = FurnaceTransferRules.extracted(stored, requested);
            check(extracted >= 0 && extracted <= stored && extracted <= requested,
                    "extraction underflow: " + i);
        }
        System.out.println("PASS: " + cases + " conserved-transfer arithmetic assertions");
    }
}
