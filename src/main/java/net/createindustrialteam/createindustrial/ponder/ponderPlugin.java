package net.createindustrialteam.createindustrial.ponder;

import net.createmod.ponder.api.registration.PonderSceneRegistrationHelper;
import net.createmod.ponder.api.registration.PonderPlugin;
import net.minecraft.resources.ResourceLocation;

public class CreateIndustrialPonderPlugin implements PonderPlugin {

    @Override
    public String getModId() {
        return "createindustrial";
    }

    @Override
    public void registerScenes(
            PonderSceneRegistrationHelper<ResourceLocation> helper) {

        helper.forComponents(
                ResourceLocation.fromNamespaceAndPath(
                        "createindustrial", "your_block"
                )
        ).addStoryBoard(
                "machines/smth",
                smth::intro
        );
    }
}