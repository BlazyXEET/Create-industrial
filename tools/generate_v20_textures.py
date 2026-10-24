#!/usr/bin/env python3
"""V20: Crisp, restrained, vanilla-compatible 16x16 industrial pixel art.

Build-time only; Pillow is NOT required by Minecraft. Uses shape-specific silhouettes,
restrained 5-7 tone palettes, and crisp nearest-neighbour pixels (no gradients/noise).
Run: python3 tools/generate_v20_textures.py
"""
from pathlib import Path
from PIL import Image, ImageDraw
import math, colorsys

ROOT=Path(__file__).resolve().parents[1]/'src/main/resources/assets/createindustrial/textures'
BLOCK=ROOT/'block'; ITEM=ROOT/'item'; WELDER=ITEM/'welder'
PALETTES={
 'aluminium':('#2e434c','#526b77','#829ca6','#bfd1d4','#eff2e9','#ffffff'),
 'lead':('#293441','#394958','#576873','#7e929f','#b4c4cc','#e2e9e8'),
 'nickel':('#354a50','#4b6667','#668884','#95aaa1','#d1d9bc','#f2e7c7'),
 'silver':('#35424b','#566773','#899eab','#c4d3da','#eef3ee','#ffffff'),
 'tin':('#344851','#56727b','#8ca2a8','#c8d0c9','#e8e7d4','#f4f2e5'),
 'uranium':('#263d31','#3f6244','#658957','#97aa6a','#c5c990','#e2dfb7'),
 'plutonium':('#253632','#38584e','#568071','#8bac83','#c4d5a7','#e6e5bb'),
 'pig_iron':('#342d32','#59444b','#84666a','#a88e8b','#cfbab0','#eaded0'),
 'steel':('#233743','#395464','#587788','#87a1aa','#c4d4d6','#ebf3ed'),
 'zinc':('#3b5050','#5d7b71','#86a59b','#b4c4b1','#dce5d7','#f1f5e8'),
 'bauxite':('#493026','#774338','#ae5b3f','#d98755','#efa56b','#ffd09c'),
 'copper':('#5c2d23','#994c33','#c77c4d','#e2a56c','#f0c28b','#fbe2b2'),
 'gold':('#63451b','#a16c24','#d69c34','#efc55b','#f5df8a','#fff3ba'),
 'iron':('#394854','#5e7582','#8da6b3','#bdcdd0','#e5e9de','#fff7df'),
}
materials=['aluminium','lead','nickel','silver','tin','uranium']
texture_outputs={}

def color(h):
 if isinstance(h,tuple):return h
 h=h.lstrip('#');return tuple(int(h[i:i+2],16) for i in (0,2,4))+(255,)

def blend(a,b,f):
 a=color(a);b=color(b);return tuple(int(a[i]*(1-f)+b[i]*f) for i in range(3))+(255,)

def make():
 im=Image.new('RGBA',(16,16));return im,ImageDraw.Draw(im)

def rect(d,box,cl):d.rectangle(box,fill=color(cl))
def poly(d,coords,cl):d.polygon(coords,fill=color(cl))
def line(d,pts,cl,w=1):d.line(pts,fill=color(cl),width=w)
def px(d,x,y,cl):d.point((x,y),fill=color(cl))
def save(im,filename,folder=ITEM):
 im.save(folder/(filename+'.png'),optimize=True)
 texture_outputs[(folder.name+'/'+filename)]=True

def metal_ingot(m):
 p=PALETTES[m];im,d=make()
 poly(d,[(2,7),(5,4),(11,3),(14,5),(15,9),(12,12),(5,14),(1,11)],p[0])
 poly(d,[(3,7),(5,5),(11,4),(13,5),(13,8),(5,10),(2,9)],p[3])
 poly(d,[(5,5),(10,4),(13,5),(12,6),(5,8),(3,8)],p[4])
 poly(d,[(2,10),(5,11),(5,13),(2,11)],p[1]);poly(d,[(5,11),(13,9),(12,11),(5,13)],p[2])
 line(d,[(5,10),(13,8)],p[1]);line(d,[(4,7),(5,6),(10,5)],p[5]);px(d,8,9,p[4])
 return im

def nugget(m):
 p=PALETTES[m];im,d=make()
 poly(d,[(3,6),(6,4),(10,5),(13,8),(12,12),(8,14),(4,13),(2,10)],p[0])
 poly(d,[(4,7),(6,5),(10,6),(12,8),(8,10),(3,10)],p[3])
 poly(d,[(4,10),(8,11),(8,13),(4,12)],p[1]);poly(d,[(8,11),(12,9),(11,12),(8,13)],p[2])
 line(d,[(5,7),(7,6),(9,7)],p[5]);px(d,9,9,p[4]);return im

def raw(m):
 p=PALETTES[m];im,d=make()
 poly(d,[(2,6),(5,3),(9,4),(12,2),(14,6),(12,9),(14,12),(10,14),(6,12),(3,13),(1,9)],p[0])
 poly(d,[(3,6),(6,4),(9,5),(12,3),(13,6),(10,9),(5,10),(2,9)],p[2])
 poly(d,[(4,6),(6,5),(8,5),(7,8),(4,9)],p[4]);poly(d,[(8,11),(12,9),(13,11),(10,13),(7,12)],p[3])
 line(d,[(3,11),(5,12),(7,11)],p[1]);px(d,11,5,p[5]);px(d,9,8,p[4]);return im

def crushed(m):
 p=PALETTES[m];im,d=make()
 poly(d,[(1,10),(4,5),(7,8),(7,12),(4,14)],p[0]);poly(d,[(2,9),(4,6),(6,8),(6,10)],p[3]);px(d,4,7,p[5])
 poly(d,[(6,4),(10,2),(13,4),(12,8),(9,9)],p[0]);poly(d,[(7,4),(10,3),(11,4),(10,7),(8,7)],p[3]);px(d,9,4,p[5])
 poly(d,[(9,11),(12,8),(15,10),(14,13),(11,15)],p[0]);poly(d,[(10,11),(12,9),(14,11),(13,12)],p[3]);px(d,12,10,p[5]);return im

def pile(p,seed=0):
 im,d=make()
 poly(d,[(1,12),(3,9),(5,8),(6,5),(10,5),(12,8),(14,9),(15,12),(12,14),(3,14)],p[0])
 poly(d,[(2,12),(4,9),(6,7),(10,6),(13,10),(14,12),(12,13),(4,13)],p[2])
 poly(d,[(4,10),(7,6),(9,6),(9,8),(12,11),(9,12),(5,12)],p[3])
 for x,y,idx in [(6,8,4),(8,7,5),(10,10,4),(4,11,1),(12,12,1),(8,12,2),(5,13,3),(11,13,0)]:px(d,x,y,p[idx])
 return im

def silicon_wafer(printing=False):
 im,d=make();p=PALETTES['steel']
 poly(d,[(5,1),(10,1),(14,5),(15,10),(11,14),(5,15),(1,11),(1,5)],'#263b46')
 poly(d,[(5,2),(10,2),(13,5),(14,10),(11,13),(5,14),(2,11),(2,5)],'#839fa6' if not printing else '#669ea2')
 poly(d,[(6,3),(10,3),(12,5),(13,9),(10,12),(6,13),(3,10),(3,6)],'#bdcbd1' if not printing else '#28495c')
 line(d,[(4,6),(11,6)],'#e5ece6' if not printing else '#4ac3bf')
 if printing:
  for i in (5,8,11):line(d,[(i,4),(i,12)],'#70aabc');line(d,[(4,i),(12,i)],'#609baf')
  rect(d,(6,6,9,9),'#1a3447');rect(d,(7,7,8,8),'#a6edc9');px(d,11,4,'#eecc73')
 else:
  line(d,[(5,11),(11,11)],'#7b999e');px(d,5,4,'#f2f4ed')
 return im

def chip():
 im,d=make()
 for y in (4,7,10):rect(d,(1,y,3,y+1),'#bf934d');rect(d,(12,y,14,y+1),'#bf934d')
 for x in (4,7,10):rect(d,(x,1,x+1,3),'#c7a15f');rect(d,(x,12,x+1,14),'#a47e46')
 rect(d,(3,3,12,12),'#101e27');rect(d,(4,4,11,11),'#314b52');rect(d,(5,5,10,10),'#203540')
 rect(d,(6,6,9,9),'#557e7b');px(d,7,6,'#a5c0b4');px(d,11,5,'#86c6be');return im

def sail():
 im,d=make()
 poly(d,[(3,2),(13,8),(13,13),(3,14)],'#80633f');poly(d,[(4,3),(12,8),(12,12),(4,13)],'#e0cbae');line(d,[(4,4),(12,9)],'#fff0ce');line(d,[(3,2),(3,14)],'#533e2c',2)
 for y in (4,7,10,13):px(d,3,y,'#b68b53')
 return im

def blade():
 im,d=make();p=PALETTES['steel']
 poly(d,[(1,13),(3,8),(11,2),(14,1),(15,4),(10,9),(5,13)],p[0]);poly(d,[(3,9),(11,3),(13,2),(13,5),(8,9),(4,11)],p[3])
 line(d,[(5,10),(13,4)],p[5]);poly(d,[(1,13),(4,10),(6,13),(4,15)],'#a98742');px(d,4,13,'#e9d393');return im

def stone_variant(deep=False):
 """Hand-shaped vanilla-style stone/deepslate field (not horizontal strips).
 Only 6 restrained shades, cohesive 1-pixel crack geometry.
 """
 im,d=make()
 if deep:
  p=('#2a3035','#333a3e','#3e4549','#4a5153','#555c5d','#676b6a')
  rect(d,(0,0,15,15),p[2]);
  for pts,i in [([(0,0),(8,0),(5,3),(2,5),(0,4)],1),
                ([(10,0),(15,0),(15,5),(12,5),(8,3)],3),
                ([(0,6),(5,4),(8,7),(6,10),(0,12)],1),
                ([(8,7),(14,5),(15,10),(12,13),(7,12)],3),
                ([(0,14),(5,12),(9,15),(15,15)],1)]:poly(d,pts,p[i])
  for pts,i in [([(0,3),(2,2),(5,2)],0), ([(5,5),(8,6),(11,6)],4),
                ([(10,1),(9,3),(7,4)],0), ([(2,9),(4,8),(7,9)],0),
                ([(12,11),(11,12),(9,13)],0), ([(14,14),(15,12)],5)]:line(d,pts,p[i])
  for x,y,c in [(4,4,4),(12,3,5),(3,12,4),(9,10,1),(6,14,5),(15,7,0)]:px(d,x,y,p[c])
 else:
  p=('#626764','#747a75','#828783','#919790','#a1a69e','#b0b3a9')
  rect(d,(0,0,15,15),p[2]);
  for pts,i in [ ([(0,0),(6,0),(8,2),(4,5),(0,4)],1),
                 ([(10,0),(15,0),(15,5),(13,6),(9,3)],3),
                 ([(1,5),(6,4),(10,8),(7,10),(0,9)],3),
                 ([(11,7),(15,6),(15,12),(12,13),(9,11)],1),
                 ([(0,12),(4,11),(8,14),(7,15),(0,15)],1),
                 ([(11,14),(14,13),(15,15),(10,15)],3)]:poly(d,pts,p[i])
  for pts,i in [ ([(0,2),(3,2),(4,1)],4), ([(5,3),(7,3),(8,5)],0),
                 ([(10,2),(12,3),(15,3)],4), ([(2,8),(5,8),(6,10)],0),
                 ([(8,11),(10,10),(13,11)],4), ([(2,13),(3,12),(6,13)],0)]:line(d,pts,p[i])
  for x,y,c in [(1,6,0),(12,5,5),(7,0,4),(4,15,4),(9,13,0),(15,9,4)]:px(d,x,y,p[c])
 return im

def ore(m,deep=False):
 """Embedded jagged ore clusters with mineral highlights and stone gaps.
 Explicit hand-positioned blobs, no uniform dot grid, no AI-style gradients.
 """
 im=stone_variant(deep);d=ImageDraw.Draw(im);p=PALETTES[m]
 # Original independent shapes rather than copied Minecraft pixel coordinates.
 blobs=[
  [(1,3),(2,2),(3,2),(4,3),(3,4),(2,5),(1,5)],
  [(9,1),(10,2),(11,1),(12,2),(13,3),(12,4),(10,4)],
  [(6,6),(7,5),(8,6),(9,6),(10,7),(9,8),(8,8),(7,9),(6,8),(5,8)],
  [(1,10),(2,10),(3,9),(4,10),(4,11),(5,12),(3,13),(2,12)],
  [(10,11),(11,10),(12,10),(13,11),(13,12),(12,13),(11,13),(10,12)]
 ]
 # Slightly different ore distributions by material; stone never gets tiled/cropped.
 variants={'aluminium':(0,0),'bauxite':(0,0),'uranium':(1,0),
           'silver':(0,1),'tin':(1,1),'lead':(2,0),'nickel':(2,1)}
 phase=variants.get(m,(0,0))
 for k,cluster in enumerate(blobs):
  points=set()
  for x,y in cluster:
   # Shift one selected vein by a pixel for meaningful mineral variety.
   if k in (1,3) and (phase[0]+k)%3==0: x=max(0,min(15,x+1))
   if k in (0,4) and (phase[1]+k)%3==0: y=max(0,min(15,y+1))
   points.add((x,y))
  # Use darkest mineral on the exposed lower/right seam, medium mid-face,
  # two or three bright flecks on the top-left: recognizes as ore at distance.
  for x,y in points:
   shade = 0 if (x+1,y) not in points or (x,y+1) not in points else 2
   px(d,x,y,p[shade])
  ordered=sorted(points,key=lambda t:t[0]+t[1])
  for x,y in ordered[1::3]: px(d,x,y,p[3])
  for x,y in ordered[:2]:px(d,x,y,p[4])
  if len(ordered)>4:
   x,y=ordered[(k+phase[0])%len(ordered)];px(d,x,y,p[5 if not deep else 4])
 # A small isolated spot near a corner, characteristic of vanilla ore textures.
 px(d,6,2,p[3]);px(d,14,8,p[2]);px(d,8,14,p[4]);
 return im

def metal_block(p,kind='plate'):
 im,d=make()
 if kind in ('brass','casing'):
  rect(d,(0,0,15,15),p[0]);rect(d,(1,1,14,14),p[2]);
  rect(d,(2,2,13,13),p[1]);rect(d,(3,3,12,12),p[2]);
  line(d,[(2,2),(13,2)],p[4]);line(d,[(2,2),(2,13)],p[4]);
  line(d,[(2,13),(13,13)],p[0]);line(d,[(13,3),(13,13)],p[0]);
  if kind=='brass':
   rect(d,(4,4,11,11),p[3]);rect(d,(5,5,10,10),p[2]);line(d,[(5,5),(10,5)],p[4]);
  else:
   rect(d,(4,4,11,11),p[1]);line(d,[(4,5),(11,5)],p[3]);line(d,[(4,10),(11,10)],p[3]);
  for x,y in ((2,2),(13,2),(2,13),(13,13)):px(d,x,y,p[5])
 else:
  # A polished vanilla metal storage block, NOT an equipment face with bolts.
  rect(d,(0,0,15,15),p[2]);rect(d,(0,0,15,1),p[3]);rect(d,(0,0,1,15),p[3]);
  rect(d,(14,1,15,15),p[1]);rect(d,(1,14,14,15),p[1]);
  rect(d,(3,3,12,12),p[3]);rect(d,(4,4,11,11),p[2]);
  line(d,[(3,3),(11,3)],p[4]);line(d,[(3,3),(3,11)],p[4]);
  line(d,[(4,12),(12,12)],p[1]);line(d,[(12,4),(12,12)],p[1]);
  for x,y,c in ((5,5,3),(6,6,4),(10,8,3),(7,10,1),(2,3,4),(13,12,0)):
   px(d,x,y,p[c])
 return im

def raw_block(m):
 """Dense, uneven raw-material aggregate rather than a perfect tile pattern."""
 p=PALETTES[m];im,d=make();rect(d,(0,0,15,15),p[1]);
 shapes=[
  [(0,1),(3,0),(6,2),(5,5),(2,6),(0,4)],
  [(6,0),(10,0),(11,3),(9,6),(6,5)],
  [(12,0),(15,1),(15,6),(13,7),(11,4)],
  [(0,7),(3,6),(6,8),(5,11),(1,12),(0,10)],
  [(7,6),(10,7),(12,10),(10,13),(7,12),(5,9)],
  [(13,8),(15,7),(15,13),(12,15),(11,12)],
  [(0,13),(2,12),(5,13),(6,15),(0,15)],
  [(7,14),(9,13),(11,15),(8,15)]
 ]
 for index,points in enumerate(shapes):
  poly(d,points,p[0]);
  inset=(index%3)
  for x,y in points[:3]:
   if 0<=x<16 and 0<=y<16: px(d,x,y,p[2+inset])
  bx=sum(x for x,y in points)//len(points);by=sum(y for x,y in points)//len(points)
  px(d,bx,by,p[4]);
  if index%2==0:px(d,max(0,bx-1),by,p[3])
 for x,y in ((2,2),(8,1),(14,4),(3,8),(8,9),(12,10),(4,14)):
  px(d,x,y,p[5])
 return im

def brick(top=False):
 im,d=make();m='#64534a';base='#997869';light='#c5a38b';shade='#866356';hl='#ddbaa0'
 rect(d,(0,0,15,15),m)
 if top:
  rect(d,(1,1,14,14),base)
  for x,y in ((2,2),(9,2),(2,9),(9,9)):
   rect(d,(x,y,x+5,y+5),shade);line(d,[(x,y),(x+5,y)],light);px(d,x+1,y+1,hl);px(d,x+4,y+4,m)
 else:
  for row in range(4):
   y=row*4;offset=0 if row%2==0 else -4
   for x in range(offset,16,8):
    rect(d,(max(0,x+1),y+1,min(15,x+7),y+3),base)
    line(d,[(max(0,x+1),y+1),(min(15,x+6),y+1)],light)
    if x>=0 and x+2<16:px(d,x+2,y+2,hl)
    if x+5<16 and x+5>=0:px(d,x+5,y+3,shade)
 return im

def clay_block():
 im,d=make();rect(d,(0,0,15,15),'#958271')
 for a,c in [((1,2,7,4),'#a69581'),((8,0,14,3),'#b5a18b'),((1,8,6,11),'#8a796c'),((9,7,14,10),'#c5ad93'),((3,13,13,15),'#9f8e7c')]:rect(d,a,c)
 for xy in [(3,5),(12,6),(6,12),(0,11),(14,3)]:px(d,*xy,'#78695f')
 return im

def concrete(plaster=False,top=False):
 im,d=make();base=('#bcb5a4' if plaster else '#6c7476');rect(d,(0,0,15,15),base)
 if not plaster:
  for x,y,w,h,v in [(2,2,6,3,'#848b88'),(10,1,3,4,'#636b6d'),(0,10,7,2,'#5b6569'),(8,11,5,3,'#7e8687'),(3,6,4,1,'#a2a5a0')]:rect(d,(x,y,x+w,y+h),v)
  if top:
   for i in (3,12):line(d,[(i,1),(i,14)],'#48565c');line(d,[(1,i),(14,i)],'#48565c')
   for x in (3,12):
    for y in (3,12):px(d,x,y,'#c0bca6')
 else:
  rect(d,(1,1,14,14),'#c6bfad');rect(d,(2,2,13,13),'#c2bbab');line(d,[(2,2),(12,2)],'#ded4c1');line(d,[(2,12),(13,12)],'#a69f95')
  for x,y in [(4,4),(9,7),(6,11),(12,4)]:px(d,x,y,'#aba899')
 return im

def mesh():
 im,d=make();rect(d,(0,0,15,15),'#1d3337')
 for i in (0,4,8,12,15):line(d,[(i,0),(i,15)],'#779291' if i%8==0 else '#526e71');line(d,[(0,i),(15,i)],'#879b97' if i%8==0 else '#5c777a')
 for x in (2,6,10):
  for y in (2,6,10):rect(d,(x,y,x+1,y+1),'#142a30')
 for x,y in ((0,0),(15,0),(0,15),(15,15)):px(d,x,y,'#a7bbac')
 return im

def port(which):
 fluid='fluid' in which;incoming=which.endswith('in');im,d=make();outer='#252d34';border='#497f8e' if incoming else '#ab7c4e';bright='#6bc6c7' if incoming else '#f0bd5d'
 rect(d,(0,0,15,15),outer);rect(d,(1,1,14,14),'#566b72');rect(d,(2,2,13,13),border);rect(d,(3,3,12,12),'#233640');line(d,[(3,3),(12,3)],'#839a9b');line(d,[(3,4),(3,12)],'#728489')
 for x,y in ((1,1),(14,1),(1,14),(14,14)):px(d,x,y,'#d0d1bc')
 if incoming:
  poly(d,[(7,4),(9,4),(9,8),(12,8),(8,12),(4,8),(7,8)],bright)
  line(d,[(7,5),(7,8)],'#e0eff0')
 else:
  poly(d,[(8,3),(12,7),(9,7),(9,12),(7,12),(7,7),(4,7)],bright)
  line(d,[(8,4),(8,7)],'#fff4b9')
 if fluid:
  px(d,4,4,'#2d8fa4');px(d,11,11,'#356978')
 else:
  px(d,4,11,'#d3985a');px(d,11,4,'#c4a16e')
 return im

def hatch(state):
 im,d=make();p=['#1d2e33','#31434b','#52616b','#829095','#c0c7b8','#e4e9da'];
 rect(d,(0,0,15,15),p[0]);rect(d,(1,1,14,14),p[2]);rect(d,(2,2,13,13),p[1]);rect(d,(3,4,12,12),p[0]);rect(d,(4,5,11,11),'#1a1b1c')
 for x in (5,8,11):line(d,[(x,5),(x,11)],'#57646b' if state=='off' else '#a15d35',2)
 if state=='lit':
  rect(d,(5,7,10,9),'#db6a28');px(d,7,8,'#fff4a0');px(d,9,6,'#e5a453')
 elif state=='assembled':
  line(d,[(4,6),(11,6)],'#7eaaa6')
 else:line(d,[(4,6),(11,6)],'#667f87')
 for x,y in ((2,2),(13,2),(2,13),(13,13)):px(d,x,y,'#b5b7a8')
 return im

def laser_panel(active=False):
 im,d=make();rect(d,(0,0,15,15),'#23333d');rect(d,(1,1,14,14),'#5b6d72');rect(d,(2,2,13,13),'#1c2a32');rect(d,(3,4,12,12),'#273c41')
 line(d,[(4,5),(11,5)],'#819c9f');line(d,[(4,6),(4,11)],'#5e818a');rect(d,(5,8,10,10),'#121f27')
 if active:
  rect(d,(6,6,9,7),'#6ce4eb');line(d,[(6,11),(9,11)],'#3ab9cc');px(d,11,9,'#edfdf2')
 else:
  rect(d,(6,6,9,7),'#456878');line(d,[(6,11),(9,11)],'#41616a')
 for x,y in ((2,2),(13,2),(2,13),(13,13)):px(d,x,y,'#c1b48c')
 return im

def laser_emitter(active):
 im,d=make();rect(d,(0,0,15,15),'#17242c');rect(d,(2,2,13,13),'#354d56');rect(d,(3,3,12,12),'#0e222b');
 rect(d,(5,3,10,6),'#9ca9a6');rect(d,(6,4,9,5),'#536d74')
 line(d,[(7,6),(7,12)],'#2c7480' if not active else '#62eaf4');line(d,[(8,6),(8,12)],'#36657c' if not active else '#c1fbf2')
 line(d,[(4,12),(11,12)],'#729295');px(d,12,4,'#d9b46e');return im

def track():
 im,d=make();rect(d,(0,0,15,15),'#273940')
 for x in (2,12):rect(d,(x,0,x+1,15),'#698384');line(d,[(x,0),(x,15)],'#b4b6aa')
 rect(d,(4,1,11,14),'#1a2b31');line(d,[(6,2),(6,13)],'#4e7576');line(d,[(9,2),(9,13)],'#49646b')
 for y in (2,12):line(d,[(4,y),(11,y)],'#946e4d')
 return im

def laser_warning():
 im,d=make();rect(d,(0,0,15,15),'#494e4d')
 for x in (0,4,8,12):poly(d,[(x,0),(x+2,0),(x,15),(x-2,15)],'#c59a50')
 line(d,[(0,0),(15,0)],'#e5c27c');return im

def molten(m):
 p=PALETTES[m];im,d=make();rect(d,(0,0,15,15),p[2]);
 for y in (0,5,10):line(d,[(0,y+1),(4,y),(8,y+1),(12,y),(15,y+1)],p[3]);line(d,[(1,y+2),(5,y+2),(9,y+3),(14,y+2)],p[1])
 for x,y in ((2,4),(10,2),(12,8),(4,13)):
  line(d,[(x,y),(x+2,y)],p[4]);px(d,x+1,y,p[5])
 return im

def coal():
 im,d=make();poly(d,[(2,5),(6,2),(11,3),(14,7),(12,12),(6,14),(2,10)],'#151c21');poly(d,[(4,5),(7,3),(11,4),(12,8),(7,10),(3,8)],'#293238');poly(d,[(4,5),(6,4),(9,4),(7,6)],'#566066');line(d,[(5,9),(8,11),(11,9)],'#3d494c');return im

# Main material families: item inventory assets are strictly flat pixel art.
for m in materials:
 for n,gen in [('ingot',metal_ingot),('nugget',nugget),('raw',raw),('crushed_raw',crushed)]:
  filename=(m+'_'+n if n in ('ingot','nugget') else ('raw_'+m if n=='raw' else 'crushed_raw_'+m))
  save(gen(m),filename)
 for filename,gen in [(m+'_ore',lambda:ore(m)),('deepslate_'+m+'_ore',lambda:ore(m,True)),('raw_'+m+'_block',lambda:raw_block(m)),('block_of_'+m,lambda:metal_block(PALETTES[m]))]:save(gen(),filename,BLOCK)
# Only specific manufactured metals are registered.
for m in ('pig_iron','plutonium','steel'):
 save(metal_ingot(m),m+'_ingot');save(nugget(m),m+'_nugget');save(metal_block(PALETTES[m]),'block_of_'+m,BLOCK)
save(raw_block('zinc'),'raw_zinc_block',BLOCK)
save(raw_block('aluminium'),'raw_aluminium_block',BLOCK)
save(ore('bauxite'),'bauxite_ore',BLOCK);save(ore('bauxite',True),'deepslate_bauxite_ore',BLOCK)
save(metal_block(PALETTES['aluminium']),'block_of_aluminium',BLOCK)
save(metal_block(PALETTES['uranium']),'block_of_uranium_top',BLOCK)
for m in ('aluminium','copper','gold','iron','lead','nickel','pig_iron','plutonium','silver','steel','tin','uranium','zinc'):
 save(molten(m),'molten_'+m,BLOCK)
save(molten('pig_iron'),'slag_crust',BLOCK)
# Standalone processed materials.
save(pile(PALETTES['bauxite']),'bauxite_powder')
save(pile(('#70675f','#a39f94','#c9c3b1','#e6e1d0','#eee9df','#fcf9ed')),'alumina_powder')
save(pile(('#605a53','#9a9790','#bcbab1','#e4e0d6','#f4f3e7','#ffffff')),'alumina_dust')
save(pile(('#4a463c','#6e6655','#9f9483','#c9bda5','#d7d1bb','#ede6cf')),'impure_silicon_powder')
save(pile(('#4a5a59','#778582','#a7b6b2','#d8dfda','#eaf3eb','#ffffff')),'pure_silicon_powder')
save(coal(),'coke');save(pile(('#343239','#4b4449','#5f5d5d','#8c8078','#ada59a','#cbc1b8')),'slag')
save(silicon_wafer(),'silicon_wafer');save(silicon_wafer(True),'printed_silicon_wafer');save(chip(),'silicon_chip')
save(crushed('silver'),'silicon_crystal') # faceted quartz-like item; replace palette below
save(pile(('#555159','#8c7771','#ae9b8b','#d7c6b3','#e3d7c3','#fbefdf')),'fireclay_ball')
im,d=make()
poly(d,[(2,5),(10,3),(14,5),(14,10),(5,13),(2,11)],'#593c32')
poly(d,[(3,5),(10,4),(13,5),(12,7),(4,9),(2,8)],'#b18a73')
poly(d,[(3,9),(5,10),(5,12),(3,11)],'#775548')
poly(d,[(5,10),(13,7),(13,10),(5,12)],'#986e5d')
line(d,[(4,6),(10,5)],'#dac0a1');px(d,9,9,'#bd9579');px(d,5,11,'#ae8170')
save(im,'fireclay_brick')
save(metal_ingot('aluminium'),'aluminium_ingot');save(nugget('aluminium'),'aluminium_nugget')
save(blade(),'turbine_blade')
# Non-modelled flat aluminium plate.
im,d=make();p=PALETTES['aluminium'];poly(d,[(2,5),(12,3),(15,7),(13,11),(3,13),(1,10)],p[0]);poly(d,[(3,5),(12,4),(14,7),(12,9),(3,11),(2,9)],p[3]);line(d,[(3,6),(12,5)],p[5]);line(d,[(3,11),(12,9)],p[1]);save(im,'aluminium_sheet')
# Auxiliary icons.
im,d=make();rect(d,(3,6,12,13),'#53676b');rect(d,(4,7,11,12),'#87968f');poly(d,[(4,6),(6,2),(9,2),(11,6)],'#a2bbb0');rect(d,(5,2,10,3),'#6b8a88');line(d,[(3,13),(12,13)],'#25363c');save(im,'cooling_tower_icon')
# Convert the special chip/crystal to a cleaner crystalline silhouette.
im,d=make();poly(d,[(7,1),(10,4),(9,10),(6,15),(4,11),(5,5)],'#41535f');poly(d,[(7,2),(9,4),(8,10),(6,13),(5,10),(6,5)],'#bfd2d5');line(d,[(7,2),(7,11)],'#ffffff');poly(d,[(11,7),(14,9),(12,14),(9,12)],'#627f89');poly(d,[(11,8),(13,9),(12,12),(10,11)],'#d3e2dd');save(im,'silicon_crystal')
# Structure textures.
save(clay_block(),'fireclay',BLOCK);save(brick(),'fireclay_bricks',BLOCK);save(brick(True),'fireclay_bricks_top',BLOCK)
save(concrete(),'reinforced_concrete',BLOCK);save(concrete(top=True),'reinforced_concrete_top',BLOCK);save(concrete(plaster=True),'plastered_reinforced_concrete',BLOCK)
save(mesh(),'condensing_mesh',BLOCK)
save(metal_block(['#1d2930','#2d4148','#526972','#778a8d','#a7b5b1','#e0e5d7'],'casing'),'machine_casing',BLOCK)
save(metal_block(['#4c3726','#805c32','#a88043','#d5ad60','#efcb89','#fff0ba'],'brass'),'machine_brass',BLOCK)
for mode in ('item_in','item_out','fluid_in','fluid_out'):save(port(mode),'port_'+mode,BLOCK)
for state,name in [('off','blast_furnace_hatch_front'),('assembled','blast_furnace_hatch_front_assembled'),('lit','blast_furnace_hatch_front_lit')]:save(hatch(state),name,BLOCK)
save(laser_panel(),'laser_front',BLOCK);save(laser_panel(True),'laser_front_active',BLOCK)
save(laser_emitter(False),'laser_emitter',BLOCK);save(laser_emitter(True),'laser_emitter_active',BLOCK);save(track(),'laser_track',BLOCK);save(laser_warning(),'laser_warning',BLOCK)
# Reusable panels for the new hand-modelled Laser Printer.
save(metal_block(['#182932','#2b3d43','#4f666d','#779198','#b2bdbc','#e6e8dd'],'casing'),'laser_side',BLOCK)
save(metal_block(['#374f50','#486c6c','#688f89','#96b4a5','#c9d2ba','#f4eac8'],'brass'),'laser_top',BLOCK)
save(mesh(),'laser_vent',BLOCK)
save(metal_block(['#423221','#70522c','#a17a3a','#cb9d54','#e9be70','#fff0b7'],'brass'),'laser_bearing',BLOCK)
save(metal_block(['#182e35','#274653','#367383','#4aaabb','#8bd8d4','#defbf1'],'casing'),'laser_glass',BLOCK)
# Retain legacy converter art for old-world blocks, but it no longer belongs in new creative/recipes.
save(hatch('off'),'converter_front',BLOCK);save(hatch('lit'),'converter_front_active',BLOCK)
# Atomically update simple Welder material swatches, keeping the UV layout of the original model.
swatches={
 'bolt':('#596772','#8d9997','#c9d4c8'), 'grip':('#1b242c','#39414a','#56616a'),
 'gunmetal':('#334249','#596971','#89999a'),'gunmetal_dark':('#202d34','#39454c','#59686d'),
 'nozzle_black':('#151d26','#26333c','#434b51'),'red':('#6f2927','#b43f33','#df7661'),
 'red_light':('#aa3b2f','#d9604e','#f7a27d'),'rubber':('#1d2229','#30353c','#495158'),
 'steel':('#455866','#81959b','#bec6c0'),'steel_light':('#6b7e84','#a8bab9','#dee7d9'),
 'teal':('#125e70','#258ea1','#52b5b5'),'teal_dark':('#123e4f','#1b6071','#347d83'),
 'teal_highlight':('#318b95','#53b7b8','#8ce1cd'),'teal_mid':('#176d7c','#298c96','#56bbac'),
 'teal_shadow':('#123f50','#205b66','#347781'),
}
for n,tones in swatches.items():
 im,d=make();rect(d,(0,0,15,15),tones[1]);rect(d,(0,0,15,1),tones[2]);rect(d,(0,14,15,15),tones[0]);rect(d,(0,2,1,13),tones[0]);rect(d,(14,2,15,13),tones[2]);save(im,n,WELDER)
# The V23 Welder owns new hand-painted materials and must survive any future
# V20 bulk texture regeneration (rather than quietly reverting to old swatches).
from generate_welder_v23 import paint_welder_textures, PAL as WELDER_V23_MATERIALS
paint_welder_textures()
for name in WELDER_V23_MATERIALS:
    texture_outputs['welder/' + name] = True
# The owner's newer orange Welder is the active item asset. Old teal swatches
# remain for archival compatibility; regenerate both safely.
from generate_welder_orange import paint_welder_textures as paint_orange_welder, PALETTES as ORANGE_WELDER_MATERIALS
paint_orange_welder()
for name in ORANGE_WELDER_MATERIALS:
    texture_outputs['welder/' + name] = True
# Preserve the original user-supplied 16x16 flat icon, never regenerate it from
# the earlier teal sprite generator.
from make_welder_flat_icon import main as restore_orange_welder_icon
restore_orange_welder_icon()
texture_outputs['item/welder_flat'] = True
# Verify no original png was accidentally omitted; report the touched list.
old={p.parent.name+'/'+p.stem for p in ROOT.rglob('*.png')}
unhandled=sorted(old-set(texture_outputs))
if unhandled:raise SystemExit('Unrefreshed textures: '+', '.join(unhandled))
print(f'Generated {len(texture_outputs)} V20 vanilla-compatible 16x16 textures; all existing assets covered, including {len(swatches)} Welder swatches.')
