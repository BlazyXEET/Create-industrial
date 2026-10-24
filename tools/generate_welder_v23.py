#!/usr/bin/env python3
"""Archived generator for the superseded V23 teal Welder appearance.

Generates the archival V23 teal Minecraft item model and hand-painted 16x16 palette
textures. Also exports an editable Blender-importable GLB when trimesh is
installed (not required by the mod). Run from anywhere with Pillow available:
    python tools/generate_welder_v23.py
This updates only the optional archived teal model, never the active orange model or its selector.
"""
from __future__ import annotations

import json
import math
from pathlib import Path

from PIL import Image, ImageDraw

ROOT = Path(__file__).resolve().parents[1]
ASSET = ROOT / 'src/main/resources/assets/createindustrial'
MODEL = ASSET / 'models/item/welder_v23_teal.json'
TEX = ASSET / 'textures/item/welder'
ART = ROOT / 'art/welder'
TEX.mkdir(parents=True, exist_ok=True)
ART.mkdir(parents=True, exist_ok=True)

# Restrained steel / oxidized teal / aged brass palette inspired by Minecraft's
# material readability, with original rather than copied pixel patterns.
PAL = {
    'teal_body': ('#113d49', '#226d78', '#318b93', '#55aeb5', '#8ccbd0'),
    'teal_panel': ('#164956', '#327888', '#398f97', '#65b9bb', '#a0d0cc'),
    'teal_edge': ('#102f3c', '#265b6b', '#317585', '#63a4b1', '#8fc3c8'),
    'brass': ('#443425', '#795b31', '#af8847', '#d3b36c', '#efd397'),
    'brass_dark': ('#382f2a', '#664b2c', '#94703c', '#b89352', '#d5b877'),
    'steel': ('#323f4b', '#566976', '#7d919b', '#acbec1', '#e0e7de'),
    'steel_light': ('#4d5f68', '#81949b', '#afc2c2', '#d1ddda', '#f2f2e5'),
    'gunmetal': ('#172932', '#293c46', '#415662', '#62747b', '#93a0a0'),
    'gunmetal_dark': ('#101b23', '#1d2b33', '#303c42', '#45535a', '#63737a'),
    'grip': ('#0e1c23', '#1d2d35', '#2e4049', '#475a61', '#66777b'),
    'rubber_rib': ('#101b1f', '#1e2b30', '#2c3a3e', '#45565a', '#657478'),
    'trigger_red': ('#5a282b', '#963c39', '#c65e49', '#eb8a62', '#f4bd8b'),
    'ceramic': ('#48474a', '#a2a09a', '#c6c4b7', '#e2dcc5', '#f5ead6'),
    'vent': ('#111d25', '#202e35', '#33454a', '#536366', '#748187'),
    'indicator': ('#314943', '#7e7742', '#c9aa53', '#e1d080', '#faf0af'),
    'screw': ('#202b33', '#4e5a5e', '#8e9998', '#c9cbba', '#f2e8cf'),
}


def rgba(h: str):
    h = h.removeprefix('#')
    return tuple(int(h[i:i + 2], 16) for i in (0, 2, 4)) + (255,)


def paint_welder_textures():
    """Purposeful 16x16 pixels: cast bevels, brushing, rubber ribs, brass grain."""
    for name, c in PAL.items():
        im = Image.new('RGBA', (16, 16), rgba(c[2]))
        d = ImageDraw.Draw(im)
        # Minecraft-style strong edge value hierarchy, rather than noisy gradients.
        d.rectangle((0, 0, 15, 0), fill=rgba(c[4]))
        d.rectangle((0, 1, 15, 1), fill=rgba(c[3]))
        d.rectangle((0, 14, 15, 15), fill=rgba(c[0]))
        d.line((0, 2, 0, 13), fill=rgba(c[1]))
        d.line((15, 2, 15, 13), fill=rgba(c[3]))
        if name.startswith('teal'):
            d.line((2, 3, 12, 3), fill=rgba(c[3]))
            d.line((2, 12, 11, 12), fill=rgba(c[1]))
            d.line((4, 6, 8, 6), fill=rgba(c[3]))
            d.point((11, 9), fill=rgba(c[1]))
            d.point((12, 9), fill=rgba(c[1]))
        elif name.startswith('brass'):
            d.line((3, 4, 12, 4), fill=rgba(c[3]))
            d.line((4, 10, 13, 10), fill=rgba(c[1]))
            d.line((2, 6, 5, 6), fill=rgba(c[4]))
            d.line((10, 8, 13, 8), fill=rgba(c[3]))
        elif name.startswith('steel'):
            d.line((2, 3, 13, 3), fill=rgba(c[3]))
            d.line((4, 8, 10, 8), fill=rgba(c[1]))
            d.point((11, 5), fill=rgba(c[4]))
        elif name in ('grip', 'rubber_rib'):
            d.rectangle((2, 2, 13, 13), fill=rgba(c[2]))
            for y in (4, 7, 10, 13):
                d.line((3, y, 12, y), fill=rgba(c[0]))
                if y < 13:
                    d.line((3, y + 1, 12, y + 1), fill=rgba(c[3]))
        elif name.startswith('gunmetal'):
            d.line((2, 3, 12, 3), fill=rgba(c[3]))
            d.line((3, 10, 13, 10), fill=rgba(c[1]))
        elif name == 'vent':
            d.rectangle((2, 3, 13, 12), fill=rgba(c[0]))
            for x in (3, 6, 9, 12):
                d.line((x, 4, x, 11), fill=rgba(c[2]))
                d.point((x, 4), fill=rgba(c[3]))
        elif name == 'screw':
            d.ellipse((3, 3, 12, 12), fill=rgba(c[3]), outline=rgba(c[0]))
            d.line((6, 6, 9, 9), fill=rgba(c[1]))
            d.line((6, 9, 9, 6), fill=rgba(c[1]))
        elif name == 'trigger_red':
            d.line((3, 3, 13, 3), fill=rgba(c[4]))
            d.line((2, 10, 12, 10), fill=rgba(c[1]))
        elif name == 'indicator':
            d.rectangle((3, 3, 12, 12), fill=rgba(c[2]))
            d.rectangle((5, 5, 10, 9), fill=rgba(c[4]))
            d.line((5, 10, 10, 10), fill=rgba(c[1]))
        elif name == 'ceramic':
            d.line((2, 4, 12, 4), fill=rgba(c[4]))
            d.line((3, 12, 13, 12), fill=rgba(c[1]))
        im.save(TEX / f'{name}.png', optimize=True)
    return len(PAL)


parts = []


def box(name, p1, p2, material, *, rotation=None, faces=None):
    assert material in PAL, (name, material)
    assert all(p1[a] < p2[a] for a in range(3)), name
    data = {'name': name, 'from': list(p1), 'to': list(p2)}
    if rotation is not None:
        origin, angle = rotation
        assert angle in (-45, -22.5, 0, 22.5, 45)
        data['rotation'] = {'origin': origin, 'axis': 'z', 'angle': angle, 'rescale': False}
    uv_faces = {}
    for d in ('north', 'south', 'east', 'west', 'up', 'down'):
        chosen = (faces or {}).get(d, material)
        assert chosen in PAL
        # Pixel-space UV scales with cuboid dimensions, avoiding textures that
        # stretch one pixel into a long, noisy strip. Keep within 16x16 atlas.
        dx = p2[0] - p1[0]
        dy = p2[1] - p1[1]
        dz = p2[2] - p1[2]
        w, h = ((dx, dy) if d in ('north', 'south') else
                (dz, dy) if d in ('east', 'west') else (dx, dz))
        w = max(0.1, min(16.0, w))
        h = max(0.1, min(16.0, h))
        # For shallow elements, center the sampled pixels around the middle of
        # the tile, where the authored surface pattern is designed to live.
        u0 = round((16 - w) / 2, 3)
        v0 = round((16 - h) / 2, 3)
        uv_faces[d] = {'uv': [u0, v0, round(u0 + w, 3), round(v0 + h, 3)], 'texture': f'#{chosen}'}
    data['faces'] = uv_faces
    parts.append(data)


# Opposite the nozzle is the palm grip. X runs from weld tip (-X) to rear (+X).
# Z is thickness; Y is vertical. This orientation keeps vanilla hand transforms.
# True layered silhouette: uninterrupted rectangular housing, forearm-like torch
# nose, open trigger guard and distinct angled rubber handle.
box('Internal machined dark-metal chassis', (4.6, 8.05, 6.45), (16.45, 10.6, 9.55), 'gunmetal_dark')
box('Upper teal forged shell', (5.15, 9.05, 6.23), (15.55, 11.1, 9.77), 'teal_body', faces={'up': 'teal_panel'})
box('Lower teal reinforced shell', (5.35, 8.02, 6.46), (15.7, 9.2, 9.54), 'teal_edge')
box('Left removable teal side plate', (6.08, 8.55, 6.06), (14.65, 10.65, 6.27), 'teal_panel')
box('Right removable teal side plate', (6.08, 8.55, 9.73), (14.65, 10.65, 9.94), 'teal_panel')
box('Chassis upper spine', (4.75, 10.98, 6.76), (16.17, 11.39, 9.23), 'teal_edge')
box('Upper steel spine insert', (7.1, 11.38, 7.52), (14.2, 11.62, 8.48), 'steel')
box('Aged brass rear sleeve', (14.9, 8.4, 6.13), (16.23, 11.18, 9.86), 'brass_dark')
box('Rear teal service cap', (16.2, 8.18, 6.4), (17.3, 11.25, 9.6), 'teal_body')
box('Rear rubber impact bumper', (17.25, 8.55, 6.76), (17.63, 10.92, 9.24), 'grip')
box('Brass upper front coupling seam', (4.8, 8.65, 6.26), (5.35, 10.88, 9.74), 'brass')
box('Tapered nozzle housing dark core', (2.7, 8.85, 6.9), (4.92, 10.5, 9.1), 'gunmetal')
box('Front matte teal tapered housing', (3.03, 9.08, 6.56), (5.09, 10.56, 9.44), 'teal_body')
box('Front underside rib', (3.08, 8.76, 7.11), (5.22, 9.11, 8.89), 'teal_edge')
box('Metal nozzle mounting ring', (2.28, 9.16, 7.15), (3.12, 10.42, 8.85), 'brass')
box('Machined neck straight', (0.64, 9.4, 7.64), (2.45, 10.14, 8.36), 'steel')
box('Neck shadow core', (-0.6, 9.49, 7.77), (0.93, 10.07, 8.23), 'gunmetal_dark')
# All of the angled head shares ONE rotation origin to prevent seams when
# Minecraft applies the 22.5-degree item element rotation.
NOZZLE = ([0.6, 9.78, 8.0], 22.5)
box('Angled torch barrel', (-2.02, 9.36, 7.67), (0.76, 10.12, 8.33), 'gunmetal', rotation=NOZZLE)
box('Angled steel reinforcement', (-1.48, 9.49, 7.59), (-0.92, 10.04, 8.4), 'steel', rotation=NOZZLE)
box('Angled brass focus ring', (-2.35, 9.24, 7.52), (-1.78, 10.22, 8.48), 'brass', rotation=NOZZLE)
box('Angled graphite extension', (-3.15, 9.5, 7.75), (-2.28, 9.98, 8.25), 'gunmetal_dark', rotation=NOZZLE)
box('Heat-resistant pale ceramic tip', (-3.42, 9.46, 7.67), (-3.05, 10.02, 8.33), 'ceramic', rotation=NOZZLE)
box('Black torch opening', (-3.47, 9.59, 7.82), (-3.42, 9.91, 8.18), 'vent', rotation=NOZZLE)
# Side-plate structure: put seams and brass strips on both sides (not one-sided).
for side, z, start in [('left', 5.96, 6.0), ('right', 9.94, 9.94)]:
    zplate = (z, z + 0.12)
    box(f'{side} brass side trim upper', (6.05, 10.67, zplate[0]), (14.65, 10.85, zplate[1]), 'brass_dark')
    box(f'{side} dark side lower groove', (6.4, 8.37, zplate[0]), (14.25, 8.57, zplate[1]), 'gunmetal_dark')
    box(f'{side} rear mechanical plate', (12.78, 9.03, zplate[0]), (14.28, 9.83, zplate[1]), 'gunmetal')
    for x in (6.56, 13.82):
        box(f'{side} countersunk service screw {x}', (x, 9.68, zplate[0] - .14), (x + .38, 10.03, zplate[1] + .14), 'screw')
# Tiny detailed top vent cluster, appropriately subdued and mechanical.
box('Raised charcoal ventilation bezel', (10.1, 11.34, 6.82), (14.45, 11.57, 9.15), 'gunmetal_dark')
for j, x in enumerate((10.46, 11.54, 12.62, 13.70), 1):
    box(f'Vent slot {j}', (x, 11.54, 7.07), (x + .47, 11.65, 8.94), 'vent')
box('Brass top control mount', (7.65, 11.35, 7.02), (8.95, 11.57, 8.98), 'brass_dark')
box('Raised black rocker switch', (7.94, 11.54, 7.36), (8.65, 11.92, 8.64), 'grip')
box('Status inset rim', (15.25, 11.25, 7.28), (16.2, 11.47, 8.72), 'gunmetal_dark')
box('Status amber glass', (15.48, 11.46, 7.58), (15.96, 11.59, 8.41), 'indicator')
# Anatomical palm grip (not a featureless 3D brick). The entire handle and
# individual grooves rotate around one pivot, forming a slight rearward rake.
HANDLE = ([12.8, 8.5, 8.0], 22.5)
box('Handle collar under frame', (11.02, 7.88, 6.54), (15.11, 8.59, 9.46), 'brass_dark')
box('Angled steel grip internal frame', (11.55, 3.42, 6.99), (14.2, 8.26, 9.01), 'gunmetal_dark', rotation=HANDLE)
box('Angled ergonomic black rubber grip', (11.31, 3.65, 6.74), (14.29, 7.9, 9.26), 'grip', rotation=HANDLE)
box('Palm strap left', (11.27, 4.0, 6.60), (14.2, 7.5, 6.79), 'rubber_rib', rotation=HANDLE)
box('Palm strap right', (11.27, 4.0, 9.21), (14.2, 7.5, 9.40), 'rubber_rib', rotation=HANDLE)
for i, y in enumerate((4.12, 4.88, 5.64, 6.40), 1):
    box(f'Raised anti-slip grip band {i}', (11.15, y, 6.53), (14.36, y + .27, 9.47), 'rubber_rib', rotation=HANDLE)
box('Rubber padded handle butt', (11.1, 3.16, 6.61), (14.35, 3.76, 9.39), 'gunmetal', rotation=HANDLE)
box('Handle heel brass service stud', (11.83, 3.03, 7.36), (13.72, 3.19, 8.64), 'brass_dark', rotation=HANDLE)
# Red mechanical trigger inside deliberately OPEN trigger guard.
box('Trigger inner pivot', (9.73, 7.34, 7.1), (10.64, 8.2, 8.9), 'gunmetal_dark')
box('Red release trigger', (9.97, 6.25, 7.42), (10.58, 7.73, 8.58), 'trigger_red', rotation=([10.36, 7.47, 8], -22.5))
box('Trigger red tip highlight', (10.17, 6.31, 7.51), (10.58, 6.64, 8.5), 'trigger_red')
box('Trigger guard front vertical', (8.83, 5.58, 7.18), (9.22, 8.1, 8.82), 'gunmetal')
box('Trigger guard underside', (8.85, 5.55, 7.2), (12.1, 5.95, 8.8), 'gunmetal')
box('Trigger guard rear', (11.75, 5.58, 7.25), (12.1, 6.62, 8.75), 'gunmetal')
# Final small geometric details: useful seams and touch points, not noisy greebles.
box('Front left anti-scuff strip', (3.37, 9.46, 6.37), (4.67, 9.72, 6.57), 'brass')
box('Front right anti-scuff strip', (3.37, 9.46, 9.43), (4.67, 9.72, 9.63), 'brass')
box('Back top machined chamfer', (15.58, 11.15, 6.56), (16.6, 11.42, 9.44), 'steel')


def json_model():
    return {
        '__comment': 'Create: Industrial V23 Welder. Source: tools/generate_welder_v23.py. Authoritative actual Minecraft item geometry, not a render.',
        'gui_light': 'front',
        'ambientocclusion': True,
        'textures': {**{k: f'createindustrial:item/welder/{k}' for k in PAL}, 'particle': 'createindustrial:item/welder/teal_body'},
        'elements': parts,
        'display': {
            'gui': {'rotation': [18, 30, -22], 'translation': [1.3, -0.25, 0], 'scale': [.70, .70, .70]},
            'ground': {'rotation': [0, 10, 0], 'translation': [2.1, 2.1, 0], 'scale': [.62, .62, .62]},
            'fixed': {'rotation': [0, 180, 0], 'translation': [1.2, .45, 0], 'scale': [.61, .61, .61]},
            'firstperson_righthand': {'rotation': [-16, -90, -29], 'translation': [0.5, 3.3, 0.8], 'scale': [.80, .80, .80]},
            'firstperson_lefthand': {'rotation': [-16, 90, 29], 'translation': [0.5, 3.3, 0.8], 'scale': [.80, .80, .80]},
            'thirdperson_righthand': {'rotation': [-14, -90, -38], 'translation': [0.7, 3.1, 0.4], 'scale': [.80, .80, .80]},
            'thirdperson_lefthand': {'rotation': [-14, 90, 38], 'translation': [0.7, 3.1, 0.4], 'scale': [.80, .80, .80]},
            'head': {'rotation': [0, 180, 0], 'translation': [0, 4.5, 0], 'scale': [.67, .67, .67]},
        },
    }


def export_blender_importable_glb():
    """Export the SAME cuboids with the real 16x16 PNGs embedded into the GLB.

    Blender imports the GLB as separate named meshes with editable, referenced
    pixel-art textures. This is a modeling source, NOT what Minecraft loads.
    """
    try:
        import numpy as np
        import trimesh
    except ImportError:
        print('Skipped optional Blender GLB: trimesh or numpy missing.')
        return None
    scene = trimesh.Scene()
    materials = {
        name: trimesh.visual.material.PBRMaterial(
            name=f'createindustrial_welder_{name}',
            baseColorTexture=Image.open(TEX / f'{name}.png').convert('RGBA'),
            metallicFactor=0.0,
            roughnessFactor=1.0,
            alphaMode='OPAQUE',
        )
        for name in PAL
    }
    face_quads = {
        'north': lambda x0, y0, z0, x1, y1, z1: [(x0,y0,z0),(x0,y1,z0),(x1,y1,z0),(x1,y0,z0)],
        'south': lambda x0, y0, z0, x1, y1, z1: [(x0,y0,z1),(x1,y0,z1),(x1,y1,z1),(x0,y1,z1)],
        'east': lambda x0, y0, z0, x1, y1, z1: [(x1,y0,z0),(x1,y1,z0),(x1,y1,z1),(x1,y0,z1)],
        'west': lambda x0, y0, z0, x1, y1, z1: [(x0,y0,z0),(x0,y0,z1),(x0,y1,z1),(x0,y1,z0)],
        'up': lambda x0, y0, z0, x1, y1, z1: [(x0,y1,z0),(x0,y1,z1),(x1,y1,z1),(x1,y1,z0)],
        'down': lambda x0, y0, z0, x1, y1, z1: [(x0,y0,z0),(x1,y0,z0),(x1,y0,z1),(x0,y0,z1)],
    }
    for i, part in enumerate(parts):
        p1 = part['from']
        p2 = part['to']
        x0,y0,z0 = p1
        x1,y1,z1 = p2
        groups = {}
        for face, generate in face_quads.items():
            data = part['faces'][face]
            mat = data['texture'][1:]
            group = groups.setdefault(mat, {'vertices': [], 'uv': [], 'triangles': []})
            quad = generate(x0,y0,z0,x1,y1,z1)
            uv0, vv0, uv1, vv1 = data['uv']
            # GLB UV's origin is bottom left, Minecraft's is top left.
            coords = [
                (uv0/16.0, 1-vv1/16.0),
                (uv1/16.0, 1-vv1/16.0),
                (uv1/16.0, 1-vv0/16.0),
                (uv0/16.0, 1-vv0/16.0),
            ]
            offset = len(group['vertices'])
            group['vertices'].extend(quad)
            group['uv'].extend(coords)
            group['triangles'].extend([(offset,offset+1,offset+2),(offset,offset+2,offset+3)])
        for mat_name, values in groups.items():
            mesh = trimesh.Trimesh(vertices=values['vertices'], faces=values['triangles'], process=False)
            r = part.get('rotation')
            if r:
                transform = trimesh.transformations.rotation_matrix(
                    math.radians(r['angle']), [0, 0, 1], r['origin'])
                mesh.apply_transform(transform)
            mesh.apply_translation([-8,-8,-8])
            mesh.apply_scale(1/16.0)
            mesh.visual = trimesh.visual.texture.TextureVisuals(
                uv=np.array(values['uv'], dtype=float), material=materials[mat_name])
            scene.add_geometry(mesh, geom_name=f'{i:02d} {part["name"]} [{mat_name}]')
    out = ART / 'welder-v23-create-industrial.glb'
    scene.export(out)
    return out


def main():
    count = paint_welder_textures()
    # Never overwrite models/item/welder.json: that file chooses 2D or 3D.
    MODEL.write_text(json.dumps(json_model(), indent=2) + '\n', encoding='utf-8')
    glb = export_blender_importable_glb()
    print(f'Generated {len(parts)} cuboids; {count} original 16x16 textures; Minecraft model: {MODEL}')
    if glb:
        print(f'Blender-importable GLB: {glb}')


if __name__ == '__main__':
    main()
