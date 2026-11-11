
package net.createindustrialteam.createindustrial;

import net.createindustrialteam.createindustrial.blocks.ModBlockDataGen;

import net.minecraft.data.DataGenerator;

import net.neoforged.bus.api.SubscribeEvent;
import net.neoforged.neoforge.data.event.GatherDataEvent;

public class ModDataGenerators {

    @SubscribeEvent
    public static void gatherData(GatherDataEvent event) {

        DataGenerator generator = event.getGenerator();

        generator.addProvider(
                event.includeClient(),
                new ModBlockDataGen(
                        generator.getPackOutput(),
                        event.getExistingFileHelper()
                )
        );
    }
}
