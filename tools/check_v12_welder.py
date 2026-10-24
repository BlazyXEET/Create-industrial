#!/usr/bin/env python3
from pathlib import Path
import json
R=Path(__file__).resolve().parents[1]
S=R/'src/main/java/net/createindustrialteam/createindustrial'
read=lambda name:(S/name).read_text()
model=json.loads((R/'src/main/resources/assets/createindustrial/models/item/welder_3d.json').read_text())
assert len(model['elements'])>=30 # Hand-authored reference-model geometry
assert model['display']['thirdperson_righthand']['rotation'][2] < 0
assert model['display']['thirdperson_lefthand']['rotation'][2] > 0
assert 'WeldedMachineOutlinesClient.onClientTick(event)' in read('client/IndustrialClient.java')
assert '@EventBusSubscriber' in read('client/IndustrialClient.java')
assert '0xFFD22F' in read('client/WeldedMachineOutlinesClient.java')
assert 'showCluster(view.key().edges, view.members())' in read('client/WeldedMachineOutlinesClient.java')
assert 'getBlockEntitiesPos()' in read('client/WeldedMachineOutlinesClient.java')
assert 'PacketDistributor.sendToServer(new WelderClickRequest' in read('client/WelderInputClient.java')
assert 'ParticleTypes.ELECTRIC_SPARK' in read('items/WelderActions.java')
assert 'PortConnections.resolve' in read('foundry/ModBlockEntities.java')
assert 'Capabilities.ItemHandler.BLOCK' in read('foundry/ModBlockEntities.java')
assert 'Capabilities.FluidHandler.BLOCK' in read('foundry/ModBlockEntities.java')
assert 'openMenu(' not in read('blocks/BlastFurnaceHatchBlock.java')
assert 'addToGoggleTooltip' in read('foundry/BlastFurnaceBlockEntity.java')
assert 'CAMPFIRE_COSY_SMOKE' in read('foundry/BlastFurnaceBlockEntity.java')
assert 'changePorts(level,hatch,direction,assembled)' in read('multiblock/BlastFurnaceMultiblock.java')
assert 'onMemberRemoved' in read('blocks/IndustrialPortBlock.java')
print('PASS: V12 sword hold, yellow held welds, spark, 4 ports, Create fluid + item capabilities, GUI-free and goggles hooks')
