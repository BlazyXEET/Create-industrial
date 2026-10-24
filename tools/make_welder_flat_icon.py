#!/usr/bin/env python3
"""Restore the exact user-supplied 16x16 orange Welder item sprite.

The art reference is included with the source; no approximation or scaling.
This modifies appearance only; no Java code or item IDs change.
"""
from pathlib import Path
from PIL import Image
ROOT=Path(__file__).resolve().parents[1]
REFERENCE=ROOT/'art/welder/reference-welder-icon-16x16.png'
OUTPUT=ROOT/'src/main/resources/assets/createindustrial/textures/item/welder_flat.png'

def generate_icon():
    with Image.open(REFERENCE) as src:
        sprite=src.convert('RGBA')
    if sprite.size != (16,16):
        raise ValueError('Reference must be an exact 16x16 pixel-art icon')
    return sprite

def main():
    OUTPUT.parent.mkdir(parents=True,exist_ok=True)
    generate_icon().save(OUTPUT,optimize=True)
    print('Restored user-provided orange Welder icon:',OUTPUT)

if __name__=='__main__':main()
