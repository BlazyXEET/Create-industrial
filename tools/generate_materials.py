#!/usr/bin/env python3
"""Rebuild material resources deterministically; never touches approved machine artwork."""
from pathlib import Path
import json, random
from PIL import Image, ImageDraw

ROOT = Path(__file__).resolve().parents[1]
RES = ROOT / 'src/main/resources'
A = RES / 'assets/createindustrial'
D = RES / 'data/createindustrial'
CATALOG = json.loads((ROOT/'materials.json').read_text())['materials']
MANUFACTURED = json.loads((ROOT/'materials.json').read_text())['manufactured']

def put(path, value):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, indent=2)+'\n', encoding='utf-8')
def ident(name): return 'createindustrial:'+name
def item(name): return {'item': ident(name)}
def result(name, count=1, chance=None):
    r={'id':ident(name)}
    if count!=1: r['count']=count
    if chance is not None: r['chance']=chance
    return r
def recipe(name, value): put(D/'recipe'/f'{name}.json',value)
def process(name, kind, ingredients, results, ticks=200, heat=None):
    r={'type':'create:'+kind,'ingredients':ingredients,'results':results}
    if kind in ('crushing','milling','cutting'): r['processing_time']=ticks
    if heat: r['heat_requirement']=heat
    recipe(name,r)
def tag(ns,kind,name,values):
    p=RES/f'data/{ns}/tags/{kind}/{name}.json'
    old=json.loads(p.read_text()) if p.exists() else {'replace':False,'values':[]}
    old['values']=list(dict.fromkeys(old['values']+values)); put(p,old)
def cube(name):
    put(A/'blockstates'/f'{name}.json',{'variants':{'':{'model':ident('block/'+name)}}})
    put(A/'models/block'/f'{name}.json',{'parent':'minecraft:block/cube_all','textures':{'all':ident('block/'+name)}})
    put(A/'models/item'/f'{name}.json',{'parent':ident('block/'+name)})
def sprite(name): put(A/'models/item'/f'{name}.json',{'parent':'minecraft:item/generated','textures':{'layer0':ident('item/'+name)}})
def self_loot(name):
    put(D/'loot_table/blocks'/f'{name}.json',{'type':'minecraft:block','pools':[{'rolls':1,'conditions':[{'condition':'minecraft:survives_explosion'}], 'entries':[{'type':'minecraft:item','name':ident(name)}]}]})
def ore_loot(name,raw):
    put(D/'loot_table/blocks'/f'{name}.json',{'type':'minecraft:block','pools':[{'rolls':1,'entries':[{'type':'minecraft:alternatives','children':[
        {'type':'minecraft:item','name':ident(name),'conditions':[{'condition':'minecraft:match_tool','predicate':{'predicates':{'minecraft:enchantments':[{'enchantments':'minecraft:silk_touch','levels':{'min':1}}]}}}]},
        {'type':'minecraft:item','name':ident(raw),'functions':[{'function':'minecraft:apply_bonus','enchantment':'minecraft:fortune','formula':'minecraft:ore_drops'},{'function':'minecraft:explosion_decay'}]}
    ]}]}]})
def storage_recipe(block,unit,ns='createindustrial'):
    recipe(block,{'type':'minecraft:crafting_shaped','category':'misc','pattern':['###']*3,'key':{'#':{'item':ns+':'+unit}},'result':{'id':ident(block),'count':1}})
    recipe(unit+'_from_'+block,{'type':'minecraft:crafting_shapeless','category':'misc','ingredients':[item(block)],'result':{'id':ns+':'+unit,'count':9}})
    process('compacting/'+block,'compacting',[{'item':ns+':'+unit}]*9,[result(block)])
def feature(name,targets,size,lo,hi,count=None,rarity=None):
    put(D/'worldgen/configured_feature'/f'{name}.json',{'type':'minecraft:ore','config':{'size':size,'discard_chance_on_air_exposure':0.25,'targets':targets}})
    placement=[{'type':'minecraft:count','count':count}] if count else [{'type':'minecraft:rarity_filter','chance':rarity}]
    placement += [{'type':'minecraft:in_square'},{'type':'minecraft:height_range','height':{'type':'minecraft:uniform','min_inclusive':{'absolute':lo},'max_inclusive':{'absolute':hi}}},{'type':'minecraft:biome'}]
    put(D/'worldgen/placed_feature'/f'{name}.json',{'feature':ident(name),'placement':placement})
def target(tag_id,state): return {'target':{'predicate_type':'minecraft:tag_match','tag':tag_id},'state':{'Name':state}}

def shade(color, offset): return tuple(max(0,min(255,c+offset)) for c in color)
def texture(name,color,kind,deep=False):
    rng=random.Random(name)
    im=Image.new('RGB',(16,16)); px=im.load()
    base=(66,68,70) if deep else (121,121,117)
    for y in range(16):
        for x in range(16):
            b=base if kind=='ore' else color
            px[x,y]=shade(b,rng.choice([-8,-4,0,0,3,6]))
    dr=ImageDraw.Draw(im)
    if kind in ('ore','raw'):
        for x,y,w,h in [(2,2,4,3),(10,1,3,4),(6,6,4,4),(1,10,4,4),(11,10,4,4),(7,13,3,2)]:
            dr.rectangle([x,y,x+w-1,y+h-1], fill=shade(color,-26))
            dr.rectangle([x,y,x+w-2,y+h-2], fill=color)
            dr.line([x,y,x+w-2,y],fill=shade(color,40))
    if kind=='metal':
        dr.rectangle([0,0,15,15],outline=shade(color,-52))
        dr.line([1,1,14,1],fill=shade(color,49)); dr.line([1,1,1,14],fill=shade(color,27))
        dr.line([2,14,14,14],fill=shade(color,-29))
        for x,y in [(2,11),(3,10),(4,9),(5,8),(6,7),(7,6),(8,5),(9,4),(10,3),(11,2)]:
            px[x,y]=shade(color,17)
    p=A/'textures/block'/f'{name}.png'; p.parent.mkdir(parents=True,exist_ok=True); im.save(p)
def item_texture(name,color,kind):
    im=Image.new('RGBA',(16,16)); dr=ImageDraw.Draw(im)
    if kind=='ingot': points=[(2,6),(5,3),(12,3),(14,8),(11,12),(2,12),(1,9)]
    elif kind=='nugget': points=[(5,5),(9,4),(12,7),(10,11),(5,12),(3,8)]
    elif kind=='dust': points=[(2,12),(4,9),(6,9),(8,5),(10,8),(12,9),(14,13),(8,14)]
    else: points=[(2,5),(5,2),(10,3),(13,6),(12,11),(9,14),(4,13),(1,9)]
    dr.polygon(points,fill=shade(color,-40)+(255,))
    dr.polygon([(x,y-1) for x,y in points], fill=color+(255,))
    dr.line(points[:3],fill=shade(color,48)+(255,),width=1)
    if kind in ('raw','crushed'):
        dr.rectangle([5,6,8,8],fill=shade(color,26)+(255,)); dr.rectangle([9,9,11,10],fill=shade(color,-21)+(255,))
    p=A/'textures/item'/f'{name}.png';p.parent.mkdir(parents=True,exist_ok=True); im.save(p)

features=[]
lang=json.loads((A/'lang/en_us.json').read_text())
for m in CATALOG:
    mid=m['id']; ore=m['ore']; raw='raw_'+mid; rb=raw+'_block'; storage='block_of_'+mid
    blocks=[ore+'_ore','deepslate_'+ore+'_ore',rb]
    for b in blocks:
        cube(b); tag('minecraft','block','mineable/pickaxe',[ident(b)])
        tag('minecraft','block','needs_'+m['tool']+'_tool',[ident(b)])
        lang['block.createindustrial.'+b]=b.replace('_',' ').title().replace('Bauxite Ore','Bauxite Ore')
    for b in blocks[:2]:
        ore_loot(b,raw); texture(b,tuple(m['ore_color']),'ore',b.startswith('deepslate'))
        tag('c','block','ores',[ident(b)]);tag('c','item','ores',[ident(b)])
        tag('c','block','ores/'+mid,[ident(b)]);tag('c','item','ores/'+mid,[ident(b)])
    texture(rb,tuple(m['ore_color']),'raw');self_loot(rb);storage_recipe(rb,raw)
    storage_recipe(storage,mid+'_ingot');storage_recipe(mid+'_ingot',mid+'_nugget')
    if mid not in ('aluminium','uranium'):
        cube(storage);self_loot(storage)
        tag('minecraft','block','mineable/pickaxe',[ident(storage)])
        tag('minecraft','block','needs_iron_tool',[ident(storage)])
        lang['block.createindustrial.'+storage]='Block of '+mid.title()
    # The ingot/nugget recipe has an item result, and is safe for a press too.
    texture(storage,tuple(m['color']),'metal')
    for name,kind in [(raw,'raw'),('crushed_raw_'+mid,'crushed'),(mid+'_ingot','ingot'),(mid+'_nugget','nugget')]:
        sprite(name);item_texture(name,tuple(m['ore_color'] if kind in ('raw','crushed') else m['color']),kind)
        lang['item.createindustrial.'+name]=name.replace('_',' ').title()
    for category,value in [('raw_materials',raw),('ingots',mid+'_ingot'),('nuggets',mid+'_nugget')]:
        tag('c','item',category,[ident(value)]);tag('c','item',category+'/'+mid,[ident(value)])
    tag('create','item','crushed_raw_materials',[ident('crushed_raw_'+mid)])
    for category,b in [('storage_blocks',storage),('storage_blocks',rb),('storage_blocks/raw_'+mid,rb),('storage_blocks/'+mid,storage)]:
        for kind in ('block','item'): tag('c',kind,category,[ident(b)])
    for b in blocks[:2]:
        process('crushing/'+b,'crushing',[item(b)],[result('crushed_raw_'+mid),result('crushed_raw_'+mid,chance=0.25)],250)
    process('crushing/'+raw,'crushing',[item(raw)],[result('crushed_raw_'+mid)],400)
    # Exactly nine raw items per block, with no bonus roll; reversible storage cannot multiply ores.
    process('crushing/'+rb,'crushing',[item(rb)],[result('crushed_raw_'+mid,9)],3600)
    if mid=='aluminium':
        pass # The complete bauxite chain is generated by generate_refining.py below.
    else:
        process('splashing/crushed_raw_'+mid,'splashing',[item('crushed_raw_'+mid)],[result(mid+'_nugget',9)])
        for source in (raw,'crushed_raw_'+mid):
            for kind,ticks in [('smelting',300),('blasting',150)]:
                recipe(kind+'/'+source,{'type':'minecraft:'+kind,'category':'misc','ingredient':item(source),'result':result(mid+'_ingot'),'experience':0.5,'cookingtime':ticks})
    name=ore+'_veins';features.append(ident(name))
    feature(name,[target('minecraft:stone_ore_replaceables',ident(blocks[0])),target('minecraft:deepslate_ore_replaceables',ident(blocks[1]))],m['vein_size'],m['min_y'],m['max_y'],count=m['veins_per_chunk'])
    name=mid+'_dense_deposits';features.append(ident(name))
    feature(name,[target('minecraft:stone_ore_replaceables',ident(rb)),target('minecraft:deepslate_ore_replaceables',ident(rb))],m['dense_size'],m['min_y'],min(32,m['max_y']),rarity=m['dense_rarity'])

for m in MANUFACTURED:
    mid=m['id'];storage='block_of_'+mid
    cube(storage);self_loot(storage);texture(storage,tuple(m['color']),'metal')
    tag('minecraft','block','mineable/pickaxe',[ident(storage)])
    tag('minecraft','block','needs_iron_tool',[ident(storage)])
    storage_recipe(storage,mid+'_ingot');storage_recipe(mid+'_ingot',mid+'_nugget')
    lang['block.createindustrial.'+storage]='Block of '+mid.title()
    for suffix in ('ingot','nugget'):
        name=mid+'_'+suffix;sprite(name);item_texture(name,tuple(m['color']),suffix)
        lang['item.createindustrial.'+name]=name.replace('_',' ').title()
        category=suffix+'s'
        tag('c','item',category,[ident(name)]);tag('c','item',category+'/'+mid,[ident(name)])
    for kind in ('block','item'):
        tag('c',kind,'storage_blocks',[ident(storage)]);tag('c',kind,'storage_blocks/'+mid,[ident(storage)])

# Complete Create's existing zinc family and add rare compact deposits for existing metals.
cube('raw_zinc_block');self_loot('raw_zinc_block');texture('raw_zinc_block',(154,173,164),'raw');storage_recipe('raw_zinc_block','raw_zinc','create')
process('crushing/raw_zinc_block','crushing',[item('raw_zinc_block')],[{'id':'create:crushed_raw_zinc','count':9}],3600)
lang['block.createindustrial.raw_zinc_block']='Block of Raw Zinc'
tag('minecraft','block','mineable/pickaxe',[ident('raw_zinc_block')]);tag('minecraft','block','needs_stone_tool',[ident('raw_zinc_block')])
for kind in ('block','item'):
    tag('c',kind,'storage_blocks',[ident('raw_zinc_block')]);tag('c',kind,'storage_blocks/raw_zinc',[ident('raw_zinc_block')])
for mid,lo,hi,rarity,size in [('iron',-48,32,64,4),('copper',-16,64,48,5),('gold',-64,0,96,3),('zinc',-32,64,64,4)]:
    name=mid+'_dense_deposits';features.append(ident(name));out=ident('raw_zinc_block') if mid=='zinc' else 'minecraft:raw_'+mid+'_block'
    feature(name,[target('minecraft:stone_ore_replaceables',out),target('minecraft:deepslate_ore_replaceables',out)],size,lo,hi,rarity=rarity)
put(D/'neoforge/biome_modifier/industrial_ores.json',{'type':'neoforge:add_features','biomes':'#minecraft:is_overworld','features':features,'step':'underground_ores'})

sprite('alumina_dust');item_texture('alumina_dust',(218,218,205),'dust');lang['item.createindustrial.alumina_dust']='Alumina Dust'
# Slow renewability with real consumed inputs; simplified gameplay metallurgy.
water={'type':'neoforge:single','fluid':'minecraft:water','amount':250}
process('mixing/alumina_from_clay','mixing',[{'item':'minecraft:clay_ball'}]*4+[water],[result('alumina_powder')],heat='heated')
# Granite is renewable through Create compacting flint/red sand/lava. Crushing is slower than milling.
process('crushing/granite_trace_uranium','crushing',[{'item':'minecraft:granite'}],[{'id':'minecraft:red_sand'}]+[
    result('crushed_raw_'+mid,chance=chance) for mid,chance in [('uranium',.01),('silver',.02),('tin',.06),('lead',.03),('nickel',.04)]],500)
process('mixing/coke','mixing',[{'item':'minecraft:coal'}]*2,[result('coke')],heat='heated')
process('compacting/slag','compacting',[{'type':'neoforge:single','fluid':'createindustrial:molten_slag','amount':144}],[result('slag')])
process('mixing/slag_concrete','mixing',[item('slag')]*2+[{'item':'minecraft:gravel'},{'item':'minecraft:iron_nugget'},water],[result('reinforced_concrete',4)])
for mid,namespace in [(m,'minecraft') for m in ('iron','copper','gold')]+[('zinc','create')]+[(m['id'],'createindustrial') for m in CATALOG+MANUFACTURED]:
    process('compacting/cast_'+mid,'compacting',[{'type':'neoforge:single','fluid':'createindustrial:molten_'+mid,'amount':144}],
            [{'id':namespace+':'+mid+'_ingot'}])
for name,color in [('coke',(55,57,62)),('slag',(101,79,58))]:
    sprite(name);item_texture(name,color,'raw');lang['item.createindustrial.'+name]=name.title()
tag('createindustrial','item','blast_furnace_fluxes',['minecraft:calcite','create:limestone'])
# Intentionally abstract late-game transmutation, not a simulation of nuclear chemistry.
process('mixing/plutonium','mixing',[item('uranium_ingot')]*8+[{'item':'minecraft:nether_star'}],[result('plutonium_ingot')],heat='superheated')
# Complete automation for existing decorative materials; no new machines or custom energy system.
process('mixing/reinforced_concrete','mixing',[{'item':'minecraft:gravel'}]*2+[{'item':'minecraft:sand'}]*2+[{'item':'minecraft:iron_nugget'},water],[result('reinforced_concrete',4)])
process('mixing/plastered_reinforced_concrete','mixing',[item('reinforced_concrete'),{'item':'minecraft:clay_ball'},water],[result('plastered_reinforced_concrete')])
recipe('condensing_mesh',{'type':'minecraft:crafting_shaped','category':'building','pattern':['I I',' W ','I I'],'key':{'I':{'item':'minecraft:iron_nugget'},'W':{'item':'minecraft:iron_bars'}},'result':result('condensing_mesh',2)})
put(A/'lang/en_us.json',lang)
surfaces={'variants':{f'level={level},metal={mid}':{'model':ident(f'block/molten_surface_{mid}_{level}')}
                      for mid in ('iron','copper','gold') for level in range(1,5)}}
for mid,color in [('aluminium',(255,206,121)),('uranium',(235,174,87)),('zinc',(229,213,173)),
                  ('silver',(255,220,155)),('tin',(219,183,122)),('lead',(206,150,109)),
                  ('nickel',(246,195,139)),('steel',(245,181,120)),('plutonium',(230,181,141)),('pig_iron',(234,155,75))]:
    texture('molten_'+mid,color,'raw')
    for level in range(1,5):
        model=json.loads((A/f'models/block/molten_surface_iron_{level}.json').read_text())
        model['textures']={k:ident('block/molten_'+mid) for k in model['textures']}
        put(A/f'models/block/molten_surface_{mid}_{level}.json',model)
        surfaces['variants'][f'level={level},metal={mid}']={'model':ident(f'block/molten_surface_{mid}_{level}')}
put(A/'blockstates/molten_surface.json',surfaces)
texture('slag_crust',(120,81,48),'raw')
slag_variants={}
for key,value in surfaces['variants'].items():
    if ',slag=' in key: continue
    model_path=value['model'].split(':',1)[1]
    base=json.loads((A/'models'/f'{model_path}.json').read_text())
    h=base['elements'][0]['to'][1]
    covered=json.loads(json.dumps(base));covered['textures']['slag']=ident('block/slag_crust')
    for x,z,w,d in [(1,1,5,4),(8,8,6,5),(2,10,4,4)]:
        covered['elements'].append({'from':[x,h,z],'to':[x+w,h+.5,z+d],
            'faces':{f:{'texture':'#slag'} for f in ('up','north','south','east','west')}})
    put(A/'models'/f'{model_path}_slag.json',covered)
    slag_variants[key+',slag=false']=value
    slag_variants[key+',slag=true']={'model':value['model']+'_slag'}
put(A/'blockstates/molten_surface.json',{'variants':slag_variants})
# Material inventory items stay flat; block geometry is independent.
print(f'Generated {len(CATALOG)} ore families, zinc storage, {len(features)} worldgen features and Create processing routes.')
from generate_refining import generate
generate()
