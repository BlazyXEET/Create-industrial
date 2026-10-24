#!/usr/bin/env python3
"""V14 source-level regression checks; real Minecraft tests run separately."""
from pathlib import Path
import json
R=Path(__file__).resolve().parents[1]
J=R/'src/main/java/net/createindustrialteam/createindustrial'
A=R/'src/main/resources/assets/createindustrial'
read=lambda q:(J/q).read_text()
layout=read('multiblock/LargeBlastFurnaceLayout.java')
assert 'new String[]{"BBBBB", "I...O", "B...B", "F...G", "BBCBB"}' in layout
assert 'new String[]{".BBB.", "B...B", "B...B", "B...B", ".BBB."}' in layout
ports=read('multiblock/BlastFurnaceMultiblock.java')
assert 'BlockPos items = center.relative(facing.getOpposite())' in ports
assert 'BlockPos fluids = center.relative(facing)' in ports
resolver=read('foundry/PortConnections.java')
assert 'mode.isFluid()' in resolver and 'rowCenter.relative(front.getOpposite())' in resolver
assert 'rowCenter.relative(front)' in resolver
assert 'rowCenter.below()' in resolver
client=read('client/WelderInputClient.java')
assert 'WelderAirTargetClient.isAltDown(mc)' in client
assert 'false, true' in client
assert 'mc.player.isShiftKeyDown()' in client
selection=read('client/WelderSelectionClient.java')
assert 'AIR_POINT' in selection and 'WelderAirTargetClient.target(mc)' in selection
network=read('network/WelderClickRequest.java')
assert 'boolean clearInAir, boolean selectAir' in network
assert 'player.serverLevel().getBlockState(target).isAir()' in network
assert 'ClipContext.Block.OUTLINE' in network and 'HitResult.Type.MISS' in network
assert 'WelderActions.use(player, hand, target, Direction.UP)' in network
assert 'largeFurnaceAltAirCorners' in read('gametest/IndustrialGameTests.java')
icon=read('ModCreativeTabs.java'); assert 'ModItems.CREATIVE_TAB_ICON.get()' in icon
assert 'register("cooling_tower_icon"' in read('items/ModItems.java')
icon_model=json.loads((A/'models/item/cooling_tower_icon.json').read_text())
assert icon_model['textures']['layer0']=='createindustrial:item/cooling_tower_icon'
assert (A/'textures/item/cooling_tower_icon.png').is_file()
print('PASS: corrected layer 2 & 3, port resolver, 2-click ALT air targeting with LOS checks, Creative icon, GameTest')
