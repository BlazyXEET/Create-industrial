package net.createindustrialteam.createindustrial.items;

import net.createindustrialteam.createindustrial.blocks.ModBlocks;
import net.minecraft.world.item.BlockItem;
import net.neoforged.bus.api.IEventBus;
import net.neoforged.neoforge.registries.DeferredItem;
import net.neoforged.neoforge.registries.DeferredRegister;

public class ModItems {
    public static final DeferredRegister.Items ITEMS =
            DeferredRegister.createItems("createindustrial");


    public static final DeferredItem<BlockItem> BLOCK_OF_ALUMINIUM_ITEM =
            ITEMS.registerSimpleBlockItem("block_of_aluminium", ModBlocks.BLOCK_OF_ALUMINIUM);

    public static void register(IEventBus modeventBus){
        ITEMS.register(modeventBus);
    }
}
