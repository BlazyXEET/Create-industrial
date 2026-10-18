package net.createindustrialteam.createindustrial.blocks;

import net.minecraft.core.BlockBox;
import net.minecraft.core.BlockPos;
import net.minecraft.world.level.BlockGetter;
import net.minecraft.world.level.block.Block;
import net.minecraft.world.level.block.state.BlockState;
import net.minecraft.world.phys.shapes.CollisionContext;
import net.minecraft.world.phys.shapes.Shapes;
import net.minecraft.world.phys.shapes.VoxelShape;
import net.neoforged.neoforge.client.event.RenderHighlightEvent;

public class ReactorFuelRodFrameBlock extends Block {
    public static final VoxelShape SHAPE = Shapes.or(
            Block.box(0,4,0, 16, 6, 16),
            Block.box(0,12,0, 16, 14, 16)
    );
    public ReactorFuelRodFrameBlock(Properties props) {super(props);}

    @Override
    protected VoxelShape getShape(BlockState State, BlockGetter Level, BlockPos pos, CollisionContext ctx){
        return SHAPE;
    }
}
