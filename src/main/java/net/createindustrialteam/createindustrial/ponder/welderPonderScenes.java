package net.createindustrialteam.createindustrial.ponder;

import net.createmod.ponder.api.scene.SceneBuilder;
import net.createmod.ponder.api.scene.SceneBuildingUtil;
import net.createindustrialteam.createindustrial.ponder.util.PonderScene;
import net.createmod.ponder.foundation.instruction.PonderInstruction;
import net.minecraft.core.Direction;

public class welderPonderScenes extends PonderScene {
    public static void intro(SceneBuilder scene, SceneBuildingUtil util) {
        scene.title("welder_intro", "Welding multiblocks together");
        zoom(scene, 0.4f);
        setupScene(7,scene);

        var pos = util.grid().at(2,1,2);
        var sel = util.select().position(pos);

        for (int y = 1; y <= 8; y++) {
            reveal(scene, util.select().layer(y), Direction.DOWN);
            scene.idle(2); // pause between layers
        }
        scene.idle(20);
        showTextAbove(scene, util, "i am gay", pos);

    };
};
