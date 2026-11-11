package net.createindustrialteam.createindustrial;

import com.mojang.logging.LogUtils;
import net.createindustrialteam.createindustrial.blocks.ModBlockDataGen;
import net.createindustrialteam.createindustrial.blocks.ModBlocks;
import net.createindustrialteam.createindustrial.items.ModCreativeModTabs;
import net.createindustrialteam.createindustrial.items.ModItems;
import net.neoforged.bus.api.IEventBus;
import net.neoforged.fml.ModContainer;
import net.neoforged.fml.common.Mod;
import net.neoforged.fml.config.ModConfig;
import net.neoforged.fml.event.lifecycle.FMLCommonSetupEvent;
import net.neoforged.neoforge.data.event.GatherDataEvent;
import net.neoforged.neoforge.event.BuildCreativeModeTabContentsEvent;
import net.neoforged.neoforge.event.server.ServerStartingEvent;
import net.neoforged.neoforge.common.NeoForge;
import net.neoforged.bus.api.SubscribeEvent;
import org.slf4j.Logger;

@Mod(CreateIndustrial.MODID)
public class CreateIndustrial {
    public static final String MODID = "createindustrial";
    public static final Logger LOGGER = LogUtils.getLogger();

    public CreateIndustrial(IEventBus modEventBus, ModContainer modContainer) {
        modEventBus.addListener(this::commonSetup);
        modEventBus.addListener(this::addCreative);

        modEventBus.register(ModDataGenerators.class);
        ModBlocks.register(modEventBus);
        ModItems.register(modEventBus);
        ModCreativeModTabs.register(modEventBus);


        NeoForge.EVENT_BUS.register(this);

        modContainer.registerConfig(ModConfig.Type.COMMON, Config.SPEC);
    }

    private void commonSetup(FMLCommonSetupEvent event) {
    }


    private void addCreative(BuildCreativeModeTabContentsEvent event) {
    }

    @SubscribeEvent
    public void onServerStarting(ServerStartingEvent event) {
    }
}