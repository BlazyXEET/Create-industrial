#!/usr/bin/env python3
"""V17 processing recipes and original 16-pixel artwork. Safe to regenerate."""
from pathlib import Path
import json, random
from PIL import Image, ImageDraw

ROOT=Path(__file__).resolve().parents[1]
RES=ROOT/'src/main/resources';A=RES/'assets/createindustrial';D=RES/'data/createindustrial'
NS='createindustrial:'
def put(p,v):
    p.parent.mkdir(parents=True,exist_ok=True);p.write_text(json.dumps(v,indent=2)+'\n')
def ingredient(s):return {'item':s if ':' in s else NS+s}
def output(s,n=1,chance=None):
    r={'id':s if ':' in s else NS+s}
    if n!=1:r['count']=n
    if chance is not None:r['chance']=chance
    return r
def recipe(name,v):put(D/'recipe'/f'{name}.json',v)
def process(name,kind,inputs,outputs,heat=None,time=None):
    r={'type':('createindustrial:' if kind=='laser_printing' else 'create:')+kind,
       'ingredients':[ingredient(x) if isinstance(x,str) else x for x in inputs],'results':outputs}
    if heat:r['heat_requirement']=heat
    if time:r['processing_time']=time
    recipe(name,r)
def craft(name,pattern,key,result,n=1):
    recipe(name,{'type':'minecraft:crafting_shaped','category':'misc','pattern':pattern,
                 'key':{k:ingredient(v) for k,v in key.items()},'result':output(result,n)})
def shapeless(name,inputs,result,n=1):
    recipe(name,{'type':'minecraft:crafting_shapeless','category':'misc',
                 'ingredients':[ingredient(i) for i in inputs],'result':output(result,n)})
def tag(kind,name,values):
    p=RES/'data/minecraft/tags'/kind/(name+'.json')
    old=json.loads(p.read_text()) if p.exists() else {'replace':False,'values':[]}
    old['values']=list(dict.fromkeys(old['values']+values));put(p,old)
def sprite(name):put(A/'models/item'/f'{name}.json',{'parent':'minecraft:item/generated','textures':{'layer0':NS+'item/'+name}})
def save(im,name,kind='item'):
    p=A/'textures'/kind/(name+'.png');p.parent.mkdir(parents=True,exist_ok=True);im.save(p)
def shade(c,n):return tuple(max(0,min(255,v+n)) for v in c)

def recipes():
    # Remove superseded shortcuts, including resources left by an older generator run.
    for name in ['mixing/steel','mixing/steel_from_pig_iron','mixing/aluminium_reduction']+[
            k+'/'+s for k in ('smelting','blasting') for s in ('raw_aluminium','crushed_raw_aluminium')]:
        (D/'recipe'/f'{name}.json').unlink(missing_ok=True)
    water={'type':'neoforge:single','fluid':'minecraft:water','amount':250}
    process('mixing/impure_silicon','mixing',['minecraft:sand'],[output('impure_silicon_powder',chance=.1)],'heated')
    process('splashing/impure_silicon','splashing',['impure_silicon_powder'],[
        output('pure_silicon_powder'),output('minecraft:iron_nugget',chance=.5),
        output('minecraft:iron_nugget',chance=.5),output('aluminium_nugget',chance=.2)])
    process('compacting/silicon_crystal','compacting',['pure_silicon_powder',water],[output('silicon_crystal')],'heated')
    process('cutting/silicon_wafers','cutting',['silicon_crystal'],[output('silicon_wafer',8)],time=200)
    # Silicon printing recipes are intentionally unavailable in V20.
    powders=[output('bauxite_powder',2),output('bauxite_powder',chance=.5),output('bauxite_powder',chance=.5)]
    for source in ('raw_aluminium','bauxite_ore','deepslate_bauxite_ore'):
        process('crushing/'+source,'crushing',[source],powders,time=300)
    # Raw storage must remain equivalent to its nine ingredients; unpack before refining.
    process('crushing/raw_aluminium_block','crushing',['raw_aluminium_block'],[output('raw_aluminium',9)],time=200)
    for source in ('bauxite_powder','crushed_raw_aluminium'):
        process('splashing/'+source,'splashing',[source],[output('alumina_powder'),output('alumina_powder',chance=.5),
            output('minecraft:iron_nugget',chance=.4),output('impure_silicon_powder',chance=.05)])
    shapeless('legacy_alumina_powder',['alumina_dust'],'alumina_powder')
    process('compacting/aluminium','compacting',['alumina_powder'],[output('aluminium_ingot')],'heated')
    process('pressing/aluminium_sheet','pressing',['aluminium_ingot'],[output('aluminium_sheet')])
    craft('turbine_blade',[' A ',' A ',' I '],{'A':'aluminium_sheet','I':'minecraft:iron_nugget'},'turbine_blade')
    # Use Create's functional windmill sail; the blade is a second consumable route to the same working sail.
    craft('aluminium_windmill_sail',['AA','AA'],{'A':'aluminium_sheet'},'create:white_sail')
    craft('blade_windmill_sail',[' B ','BIB',' B '],{'B':'turbine_blade','I':'minecraft:iron_nugget'},'create:white_sail',4)
    shapeless('fireclay_balls',['fireclay'],'fireclay_ball',4)
    craft('fireclay',['CC','CC'],{'C':'fireclay_ball'},'fireclay')
    for kind,ticks in [('smelting',200),('blasting',100)]:
        recipe(kind+'/fireclay_brick',{'type':'minecraft:'+kind,'category':'misc','ingredient':ingredient('fireclay_ball'),
             'result':output('fireclay_brick'),'experience':.1,'cookingtime':ticks})
    craft('fireclay_bricks',['BB','BB'],{'B':'fireclay_brick'},'fireclay_bricks')
    # Slow renewable refractory supply for existing worlds and fully automated factories.
    process('mixing/fireclay','mixing',['minecraft:clay_ball']*4+['minecraft:gravel',water],[output('fireclay_ball',4)])
    # V20: Laser Printer and Steel Converter are retired from new gameplay.
    # Their registry IDs remain in Java only for backwards-compatible world loading.
    (D/'recipe/laser_printer.json').unlink(missing_ok=True)
    (D/'recipe/steel_converter.json').unlink(missing_ok=True)
    (D/'recipe/laser_printing/silicon_wafer.json').unlink(missing_ok=True)
    (D/'recipe/cutting/silicon_chips.json').unlink(missing_ok=True)

def materials_art():
    catalog=json.loads((ROOT/'materials.json').read_text())
    # Identifiable silhouettes: pisolitic bauxite, fine uranium veins, silver filaments,
    # angular cassiterite tin, cubic galena lead, and mottled nickel clusters.
    masks={
        'aluminium':[(2,2,3,2),(10,1,3,3),(6,7,3,3),(1,11,3,3),(12,10,3,3),(8,13,2,2)],
        'uranium':[(1,2,2,1),(3,3,1,3),(4,6,2,2),(9,1,1,4),(10,4,2,2),(10,9,2,3),(8,12,2,2),(2,12,2,2)],
        'silver':[(1,4,4,1),(4,3,3,1),(6,2,2,1),(9,8,4,1),(12,7,2,1),(3,12,5,1),(2,13,2,1),(10,13,3,1)],
        'tin':[(2,1,2,3),(4,3,2,2),(10,3,3,2),(8,8,2,3),(2,10,2,3),(12,11,2,3),(7,14,2,1)],
        'lead':[(1,2,4,3),(10,1,3,4),(5,7,4,4),(1,12,3,3),(11,11,4,4)],
        'nickel':[(3,2,2,2),(5,3,3,2),(2,4,2,2),(11,2,2,3),(10,5,2,1),(6,9,2,3),(8,11,2,2),(1,12,3,2),(12,11,2,3)]}
    for m in catalog['materials']:
        mid=m['id'];color=tuple(m['ore_color'])
        for deep in (False,True):
            name=('deepslate_' if deep else '')+m['ore']+'_ore';rng=random.Random(name)
            im=Image.new('RGB',(16,16));px=im.load()
            # Coherent rock pixels, with layered deepslate instead of photographic noise.
            for y in range(16):
                for x in range(16):
                    base=(64,65,66) if deep else (121,120,118)
                    grain=rng.choice([-10,-5,0,0,4,8])
                    if deep and y in (0,5,10):grain-=12
                    px[x,y]=shade(base,grain)
            for x,y,w,h in masks[mid]:
                for dx in range(w):
                    for dy in range(h):
                        # Remove a corner from larger clusters; little crystals stay sharp.
                        if w>=3 and h>=3 and (dx,dy) in ((w-1,0),(0,h-1)):continue
                        n=38 if dy==0 else -36 if dy==h-1 else rng.choice([-12,0,8])
                        px[x+dx,y+dy]=shade(color,n)
                if mid in ('silver','tin','lead'):px[x,y]=shade(color,65)
            save(im,name,'block')
        # Interlocking raw chunks, with shadowed gaps rather than ore pasted on solid color.
        rng=random.Random(mid);im=Image.new('RGB',(16,16),shade(color,-58));dr=ImageDraw.Draw(im)
        for x,y,w,h in [(0,0,7,6),(8,-1,8,7),(-2,7,7,9),(6,7,5,5),(12,7,6,8),(5,13,7,5)]:
            dr.polygon([(x+1,y),(x+w-2,y),(x+w,y+2),(x+w-1,y+h-1),(x+1,y+h),(x,y+2)],fill=shade(color,rng.choice([-12,0,7])))
            dr.line([(x+1,y+1),(x+w-2,y+1),(x+w-1,y+2)],fill=shade(color,42))
            dr.line([(x+w-1,y+3),(x+w-2,y+h-1)],fill=shade(color,-31))
        save(im,'raw_'+mid+'_block','block')

def items_art():
    colors={'impure_silicon_powder':(122,108,92),'pure_silicon_powder':(179,185,205),
            'bauxite_powder':(184,101,59),'alumina_powder':(226,222,200)}
    for name,color in colors.items():
        im=Image.new('RGBA',(16,16));dr=ImageDraw.Draw(im)
        dr.polygon([(1,12),(4,10),(5,7),(7,8),(9,4),(11,8),(12,10),(14,12),(12,14),(4,14)],fill=shade(color,-40)+(255,))
        dr.polygon([(2,11),(5,10),(6,7),(8,8),(9,5),(11,9),(13,11),(10,12),(5,12)],fill=color+(255,))
        for x,y in [(6,9),(9,7),(10,10),(4,11),(8,11)]:dr.point((x,y),fill=shade(color,42)+(255,))
        save(im,name);sprite(name)
    for printed in (False,True):
        name=('printed_' if printed else '')+'silicon_wafer';im=Image.new('RGBA',(16,16));dr=ImageDraw.Draw(im)
        dr.polygon([(5,1),(11,1),(14,4),(14,11),(11,14),(5,14),(1,10),(1,5)],fill=(50,54,74,255))
        dr.polygon([(5,2),(10,2),(13,5),(13,10),(10,13),(5,13),(2,10),(2,5)],fill=(102,117,157,255))
        dr.line([(3,6),(7,2),(10,2)],fill=(170,185,218,255))
        dr.line([(4,11),(12,3)],fill=(135,160,190,255));dr.line([(6,13),(13,6)],fill=(125,125,174,255))
        if printed:
            for y in (4,7,10):
                for x in (4,7,10):
                    dr.rectangle((x,y,x+1,y+1),fill=(43,58,70,255));dr.point((x,y),fill=(220,174,76,255))
            dr.line((3,6,12,6),fill=(194,148,63,255));dr.line((6,3,6,12),fill=(194,148,63,255))
        save(im,name);sprite(name)
    im=Image.new('RGBA',(16,16));dr=ImageDraw.Draw(im)
    for y in (4,7,10):dr.line((2,y,13,y),fill=(221,180,84,255))
    for x in (4,7,10):dr.line((x,2,x,13),fill=(221,180,84,255))
    dr.rectangle((4,4,11,11),fill=(37,43,45,255));dr.rectangle((6,6,9,9),fill=(78,97,102,255))
    dr.line((5,5,10,5),fill=(138,155,153,255));save(im,'silicon_chip');sprite('silicon_chip')
    im=Image.new('RGBA',(16,16));dr=ImageDraw.Draw(im)
    dr.polygon([(7,1),(10,3),(12,11),(9,14),(4,12),(3,7)],fill=(61,64,91,255))
    dr.polygon([(7,2),(9,4),(9,12),(5,10),(4,7)],fill=(145,151,184,255));dr.line((7,3,5,7,6,10),fill=(207,211,227,255),width=1)
    save(im,'silicon_crystal');sprite('silicon_crystal')
    for name in ('aluminium_sheet','turbine_blade','fireclay_ball','fireclay_brick'):
        im=Image.new('RGBA',(16,16));dr=ImageDraw.Draw(im)
        if name=='aluminium_sheet':
            dr.polygon([(1,6),(9,2),(14,7),(6,13),(1,10)],fill=(96,114,127,255));dr.polygon([(2,6),(9,3),(13,7),(6,11)],fill=(186,206,216,255));dr.line((2,6,9,3,12,6),fill=(235,245,244,255))
        elif name=='turbine_blade':
            dr.polygon([(6,13),(7,4),(10,1),(13,2),(11,9),(8,14)],fill=(89,110,121,255));dr.polygon([(7,11),(8,4),(11,2),(12,3),(10,9)],fill=(188,209,218,255));dr.line((8,5,11,2),fill=(238,245,244,255));dr.rectangle((5,12,8,14),fill=(134,121,91,255))
        elif name=='fireclay_ball':
            dr.polygon([(3,5),(7,3),(12,4),(14,8),(12,12),(5,13),(2,10)],fill=(115,95,83,255));dr.polygon([(4,5),(8,4),(11,5),(12,9),(9,11),(5,10)],fill=(168,149,126,255));dr.line((5,5,8,5),fill=(208,192,162,255))
        else:
            dr.polygon([(1,6),(10,3),(14,5),(14,10),(5,13),(1,10)],fill=(142,112,77,255));dr.polygon([(2,6),(10,4),(13,5),(5,8)],fill=(220,195,145,255));dr.polygon([(2,7),(5,9),(13,6),(13,9),(5,12),(2,10)],fill=(192,162,111,255));dr.line((3,7,5,8,12,6),fill=(241,219,172,255))
        save(im,name);sprite(name)

def machine_art():
    # Small palettes and hard edges match Create's brass/andesite machinery.
    for name,base in [('machine_casing',(89,99,91)),('machine_brass',(163,125,59)),
                      ('converter_front',(86,78,69)),('fireclay',(142,124,104))]:
        rng=random.Random(name);im=Image.new('RGB',(16,16));px=im.load()
        for y in range(16):
            for x in range(16):px[x,y]=shade(base,rng.choice([-7,-3,0,3,6]))
        dr=ImageDraw.Draw(im)
        if name=='fireclay':
            for y in (3,8,13):
                dr.line((0,y,15,y),fill=shade(base,-19));dr.line((2,y+1,10,y+1),fill=shade(base,17))
        else:
            dr.rectangle((0,0,15,15),outline=shade(base,-38));dr.rectangle((1,1,14,14),outline=shade(base,25))
            for x,y in [(2,2),(13,2),(2,13),(13,13)]:
                dr.point((x,y),fill=(204,190,142));dr.point((x,y+1),fill=(50,58,55))
            if name.endswith('front'):
                dr.rectangle((3,4,12,11),fill=(23,33,34));dr.line((4,5,11,5),fill=(111,145,151));
                if name=='laser_front':dr.line((6,6,10,10),fill=(105,144,179))
                else:
                    for x in range(4,12,2):dr.line((x,7,x,10),fill=(146,92,48))
        save(im,name,'block')
    # Brickwork uses the same ceramic colors as the new individual firebrick item.
    im=Image.new('RGB',(16,16),(104,89,67));dr=ImageDraw.Draw(im)
    for row in range(4):
        y=row*4
        for x in range(-4 if row%2 else 0,16,8):
            dr.rectangle((x,y,x+6,y+2),fill=(184+row*3,158+row*2,112+row*2));dr.line((x,y,x+6,y),fill=(220,197,151))
    save(im,'fireclay_bricks','block')
    faces=('up','down','north','south','east','west')
    def box(lo,hi,texture):return {'from':lo,'to':hi,'faces':{f:{'texture':'#'+texture} for f in faces}}
    for name in ('steel_converter',):
        converter=name=='steel_converter';front='converter_front' if converter else 'laser_front'
        elements=[box([0,0,0],[16,3,16],'casing'),box([1,3,1],[15,13,15],'body'),
                  box([0,13,0],[16,16,16],'brass')]
        if converter:
            elements += [box([2,3,0],[14,13,2],'front'),box([6,14,4],[10,16,10],'brass')]
        else:
            elements += [box([2,3,0],[14,11,2],'front'),box([6,11,5],[10,14,11],'brass')]
        for active in (False,True):
            model={'parent':'minecraft:block/block','textures':{'casing':NS+'block/machine_casing','body':NS+'block/'+('fireclay_bricks' if converter else 'machine_casing'),
                              'brass':NS+'block/machine_brass','shaft':'create:block/axis','front':NS+'block/'+front+('_active' if active else ''),
                              'particle':NS+'block/machine_casing'},'elements':elements}
            put(A/'models/block'/f'{name}{"_active" if active else ""}.json',model)
        hot=Image.open(A/'textures/block'/f'{front}.png').convert('RGB');dr=ImageDraw.Draw(hot)
        if converter:
            for x in range(4,12,2):dr.line((x,7,x,10),fill=(255,181,65))
        else:dr.line((6,6,10,10),fill=(117,238,249));dr.point((10,10),fill=(241,255,255))
        save(hot,front+'_active','block')
        put(A/'blockstates'/f'{name}.json',{'variants':{f'active={str(active).lower()},facing={f}':
            {'model':NS+'block/'+name+('_active' if active else ''),'y':angle}
            for active in (False,True) for f,angle in [('north',0),('east',90),('south',180),('west',270)]}})
        put(A/'models/item'/f'{name}.json',{'parent':NS+'block/'+name})
        tag('block','mineable/pickaxe',[NS+name]);tag('block','needs_iron_tool',[NS+name])
        put(D/'loot_table/blocks'/f'{name}.json',{'type':'minecraft:block','pools':[{'rolls':1,'conditions':[{'condition':'minecraft:survives_explosion'}],
             'entries':[{'type':'minecraft:item','name':NS+name}]}]})

def fireclay_data():
    put(A/'blockstates/fireclay.json',{'variants':{'':{'model':NS+'block/fireclay'}}})
    put(A/'models/block/fireclay.json',{'parent':'minecraft:block/cube_all','textures':{'all':NS+'block/fireclay'}})
    put(A/'models/item/fireclay.json',{'parent':NS+'block/fireclay'})
    tag('block','mineable/shovel',[NS+'fireclay'])
    put(D/'loot_table/blocks/fireclay.json',{'type':'minecraft:block','pools':[{'rolls':1,'entries':[{'type':'minecraft:alternatives','children':[
        {'type':'minecraft:item','name':NS+'fireclay','conditions':[{'condition':'minecraft:match_tool','predicate':{'predicates':{'minecraft:enchantments':[{'enchantments':'minecraft:silk_touch','levels':{'min':1}}]}}}]},
        {'type':'minecraft:item','name':NS+'fireclay_ball','functions':[{'function':'minecraft:set_count','count':4},{'function':'minecraft:explosion_decay'}]}]}]}]})
    for feature,count,placement in [('river_fireclay',2,[{'type':'minecraft:heightmap','heightmap':'WORLD_SURFACE_WG'}]),
            ('coal_fireclay',8,[{'type':'minecraft:height_range','height':{'type':'minecraft:uniform','min_inclusive':{'absolute':0},'max_inclusive':{'absolute':128}}}])]:
        put(D/'worldgen/configured_feature'/f'{feature}.json',{'type':NS+feature,'config':{}})
        put(D/'worldgen/placed_feature'/f'{feature}.json',{'feature':NS+feature,'placement':
            [{'type':'minecraft:count','count':count},{'type':'minecraft:in_square'}]+placement+[{'type':'minecraft:biome'}]})
    # Runs after vanilla coal in the same decoration step.
    put(D/'neoforge/biome_modifier/fireclay.json',{'type':'neoforge:add_features','biomes':'#minecraft:is_overworld',
        'features':[NS+'river_fireclay',NS+'coal_fireclay'],'step':'underground_decoration'})

def generate():
    recipes();materials_art();items_art();machine_art();fireclay_data()
    lang=json.loads((A/'lang/en_us.json').read_text())
    for name in ['impure_silicon_powder','pure_silicon_powder','silicon_crystal','silicon_wafer','printed_silicon_wafer','silicon_chip',
                 'bauxite_powder','alumina_powder','aluminium_sheet','turbine_blade','fireclay_ball','fireclay_brick']:
        lang['item.createindustrial.'+name]=name.replace('_',' ').title()
    for name,title in [('fireclay','Fireclay'),('laser_printer','Laser Printer (Legacy / Retired)'),('steel_converter','Air-Blown Steel Converter')]:
        lang['block.createindustrial.'+name]=title
    lang.update({'goggle.createindustrial.converter':'Air-blown steel refining',
        'goggle.createindustrial.printer':'Laser printing','goggle.createindustrial.process_progress':'Progress: %s / %s work',
        'goggle.createindustrial.requires_64_rpm':'Requires at least 64 RPM',
        'goggle.createindustrial.redstone_paused':'Paused by redstone',
        'goggle.createindustrial.converter_tanks':'Pig iron: %s mB | Steel: %s mB | Slag: %s mB',
        'goggle.createindustrial.requires_superheat':'Requires a superheated Blaze Burner below',
        'goggle.createindustrial.blocked_lance':'Clear the upper front air outlet'})
    put(A/'lang/en_us.json',lang)
    # V20 source of truth: always repaint assets after data generation.
    # Do NOT regenerate removed Laser Printer recipes, loot or creative items.
    import subprocess, sys
    subprocess.run([sys.executable, str(ROOT/'tools/generate_v20_textures.py')], check=True)
    (D/'recipe/steel_converter.json').unlink(missing_ok=True)
    put(D/'recipe/mixing/steel_refining.json', {
      'type':'create:mixing', 'heat_requirement':'superheated',
      'ingredients':[{'type':'neoforge:single','fluid':NS+'molten_pig_iron','amount':576},
                     {'item':'minecraft:calcite'},{'item':'minecraft:iron_nugget'},{'item':'minecraft:iron_nugget'}],
      'results':[{'id':NS+'molten_steel','amount':576},{'id':NS+'molten_slag','amount':144}]})
    lang = json.loads((A/'lang/en_us.json').read_text())
    lang['block.createindustrial.steel_converter'] = 'Steel Converter (Legacy)'
    lang['goggle.createindustrial.converter'] = 'Legacy converter: use superheated Create Basin for steel'
    put(A/'lang/en_us.json',lang)
    # Clear any leftover recipes from older generator runs on a dirty checkout.
    for retired in ('laser_printer.json','steel_converter.json','laser_printing/silicon_wafer.json','cutting/silicon_chips.json'):
        (D/'recipe'/retired).unlink(missing_ok=True)
    (D/'loot_table/blocks/laser_printer.json').unlink(missing_ok=True)
    (A/'models/item/laser_printer.json').unlink(missing_ok=True)
    print('Generated V20 refining recipes and 135 consistent 16x16 textures. Printer and special-port gameplay remain retired.')
if __name__=='__main__':generate()
