#!/usr/bin/env python3
"""Generate a true 3-D textured furnace GLB and rendered preview from the
identical 29+1 voxel pattern defined in BlastFurnaceMultiblock.java.

The 4 raised bricks occupy N/E/S/W (not the four corners).
Hatch is at (0, 1, +1); the hollow shaft is at (0, 2, 0).
"""
from pathlib import Path
import numpy as np
from PIL import Image, ImageDraw, ImageFont
import trimesh
from trimesh.visual.texture import TextureVisuals
from trimesh.visual.material import PBRMaterial

ROOT = Path(__file__).resolve().parents[1]
ART = ROOT / 'art/blast_furnace'
TEX = ROOT / 'src/main/resources/assets/createindustrial/textures/block'
ART.mkdir(parents=True, exist_ok=True)

# Entries are (x,y,z) for the actual Minecraft blocks. Furnace front is +Z.
blocks = {}
for y in range(4):
    for x in (-1,0,1):
        for z in (-1,0,1):
            if y == 0:
                blocks[x,y,z] = 'fireclay_bricks'
            elif y == 1:
                blocks[x,y,z] = 'blast_furnace_hatch' if (x,z)==(0,1) else 'fireclay_bricks'
            elif y == 2 and (x,z)!=(0,0):
                blocks[x,y,z] = 'fireclay_bricks'
            elif y == 3 and abs(x)+abs(z)==1:
                blocks[x,y,z] = 'fireclay_bricks'

assert len(blocks)==30
assert sum(v=='fireclay_bricks' for v in blocks.values())==29
assert sum(v=='blast_furnace_hatch' for v in blocks.values())==1
assert {(x,z) for (x,y,z) in blocks if y==3}=={(0,-1),(0,1),(-1,0),(1,0)}
assert (0,2,0) not in blocks and (0,3,0) not in blocks

names=['fireclay_bricks','fireclay_bricks_top','blast_furnace_hatch_front','blast_furnace_hatch_front_assembled']
atlas=Image.new('RGB',(64,16))
for i,n in enumerate(names):
    atlas.paste(Image.open(TEX/f'{n}.png').convert('RGB'),(16*i,0))
atlas.save(ART/'furnace-atlas.png')

# Outward facing vertex order for each cube face.
quads={
    'top': ([(0,1,0),(0,1,1),(1,1,1),(1,1,0)],(0,1,0)),
    'bottom': ([(0,0,0),(1,0,0),(1,0,1),(0,0,1)],(0,-1,0)),
    'front': ([(0,0,1),(1,0,1),(1,1,1),(0,1,1)],(0,0,1)),
    'back': ([(1,0,0),(0,0,0),(0,1,0),(1,1,0)],(0,0,-1)),
    'left': ([(0,0,0),(0,0,1),(0,1,1),(0,1,0)],(-1,0,0)),
    'right': ([(1,0,1),(1,0,0),(1,1,0),(1,1,1)],(1,0,0)),
}

vertices=[];triangles=[];uvs=[];render_faces=[]
for (x,y,z),kind in blocks.items():
    for face,(corners,normal) in quads.items():
        if (x+normal[0],y+normal[1],z+normal[2]) in blocks:
            continue
        tex_id=(1 if face=='top' else (2 if kind=='blast_furnace_hatch' and face=='front' else 0))
        quad=[]
        for ox,oy,oz in corners:
            # Exact 1-meter Minecraft blocks (x,z spread -1..1)
            quad.append(np.array([x+ox-0.5,y+oy,z+oz-0.5],dtype=float))
        idx=len(vertices)
        vertices.extend(quad)
        triangles.extend([(idx,idx+1,idx+2),(idx,idx+2,idx+3)])
        # UV corners sample the correct 16px atlas cell.
        u0=tex_id/4;u1=(tex_id+1)/4
        uvs.extend([(u0,0),(u1,0),(u1,1),(u0,1)])
        render_faces.append((quad,normal,tex_id))

# Every Minecraft block is a separately editable mesh in Blender, including its
# hidden faces, instead of baking the whole multiblock into one solid model.
material=PBRMaterial(baseColorTexture=atlas,metallicFactor=0,roughnessFactor=1,doubleSided=True)
scene=trimesh.Scene()
for (x,y,z),kind in blocks.items():
    verts=[];faces=[];uv=[]
    for side,(corners,normal) in quads.items():
        tex_id=1 if side=='top' else (2 if kind=='blast_furnace_hatch' and side=='front' else 0)
        initial=len(verts)
        verts.extend([(x+ox-0.5,y+oy,z+oz-0.5) for ox,oy,oz in corners])
        faces.extend([(initial,initial+1,initial+2),(initial,initial+2,initial+3)])
        u0=tex_id/4;u1=(tex_id+1)/4
        uv.extend([(u0,0),(u1,0),(u1,1),(u0,1)])
    part=trimesh.Trimesh(vertices=verts,faces=faces,process=False)
    part.visual=TextureVisuals(uv=np.array(uv),material=material)
    scene.add_geometry(part,geom_name=f'{kind}__x{x}_y{y}_z{z}')
scene.export(ART/'blast-furnace-3x3x4.glb')

# Software-rasterized, texture-mapped render: the preview visualizes the same
# cube faces and the exact supplied PNG textures, not an imagined AI image.
W,H=1080,1000
background=np.empty((H,W,3),dtype=np.uint8)
for row in range(H):
    v=int(239 - row / H * 17)
    background[row,:,:]=[v,v+1,v+2]
zbuffer=np.full((H,W),float('inf'),dtype=np.float32)

cam=np.array([7.5,7.5,9.5]); target=np.array([0.,1.6,0.])
forward=target-cam;forward/=np.linalg.norm(forward)
right=np.cross(forward,[0.,1.,0.]);right/=np.linalg.norm(right)
up=np.cross(right,forward);up/=np.linalg.norm(up)
scale=179

def project(pos):
    d=pos-target
    return (np.dot(d,right)*scale + W/2,
            H*.56-np.dot(d,up)*scale,
            np.dot(pos-cam,forward))

tex_data=np.asarray(atlas)
for quad,normal,tex_id in render_faces:
    center=sum(quad)/4
    if np.dot(np.array(normal),cam-center)<0:
        continue
    projected=[project(p) for p in quad]
    # Atlas face coordinates, 0=top row in PIL image.
    source=[(tex_id*16,15),(tex_id*16+15,15),(tex_id*16+15,0),(tex_id*16,0)]
    for ii,jj,kk in [(0,1,2),(0,2,3)]:
        a,b,c=np.array([projected[k][:2] for k in (ii,jj,kk)])
        depths=np.array([projected[k][2] for k in (ii,jj,kk)])
        ua,ub,uc=[np.array(source[k],dtype=float) for k in (ii,jj,kk)]
        xmin=max(0,int(np.floor(min(a[0],b[0],c[0]))));xmax=min(W-1,int(np.ceil(max(a[0],b[0],c[0]))))
        ymin=max(0,int(np.floor(min(a[1],b[1],c[1]))));ymax=min(H-1,int(np.ceil(max(a[1],b[1],c[1]))))
        if xmax<xmin or ymax<ymin:continue
        xs,ys=np.meshgrid(np.arange(xmin,xmax+1),np.arange(ymin,ymax+1))
        area=(b[1]-c[1])*(a[0]-c[0])+(c[0]-b[0])*(a[1]-c[1])
        if abs(area)<1e-8:continue
        w1=((b[1]-c[1])*(xs-c[0])+(c[0]-b[0])*(ys-c[1]))/area
        w2=((c[1]-a[1])*(xs-c[0])+(a[0]-c[0])*(ys-c[1]))/area
        w3=1-w1-w2
        mask=(w1>=-0.0001)&(w2>=-0.0001)&(w3>=-0.0001)
        depth=w1*depths[0]+w2*depths[1]+w3*depths[2]
        current_z=zbuffer[ymin:ymax+1,xmin:xmax+1]
        mask&=(depth<current_z)
        if not np.any(mask):continue
        uu=w1*ua[0]+w2*ub[0]+w3*uc[0]
        vv=w1*ua[1]+w2*ub[1]+w3*uc[1]
        iu=np.clip(np.rint(uu).astype(int),0,63)
        iv=np.clip(np.rint(vv).astype(int),0,15)
        color=tex_data[iv,iu,:].astype(np.float32)
        brightness=1 if normal==(0,1,0) else (0.86 if normal==(1,0,0) else (0.75 if normal==(0,0,1) else 0.7))
        color=np.clip(color*brightness,0,255).astype('uint8')
        dst=background[ymin:ymax+1,xmin:xmax+1]
        dst[mask]=color[mask]
        current_z[mask]=depth[mask]

im=Image.fromarray(background)
draw=ImageDraw.Draw(im)
draw.text((58,45),'CREATE: INDUSTRIAL   /   BLAST FURNACE',fill=(60,58,55),stroke_width=0)
draw.text((58,69),'3 x 3 x 4  |  29 FIRECLAY BRICKS + 1 HATCH',fill=(105,100,98))
im.save(ART/'blast-furnace-preview.png')

# The top-only guide has no perspective ambiguity.
C=75
out=Image.new('RGB',(C*3+40,C*3+100),(245,245,245))
d=ImageDraw.Draw(out)
d.text((20,12),'LAYER 4   /   TOP VIEW',fill=(35,35,35))
for dz,z in enumerate((-1,0,1)):
 for dx,x in enumerate((-1,0,1)):
  start=(20+dx*C,45+dz*C)
  filled=(x,3,z) in blocks
  d.rectangle([start,(start[0]+C-2,start[1]+C-2)],fill=((158,105,97) if filled else (220,221,221)),outline=(107,86,82),width=2)
  if filled:
   small=Image.open(TEX/'fireclay_bricks_top.png').resize((C-6,C-6),resample=Image.Resampling.NEAREST)
   out.paste(small,(start[0]+2,start[1]+2))
  else:
   d.text((start[0]+C//2-8,start[1]+C//2-6),'AIR',fill=(100,100,100))
d.text((20,3*C+60),'Bricks: N / E / S / W     Center + corners: air',fill=(75,75,75))
out.save(ART/'top-layer-corrected.png')
print('Valid block count: 29 fireclay + 1 hatch')
print('Wrote',ART/'blast-furnace-3x3x4.glb')
print('Wrote',ART/'blast-furnace-preview.png')
