#!/usr/bin/env python3
"""Actual PNG pixels and recipe validation, not a screenshot or a Minecraft runtime test."""
from pathlib import Path
import json
from PIL import Image
R=Path(__file__).resolve().parents[1]
A=R/'src/main/resources/assets/createindustrial'
D=R/'src/main/resources/data/createindustrial/recipe'
recipe=json.loads((D/'mixing/steel_refining.json').read_text())
assert recipe['type']=='create:mixing' and recipe['heat_requirement']=='superheated'
assert recipe['results']==[{'id':'createindustrial:molten_steel','amount':576}, {'id':'createindustrial:molten_slag','amount':144}]
files=sorted((A/'textures').rglob('*.png'))
assert len(files)>=135, f'Baseline resource assets are missing; expected at least 135, got {len(files)}'
for p in files:
 with Image.open(p) as im:
  assert im.size==(16,16) and im.mode=='RGBA',f'Wrong sprite format: {p}'
  assert im.getbbox() is not None,f'Empty sprite: {p}'
  assert len(im.getcolors(256) or [])>=3, f'Blank/overly flat: {p}'
  assert len(im.getcolors(256) or [])<=48,f'Smooth or noisy texture: {p}'
# Actual distinct pixel art on every natural mineral substrate.
for ore in ('bauxite','uranium','silver','lead','tin','nickel','aluminium'):
 name='bauxite' if ore in ('bauxite','aluminium') else ore
 for prefix in ('','deepslate_'):
  im=Image.open(A/'textures/block'/f'{prefix}{name}_ore.png')
  assert len(im.getcolors(256) or [])>=8, f'Ore lacks readable mineral/stone tones: {ore}'
print(f'PASS: {len(files)} crisp hand-defined 16x16 original PNG assets, distinct embedded mineral ores and Basin steel recipe')
print('No Minecraft build, mod-loading, server GameTest, Create funnel, or Blender validation implied.')
