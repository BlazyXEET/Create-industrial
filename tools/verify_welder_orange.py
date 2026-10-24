#!/usr/bin/env python3
"""Static checks for the owner's orange/graphite Welder replacement assets.

This verifies the Minecraft JSON, real 16x16 texture sprites, and reversible
fallback, but cannot replace a Minecraft client render or gameplay test.
"""
from __future__ import annotations

import json
from pathlib import Path
from PIL import Image, ImageChops

ROOT=Path(__file__).resolve().parents[1]
ASSETS=ROOT/'src/main/resources/assets/createindustrial'
MODELS=ASSETS/'models/item'
MATS=ASSETS/'textures/item/welder'
model=json.loads((MODELS/'welder_3d.json').read_text())
parts=model['elements']
assert 30<=len(parts)<=50, len(parts)
assert len({e['name'] for e in parts})==len(parts), 'Duplicate element name'
assert any('Orange handle' in e['name'] for e in parts)
assert any('Nozzle bright broad tip' in e['name'] for e in parts)
assert any('Graphite head' in e['name'] for e in parts)
assert any('Rear angled graphite lever' in e['name'] for e in parts)
assert not any('teal' in name.lower() for name in model['textures']), 'Old teal palette accidentally active'
textures=model['textures']
assert len(textures)>=10
references=set()
for e in parts:
    a,b=e['from'],e['to']
    assert all(isinstance(q,(int,float)) for q in a+b)
    assert all(a[i]<b[i] for i in range(3)), e['name']
    assert all(-16<=q<=32 for q in a+b), e['name']
    if 'rotation' in e:
        rot=e['rotation']
        assert rot['axis']=='z' and rot['angle'] in (-45,-22.5,0,22.5,45)
    assert set(e['faces'])=={'north','south','east','west','up','down'}
    for face in e['faces'].values():
        key=face['texture'].removeprefix('#')
        assert key in textures,(e['name'],key)
        references.add(key)
        u,v,U,V=face['uv']
        assert 0<=u<U<=16 and 0<=v<V<=16,(e['name'],face)
for name in references:
    identifier=textures[name]
    assert identifier=='createindustrial:item/welder/'+name,identifier
    with Image.open(MATS/(name+'.png')) as img:
        assert img.size==(16,16) and img.mode=='RGBA',name
        colors=len(img.getcolors(256) or [])
        assert 4<=colors<=48,(name,colors)
# The default is the 3D orange item, but the 2D mode must retain the exact
# source pixels supplied by the user (not an approximated replacement).
selector=json.loads((MODELS/'welder.json').read_text())
assert selector['parent']=='createindustrial:item/welder_3d'
ref=Image.open(ROOT/'art/welder/reference-welder-icon-16x16.png').convert('RGBA')
sprite=Image.open(ASSETS/'textures/item/welder_flat.png').convert('RGBA')
assert ref.size==sprite.size==(16,16)
assert ImageChops.difference(ref,sprite).getbbox() is None,'2D icon differs from supplied reference'
for placement in ('gui','ground','fixed','firstperson_righthand','firstperson_lefthand','thirdperson_righthand','thirdperson_lefthand','head'):
    d=model['display'][placement]
    assert len(d['rotation'])==len(d['translation'])==len(d['scale'])==3
    assert all(0<n<=1 for n in d['scale'])
# Archive exists so the previous approved model can be recovered without
# overwriting this version's welder_3d.json.
archived=json.loads((MODELS/'welder_v23_teal.json').read_text())
assert len(archived['elements'])==62
assert (ROOT/'art/welder/welder-orange-reference.glb').is_file()
print(f'PASS: orange reference Welder {len(parts)} authored parts, {len(references)} pixel materials, exact supplied 2D icon, legacy model retained.')
print('Model/resource checks only. Minecraft loading and in-game hand placement unverified.')
