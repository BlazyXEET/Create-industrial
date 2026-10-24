#!/usr/bin/env python3
"""Build a small Minecraft 1.21.1 resource pack that hides the 3D Welder.

Enable the pack in Options > Resource Packs; disable it to bring the 3D
model back. No mod/JAR changes and no Java gameplay changes are required.
"""
from __future__ import annotations

import argparse
import io
import json
from pathlib import Path
from zipfile import ZIP_DEFLATED, ZipFile

from PIL import Image

ROOT = Path(__file__).resolve().parents[1]
ICON = ROOT / 'src/main/resources/assets/createindustrial/textures/item/welder_flat.png'
DEFAULT_OUTPUT = ROOT / 'dist/CreateIndustrial-Welder-2D-Override-Resource-Pack.zip'


def build_pack(output: Path) -> None:
    output.parent.mkdir(parents=True, exist_ok=True)
    model = {
        'parent': 'minecraft:item/generated',
        'textures': {'layer0': 'createindustrial:item/welder_flat'},
    }
    metadata = {
        'pack': {
            'pack_format': 34,  # Java 1.21 / 1.21.1 resource pack version.
            'description': 'Create: Industrial - flat 2D Welder icon (disable pack for 3D)',
        }
    }
    with Image.open(ICON) as img:
        assert img.size == (16, 16) and img.mode == 'RGBA'
        preview = img.resize((128,128), resample=Image.Resampling.NEAREST)
        icon_bytes = io.BytesIO()
        preview.save(icon_bytes, format='PNG')

    with ZipFile(output, 'w', compression=ZIP_DEFLATED, compresslevel=9) as archive:
        archive.writestr('pack.mcmeta', json.dumps(metadata, indent=2) + '\n')
        archive.writestr('pack.png', icon_bytes.getvalue())
        archive.writestr('assets/createindustrial/models/item/welder.json', json.dumps(model, indent=2) + '\n')
        archive.write(ICON, 'assets/createindustrial/textures/item/welder_flat.png')
        archive.writestr('README.txt',
            'Minecraft Java 1.21.1. Enable this zip in Options > Resource Packs.\n'
            'Move it above other Create Industrial model packs. Disable to restore 3D.\n'
            'Only createindustrial:welder appearance is changed. Welding rules stay unchanged.\n')
    with ZipFile(output) as archive:
        assert archive.testzip() is None
        assert len(archive.namelist()) == 5
    print(f'Built optional 2D override resource pack: {output}')


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--output', type=Path, default=DEFAULT_OUTPUT)
    args = parser.parse_args()
    build_pack(args.output.resolve())


if __name__ == '__main__':
    main()
