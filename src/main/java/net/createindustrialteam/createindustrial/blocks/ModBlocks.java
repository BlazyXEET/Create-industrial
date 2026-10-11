package net.createindustrialteam.createindustrial.blocks;

import net.minecraft.world.level.block.Block;
import net.minecraft.world.level.block.SoundType;
import net.minecraft.world.level.block.state.BlockBehaviour;
import net.neoforged.bus.api.IEventBus;
import net.neoforged.neoforge.registries.DeferredBlock;
import net.neoforged.neoforge.registries.DeferredRegister;

public class ModBlocks {

    public static final DeferredRegister.Blocks BLOCKS =
            DeferredRegister.createBlocks("createindustrial");



    public static final DeferredBlock<Block> BLOCK_OF_ALUMINIUM = BLOCKS.registerSimpleBlock(
            "block_of_aluminium",
            BlockBehaviour.Properties.of()
                    .sound(SoundType.METAL)
                    .strength(0.5f,1f)
                    .requiresCorrectToolForDrops()





    );
    public static void register(IEventBus modEventBus){
        BLOCKS.register(modEventBus);
    }
}