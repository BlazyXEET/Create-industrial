#!/usr/bin/env python3
"""Validate the packaged resource graph without pretending this is a game run."""
from __future__ import annotations
import json
import struct
import sys
import zlib
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
RES = ROOT / "src/main/resources"
ASSETS = RES / "assets/createindustrial"
MODELS = ASSETS / "models"
failures: list[str] = []

def check(value: bool, message: str) -> None:
    if not value:
        failures.append(message)

def read_json(path: Path) -> dict:
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except (OSError, ValueError) as exc:
        failures.append(f"{path.relative_to(ROOT)}: {exc}")
        return {}

all_json = sorted(RES.rglob("*.json"))
for p in all_json:
    read_json(p)

def local_path(identifier: str, category: str, suffix: str) -> Path | None:
    namespace, name = identifier.split(":", 1) if ":" in identifier else ("minecraft", identifier)
    if namespace != "createindustrial":
        return None  # External resources are checked when Minecraft builds its atlas.
    check(".." not in Path(name).parts, f"Unsafe resource path: {identifier}")
    return ASSETS / category / (name + suffix)

cache: dict[Path, dict] = {}
def model_data(path: Path, visiting: set[Path] | None = None) -> dict:
    if path in cache:
        return cache[path]
    visiting = set() if visiting is None else visiting.copy()
    check(path not in visiting, f"Model parent cycle: {path}")
    if path in visiting:
        return {}
    visiting.add(path)
    data = read_json(path)
    textures = {}
    parent = data.get("parent")
    if parent:
        pp = local_path(parent, "models", ".json")
        if pp is not None:
            check(pp.is_file(), f"Missing parent: {parent}")
            if pp.is_file():
                textures.update(model_data(pp, visiting).get("textures", {}))
    textures.update(data.get("textures", {}))
    data = {**data, "textures": textures}
    cache[path] = data
    return data

def resolve(value: str, textures: dict, visited: set[str] | None = None) -> str | None:
    visited = set() if visited is None else visited.copy()
    if not value.startswith("#"):
        return value
    key = value[1:]
    if key in visited or key not in textures:
        failures.append(f"Unresolved/cyclic texture alias: {value}")
        return None
    visited.add(key)
    return resolve(textures[key], textures, visited)

models = sorted(MODELS.rglob("*.json"))
for p in models:
    data = model_data(p)
    textures = data.get("textures", {})
    values = list(textures.values())
    for element in data.get("elements", []):
        check(all(a < b for a, b in zip(element["from"], element["to"])), f"Degenerate cuboid: {p}")
        rotation = element.get("rotation")
        if rotation:
            check(rotation.get("angle") in (-45, -22.5, 0, 22.5, 45), f"Unsupported element angle: {p}")
        values += [face["texture"] for face in element.get("faces", {}).values()]
    for value in values:
        resolved = resolve(value, textures)
        path = local_path(resolved, "textures", ".png") if resolved else None
        if path is not None:
            check(path.is_file(), f"Missing texture: {resolved} ({p.name})")

blockstates = sorted((ASSETS / "blockstates").glob("*.json"))
for path in blockstates:
    data = read_json(path)
    entries = list(data.get("variants", {}).values())
    entries += [entry["apply"] for entry in data.get("multipart", [])]
    for entry in entries:
        for variant in entry if isinstance(entry, list) else [entry]:
            model = local_path(variant["model"], "models", ".json")
            if model is not None:
                check(model.is_file(), f"Missing blockstate model: {variant['model']}")
            for axis in ("x", "y"):
                check(variant.get(axis, 0) in (0, 90, 180, 270), f"Bad rotation in {path.name}")

materials = ("block_of_aluminium", "block_of_uranium", "reinforced_concrete",
             "plastered_reinforced_concrete", "condensing_mesh", "fireclay_bricks")
expected = {"north":(0,0), "east":(0,90), "south":(0,180), "west":(0,270), "up":(270,0), "down":(90,0)}
for material in materials:
    variants = read_json(ASSETS / "blockstates" / f"{material}.json").get("variants", {})
    check(set(variants) == {f"facing={d}" for d in expected}, f"Six-direction variants missing: {material}")
    for direction, (x,y) in expected.items():
        variant = variants.get(f"facing={direction}", {})
        check((variant.get("x",0),variant.get("y",0)) == (x,y), f"Incorrect facing transform: {material}/{direction}")
        check(variant.get("uvlock",False) is False, f"Texture incorrectly world-locked: {material}")

hatch = read_json(ASSETS / "blockstates/blast_furnace_hatch.json").get("variants", {})
check(len(hatch) == 32, "Expected all 32 hatch facing/assembled/lit/scale variants")
for key, variant in hatch.items():
    props = dict(token.split("=") for token in key.split(","))
    is_hot = props.get("lit") == "true" and props.get("assembled") == "true"
    check(variant["model"].endswith("_lit") == is_hot, f"Incorrect burning model: {key}")

pngs = sorted((ASSETS / "textures").rglob("*.png"))
for path in pngs:
    raw = path.read_bytes()
    check(raw[:8] == b"\x89PNG\r\n\x1a\n", f"Invalid PNG: {path}")
    try:
        w,h = struct.unpack(">II",raw[16:24])
        if "gui" not in path.parts:
            check((w,h) == (16,16), f"Expected 16x16 pixel texture: {path.name}")
        offset = 8
        while offset < len(raw):
            length = struct.unpack(">I",raw[offset:offset+4])[0]
            tag = raw[offset+4:offset+8]
            payload = raw[offset+8:offset+8+length]
            crc = struct.unpack(">I",raw[offset+8+length:offset+12+length])[0]
            check(zlib.crc32(tag+payload) & 0xFFFFFFFF == crc, f"PNG CRC mismatch: {path.name}")
            offset += length+12
    except (struct.error, IndexError):
        failures.append(f"Truncated PNG: {path.name}")

sounds = read_json(ASSETS / "sounds.json")
for event in sounds.values():
    for entry in event.get("sounds", []):
        entry = {"name":entry} if isinstance(entry,str) else entry
        if entry.get("type") == "event":
            continue
        path = local_path(entry["name"],"sounds",".ogg")
        if path is not None:
            check(path.is_file() and path.read_bytes().startswith(b"OggS"), f"Missing/invalid audio: {entry['name']}")

java = ROOT / "src/main/java/net/createindustrialteam/createindustrial"
controller = (java / "blocks/BlastFurnaceHatchBlock.java").read_text()
check("openMenu(" not in controller and "useItemOn(" in controller, "No-GUI hatch interaction regression")
ports = read_json(ASSETS / "blockstates/industrial_port.json").get("variants", {})
check(len(ports) == 16, "V18 legacy ports must retain serialized state variants for migration")
for mode in ("item_in","item_out","fluid_in","fluid_out"):
    check((ASSETS / f"textures/block/port_{mode}.png").is_file(), f"Missing port sprite {mode}")
client = (java / "client/IndustrialClient.java").read_text()
check("@EventBusSubscriber" in client and "WeldedMachineOutlinesClient.onClientTick(event)" in client,
      "Held-Welder outline client registration missing")
welder = (java / "items/WelderItem.java").read_text()
check("onItemUseFirst(ItemStack stack, UseOnContext context)" in welder, "Early interaction hook missing")
for name in ("items/WelderActions.java","client/WelderSelectionClient.java"):
    code = (java/name).read_text()
    check("displayClientMessage" not in code and "sendSystemMessage" not in code, f"Text popup returned: {name}")
for p in java.rglob("*.java"):
    check("SuperGlueEntity" not in p.read_text(), f"Unexpected glue entity dependency: {p.name}")
check((RES/"data/createindustrial/structure/empty.nbt").is_file(),"GameTest template missing")
icon_data = read_json(MODELS / "item/cooling_tower_icon.json")
check(icon_data.get("textures",{}).get("layer0") == "createindustrial:item/cooling_tower_icon",
      "Create: Industrial tab badge model missing or points to wrong texture")
check((ASSETS / "textures/item/cooling_tower_icon.png").is_file(),
      "User-provided cooling-tower tab texture missing")

# Welder model selector can point to the preserved 62-part 3D model OR a
# simple generated 2D sprite. Source tests should accept both choices.
selector = read_json(MODELS / "item/welder.json")
check(selector.get("parent") in ("createindustrial:item/welder_3d", "createindustrial:item/welder_2d"),
      "Welder model selector must choose the 3D or 2D appearance")
check(not selector.get("elements"), "Do not put geometry in the Welder selector")
model = read_json(MODELS / "item/welder_3d.json")
check(len(model.get("elements",[])) >= 30, "Reference-orange Welder 3D geometry missing or regressed")
for ctx in ("firstperson_righthand","firstperson_lefthand","thirdperson_righthand","thirdperson_lefthand"):
    check(ctx in model.get("display",{}), f"Welder 3D display transform missing: {ctx}")
flat_model = read_json(MODELS / "item/welder_2d.json")
check(flat_model.get("parent") == "minecraft:item/generated" and not flat_model.get("elements"),
      "Welder 2D model must be a flat generated sprite")
check(flat_model.get("textures",{}).get("layer0") == "createindustrial:item/welder_flat",
      "Welder flat icon texture is missing from the model")
check((ASSETS / "textures/item/welder_flat.png").is_file(), "Welder flat icon missing")

# Material inventory art must never regress to the former cube-based items.
manifest = read_json(ROOT / 'art/pixel-art/manifest.json')
for name in manifest.get('sprite_items', []):
    item_model = read_json(MODELS / 'item' / (name + '.json'))
    check(item_model.get('parent') == 'minecraft:item/generated', f'Material is not a flat sprite: {name}')
    check(not item_model.get('elements') and not item_model.get('display'), f'Unexpected material geometry/transform: {name}')
    check(item_model.get('textures', {}).get('layer0') == 'createindustrial:item/' + name, f'Wrong item sprite: {name}')

if failures:
    for message in failures:
        print("FAIL:",message,file=sys.stderr)
    raise SystemExit(1)
print(f"PASS: {len(all_json)} resource JSONs, {len(models)} models, {len(pngs)} PNGs, {len(blockstates)} blockstates.")
print("PASS: six-facing material variants, 32 hatch variants, legacy port data, sound headers and flat item sprites.")
print("This is resource/static validation, not Minecraft rendering or Java API compilation.")
