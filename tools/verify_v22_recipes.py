#!/usr/bin/env python3
"""Static V22 recipe/progression contract; Minecraft still parses recipes in GameTests."""
from collections import Counter
from pathlib import Path
import json

root=Path(__file__).resolve().parents[1]
recipes=root/'src/main/resources/data/createindustrial/recipe'

def read(path):
    return json.loads((recipes/path).read_text(encoding='utf-8'))

def check(value,message):
    if not value: raise AssertionError(message)

for removed in ('laser_printer.json','steel_converter.json',
                'laser_printing/silicon_wafer.json','cutting/silicon_chips.json'):
    check(not (recipes/removed).exists(),f'retired machine recipe restored: {removed}')
for path in recipes.rglob('*.json'):
    obj=read(path.relative_to(recipes))
    text=json.dumps(obj).lower()
    check('createindustrial:steel_converter' not in text,f'steel converter recipe returned: {path.name}')
    check('createindustrial:laser_printer' not in text,f'laser printer recipe returned: {path.name}')
    check('createindustrial:industrial_port' not in text,f'port crafting returned: {path.name}')

steel=read('mixing/steel_refining.json')
check(steel['type']=='create:mixing' and steel['heat_requirement']=='superheated',
      'steel must require Create superheated Basin mixing')
inputs=Counter((entry.get('fluid',entry.get('item')),entry.get('amount',1))
               for entry in steel['ingredients'])
check(inputs==Counter({('createindustrial:molten_pig_iron',576):1,
                       ('minecraft:calcite',1):1,('minecraft:iron_nugget',1):2}),
      'steel recipe ingredients changed: preserve pig iron, flux and recycled iron')
outputs={entry['id']:entry.get('amount',1) for entry in steel['results']}
check(outputs=={'createindustrial:molten_steel':576,'createindustrial:molten_slag':144},
      'steel input/output balance changed without review')
for metal in ('steel','pig_iron'):
    casting=read(f'compacting/cast_{metal}.json')
    check(casting['type']=='create:compacting',f'{metal} requires Create compacting')
    check(casting['ingredients']==[{'type':'neoforge:single',
          'fluid':f'createindustrial:molten_{metal}', 'amount':144}],
          f'{metal} casting must consume 144mB per ingot')
    check(casting['results']==[{'id':f'createindustrial:{metal}_ingot'}],
          f'{metal} casting must yield one ingot')
flux=json.loads((root/'src/main/resources/data/createindustrial/tags/item/blast_furnace_fluxes.json').read_text())
check('minecraft:calcite' in flux.get('values',[]), 'calcite flux is not reachable')
for ore in ('bauxite','uranium','silver','tin','lead','nickel'):
    check((recipes/'crushing'/f'{ore}_ore.json').is_file(),f'missing {ore} crushing recipe')
print('PASS: V22 superheated Basin steel conservation, casts, flux, six ore families, retired machines')
