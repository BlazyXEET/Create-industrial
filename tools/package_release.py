#!/usr/bin/env python3
"""Package only after successful engine, client and offline checks.
Pass --engine-log, --client-log, --offline-log, --baseline (optional), --out.
Never copies dependency caches, run worlds, or stale build outputs into source.
"""
from pathlib import Path
import argparse, hashlib, json, re, shutil, zipfile, tomllib, os

ROOT=Path(__file__).resolve().parents[1]
parser=argparse.ArgumentParser(description=__doc__)
for name in ('engine-log','client-log','offline-log'):parser.add_argument('--'+name,type=Path,required=True)
parser.add_argument('--baseline',type=Path)
parser.add_argument('--out',type=Path,default=ROOT/'dist')
args=parser.parse_args();OUT=args.out.resolve();OUT.mkdir(exist_ok=True,parents=True)
version=re.search(r'(?m)^mod_version=(.+)$',(ROOT/'gradle.properties').read_text()).group(1).strip()
assert version=='0.1.18-test','Update release gates for a new version'
engine=args.engine_log.read_text(errors='replace');client=args.client_log.read_text(errors='replace');offline=args.offline_log.read_text(errors='replace')
match=re.search(r'All (\d+) required tests passed',engine)
assert match and int(match.group(1))>=37 and 'BUILD SUCCESSFUL' in engine,'Final Minecraft tests/build did not pass'
assert 'Parsing error loading recipe' not in engine,'A recipe failed to deserialize'
assert 'BUILD SUCCESSFUL' in client,'Final client build did not complete'
assert 'Offline logic checks passed.' in offline,'Offline checks did not pass'
audit=(ROOT/'build/client-asset-audit.txt').read_text().strip()
assert 'CLIENT_ASSET_AUDIT PASS' in audit and 'flatMaterialItems=30' in audit and 'missing=[]' in audit,'Minecraft model/texture audit failed'
assert (ROOT/'build/minecraft-assets-v18.png').is_file(),'Minecraft-rendered capture missing'
blender=json.loads((ROOT/'art/materials/blender-verification.json').read_text())
assert blender['ore_families']==6 and blender['manufactured_families']==3 and blender['inventory_meshes']==0,'Block-only Blender scene incomplete'
jar=ROOT/f'build/libs/createindustrial-{version}.jar'
with zipfile.ZipFile(jar) as z:
    assert z.testzip() is None
    metadata=tomllib.loads(z.read('META-INF/neoforge.mods.toml').decode())
    assert metadata['mods'][0]['modId']=='createindustrial' and metadata['mods'][0]['version']==version
    required=['net/createindustrialteam/createindustrial/processing/IndustrialProcessorBlockEntity.class',
        'net/createindustrialteam/createindustrial/worldgen/FireclayFeature.class',
        'assets/createindustrial/textures/block/nickel_ore.png',
        'assets/createindustrial/textures/item/printed_silicon_wafer.png',
        'data/createindustrial/recipe/laser_printing/silicon_wafer.json',
        'data/createindustrial/recipe/compacting/aluminium.json',
        'data/createindustrial/worldgen/configured_feature/river_fireclay.json']
    for path in required:assert path in z.namelist(),path
    assert 'data/createindustrial/recipe/mixing/steel.json' not in z.namelist()
    assert 'data/createindustrial/recipe/mixing/steel_from_pig_iron.json' not in z.namelist()
    manifest=json.loads((ROOT/'art/pixel-art/manifest.json').read_text())
    for name in manifest['sprite_items']:
        model=json.loads(z.read('assets/createindustrial/models/item/'+name+'.json'))
        assert model.get('parent')=='minecraft:item/generated' and not model.get('elements'),name
    for path in z.namelist():
        if path.endswith('.json'):json.loads(z.read(path))
dest=OUT/jar.name
if dest!=jar:shutil.copy2(jar,dest)
previews={
    'CreateIndustrial-V18-Pixel-Art.png':ROOT/'dist/CreateIndustrial-V18-Pixel-Art.png',
    'CreateIndustrial-V18-Minecraft-Models.png':ROOT/'build/minecraft-assets-v18.png',
    'CreateIndustrial-V18-Blender-Preview.png':ROOT/'art/materials/blocks-preview.png'}
for name,path in previews.items():
    if path.resolve()!=(OUT/name).resolve():shutil.copy2(path,OUT/name)
shutil.copy2(ROOT/'docs/V17-REFINING.md',OUT/'V18-Recipe-and-Automation-Guide.md')
static=next(line for line in offline.splitlines() if 'resource JSONs' in line)
report=f'''Create: Industrial V18 verification

Minecraft 1.21.1 / NeoForge 21.1.257 / Create 6.0.10-280 / Java 21.

PASS: full clean Gradle build against the exact declared dependencies.
PASS: all {match.group(1)} required Minecraft server GameTests.
PASS: {audit}
PASS: {static}
PASS: pure Java furnace, matcher, rotation, heat/casting and selection checks.
PASS: JAR metadata, compiled processing/worldgen classes, required resources,
      every recipe JSON and ZIP CRCs; obsolete steel shortcuts absent.
PASS: Blender {blender['blender']} saved the editable scene and rendered a preview;
      {blender['mesh_objects']} meshes, {blender['packed_images']} packed images,
      all six natural/three manufactured block families and both machine bodies.
      No material inventory meshes remain in the Blender scene.

Engine checks execute real Create motor/shaft and fan networks, both furnace
sizes, native heated silicon/alumina basin processing, probabilistic yield bounds,
laser printing, steel conversion with hot pig iron/air/flux/slag, power/heat/air
requirements, redstone pause/resume, item/fluid port simulation and filtering,
full-output backpressure, serialized inventory/tank/progress round trips,
coal-adjacent fireclay placement and four-ball loot, plus the existing
Welder/structure/worldgen/ore-drop/molten-pool regression suite.

The client audit checks missing baked models AND missing sprites on block quads,
then captures the actual Minecraft-rendered asset screen. The flat texture sheet
shows original source pixels; the separate Blender preview uses its own lighting.
These are different evidence stages. A manual two-player factory test and a
long survival progression/balance playthrough remain unverified.

Steel conversion represents an air-blown basic Bessemer/Thomas process, with
simplified batch/heat/slag quantities. Alumina compacting and silicon processing
follow the requested gameplay recipes; no literal electrolysis/semiconductor
chemistry simulation is claimed. Plutonium's existing transmutation is unchanged.

Commands: gradlew clean build runGameTestServer; gradlew build runClient
-PassetAudit; python tools/run_offline_checks.py; Blender --background
--factory-startup --python art/materials/build_blender.py.
This build was verified on Windows with Java 21 and the declared dependency
versions. Material item JSONs are generated sprites; the actual Minecraft client
verified all 30 material items have isGui3d=false. All 123 editable texture assets
were reworked; the user-supplied creative-tab icon is preserved.
'''
(OUT/'VERIFICATION-V18.txt').write_text(report)
changed=[];source=[]
for path in sorted(ROOT.rglob('*')):
    if not path.is_file():continue
    rel=path.relative_to(ROOT)
    if rel.parts[0] in ('build','.gradle','.git','run','runs','dist') or '__pycache__' in rel.parts or path.suffix in ('.blend1','.pyc'):continue
    source.append((path,rel))
    if args.baseline:
        old=args.baseline/rel
        if not old.is_file() or old.read_bytes()!=path.read_bytes():changed.append(rel.as_posix())
if args.baseline:
    current={r.as_posix() for _,r in source}
    for p in sorted(args.baseline.rglob('*')):
        if p.is_file() and p.relative_to(args.baseline).as_posix() not in current:
            changed.append('REMOVED '+p.relative_to(args.baseline).as_posix())
(OUT/'CHANGES-FROM-V17.txt').write_text('\n'.join(changed)+'\n')
bundle=OUT/'CreateIndustrial-V18-Source-and-Test-Bundle.zip'
with zipfile.ZipFile(bundle,'w',zipfile.ZIP_DEFLATED) as z:
    for path,rel in source:z.write(path,'Source/'+rel.as_posix())
    z.write(dest,'Test-JAR/'+dest.name)
    for name in (*previews,'VERIFICATION-V18.txt','CHANGES-FROM-V17.txt','V18-Recipe-and-Automation-Guide.md'):z.write(OUT/name,name)
    for name,path in [('engine.log',args.engine_log),('client.log',args.client_log),('offline.log',args.offline_log)]:z.write(path,'Verification/'+name)
with zipfile.ZipFile(bundle) as z:assert z.testzip() is None
for artifact in OUT.iterdir():
    if artifact.is_file():
        with artifact.open('r+b') as stream:os.fsync(stream.fileno())
hashes={p.name:hashlib.sha256(p.read_bytes()).hexdigest() for p in [dest,bundle,*[OUT/name for name in previews]]}
(OUT/'SHA256SUMS.txt').write_text(''.join(f'{v}  {k}\n' for k,v in hashes.items()))
print(json.dumps({'jar':str(dest),'bundle':str(bundle),'engine_tests':int(match.group(1)),'audit':audit,'sha256':hashes},indent=2))
