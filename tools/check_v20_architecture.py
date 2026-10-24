#!/usr/bin/env python3
"""Source-level invariants to catch accidental resurrection of ports or printing."""
from pathlib import Path
R=Path(__file__).resolve().parents[1]
J=R/'src/main/java/net/createindustrialteam/createindustrial'
D=R/'src/main/resources/data/createindustrial/recipe'
def read(name):return (J/name).read_text()
assert not (D/'laser_printer.json').exists()
assert not (D/'laser_printing/silicon_wafer.json').exists()
assert not (D/'cutting/silicon_chips.json').exists()
assert 'LASER_PRINTER.get()' not in read('ModCreativeTabs.java')
assert 'registerSimpleBlockItem("laser_printer"' not in read('items/ModItems.java')
assert 'converter() && tickConverter()' in read('processing/IndustrialProcessorBlockEntity.java')
assert 'new IndustrialPortBlock' not in read('multiblock/BlastFurnaceMultiblock.java')
assert 'changePorts(' not in read('multiblock/BlastFurnaceMultiblock.java')
assert 'case \'I\'' not in read('multiblock/BlastFurnaceMultiblock.java')
assert '"B...B", "B...B", "B...B"' in read('multiblock/LargeBlastFurnaceLayout.java')
assert 'migrateLegacyPorts(level, controller)' in read('multiblock/MachineRegistry.java')
assert 'invalidateMemberCapabilities(level, hatch, front)' in read('multiblock/BlastFurnaceMultiblock.java')
assert 'ModBlocks.FIRECLAY_BRICKS.get()' in read('foundry/ModBlockEntities.java')
assert read('foundry/ModBlockEntities.java').count('ModBlocks.FIRECLAY_BRICKS.get()')==2
assert 'Capabilities.ItemHandler.BLOCK, BLAST_FURNACE' in read('foundry/ModBlockEntities.java')
assert 'Capabilities.FluidHandler.BLOCK, BLAST_FURNACE' in read('foundry/ModBlockEntities.java')
assert 'getSlots() { return 4; }' in read('foundry/FurnaceItemHandler.java')
assert 'if (simulate) return offered.copyWithCount(transfer);' in read('foundry/FurnaceItemHandler.java')
assert 'machine.acceptMolten(fluid, action.execute())' in read('foundry/FurnaceFluidHandler.java')
assert 'match != null && match != candidate' in read('foundry/FurnaceConnections.java')
assert 'smallFurnaceAnyFaceFunnelAndPipe' in read('gametest/IndustrialGameTests.java')
assert 'bigFurnaceEveryCasingFaceAndTransfer' in read('gametest/IndustrialGameTests.java')
assert 'oldPortWorldMigratesToSeamlessBrickCasing' in read('gametest/IndustrialGameTests.java')
for obsolete in ('PortConnections.java','PortItemHandler.java','PortFluidHandler.java'):
 assert not (J/'foundry'/obsolete).exists(), obsolete
assert 'return automationAvailable() ? AUTOMATION_SLOTS : NO_AUTOMATION_SLOTS;' in read('foundry/BlastFurnaceBlockEntity.java')
assert 'level.getBlockEntity(worldPosition) == this' in read('foundry/BlastFurnaceBlockEntity.java')
assert 'machine.automationAvailable()' in read('foundry/FurnaceItemHandler.java')
assert 'machine.automationAvailable()' in read('foundry/FurnaceFluidHandler.java')
print('PASS: No newly generated ports/printer; all-face shared handlers, migration, and GameTests exist')
