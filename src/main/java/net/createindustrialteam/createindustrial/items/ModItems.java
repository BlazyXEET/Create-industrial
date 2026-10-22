package net.createindustrialteam.createindustrial.items;

import net.createindustrialteam.createindustrial.blocks.ModBlocks;
import net.minecraft.world.item.BlockItem;
import net.minecraft.world.item.Item;
import net.neoforged.bus.api.IEventBus;
import net.neoforged.neoforge.registries.DeferredItem;
import net.neoforged.neoforge.registries.DeferredRegister;

public class ModItems {
    public static final DeferredRegister.Items ITEMS =
            DeferredRegister.createItems("createindustrial");
    // Block items
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

    public static final DeferredItem<BlockItem> BLOCK_OF_PLUTONIUM =
            ITEMS.registerSimpleBlockItem("block_of_plutonium", ModBlocks.BLOCK_OF_PLUTONIUM);

    public static final DeferredItem<BlockItem> BLOCK_OF_CALIFORNIUM =
            ITEMS.registerSimpleBlockItem("block_of_californium", ModBlocks.BLOCK_OF_CALIFORNIUM);

    public static final DeferredItem<BlockItem> BLOCK_OF_STEEL =
            ITEMS.registerSimpleBlockItem("block_of_steel", ModBlocks.BLOCK_OF_STEEL);

    public static final DeferredItem<BlockItem> FIRE_BRICKS =
            ITEMS.registerSimpleBlockItem("fire_bricks", ModBlocks.FIRE_BRICKS);


    public static final DeferredItem<BlockItem> REACTOR_FUEL_ROD_FRAME =
            ITEMS.registerSimpleBlockItem("reactor_fuel_rod_frame", ModBlocks.REACTOR_FUEL_ROD_FRAME);

    public static final DeferredItem<BlockItem> BAUXITE_ORE =
            ITEMS.registerSimpleBlockItem("bauxite_ore", ModBlocks.BAUXITE_ORE);

    // regular items
    public static final DeferredItem<Item> FIRE_BRICK =
        ITEMS.registerSimpleItem("fire_brick");

    public static final DeferredItem<Item> BAUXITE_POWDER =
        ITEMS.registerSimpleItem("bauxite_powder");

    public static final DeferredItem<Item> STEEL_INGOT =
        ITEMS.registerSimpleItem("steel_ingot");

    public static final DeferredItem<Item> QUARTZITE_DUST =
        ITEMS.registerSimpleItem("quartzite_dust");

    public static final DeferredItem<Item> IMPURE_SILICON_DUST =
        ITEMS.registerSimpleItem("impure_silicon_dust");

    public static final DeferredItem<Item> PURE_SILICON_DUST =
        ITEMS.registerSimpleItem("pure_silicon_dust");

    public static final DeferredItem<Item> ALUMINIUM_NUGGET =
        ITEMS.registerSimpleItem("aluminium_nugget");

    public static final DeferredItem<Item> WELDER =
    ITEMS.registerSimpleItem("welder");

    public static final DeferredItem<Item> SILICON_WAFER =
    ITEMS.registerSimpleItem("silicon_wafer");

    public static final DeferredItem<Item> PRINTED_SILICON_WAFER =
    ITEMS.registerSimpleItem("printed_silicon_wafer");

    public static final DeferredItem<Item> PLUTONIUM_INGOT =
    ITEMS.registerSimpleItem("plutonium_ingot");

    public static final DeferredItem<Item> STEEL_PLATE =
    ITEMS.registerSimpleItem("steel_plate");

    public static final DeferredItem<Item> SILICON_CHIP =
    ITEMS.registerSimpleItem("silicon_chip");

    public static final DeferredItem<Item> UNFIRED_FIRECLAY =
    ITEMS.registerSimpleItem("unfired_fireclay");

    //Marker
    public static void register(IEventBus modEventBus){
        ITEMS.register(modEventBus);
    }
}


