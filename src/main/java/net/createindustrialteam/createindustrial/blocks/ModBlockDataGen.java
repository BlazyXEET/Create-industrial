
package net.createindustrialteam.createindustrial.blocks;

import net.minecraft.data.PackOutput;
import net.minecraft.world.level.block.Block;

import net.neoforged.neoforge.client.model.generators.BlockStateProvider;
import net.neoforged.neoforge.client.model.generators.ModelFile;
import net.neoforged.neoforge.common.data.ExistingFileHelper;

public class ModBlockDataGen extends BlockStateProvider {

    public ModBlockDataGen(
            PackOutput output,
            ExistingFileHelper exFileHelper
    ) {
        super(output, "createindustrial", exFileHelper);
    }
    private void generateSimpleBlock(Block block, String blockName) {
        simpleBlockWithItem( block,models().cubeAll(blockName, modLoc("block/" + blockName)));
    }

    @Override
    protected void registerStatesAndModels() {
        generateSimpleBlock(ModBlocks.KIRK_BLOCK.get(), "kirk_block");
        generateSimpleBlock(ModBlocks.BLOCK_OF_ALUMINIUM.get(), "block_of_aluminium");
        generateSimpleBlock(ModBlocks.BLOCK_OF_STEEL.get(), "block_of_steel");
        generateSimpleBlock(ModBlocks.BAUXITE_ORE.get(), "bauxite_ore");
        generateSimpleBlock(ModBlocks.BLOCK_OF_URANIUM.get(), "block_of_uranium");
        generateSimpleBlock(ModBlocks.BLOCK_OF_PLUTONIUM.get(), "block_of_plutonium");
        generateSimpleBlock(ModBlocks.BLOCK_OF_CALIFORNIUM.get(), "block_of_californium");
        generateSimpleBlock(ModBlocks.CONDENSING_MESH.get(), "condensing_mesh");
        generateSimpleBlock(ModBlocks.REFRACTORY_BRICKS.get(), "refractory_bricks");

        simpleBlockWithItem( ModBlocks.REINFORCED_CONCRETE.get(),models().cubeBottomTop(
                                "reinforced_concrete",
                        modLoc("block/reinforced_concrete"),
                        modLoc("block/reinforced_concrete_top"),
                        modLoc("block/reinforced_concrete_top")));


    }
}
