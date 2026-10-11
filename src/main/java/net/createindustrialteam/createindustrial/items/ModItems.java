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

    public static final DeferredItem<BlockItem> REINFORCED_CONCRETE =
            ITEMS.registerSimpleBlockItem("reinforced_concrete", ModBlocks.REINFORCED_CONCRETE);

    public static final DeferredItem<BlockItem> PLASTERED_REINFORCED_CONCRETE =
            ITEMS.registerSimpleBlockItem("plastered_reinforced_concrete", ModBlocks.PLASTERED_REINFORCED_CONCRETE);

    public static final DeferredItem<BlockItem> CONDENSING_MESH =
            ITEMS.registerSimpleBlockItem("condensing_mesh", ModBlocks.CONDENSING_MESH);

    public static final DeferredItem<BlockItem> BLOCK_OF_URANIUM =
            ITEMS.registerSimpleBlockItem("block_of_uranium", ModBlocks.BLOCK_OF_URANIUM);


    public static void register(IEventBus modeventBus){
        ITEMS.register(modeventBus);
    }
}
