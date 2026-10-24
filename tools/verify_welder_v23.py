#!/usr/bin/env python3
"""Static contract tests for the shipped V23 JSON model and its pixel textures.

Does not claim to simulate Minecraft rendering or verify hand positioning in game.
"""
from __future__ import annotations

import json
from pathlib import Path
from PIL import Image

ROOT = Path(__file__).resolve().parents[1]
ASSETS = ROOT / 'src/main/resources/assets/createindustrial'
MODEL = ASSETS / 'models/item/welder_v23_teal.json'
MATS = ASSETS / 'textures/item/welder'
j = json.loads(MODEL.read_text())
parts = j.get('elements', [])
assert len(parts) == 62, f'Expected 62 authored parts, found {len(parts)}'
assert len({p['name'] for p in parts}) == len(parts), 'Duplicate part names'
tex = j['textures']
assert len(tex) >= 16
faces = ('north', 'south', 'east', 'west', 'up', 'down')
referenced = set()
for part in parts:
    a, b = part['from'], part['to']
    assert all(isinstance(v,(float,int)) for v in a+b)
    assert all(a[k] < b[k] for k in range(3)), part['name']
    assert all(-16 <= x <= 32 for x in a+b), part['name']
    if 'rotation' in part:
        r = part['rotation']
        assert r['axis'] == 'z' and r['angle'] in (-45,-22.5,0,22.5,45), part['name']
        assert len(r['origin']) == 3 and isinstance(r['rescale'],bool)
    assert set(part['faces']) == set(faces), part['name']
    for face in part['faces'].values():
        k = face['texture']
        assert k.startswith('#') and k[1:] in tex, (part['name'], k)
        referenced.add(k[1:])
        u0,v0,u1,v1 = face['uv']
        assert 0 <= u0 < u1 <= 16 and 0 <= v0 < v1 <= 16, part['name']
for key in referenced:
    assert tex[key] == 'createindustrial:item/welder/'+key, key
    path = MATS / (key + '.png')
    assert path.is_file(), f'Missing {path}'
    im=Image.open(path)
    assert im.size == (16,16) and im.mode == 'RGBA', path
    assert 4 <= len(im.getcolors(256) or []) <= 48, f'Unusable flat/noisy material: {path}'
for display in ('gui','ground','fixed','firstperson_righthand','firstperson_lefthand','thirdperson_righthand','thirdperson_lefthand','head'):
    assert display in j['display']
    d=j['display'][display]
    assert len(d['rotation'])==len(d['translation'])==len(d['scale'])==3
    assert all(0 < x <= 1 for x in d['scale'])
assert any('Red release trigger' in p['name'] for p in parts)
assert any('Angled torch barrel' in p['name'] and p.get('rotation') for p in parts)
assert len([p for p in parts if 'grip band' in p['name']]) == 4
assert len([p for p in parts if 'service screw' in p['name']]) == 4
print(f'PASS: V23 Welder: {len(parts)} geometry elements, {len(referenced)} referenced textures, 8 display positions, angled nozzle and grip details.')
print('Static asset verification only; client rendering and item transforms still require actual Minecraft testing.')
