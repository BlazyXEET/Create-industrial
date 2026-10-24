package net.createindustrialteam.createindustrial.foundry;

public final class FurnaceRulesTest {
    public static void main(String[] args) {
        expect(FurnaceRules.fillLevel(0) == 0, "empty tank");
        expect(FurnaceRules.fillLevel(1) == 1, "smallest melt must show");
        expect(FurnaceRules.fillLevel(FurnaceRules.CAPACITY_MB) == 4, "full tank");
        expect(FurnaceRules.fillLevel(FurnaceRules.CAPACITY_MB / 2) == 2, "half full");
        expect(FurnaceRules.canAccept(0, FurnaceRules.INGOT_MB, true), "accept first ingot");
        expect(!FurnaceRules.canAccept(2880, 144, true), "no overflow");
        expect(!FurnaceRules.canAccept(144, 144, false), "no mixing unrelated metals");
        expect(FurnaceRules.canCast(144, 1550, 1538), "hot iron cast");
        expect(!FurnaceRules.canCast(143, 1600, 1538), "no material duplication");
        expect(!FurnaceRules.canCast(144, 900, 1538), "cold iron cannot cast");
        int hot=20;
        for(int i=0;i<500;i++) hot=FurnaceRules.nextTemperature(hot,true,i);
        expect(hot==FurnaceRules.MAX_C,"furnace temperature must cap");
        for(int i=0;i<6000;i++) hot=FurnaceRules.nextTemperature(hot,false,i);
        expect(hot==FurnaceRules.AMBIENT_C,"temperature cools to ambient");
        int natural=20,blast=20,large=1700,small=1700;
        for(int i=0;i<800;i++) {
            natural=FurnaceRules.nextTemperature(natural,true,i,false,false,true);
            blast=FurnaceRules.nextTemperature(blast,true,i,true,false,true);
            large=FurnaceRules.nextTemperature(large,false,i,false,true,true);
            small=FurnaceRules.nextTemperature(small,false,i,false,false,true);
        }
        expect(natural<=1100 && blast==1700,"air blast must be needed for high temperatures");
        expect(large>small,"larger refractory mass must cool more slowly");
        expect(FurnaceRules.capacity(true)==4*FurnaceRules.capacity(false),"large hearth capacity");
        expect(!FurnaceRules.canAccept(11520,144,true,FurnaceRules.capacity(true)),"large hearth overflow");
        expect(FurnaceRules.fillLevel(11520,11520)==4,"large hearth fill visualization");
        System.out.println("FurnaceRulesTest: PASS");
    }
    private static void expect(boolean result, String message) { if(!result) throw new AssertionError(message); }
}
