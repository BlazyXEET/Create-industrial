package net.createindustrialteam.createindustrial.ponder;

import net.createmod.catnip.math.Pointing;
import net.createmod.ponder.api.scene.SceneBuilder;
import net.createmod.ponder.api.scene.SceneBuildingUtil;
import net.createindustrialteam.createindustrial.ponder.util.PonderScene;
import net.createmod.ponder.foundation.instruction.PonderInstruction;
import net.minecraft.core.BlockPos;
import net.minecraft.core.Direction;

public class welderPonderScenes extends PonderScene {
    public static void customShowTextAbove(
            SceneBuilder scene,
            SceneBuildingUtil util,
            String text,
            BlockPos pos,
            int duration
    ) {
        scene.overlay().showText(duration)
                .text(text)
                .pointAt(util.vector().topOf(pos))
                .placeNearTarget();
    }
    public static void intro(SceneBuilder scene, SceneBuildingUtil util) {
        scene.title("welder_intro", "Welding multiblocks together");
        zoom(scene, 0.4f);
        setupScene(7,scene);

        var pos = util.grid().at(2,1,2);
        var firstPointerPos = util.grid().at(0,7,0);
        var secondPointerPos = util.grid().at(6,1,7);
        var sel = util.select().position(pos);

        for (int y = 1; y <= 8; y++) {
            reveal(scene, util.select().layer(y), Direction.DOWN);
            scene.idle(2); // pause between layers
        }
        scene.idle(10);
        customShowTextAbove(scene, util, "blank 1", pos,15);
        scene.idle(20);
        customShowTextAbove(scene, util, "blank 2", pos,15);
        scene.idle(20);
        scene.overlay().showControls(util.vector().topOf(firstPointerPos), Pointing.DOWN, 20).rightClick();
        scene.idle(10);
        scene.overlay().showControls(util.vector().topOf(secondPointerPos), Pointing.UP, 20).leftClick();
        print("hello world");
    };
};
