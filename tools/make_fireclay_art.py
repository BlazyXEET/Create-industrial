#!/usr/bin/env python3
"""Author-controlled 16px texture study: a restricted refractory-clay palette, brick
courses laid by hand, purposeful chipped edges, and a cut-out hatch grille.
Reproduces the PNG files shipped in assets; runtime does not require Python.
"""
from pathlib import Path
from PIL import Image

ASSETS = Path(__file__).resolve().parents[1] / 'src/main/resources/assets/createindustrial/textures/block'
ASSETS.mkdir(parents=True, exist_ok=True)

PALETTE = [
    (151, 101, 92), (165, 114, 107), (138, 93, 88),
    (175, 122, 113), (123, 82, 78), (155, 105, 103),
]
MORTAR = (120, 108, 105)
MORTAR_LIGHT = (171, 154, 147)


def shade(color, amount):
    return tuple(max(0, min(255, v + amount)) for v in color)


def brick_face(variant=0):
    im = Image.new('RGB', (16, 16), MORTAR)
    pix = im.load()
    # Four low courses, eight-pixel stretchers, staggered joints.
    offsets = (0, 4, 0, 4) if variant == 0 else (2, 6, 2, 6)
    for y in range(16):
        row = y // 4
        inside = y % 4
        for x in range(16):
            joint = (x + offsets[row]) % 8
            if inside == 0:
                pix[x, y] = MORTAR_LIGHT if (x + row) % 4 != 0 else MORTAR
                continue
            if joint == 0:
                pix[x, y] = MORTAR if inside == 3 else MORTAR_LIGHT
                continue
            brick = ((x + offsets[row]) // 8 + row * 3 + variant) % len(PALETTE)
            color = PALETTE[brick]
            if inside == 1: color = shade(color, 13)
            elif inside == 3: color = shade(color, -17)
            if joint == 1: color = shade(color, -7)
            if joint == 7: color = shade(color, 9)
            pix[x, y] = color
    # Sparse hand-positioned fireclay flecks. No noise texture/filter.
    marks = ((2, 2), (11, 3), (7, 6), (13, 7), (3, 10), (9, 11), (5, 14))
    for j, (x, y) in enumerate(marks):
        x = (x + variant) % 16
        if pix[x, y] not in (MORTAR, MORTAR_LIGHT):
            pix[x, y] = shade(pix[x, y], (15 if j % 2 == 0 else -17))
    return im


def hatch_face(assembled=False):
    image = brick_face(0)
    p = image.load()
    # Deep, chamfered rectangular port, riveted into the fireclay face.
    outline = (48, 45, 46)
    edge = (88, 78, 74)
    inside = (19, 20, 22)
    for y in range(4, 14):
        xmin, xmax = (6, 9) if y == 4 else ((5, 10) if y == 5 else (4, 11))
        for x in range(xmin, xmax + 1):
            if x in (xmin, xmax) or y in (4, 13):
                p[x, y] = edge if x % 2 == 0 else outline
            else:
                p[x, y] = (25, 24, 25) if x > 6 else inside
    # Bracket and chamfer, not a random black hole.
    for x, y in ((3, 8), (12, 8), (3, 12), (12, 12)):
        p[x, y] = (122, 106, 98)
    if assembled:
        # Welded retaining strap, *not* a fake glowing fire. Heat/fuel and
        # active-light states belong to the future real furnace processor.
        for x in range(5, 11):
            p[x, 9] = (99, 98, 92) if x % 2 == 0 else (83, 84, 80)
            p[x, 10] = (45, 50, 51)
        for x in (6, 9):
            p[x, 9] = (168, 131, 69)  # brass rivet heads
        p[4, 9] = p[11, 9] = (61, 67, 67)
    return image


if __name__ == '__main__':
    for name, im in (
            ('fireclay_bricks', brick_face(0)),
            ('fireclay_bricks_top', brick_face(1)),
            ('blast_furnace_hatch_front', hatch_face(False)),
            ('blast_furnace_hatch_front_assembled', hatch_face(True))):
        im.save(ASSETS / (name + '.png'))
        print('Wrote', name + '.png')
