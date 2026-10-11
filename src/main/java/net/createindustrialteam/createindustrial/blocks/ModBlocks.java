package net.createindustrialteam.createindustrial.blocks;

import net.minecraft.world.level.block.Block;
import net.minecraft.world.level.block.SoundType;
import net.minecraft.world.level.block.TransparentBlock;
import net.minecraft.world.level.block.state.BlockBehaviour;
import net.neoforged.bus.api.IEventBus;
import net.neoforged.neoforge.registries.DeferredBlock;
import net.neoforged.neoforge.registries.DeferredRegister;

public class ModBlocks {

    public static final DeferredRegister.Blocks BLOCKS =
            DeferredRegister.createBlocks("createindustrial");


    //basic blocks
    public static final DeferredBlock<Block> BLOCK_OF_ALUMINIUM = BLOCKS.registerSimpleBlock(
            "block_of_aluminium",
            BlockBehaviour.Properties.of()
                    .sound(SoundType.METAL)
                    .strength(0.5f,1f)
                    .requiresCorrectToolForDrops()

    );

    public static final DeferredBlock<Block> REINFORCED_CONCRETE = BLOCKS.registerSimpleBlock(
            "reinforced_concrete",
            BlockBehaviour.Properties.of()
                    .sound(SoundType.STONE)
                    .strength(0.9f,8f)
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
                    .strength(0.9f,8f)
                    .requiresCorrectToolForDrops()

    );


    // more advanced block renderings
    public static final DeferredBlock<Block> CONDENSING_MESH = BLOCKS.registerSimpleBlock(
            "condensing_mesh",
            BlockBehaviour.Properties.of()
                    .sound(SoundType.COPPER_GRATE)
                    .strength(0.9f,8f)
                    .requiresCorrectToolForDrops()
                    .noOcclusion()

    );






    public static void register(IEventBus modEventBus){
        BLOCKS.register(modEventBus);
    }
}