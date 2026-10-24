#!/usr/bin/env python3
"""Guard against the fixture error that failed V10's Minecraft GameTests."""
from pathlib import Path
p = Path(__file__).resolve().parents[1] / 'src/main/java/net/createindustrialteam/createindustrial/gametest/IndustrialGameTests.java'
s = p.read_text(encoding='utf-8')
a = s.index('public static void sixWayMaterialPlacement(')
b = s.index('\n    @GameTest(', a + 1)
test = s[a:b]
for required in ('p.setXRot(pitch)', 'p.setYRot(yaw)', 'p.setYHeadRot(yaw)',
                 'Direction observedLook = context.getNearestLookingDirection()',
                 'observedFacing == look.getOpposite()'):
    assert required in test, f'Missing six-way rotation GameTest guard: {required}'
assert 'getNearestLookingDirection().getOpposite()' in (p.parents[1] / 'blocks/RotatableMaterialBlock.java').read_text(encoding='utf-8')
print('PASS: GameTest sets FakePlayer body and head rotation and checks actual facing')
