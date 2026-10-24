#!/usr/bin/env python3
"""Rebuild the orange-and-graphite Welder from the owner's 24 Oct reference.

Visual only: generates Minecraft item JSON, 16x16 swatch textures, and an
optional Blender-importable GLB. Does not modify model selection or Java logic.
"""
from __future__ import annotations

import json
import math
from pathlib import Path
from PIL import Image, ImageDraw

ROOT = Path(__file__).resolve().parents[1]
ASSETS = ROOT / 'src/main/resources/assets/createindustrial'
MODEL = ASSETS / 'models/item/welder_3d.json'
TEX = ASSETS / 'textures/item/welder'
ART = ROOT / 'art/welder'

# Real, limited pixel-art palettes based on the supplied model image.  The
# tool's rectangular orange grip and graphite horizontal body are intentional.
PALETTES = {
    'orange_grip': ('#5a1507', '#8d2709', '#cf4204', '#f47d06', '#ffa936'),
    'orange_front': ('#75210a', '#ad3105', '#ec5c03', '#ff8a0e', '#ffc15b'),
    'orange_edge': ('#471408', '#712009', '#a32a05', '#d84705', '#f46f0d'),
    'orange_top': ('#38140f', '#671d11', '#8e260e', '#b63b0a', '#dc580a'),
    'graphite': ('#080b10', '#11141c', '#1d222d', '#303645', '#4b5260'),
    'graphite_dark': ('#05070b', '#0a0b10', '#12151c', '#222634', '#383c4a'),
    'graphite_lip': ('#0a0d13', '#151924', '#222939', '#323c4b', '#515968'),
    'steel_vent': ('#161c27', '#353c4b', '#545d6e', '#747c8b', '#9298a3'),
    'muzzle_steel': ('#59616c', '#808994', '#aeb4bd', '#d5d8d9', '#f1f1eb'),
    'muzzle_tip': ('#858a8d', '#a8afb4', '#d0d4d5', '#ededec', '#ffffff'),
    'rear_lever': ('#090d12', '#181c23', '#2b303a', '#464d5a', '#636a76'),
    'handle_shadow': ('#3e140c', '#671c0a', '#91250a', '#ad320a', '#cd4b11'),
}


def rgba(h):
    return tuple(int(h[i:i+2], 16) for i in (1,3,5)) + (255,)


def paint_welder_textures():
    TEX.mkdir(parents=True, exist_ok=True)
    for name, palette in PALETTES.items():
        im = Image.new('RGBA', (16,16), rgba(palette[2]))
        d = ImageDraw.Draw(im)
        # Pixel clusters, not gradients: Minecraft-like highlights and edging.
        d.rectangle((0,0,15,1), fill=rgba(palette[4]))
        d.rectangle((0,13,15,15), fill=rgba(palette[0]))
        d.rectangle((0,2,1,12), fill=rgba(palette[1]))
        d.rectangle((14,2,15,12), fill=rgba(palette[3]))
        if name in ('orange_grip','orange_front','orange_edge'):
            # The reference has a broad orange highlight along the middle of
            # its rectangular body and a crisp pale edge, not noisy speckles.
            d.polygon([(7,2),(10,2),(11,5),(10,12),(8,12),(7,9)], fill=rgba(palette[3]))
            d.polygon([(9,3),(11,3),(11,9),(10,11),(9,11)], fill=rgba(palette[4]))
            d.line((3,3,3,11), fill=rgba(palette[1]))
            d.line((5,12,12,12), fill=rgba(palette[1]))
        elif name == 'orange_top':
            d.rectangle((2,2,13,5), fill=rgba(palette[1]))
            d.line((3,5,12,5), fill=rgba(palette[3]))
        elif name.startswith('graphite') or name == 'rear_lever':
            d.rectangle((2,3,13,5), fill=rgba(palette[1]))
            d.line((4,3,11,3), fill=rgba(palette[3]))
            d.line((3,11,12,11), fill=rgba(palette[1]))
        elif name == 'steel_vent':
            d.rectangle((2,3,13,12), fill=rgba(palette[1]))
            for x in (4,7,10,13):
                d.line((x,4,x,10), fill=rgba(palette[3]))
                d.point((x,11), fill=rgba(palette[0]))
        elif name.startswith('muzzle'):
            d.rectangle((2,2,13,5), fill=rgba(palette[3]))
            d.rectangle((3,9,12,12), fill=rgba(palette[1]))
            d.line((3,2,13,2), fill=rgba(palette[4]))
        im.save(TEX/f'{name}.png', optimize=True)
    return len(PALETTES)


PARTS=[]
FACES=('north','south','east','west','up','down')


def box(name, p0, p1, mat, *, rotation=None, per_face=None, full_uv_faces=()):
    if mat not in PALETTES:
        raise ValueError(mat)
    assert all(a<b for a,b in zip(p0,p1)),name
    part={'name':name,'from':list(p0),'to':list(p1)}
    if rotation:
        origin, angle=rotation
        assert angle in (-45,-22.5,0,22.5,45)
        part['rotation']={'origin':origin,'axis':'z','angle':angle,'rescale':False}
    faces={}
    for face in FACES:
        material=(per_face or {}).get(face,mat)
        assert material in PALETTES,(name, material)
        dx,dy,dz=[p1[i]-p0[i] for i in range(3)]
        w,h=((dx,dy) if face in ('north','south') else
             (dz,dy) if face in ('east','west') else (dx,dz))
        if face in full_uv_faces:
            uv=[0,0,16,16]
        else:
            w=max(0.1,min(16,w)); h=max(0.1,min(16,h))
            u=round((16-w)/2,3);v=round((16-h)/2,3)
            uv=[u,v,round(u+w,3),round(v+h,3)]
        faces[face]={'uv':uv,'texture':'#'+material}
    part['faces']=faces
    PARTS.append(part)


# +X is the rear of the tool, -X the bright silver nozzle, Y is vertical.
# This intentionally follows the owner's simple pixel-art silhouette, not
# the busier teal gun-style V23 design.  Nozzles stay horizontal in this rig.
# The lower orange section is the palm grip, directly under the top shell.
box('Orange handle - solid rectangular core', (7.12,1.75,6.25),(13.12,11.05,9.75),'orange_grip',
    per_face={'west':'orange_edge','east':'orange_edge','up':'orange_top','down':'handle_shadow'},
    full_uv_faces=('north','south'))
box('Orange handle - near bevel', (7.04,2.12,6.02),(7.46,10.85,6.27),'orange_edge')
box('Orange handle - far bevel', (12.79,2.10,9.73),(13.2,10.78,9.97),'orange_edge')
box('Orange grip - lower shadow cap', (7.22,1.5,6.16),(13.01,2.18,9.84),'handle_shadow')
box('Orange grip - upper burnt collar', (6.94,10.26,6.09),(13.34,11.31,9.91),'orange_top')
box('Orange grip - vertical front glint', (11.23,3.65,6.006),(11.72,9.73,6.024),'orange_front')
box('Orange grip - small diagonal highlight', (9.74,3.05,6.008),(10.86,4.26,6.028),'orange_front')
box('Orange grip - lower warm bevel', (7.41,2.28,6.0),(12.89,2.68,6.045),'orange_edge')

# Dark horizontal welder upper bar with small vents, beveled plates and an
# unambiguous left-facing industrial nozzle. All parts remain Minecraft cubes.
box('Graphite head - internal lower housing', (3.95,10.80,5.84),(17.26,12.25,10.16),'graphite')
box('Graphite head - broad upper shell', (4.18,12.11,5.57),(17.32,13.68,10.43),'graphite_dark',
    per_face={'up':'graphite','north':'graphite_dark','south':'graphite_dark'})
box('Graphite head - top chamfer', (5.12,13.65,5.83),(16.75,13.88,10.17),'graphite_lip')
box('Graphite head - bottom lip', (5.09,10.63,5.67),(16.52,11.06,10.32),'graphite_lip')
box('Graphite head - short front cuff', (3.8,11.10,6.45),(5.6,13.13,9.55),'graphite')
box('Graphite head - rear cap', (16.83,11.04,5.90),(17.56,13.50,10.09),'graphite_lip')
# Far and near side gray bars, with subtle individual separator notches.
for side,z in [('near',5.51),('far',10.43)]:
    box(f'{side} dark vent inset', (7.15,11.62,z),(14.82,12.85,z+.13),'graphite_lip')
    box(f'{side} steel vent strip', (7.47,11.79,z-.045),(14.47,12.60,z+.18),'steel_vent')
    for i,x in enumerate((8.55,10.28,12.04,13.69),1):
        box(f'{side} vent divider {i}', (x,11.74,z-.063),(x+.16,12.66,z+.19),'graphite_dark')
# Silver / white stepped nozzle on LEFT. It is intentionally shorter and
# simpler than the V23 tapered blue welding gun.
box('Nozzle graphite shoulder', (2.95,11.46,6.91),(4.31,13.08,9.09),'graphite')
box('Nozzle steel shaft', (-.38,11.66,7.04),(3.17,12.91,8.96),'muzzle_steel')
box('Nozzle bright broad tip', (-1.98,11.50,6.94),(-.24,13.01,9.06),'muzzle_tip')
box('Nozzle front polished face', (-2.03,11.71,7.14),(-1.98,12.83,8.85),'muzzle_tip')
box('Nozzle top silver facet', (-.29,12.90,7.26),(2.70,13.015,8.74),'muzzle_tip')
box('Nozzle underside seam', (-.25,11.58,7.34),(2.63,11.69,8.65),'muzzle_steel')
# The rear hook / lever makes the back side unmistakable. Rotations use only
# angles supported by Minecraft JSON item element rotations.
HOOK=([17.36,11.76,8.0],45)
box('Rear angled graphite lever', (17.15,11.13,7.19),(20.12,12.13,8.82),'rear_lever',rotation=HOOK)
box('Rear lever raised end', (19.62,11.03,7.10),(20.15,12.28,8.89),'graphite_dark',rotation=HOOK)
box('Rear trigger hinge', (16.58,10.56,7.29),(17.89,11.20,8.71),'graphite_lip')
box('Rear trigger paddle', (17.42,9.55,7.30),(18.48,10.78,8.7),'rear_lever')
box('Rear underside black tab', (16.78,9.30,7.50),(17.43,10.68,8.50),'graphite_dark')


def minecraft_model():
    return {
        '__comment':'Orange reference Welder. Generator: tools/generate_welder_orange.py. Cosmetic only; Java welding logic unchanged.',
        'gui_light':'front',
        'ambientocclusion':True,
        'textures':{**{k:'createindustrial:item/welder/'+k for k in PALETTES},'particle':'createindustrial:item/welder/orange_grip'},
        'elements':PARTS,
        'display':{
            'gui':{'rotation':[17,27,-28],'translation':[.6,-.1,0],'scale':[.66,.66,.66]},
            'ground':{'rotation':[0,15,0],'translation':[1.2,2.25,0],'scale':[.65,.65,.65]},
            'fixed':{'rotation':[0,180,0],'translation':[.5,.45,0],'scale':[.62,.62,.62]},
            'firstperson_righthand':{'rotation':[-13,-90,-29],'translation':[.2,3.5,.7],'scale':[.76,.76,.76]},
            'firstperson_lefthand':{'rotation':[-13,90,29],'translation':[.2,3.5,.7],'scale':[.76,.76,.76]},
            'thirdperson_righthand':{'rotation':[-12,-90,-34],'translation':[.5,3.0,.2],'scale':[.76,.76,.76]},
            'thirdperson_lefthand':{'rotation':[-12,90,34],'translation':[.5,3.0,.2],'scale':[.76,.76,.76]},
            'head':{'rotation':[0,180,0],'translation':[0,4.2,0],'scale':[.65,.65,.65]},
        },
    }


def export_blender_glb():
    """Editable meshes with original swatch textures embedded; Blender not required."""
    try:
        import trimesh
        import numpy as np
    except ImportError:
        print('Optional GLB not generated (trimesh/numpy unavailable).')
        return None
    ART.mkdir(parents=True,exist_ok=True)
    scene=trimesh.Scene()
    mats={name:trimesh.visual.material.PBRMaterial(name='welder_'+name,
        baseColorTexture=Image.open(TEX/f'{name}.png').convert('RGBA'),
        metallicFactor=0.0,roughnessFactor=1.0,alphaMode='OPAQUE')
        for name in PALETTES}
    quads={
        'north':lambda x,y,z,X,Y,Z:[(x,y,z),(x,Y,z),(X,Y,z),(X,y,z)],
        'south':lambda x,y,z,X,Y,Z:[(x,y,Z),(X,y,Z),(X,Y,Z),(x,Y,Z)],
        'east':lambda x,y,z,X,Y,Z:[(X,y,z),(X,Y,z),(X,Y,Z),(X,y,Z)],
        'west':lambda x,y,z,X,Y,Z:[(x,y,z),(x,y,Z),(x,Y,Z),(x,Y,z)],
        'up':lambda x,y,z,X,Y,Z:[(x,Y,z),(x,Y,Z),(X,Y,Z),(X,Y,z)],
        'down':lambda x,y,z,X,Y,Z:[(x,y,z),(X,y,z),(X,y,Z),(x,y,Z)],
    }
    for i,part in enumerate(PARTS):
        groups={}
        for face,maker in quads.items():
            data=part['faces'][face]
            mat=data['texture'][1:]
            values=groups.setdefault(mat,{'v':[],'uv':[],'f':[]})
            quad=maker(*part['from'],*part['to'])
            u,v,U,V=data['uv']
            coord=[(u/16,1-V/16),(U/16,1-V/16),(U/16,1-v/16),(u/16,1-v/16)]
            off=len(values['v'])
            values['v'].extend(quad);values['uv'].extend(coord)
            values['f'].extend([(off,off+1,off+2),(off,off+2,off+3)])
        for material,values in groups.items():
            mesh=trimesh.Trimesh(vertices=values['v'],faces=values['f'],process=False)
            r=part.get('rotation')
            if r:
                mesh.apply_transform(trimesh.transformations.rotation_matrix(
                    math.radians(r['angle']),[0,0,1],r['origin']))
            mesh.apply_translation([-8,-8,-8]);mesh.apply_scale(1/16)
            mesh.visual=trimesh.visual.texture.TextureVisuals(
                uv=np.asarray(values['uv'],float),material=mats[material])
            scene.add_geometry(mesh,geom_name=f'{i:02d} {part["name"]} [{material}]')
    out=ART/'welder-orange-reference.glb'
    scene.export(out)
    return out


def main():
    ART.mkdir(parents=True,exist_ok=True)
    count=paint_welder_textures()
    MODEL.parent.mkdir(parents=True,exist_ok=True)
    MODEL.write_text(json.dumps(minecraft_model(),indent=2)+'\n',encoding='utf-8')
    output=export_blender_glb()
    print(f'Orange Welder: {len(PARTS)} Minecraft parts; {count} textures; {MODEL}')
    if output:print(f'Blender-importable textured model: {output}')


if __name__=='__main__': main()
