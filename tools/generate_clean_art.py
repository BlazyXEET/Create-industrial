#!/usr/bin/env python3
"""Original 16x16 pixel artwork. All material inventory items use generated sprites.
No antialiasing, gradients, cube ingots, or block-texture sampling on items.
Run through generate_materials.py, or directly to refresh artwork only.
"""
from pathlib import Path
import json
from PIL import Image, ImageDraw, ImageFont

ROOT=Path(__file__).resolve().parents[1]
A=ROOT/'src/main/resources/assets/createindustrial'
CAT=json.loads((ROOT/'materials.json').read_text())
COLORS={
 'aluminium':((183,202,210),(177,104,57)),
 'uranium':((141,153,139),(123,144,59)),
 'silver':((201,216,230),(171,189,205)),
 'tin':((175,188,184),(162,147,108)),
 'lead':((103,116,141),(118,117,154)),
 'nickel':((176,169,140),(166,149,92)),
 'steel':((115,137,151),(115,137,151)),
 'plutonium':((144,159,165),(144,159,165)),
 'pig_iron':((105,101,93),(105,101,93))}
def tone(c,n):return tuple(max(0,min(255,v+n)) for v in c)
def blend(a,b,w):return tuple(round(x*(1-w)+y*w) for x,y in zip(a,b))
def fresh(c=None):return Image.new('RGBA',(16,16),(0,0,0,0) if c is None else tuple(c)+(255,))
def save(im,name,kind='block'):
 p=A/'textures'/kind/(name+'.png');p.parent.mkdir(parents=True,exist_ok=True)
 im.save(p)
def sprite(name):
 p=A/'models/item'/(name+'.json')
 p.write_text(json.dumps({'parent':'minecraft:item/generated','textures':{'layer0':'createindustrial:item/'+name}},indent=2)+'\n',encoding='utf-8')
def outlined_poly(draw,points,c):
 draw.polygon(points,fill=tone(c,-53)+(255,))
def ingot(c):
 im=fresh();d=ImageDraw.Draw(im)
 # An angled vanilla-style bar, painted into one flat 16x16 sprite.
 d.polygon([(1,7),(8,3),(11,3),(15,6),(15,9),(7,13),(4,13),(0,10),(0,8)],fill=tone(c,-66))
 d.polygon([(2,7),(8,4),(11,4),(14,6),(7,10),(4,10),(1,8)],fill=tone(c,20))
 d.polygon([(1,9),(4,11),(7,11),(14,7),(14,9),(7,12),(4,12),(1,10)],fill=tone(c,-19))
 d.polygon([(1,8),(4,10),(4,12),(1,10)],fill=tone(c,-31))
 d.line([(2,7),(8,4),(11,4)],fill=tone(c,62))
 d.line([(5,10),(7,10),(13,7)],fill=tone(c,39))
 d.line([(5,11),(7,11),(12,8)],fill=tone(c,-2))
 return im
def nugget(c):
 im=fresh();d=ImageDraw.Draw(im)
 d.polygon([(6,4),(10,4),(12,6),(12,9),(9,12),(5,12),(3,10),(3,7)],fill=tone(c,-64))
 d.polygon([(6,5),(9,5),(11,7),(9,10),(5,10),(4,8)],fill=c)
 d.polygon([(6,5),(9,5),(10,6),(7,8),(4,8)],fill=tone(c,40))
 d.line([(5,11),(8,11),(10,9)],fill=tone(c,-22))
 d.point((6,6),fill=tone(c,66))
 return im
def pebble(im,x,y,c,size=4):
 d=ImageDraw.Draw(im);s=size
 d.polygon([(x+1,y),(x+s-2,y),(x+s,y+2),(x+s-1,y+s-1),(x+1,y+s),(x,y+s-2),(x,y+1)],fill=tone(c,-53))
 d.polygon([(x+1,y+1),(x+s-2,y+1),(x+s-1,y+2),(x+s-2,y+s-1),(x+1,y+s-1)],fill=c)
 d.line([(x+1,y+1),(x+s-2,y+1),(x+s-1,y+2)],fill=tone(c,36))
 d.line([(x+1,y+s-1),(x+s-2,y+s-1)],fill=tone(c,-20))
def raw(c):
 im=fresh();pebble(im,2,6,c,7);pebble(im,7,3,tone(c,6),6);pebble(im,8,9,tone(c,-9),4)
 d=ImageDraw.Draw(im)
 d.rectangle((4,8,5,9),fill=blend(c,(168,158,138),.65))
 d.point((11,5),fill=tone(c,60));d.point((9,12),fill=tone(c,18))
 return im
def crushed(c):
 im=fresh()
 for x,y,s,n in [(2,4,4,0),(8,2,4,8),(6,8,5,0),(1,10,3,-7),(12,8,2,10),(11,12,2,-12)]:
  pebble(im,x,y,tone(c,n),s)
 return im
def powder(c):
 im=fresh();d=ImageDraw.Draw(im)
 d.polygon([(2,11),(4,9),(6,9),(7,6),(9,5),(11,8),(12,9),(14,11),(14,13),(11,14),(3,14),(1,13)],fill=tone(c,-56))
 d.polygon([(2,11),(5,10),(7,8),(8,6),(10,7),(11,10),(13,11),(11,13),(4,13)],fill=c)
 d.polygon([(4,10),(6,10),(8,7),(9,7),(10,9),(8,10),(6,12),(3,12)],fill=tone(c,33))
 d.line((6,13,11,13),fill=tone(c,-18))
 for x,y in [(2,8),(12,6),(13,13),(5,6)]:d.point((x,y),fill=tone(c,12))
 return im
def stone(deep=False):
 c=(66,67,70) if deep else (126,126,123)
 im=fresh(c);d=ImageDraw.Draw(im)
 # Rock planes rather than independent speckled pixels.
 patches=[([(0,0),(5,0),(5,2),(2,2),(2,4),(0,4)],9),
 ([(7,1),(12,1),(12,3),(15,3),(15,5),(10,5),(10,4),(7,4)],-7),
 ([(2,6),(7,6),(7,8),(5,8),(5,10),(1,10),(1,8),(2,8)],-10),
 ([(10,7),(15,7),(15,10),(13,10),(13,12),(9,12),(9,9),(10,9)],8),
 ([(0,13),(4,13),(4,12),(7,12),(7,15),(0,15)],4),
 ([(10,14),(15,14),(15,15),(9,15),(9,13),(10,13)],-9)]
 for points,n in patches:d.polygon(points,fill=tone(c,n))
 if deep:
  for points in [[(0,5),(4,5),(4,4)],[(6,10),(8,10),(8,9)],[(10,0),(15,0)],[(12,12),(15,12)]]:
   d.line(points,fill=tone(c,-14))
 else:
  for x,y in [(1,1),(3,6),(11,8),(4,14),(14,3)]:d.line((x,y,x+1,y),fill=tone(c,13))
 return im
ORE_SHAPES={
'aluminium':[(2,2,4),(10,2,4),(6,7,4),(1,11,4),(11,11,4)],
'uranium':[(2,2,3),(3,5,3),(10,1,3),(9,8,4),(2,11,3),(11,12,3)],
'silver':[(1,3,4),(4,2,3),(10,5,4),(8,8,3),(2,11,4),(11,12,3)],
'tin':[(3,1,3),(10,3,4),(5,7,4),(1,11,3),(11,11,4)],
'lead':[(1,2,4),(10,1,4),(6,7,4),(2,11,4),(11,11,4)],
'nickel':[(3,2,4),(10,2,3),(1,8,3),(7,8,4),(11,12,3),(3,12,3)]}
def ore(mid,deep=False):
 im=stone(deep);c=COLORS[mid][1];d=ImageDraw.Draw(im)
 for x,y,s in ORE_SHAPES[mid]:
  d.polygon([(x+1,y),(x+s-1,y),(x+s,y+1),(x+s,y+s-1),(x+s-2,y+s),(x,y+s-1),(x,y+1)],fill=tone(c,-46))
  d.rectangle((x+1,y+1,x+s-1,y+s-1),fill=c)
  d.line((x+1,y+1,x+s-2,y+1),fill=tone(c,38))
  d.point((x+1,y+2),fill=tone(c,19))
  if mid=='silver':d.line((x+1,y+1,x+s-1,y+1),fill=tone(c,65))
  if mid=='lead':d.line((x+s-1,y+2,x+s-1,y+s-1),fill=tone(c,-20))
  if mid=='uranium':d.point((x+s-1,y+1),fill=tone(c,20))
 return im
def raw_block(c):
 host=blend(c,(102,96,87),.45)
 im=fresh(tone(host,-34))
 # Repeated edge chunks join cleanly between neighbouring blocks.
 chunks=[(-2,1,6,0),(5,-2,6,5),(11,3,5,-5),(3,6,6,0),(9,10,6,6),(-2,12,6,-8)]
 for x,y,s,n in chunks:
  for dx in (-16,0,16):
   for dy in (-16,0,16):pebble(im,x+dx,y+dy,tone(c,n),s)
 d=ImageDraw.Draw(im)
 for x,y in [(0,7),(8,4),(7,14),(15,0)]:d.rectangle((x,y,min(15,x+1),min(15,y+1)),fill=host)
 return im
def plate(c,kind='plain'):
 im=fresh(c);d=ImageDraw.Draw(im)
 d.rectangle((0,0,15,15),outline=tone(c,-36))
 d.line([(1,14),(1,1),(14,1)],fill=tone(c,27))
 d.line([(2,14),(14,14),(14,2)],fill=tone(c,-19))
 if kind=='brushed':
  for x in (4,7,11):d.line((x,3,x,12),fill=tone(c,6))
 elif kind=='riveted':
  for x,y in [(3,3),(12,3),(3,12),(12,12)]:
   d.point((x,y),fill=tone(c,38));d.point((x,y+1),fill=tone(c,-44))
 else:
  d.polygon([(3,9),(9,3),(11,3),(3,11)],fill=tone(c,12))
  d.line([(5,12),(12,5)],fill=tone(c,6))
 return im
def bricks(top=False):
 c=(191,165,119);im=fresh((103,94,76));d=ImageDraw.Draw(im)
 for row in range(4):
  y=row*4
  for x in range(-4 if row%2 else 0,16,8):
   d.rectangle((x,y,x+6,y+2),fill=tone(c,(row%2)*-5))
   d.line((x,y,x+6,y),fill=tone(c,19))
   d.point((x+6,y+2),fill=tone(c,-23))
 return im
def slab(c,plaster=False):
 im=fresh(c);d=ImageDraw.Draw(im)
 if not plaster:
  d.line((0,0,15,0),fill=tone(c,-30));d.line((0,0,0,15),fill=tone(c,-30))
  d.line((1,1,14,1),fill=tone(c,11))
 for x,y in [(3,5),(10,3),(8,12),(13,9),(2,13)]:
  d.line((x,y,x+1,y),fill=tone(c,-7))
 return im
def panel(c):
 im=plate(c,'riveted');d=ImageDraw.Draw(im)
 d.rectangle((4,4,11,11),fill=tone(c,-6))
 d.line((5,5,10,5),fill=tone(c,4))
 return im
def front(kind,active=False):
 im=panel((89,104,107));d=ImageDraw.Draw(im)
 d.rectangle((3,4,12,11),fill=(35,45,49))
 d.line((4,5,11,5),fill=(126,148,155))
 if kind=='laser':
  d.rectangle((5,6,10,9),fill=(53,78,90))
  d.line((6,6,9,6),fill=(101,139,154))
  d.line((6,9,10,9),fill=(33,53,63))
  if active:
   d.line((7,6,7,8),fill=(123,224,232));d.point((7,9),fill=(226,255,249))
 else:
  for x in (4,6,8,10):
   d.line((x,7,x,10),fill=(247,157,59) if active else (93,81,65))
  d.line((4,11,11,11),fill=(64,66,63))
 d.point((12,3),fill=(117,195,169) if active else (59,91,84))
 return im
def hatch(state):
 im=bricks();d=ImageDraw.Draw(im)
 d.rectangle((2,2,13,13),fill=(49,56,57));d.line([(3,12),(3,3),(12,3)],fill=(126,137,135))
 d.rectangle((4,4,11,11),fill=(73,83,81))
 if state=='assembled':
  d.rectangle((5,6,10,10),fill=(28,34,36))
  for x in (6,9):d.line((x,7,x,9),fill=(109,112,99))
 elif state=='lit':
  d.rectangle((5,6,10,10),fill=(239,119,32))
  for x in (6,9):d.line((x,7,x,9),fill=(255,208,91))
  d.line((5,11,10,11),fill=(121,61,34))
 else:
  d.line((5,7,10,7),fill=(140,149,143));d.line((8,7,8,10),fill=(140,149,143))
 for x,y in [(3,3),(12,3),(3,12),(12,12)]:d.point((x,y),fill=(168,154,112))
 return im
def port(name):
 fluid='fluid' in name;enter=name.endswith('_in')
 c=(74,139,150) if fluid else (135,159,176)
 im=panel((83,96,99));d=ImageDraw.Draw(im)
 d.rectangle((3,3,12,12),fill=(35,46,51))
 if fluid:
  d.polygon([(7,4),(8,4),(10,7),(10,9),(8,11),(6,11),(4,9),(4,7)],fill=c)
  d.point((6,7),fill=tone(c,43))
 else:
  d.rectangle((4,5,9,10),fill=c);d.line((5,6,8,6),fill=tone(c,39))
 arrow=(222,183,99) if not enter else (132,195,165)
 if enter:d.polygon([(11,5),(14,8),(11,11),(11,9),(9,9),(9,7),(11,7)],fill=arrow)
 else:d.polygon([(13,5),(10,8),(13,11),(13,9),(15,9),(15,7),(13,7)],fill=arrow)
 return im
def processing():
 for n,c in [('impure_silicon_powder',(139,126,105)),('pure_silicon_powder',(194,198,217)),
             ('bauxite_powder',(191,118,64)),('alumina_powder',(229,222,191)),('alumina_dust',(229,222,191))]:
  save(powder(c),n,'item');sprite(n)
 # Faceted silicon crystal, then a thin polished wafer and a patterned wafer.
 im=fresh();d=ImageDraw.Draw(im)
 d.polygon([(7,1),(10,3),(12,10),(9,14),(4,13),(3,8)],fill=(55,64,85))
 d.polygon([(7,2),(8,5),(7,12),(4,10),(4,8)],fill=(179,191,215))
 d.polygon([(8,3),(10,5),(11,10),(8,13),(8,6)],fill=(115,136,171))
 d.line([(7,3),(5,8),(5,10)],fill=(225,231,235))
 save(im,'silicon_crystal','item');sprite('silicon_crystal')
 for printed in (False,True):
  n=('printed_' if printed else '')+'silicon_wafer';im=fresh();d=ImageDraw.Draw(im)
  d.polygon([(5,1),(10,1),(14,5),(14,10),(10,14),(5,14),(1,10),(1,5)],fill=(49,58,81))
  d.polygon([(5,2),(10,2),(13,5),(13,10),(10,13),(5,13),(2,10),(2,5)],fill=(113,133,170))
  d.line([(3,6),(6,3),(10,3)],fill=(184,204,219))
  d.line([(4,10),(10,4)],fill=(139,157,188))
  if printed:
   for x in (5,8,11):d.line((x,4,x,11),fill=(209,172,86))
   for y in (5,8,11):d.line((4,y,11,y),fill=(66,77,99))
   for x,y in [(5,5),(8,8),(11,11)]:d.point((x,y),fill=(242,215,139))
  save(im,n,'item');sprite(n)
 im=fresh();d=ImageDraw.Draw(im)
 for x in (4,7,10):d.line((x,2,x,13),fill=(200,165,82))
 for y in (4,7,10):d.line((2,y,13,y),fill=(200,165,82))
 d.rectangle((3,3,12,12),fill=(45,58,61));d.rectangle((5,5,10,10),fill=(72,98,102))
 d.line([(4,11),(4,4),(11,4)],fill=(123,150,148));d.rectangle((7,7,9,9),fill=(39,61,69))
 save(im,'silicon_chip','item');sprite('silicon_chip')
 im=fresh();d=ImageDraw.Draw(im)
 d.polygon([(1,6),(9,2),(14,6),(14,9),(6,13),(1,10)],fill=(73,96,112))
 d.polygon([(2,6),(9,3),(13,6),(6,10),(2,8)],fill=(184,207,215))
 d.line([(3,6),(9,3),(12,5)],fill=(231,239,236));d.line((6,11,12,8),fill=(127,155,172))
 save(im,'aluminium_sheet','item');sprite('aluminium_sheet')
 im=fresh();d=ImageDraw.Draw(im)
 d.polygon([(6,12),(7,5),(10,1),(13,1),(13,4),(10,11),(8,14),(5,14)],fill=(61,83,96))
 d.polygon([(8,5),(10,2),(12,2),(12,4),(9,11),(7,12)],fill=(176,202,213))
 d.line([(9,4),(11,2),(12,2)],fill=(232,239,231));d.rectangle((5,12,8,14),fill=(146,121,75))
 save(im,'turbine_blade','item');sprite('turbine_blade')
 im=raw((171,145,115));save(im,'fireclay_ball','item');sprite('fireclay_ball')
 im=ingot((205,176,124));save(im,'fireclay_brick','item');sprite('fireclay_brick')
 for n,c in [('coke',(73,78,80)),('slag',(110,98,80))]:
  save(raw(c),n,'item');sprite(n)
def all_art():
 for m in CAT['materials']+CAT['manufactured']:
  mid=m['id'];metal,mineral=COLORS[mid]
  for suffix,fn in [('ingot',ingot),('nugget',nugget)]:
   n=mid+'_'+suffix;save(fn(metal),n,'item');sprite(n)
  style='riveted' if mid=='steel' else 'brushed' if mid in ('nickel','tin') else 'plain'
  save(plate(metal,style),'block_of_'+mid)
  if mid=='uranium':save(plate(metal,style),'block_of_uranium_top')
  if m in CAT['materials']:
   for deep in (False,True):save(ore(mid,deep),('deepslate_' if deep else '')+m['ore']+'_ore')
   save(raw_block(mineral),'raw_'+mid+'_block')
   for n,fn in [('raw_'+mid,raw),('crushed_raw_'+mid,crushed)]:
    save(fn(mineral),n,'item');sprite(n)
 save(raw_block((149,170,159)),'raw_zinc_block')
 processing()
 save(bricks(),'fireclay_bricks');save(bricks(True),'fireclay_bricks_top')
 im=fresh((147,128,105));d=ImageDraw.Draw(im)
 for points,n in [([(0,1),(5,1),(5,4),(3,6),(0,5)],8), ([(9,0),(15,0),(15,5),(11,5)],-8),
                  ([(4,8),(9,8),(11,11),(8,14),(3,13)],5), ([(0,13),(2,12),(3,15),(0,15)],-12)]:
  d.polygon(points,fill=tone((147,128,105),n))
 save(im,'fireclay')
 for n,c,plaster in [('reinforced_concrete',(151,158,155),False),('reinforced_concrete_top',(155,161,158),False),
                     ('plastered_reinforced_concrete',(207,206,191),True)]:
  save(slab(c,plaster),n)
 mesh=fresh();d=ImageDraw.Draw(mesh)
 for x in range(0,16,4):d.line((x,0,x,15),fill=(63,87,89));d.line((min(15,x+1),0,min(15,x+1),15),fill=(151,172,164))
 for y in range(0,16,4):d.line((0,y,15,y),fill=(151,172,164));d.line((0,min(15,y+1),15,min(15,y+1)),fill=(63,87,89))
 save(mesh,'condensing_mesh')
 p=A/'models/block/condensing_mesh.json';model=json.loads(p.read_text());model['render_type']='minecraft:cutout';p.write_text(json.dumps(model,indent=2)+'\n')
 save(panel((80,100,104)),'machine_casing');save(panel((165,133,76)),'machine_brass')
 for kind in ('laser','converter'):
  save(front(kind),kind+'_front');save(front(kind,True),kind+'_front_active')
 for state,name in [('plain','blast_furnace_hatch_front'),('assembled','blast_furnace_hatch_front_assembled'),('lit','blast_furnace_hatch_front_lit')]:
  save(hatch(state),name)
 for n in ('port_item_in','port_item_out','port_fluid_in','port_fluid_out'):save(port(n),n)
 # Broad hot ripples, with no ore-shaped chunks in the liquid surface.
 hot={'iron':(241,135,42),'copper':(245,144,59),'gold':(252,182,63),'aluminium':(250,177,94),'uranium':(239,153,56),
      'zinc':(245,175,95),'silver':(253,192,105),'tin':(239,164,72),'lead':(227,132,57),'nickel':(245,165,68),
      'steel':(251,160,60),'plutonium':(238,155,79),'pig_iron':(237,123,36)}
 for mid,c in hot.items():
  im=fresh(c);d=ImageDraw.Draw(im)
  for points,n in [([(0,3),(4,3),(6,5),(10,5),(12,3),(15,3)],19),
                   ([(0,10),(3,10),(5,8),(9,8),(11,10),(15,10)],-12),
                   ([(1,14),(5,14),(7,12),(11,12),(14,14)],7)]:
   d.line(points,fill=tone(c,n),width=2)
  save(im,'molten_'+mid)
 crust=stone(True);d=ImageDraw.Draw(crust);d.line([(0,12),(4,9),(6,9),(9,5),(15,3)],fill=(133,77,38));save(crust,'slag_crust')
 # Preserve the approved blue tool's geometry; tidy its small palette tiles.
 tool={'teal':(31,104,155),'teal_dark':(20,62,98),'teal_highlight':(128,191,222),'teal_mid':(58,134,180),'teal_shadow':(24,77,119),
       'gunmetal':(74,91,105),'gunmetal_dark':(43,56,66),'steel':(155,174,182),'steel_light':(204,221,223),
       'rubber':(35,43,48),'grip':(47,59,65),'nozzle_black':(31,38,43),'bolt':(147,161,159),'red':(150,64,54),'red_light':(211,105,79)}
 for name,c in tool.items():
  im=fresh(c);d=ImageDraw.Draw(im)
  d.line((0,0,15,0),fill=tone(c,11));d.line((0,15,15,15),fill=tone(c,-13))
  if name in ('grip','rubber'):
   for y in (3,7,11):d.line((1,y,14,y),fill=tone(c,-9))
  save(im,'welder/'+name,'item')
 # Record a small, reviewable visual contract for the actual registered assets.
 names=[m['id']+'_'+s for m in CAT['materials']+CAT['manufactured'] for s in ('ingot','nugget')]
 names += [p+m['id'] for m in CAT['materials'] for p in ('raw_','crushed_raw_')]
 manifest={'resolution':[16,16],'material_items':'flat generated sprites','sprite_items':names,
           'style':'original limited-palette Minecraft pixel art','preserved_brand_asset':'cooling_tower_icon.png'}
 out=ROOT/'art/pixel-art';out.mkdir(parents=True,exist_ok=True)
 (out/'manifest.json').write_text(json.dumps(manifest,indent=2)+'\n')
 print('Clean pixel art generated:',len(names),'flat material sprites; all ore, block, machine, molten and tool palette textures.')
def preview():
 out=ROOT/'dist';out.mkdir(exist_ok=True)
 def font(size,bold=False):
  return ImageFont.truetype('C:/Windows/Fonts/'+('arialbd.ttf' if bold else 'arial.ttf'),size)
 rows=CAT['materials']+CAT['manufactured'];w=1440;rh=130;h=190+len(rows)*rh+70
 im=Image.new('RGB',(w,h),(19,26,34));d=ImageDraw.Draw(im)
 d.text((34,24),'CREATE: INDUSTRIAL | V18',font=font(34,True),fill=(239,201,112))
 d.text((35,77),'Flat 16x16 inventory sprites. Exact source pixels at 5x scale.',font=font(22),fill=(179,195,207))
 headers=['Raw material','Crushed material','Ingot','Nugget','Stone ore','Deepslate ore']
 for j,label in enumerate(headers):d.text((230+j*195,144),label,font=font(18,True),fill=(171,190,204))
 for i,m in enumerate(rows):
  y=184+i*rh
  if i%2==0:d.rectangle((18,y,w-18,y+rh-6),fill=(27,38,49))
  mid=m['id'];d.text((35,y+42),mid.replace('_',' ').title(),font=font(23,True),fill=(231,237,241))
  names=[('item','raw_'+mid),('item','crushed_raw_'+mid),('item',mid+'_ingot'),('item',mid+'_nugget')]
  names += [('block',m['ore']+'_ore'),('block','deepslate_'+m['ore']+'_ore')] if 'ore' in m else [(None,''),(None,'')]
  for j,(kind,name) in enumerate(names):
   x=270+j*195
   if kind is None or not (A/'textures'/kind/(name+'.png')).is_file():
    d.text((x+20,y+44),'--',font=font(20),fill=(100,119,133));continue
   # Checkerboard makes transparency visible without altering the sprite itself.
   for xx in range(8):
    for yy in range(8):
     color=(43,53,62) if (xx+yy)%2==0 else (36,46,55)
     d.rectangle((x+xx*10,y+16+yy*10,x+xx*10+9,y+16+yy*10+9),fill=color)
   tile=Image.open(A/'textures'/kind/(name+'.png')).convert('RGBA').resize((80,80),Image.Resampling.NEAREST)
   im.paste(tile,(x,y+16),tile)
 d.text((35,h-45),'Blocks and machines retain Minecraft cube geometry. All ingots, nuggets, raw and crushed materials are flat sprites.',font=font(19),fill=(161,181,196))
 im.save(out/'CreateIndustrial-V18-Pixel-Art.png')
 print(out/'CreateIndustrial-V18-Pixel-Art.png')
if __name__=='__main__':
 from subprocess import run
 from sys import executable
 print('Deprecated V18 generator: using the V20 16x16 artwork source of truth.')
 run([executable,str(ROOT/'tools/generate_v20_textures.py')],check=True)
