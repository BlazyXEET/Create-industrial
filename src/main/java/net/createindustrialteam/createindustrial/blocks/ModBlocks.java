package net.createindustrialteam.createindustrial.blocks;

import net.minecraft.world.level.block.*;
import net.minecraft.world.level.block.state.BlockBehaviour;
import net.neoforged.bus.api.IEventBus;
import net.neoforged.neoforge.registries.DeferredBlock;
import net.neoforged.neoforge.registries.DeferredRegister;

public class ModBlocks {

    public static final DeferredRegister.Blocks BLOCKS =
            DeferredRegister.createBlocks("createindustrial");


    //basic blocks

    public static final DeferredBlock<Block> REINFORCED_CONCRETE = BLOCKS.registerSimpleBlock(
            "reinforced_concrete",
            BlockBehaviour.Properties.of()
                    .sound(SoundType.STONE)
                    .strength(0.9f,8f)
                    .requiresCorrectToolForDrops()

    );

    public static final DeferredBlock<Block> BLOCK_OF_ALUMINIUM = BLOCKS.registerSimpleBlock(
            "block_of_aluminium",
            BlockBehaviour.Properties.of()
                    .sound(SoundType.METAL)
                    .strength(0.5f,1f)
                    .requiresCorrectToolForDrops()

    );

    public static final DeferredBlock<Block> KIRK_BLOCK = BLOCKS.registerSimpleBlock(
            "kirk_block",
            BlockBehaviour.Properties.of()
                    .sound(SoundType.METAL)
                    .strength(0.5f,1f)
                    .requiresCorrectToolForDrops()
    );



    public static final DeferredBlock<Block> PLASTERED_REINFORCED_CONCRETE = BLOCKS.registerSimpleBlock(
            "plastered_reinforced_concrete",
            BlockBehaviour.Properties.of()
                    .sound(SoundType.STONE)
                    .strength(0.9f,8f)
                    .requiresCorrectToolForDrops()

    );

    public static final DeferredBlock<Block> BLOCK_OF_URANIUM = BLOCKS.registerSimpleBlock(
            "block_of_uranium",
            BlockBehaviour.Properties.of()
                    .sound(SoundType.METAL)
                    .strength(0.3f,6f)
                    .requiresCorrectToolForDrops()
                    .lightLevel(State -> 7)

    );

    public static final DeferredBlock<Block> BLOCK_OF_PLUTONIUM = BLOCKS.registerSimpleBlock(
            "block_of_plutonium",
            BlockBehaviour.Properties.of()
                    .sound(SoundType.METAL)
                    .strength(0.3f,6f)
                    .requiresCorrectToolForDrops()
                    .lightLevel(State -> 7)

    );

    public static final DeferredBlock<Block> BLOCK_OF_CALIFORNIUM = BLOCKS.registerSimpleBlock(
            "block_of_californium",
            BlockBehaviour.Properties.of()
                    .sound(SoundType.METAL)
                    .strength(0.3f,6f)
                    .requiresCorrectToolForDrops()
                    .lightLevel(State -> 7)


    );

    public static final DeferredBlock<Block> BLOCK_OF_STEEL = BLOCKS.registerSimpleBlock(
            "block_of_steel",
            BlockBehaviour.Properties.of()
                    .sound(SoundType.METAL)
                    .strength(0.3f,6f)
                    .requiresCorrectToolForDrops()

    );

    public static final DeferredBlock<Block> REFRACTORY_BRICKS = BLOCKS.registerSimpleBlock(
            "refractory_bricks",
            BlockBehaviour.Properties.of()
                    .sound(SoundType.DEEPSLATE_BRICKS)
                    .strength(0.3f,6f)
                    .requiresCorrectToolForDrops()

    );



    public static final DeferredBlock<ReactorFuelRodFrameBlock> REACTOR_FUEL_ROD_FRAME = BLOCKS.registerBlock(
            "reactor_fuel_rod_frame",
            ReactorFuelRodFrameBlock::new,
            BlockBehaviour.Properties.of()
                    .sound(SoundType.COPPER_GRATE)
                    .strength(0.2f,0.5f)
                    .requiresCorrectToolForDrops()
                    .noOcclusion()


    );



    public static final DeferredBlock<Block> CONDENSING_MESH = BLOCKS.registerSimpleBlock(
            "condensing_mesh",
            BlockBehaviour.Properties.of()
                    .sound(SoundType.COPPER_GRATE)
                    .strength(0.2f,0.5f)
                    .requiresCorrectToolForDrops()
                    .noOcclusion()

    );



 public static final DeferredBlock<Block> BAUXITE_ORE = BLOCKS.registerSimpleBlock(
        "bauxite_ore",
        BlockBehaviour.Properties.of()
                .sound(SoundType.METAL)
                .strength(0.5f,1f)
                .requiresCorrectToolForDrops()

);

    public static final DeferredBlock<Block> ALUMINA_DUST_LAYER = BLOCKS.registerSimpleBlock(
            "alumina_dust_layer",
            BlockBehaviour.Properties.of()
                    .sound(SoundType.SAND)
                    .strength(0.5f,1f)
                    .requiresCorrectToolForDrops()

    );

     public static final DeferredBlock<SlabBlock> REINFORCED_CONCRETE_SLAB = BLOCKS.register(
            "reinforced_concrete_slab",
             () -> new SlabBlock(
                     BlockBehaviour.Properties.of()
                     .sound(SoundType.STONE)
                     .strength(0.5f,1f)
                     .requiresCorrectToolForDrops()
             ));
    public static final DeferredBlock<WallBlock> REINFORCED_CONCRETE_WALL = BLOCKS.register(
            "reinforced_concrete_wall",
            () -> new WallBlock(BlockBehaviour.Properties.of()
                    .sound(SoundType.STONE)
                    .strength(0.5f,1f)
                    .requiresCorrectToolForDrops()
            )
    );;

     public static final DeferredBlock<StairBlock> REINFORCED_CONCRETE_STAIRS = BLOCKS.register(
            "reinforced_concrete_stairs",
             () -> new StairBlock(REINFORCED_CONCRETE.get().defaultBlockState(), BlockBehaviour.Properties.of()
                     .sound(SoundType.STONE)
                    .strength(0.5f,1f)
                     .requiresCorrectToolForDrops()
             )
    );

 //Marker
    public static void register(IEventBus modEventBus){
        BLOCKS.register(modEventBus);
    }
}