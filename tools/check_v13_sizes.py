#!/usr/bin/env python3
from pathlib import Path
import json
R=Path(__file__).resolve().parents[1]
S=R/'src/main/java/net/createindustrialteam/createindustrial'
read=lambda name:(S/name).read_text()
assert 'new BlastFurnaceMultiblock(FurnaceScale.SMALL)' in read('multiblock/MachineRegistry.java')
assert 'new BlastFurnaceMultiblock(FurnaceScale.LARGE)' in read('multiblock/MachineRegistry.java')
assert 'only two active ports' in read('multiblock/BlastFurnaceMultiblock.java').lower()
assert 'result.put(PortMode.ITEM_OUT' in read('multiblock/BlastFurnaceMultiblock.java')
assert 'if (size == FurnaceScale.LARGE)' in read('multiblock/BlastFurnaceMultiblock.java')
assert 'large()' in read('foundry/BlastFurnaceBlockEntity.java')
assert 'itemPort(net.createindustrialteam.createindustrial.blocks.PortMode.ITEM_IN)' in read('foundry/ModBlockEntities.java')
assert 'Mode.ITEM_IN' in read('foundry/PortItemHandler.java')
assert 'new WelderClickRequest' in read('client/WelderInputClient.java')
assert 'getBlockEntitiesPos()' in read('client/WeldedMachineOutlinesClient.java')
assert '0xFFD22F' in read('client/WeldedMachineOutlinesClient.java')
assert 'ParticleTypes.ELECTRIC_SPARK' in read('items/WelderActions.java')
assert 'openMenu(' not in read('blocks/BlastFurnaceHatchBlock.java')
assert 'addToGoggleTooltip' in read('foundry/BlastFurnaceBlockEntity.java')
assert 'CAMPFIRE_COSY_SMOKE' in read('foundry/BlastFurnaceBlockEntity.java')
assert len(json.loads((R/'src/main/resources/assets/createindustrial/models/item/welder_3d.json').read_text())['elements'])>=30
assert len(json.loads((R/'src/main/resources/assets/createindustrial/blockstates/blast_furnace_hatch.json').read_text())['variants'])==32
print('PASS: both machine types, independent Welder, size state, yellow weld outlines, GUI-free ports, and 32 hatch resource variants')
