#!/usr/bin/env python3
"""Validate optional 2D Welder appearance and safe reversible model selection.

Static resource checks only: does not assert that Minecraft client rendering passed.
"""
from __future__ import annotations

import json
import shutil
import sys
from pathlib import Path
from tempfile import TemporaryDirectory

from PIL import Image

ROOT = Path(__file__).resolve().parents[1]
MODELS = ROOT / 'src/main/resources/assets/createindustrial/models/item'
ICON = ROOT / 'src/main/resources/assets/createindustrial/textures/item/welder_flat.png'
sys.path.insert(0, str(ROOT / 'tools'))
from switch_welder_model import selected_mode, set_model  # noqa: E402

selector = MODELS / 'welder.json'
assert selected_mode(selector) in ('2d', '3d')
assert json.loads(selector.read_text()).get('elements') is None
three = json.loads((MODELS / 'welder_3d.json').read_text())
two = json.loads((MODELS / 'welder_2d.json').read_text())
assert 30 <= len(three.get('elements', [])) <= 50, 'Reference 3D model must contain authored geometry'
assert two == {
    'parent': 'minecraft:item/generated',
    'textures': {'layer0': 'createindustrial:item/welder_flat'},
}, '2D mode must be a standard Minecraft generated item'
with Image.open(ICON) as img:
    assert img.mode == 'RGBA' and img.size == (16, 16), '2D sprite must be 16x16 RGBA'
    alpha = img.getchannel('A')
    assert alpha.getextrema() == (0, 255), 'Flat icon needs transparent pixels and visible content'
    assert 7 <= len(img.getcolors(256) or []) <= 48, 'Invalid flat pixel-art palette'

# Exercise both reversible modes in a disposable copy. Do not change the
# user's chosen mode in the actual project while running verification.
with TemporaryDirectory() as temp:
    working = Path(temp)
    for name in ('welder.json', 'welder_2d.json', 'welder_3d.json'):
        shutil.copy2(MODELS / name, working / name)
    local = working / 'welder.json'
    set_model('2d', local)
    assert selected_mode(local) == '2d'
    assert not json.loads(local.read_text()).get('elements')
    set_model('3d', local)
    assert selected_mode(local) == '3d'
    assert json.loads(local.read_text())['parent'] == 'createindustrial:item/welder_3d'
    set_model('2d', local)
    assert selected_mode(local) == '2d', 'Mode switching should be repeatable'

print(f'PASS: Welder appearance switch ({selected_mode(selector).upper()} active); orange 3D source, reversible 2D sprite, both modes validated.')
print('Appearance-only checks; weld actions, assembly logic, and gameplay are unchanged.')
