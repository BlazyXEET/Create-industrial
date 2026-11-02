package net.createindustrialteam.createindustrial.ponder;

import net.createmod.ponder.api.scene.SceneBuilder;
import net.createmod.ponder.api.scene.SceneBuildingUtil;
import net.createindustrialteam.createindustrial.ponder.util.PonderScene;
import net.createmod.ponder.foundation.instruction.PonderInstruction;
import net.minecraft.core.Direction;

public class welderPonderScenes extends PonderScene {
    public static void intro(SceneBuilder scene, SceneBuildingUtil util) {
        scene.title("Welding_intro", "Welding multiblocks together");
        setupScene(5,scene);

        var starting_pos = util.grid().at(2,1,1);
        var starting_selection = util.select().position(starting_pos);
        reveal(scene, starting_selection, Direction.DOWN);
    };
};
