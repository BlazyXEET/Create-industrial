#!/usr/bin/env python3
"""Make a client-only orange 3D Welder override pack for Minecraft 1.21.1.

Useful for testing the replacement in an already-installed V24 mod without
recompiling; never changes the Welder's Java gameplay logic.
"""
import argparse
import io
import json
from pathlib import Path
from zipfile import ZipFile, ZIP_DEFLATED
from PIL import Image
ROOT=Path(__file__).resolve().parents[1]
ASSETS=ROOT/'src/main/resources/assets/createindustrial'
MODELS=ASSETS/'models/item'
TEX=ASSETS/'textures/item/welder'
DEFAULT=ROOT/'dist/CreateIndustrial-Orange-Welder-3D-Resource-Pack.zip'

def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--output',type=Path,default=DEFAULT)
    args=parser.parse_args()
    out=args.output.resolve();out.parent.mkdir(parents=True,exist_ok=True)
    model=json.loads((MODELS/'welder_3d.json').read_text())
    selector={'parent':'createindustrial:item/welder_3d'}
    required={f['texture'][1:] for e in model['elements'] for f in e['faces'].values()}
    assert all((TEX/(k+'.png')).is_file() for k in required)
    info={'pack':{'pack_format':34,'description':"Create Industrial - owner's orange Welder 3D design (cosmetic)"}}
    icon=Image.open(ROOT/'art/welder/reference-welder-icon-16x16.png').convert('RGBA')
    preview=icon.resize((128,128),Image.Resampling.NEAREST)
    buf=io.BytesIO();preview.save(buf,format='PNG')
    with ZipFile(out,'w',ZIP_DEFLATED,compresslevel=9) as z:
        z.writestr('pack.mcmeta',json.dumps(info,indent=2)+'\n')
        z.writestr('pack.png',buf.getvalue())
        z.writestr('assets/createindustrial/models/item/welder.json',json.dumps(selector,indent=2)+'\n')
        z.write(MODELS/'welder_3d.json','assets/createindustrial/models/item/welder_3d.json')
        for key in sorted(required):
            z.write(TEX/(key+'.png'), 'assets/createindustrial/textures/item/welder/'+key+'.png')
        z.writestr('README.txt','Enable above other Create Industrial packs in Minecraft 1.21.1. Only the Welder model and textures change.\n')
    with ZipFile(out) as z:
        assert z.testzip() is None
    print('PASS: orange 3D visual-only pack:',out)

if __name__=='__main__':main()
