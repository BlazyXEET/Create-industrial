package net.createindustrialteam.createindustrial.ponder;

import net.createmod.catnip.math.Pointing;
import net.createmod.ponder.api.PonderPalette;
import net.createmod.ponder.api.scene.SceneBuilder;
import net.createmod.ponder.api.scene.SceneBuildingUtil;
import net.createindustrialteam.createindustrial.ponder.util.PonderScene;
import net.createmod.ponder.foundation.instruction.PonderInstruction;
import net.minecraft.core.BlockPos;
import net.minecraft.core.Direction;
import net.minecraft.world.phys.AABB;
import net.minecraft.world.phys.Vec3;

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
        AABB bb = new AABB(
                0, 1, 0,
                0, 1,0
        );
        var sel = util.select().position(pos);

        for (int y = 1; y <= 7; y++) {
            reveal(scene, util.select().layer(y), Direction.DOWN);
            scene.idle(2); // pause between layers
        }
        scene.idle(10);
        customShowTextAbove(scene, util, "blank 1", pos,15);
        scene.idle(20);
        customShowTextAbove(scene, util, "blank 2", pos,15);
        scene.idle(20);
        scene.overlay().chaseBoundingBoxOutline(
                PonderPalette.OUTPUT, "glue", bb, 1
        );

        scene.overlay().chaseBoundingBoxOutline(
                PonderPalette.OUTPUT,
                "glue",
                bb.expandTowards(7, 8, 7),
                60
        );
        customShowTextAbove(scene, util, "blank 3", pos,15);
    };
};
