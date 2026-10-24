"""Display exact packaged 16x16 metal textures, enlarged without interpolation."""
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont
import json, zipfile, io
ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'dist';OUT.mkdir(exist_ok=True)
A=ROOT/'src/main/resources/assets/createindustrial/textures'
import os
CACHE=Path(os.environ.get('GRADLE_USER_HOME',Path.home()/'.gradle'))/'caches'
vanilla=zipfile.ZipFile(CACHE/'neoformruntime/artifacts/minecraft_1.21.1_client.jar')
create=zipfile.ZipFile(next((CACHE/'modules-2/files-2.1/com.simibubi.create/create-1.21.1').rglob('*slim.jar')))
def font(size,bold=False):
    candidates=[Path('C:/Windows/Fonts')/('segoeuib.ttf' if bold else 'segoeui.ttf'),
                Path('/usr/share/fonts/truetype/dejavu')/('DejaVuSans-Bold.ttf' if bold else 'DejaVuSans.ttf')]
    return ImageFont.truetype(str(next(p for p in candidates if p.is_file())),size)
def tex(ns,name):
    if ns=='createindustrial':return Image.open(A/'block'/f'{name}.png').convert('RGBA')
    z=vanilla if ns=='minecraft' else create
    return Image.open(io.BytesIO(z.read(f'assets/{ns}/textures/block/{name}.png'))).convert('RGBA')
catalog=json.loads((ROOT/'materials.json').read_text())
rows=[(m['id'].title()+(' / Bauxite' if m['id']=='aluminium' else ''),'createindustrial',m['ore']+'_ore',
       'deepslate_'+m['ore']+'_ore','raw_'+m['id']+'_block','block_of_'+m['id']) for m in catalog['materials']]
rows += [(m.title(),'minecraft',m+'_ore','deepslate_'+m+'_ore','raw_'+m+'_block',m+'_block') for m in ('iron','copper','gold')]
rows.append(('Zinc','create','zinc_ore','deepslate_zinc_ore','raw_zinc_block','zinc_block'))
W=1240;RH=126;H=220+len(rows)*RH+230
im=Image.new('RGB',(W,H),(18,25,34));dr=ImageDraw.Draw(im)
dr.text((38,22),'CREATE: INDUSTRIAL',font=font(35,True),fill=(244,199,68))
dr.text((38,70),'Ore textures | V17',font=font(25),fill=(235,240,246))
dr.text((38,108),'Exact texture files, shown at 6x pixel scale. These are not Minecraft screenshots.',font=font(18),fill=(156,172,188))
heads=['Stone ore','Deepslate ore','Raw storage block','Refined metal block']
for j,heading in enumerate(heads):dr.text((260+j*240,164),heading,font=font(19,True),fill=(191,208,224))
for i,(label,ns,*names) in enumerate(rows):
    y=206+i*RH
    if i%2==0:dr.rectangle((20,y-4,W-20,y+RH-8),fill=(24,34,46))
    dr.text((38,y+23),label,font=font(20,True),fill=(239,243,248))
    dr.text((38,y+58),ns,font=font(15),fill=(131,156,179))
    for j,name in enumerate(names):
        source='createindustrial' if ns=='create' and name=='raw_zinc_block' else ns
        tile=tex(source,name).resize((96,96),Image.Resampling.NEAREST)
        x=290+j*240;im.paste(tile,(x,y+4),tile)
footer=218+len(rows)*RH
dr.text((38,footer),'MANUFACTURED METALS — no natural ore blocks',font=font(21,True),fill=(244,199,68))
for i,m in enumerate(catalog['manufactured']):
    x=40+i*390
    tile=tex('createindustrial','block_of_'+m['id']).resize((96,96),Image.Resampling.NEAREST)
    im.paste(tile,(x,footer+48),tile)
    dr.text((x+118,footer+68),m['id'].replace('_',' ').title(),font=font(24,True),fill=(239,243,248))
dr.text((38,H-40),'Raw pieces and ingots use pixel textures on Minecraft cuboid models. Vanilla/Create textures retain their original artwork.',font=font(16),fill=(156,172,188))
im.save(OUT/'CreateIndustrial-V17-Ore-Textures.png')
print(OUT/'CreateIndustrial-V17-Ore-Textures.png')
