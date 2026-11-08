package net.createindustrialteam.createindustrial.ponder;

import net.createindustrialteam.createindustrial.items.ModItems;
import net.createmod.ponder.api.registration.PonderSceneRegistrationHelper;
import net.createmod.ponder.api.registration.PonderPlugin;
import net.minecraft.resources.ResourceLocation;

public class ponderPlugin implements PonderPlugin {

    @Override
    public String getModId() {
        return "createindustrial";
    }

    @Override
    public void registerScenes(
            PonderSceneRegistrationHelper<ResourceLocation> helper) {

        helper.forComponents( ModItems.WELDER.getId())
        .addStoryBoard(
                "welder_intro",
                welderPonderScenes::intro
        );
    }
}