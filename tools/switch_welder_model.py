#!/usr/bin/env python3
"""Choose the Welder item renderer without touching Java code or weld behavior.

Usage (from the project Source directory):
    python tools/switch_welder_model.py 2d
    python tools/switch_welder_model.py 3d
    python tools/switch_welder_model.py status

`welder.json` is a tiny selector; `welder_3d.json` and `welder_2d.json`
are the separate visual implementations. Future model regeneration edits
`welder_3d.json`, so it never silently undoes the selected mode.
"""
from __future__ import annotations

import argparse
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
MODELS = ROOT / 'src/main/resources/assets/createindustrial/models/item'
VALID = {mode: f'createindustrial:item/welder_{mode}' for mode in ('2d', '3d')}


def selected_mode(model_file: Path = MODELS / 'welder.json') -> str:
    """Return the active mode or raise a clear error for a damaged selector."""
    data = json.loads(model_file.read_text(encoding='utf-8'))
    for name, parent in VALID.items():
        if data.get('parent') == parent:
            return name
    raise ValueError(f'Unrecognized Welder model selector in {model_file}: {data.get("parent")!r}')


def set_model(mode: str, model_file: Path = MODELS / 'welder.json') -> None:
    """Atomically switch between two authored models. Never remove game logic."""
    if mode not in VALID:
        raise ValueError(f'Expected 2d or 3d, received {mode!r}')
    candidate = model_file.with_name(f'welder_{mode}.json')
    if not candidate.is_file():
        raise FileNotFoundError(f'Cannot enable {mode}: missing {candidate}')
    data = json.loads(candidate.read_text(encoding='utf-8'))
    if mode == '3d' and not data.get('elements'):
        raise ValueError(f'3D model lacks geometry: {candidate}')
    if mode == '2d' and (data.get('parent') != 'minecraft:item/generated' or data.get('elements')):
        raise ValueError(f'2D model must use a flat generated sprite: {candidate}')
    payload = {
        '__comment': 'Welder visual mode: 3d or 2d. Change only this parent or run tools/switch_welder_model.py; gameplay is unaffected.',
        'parent': VALID[mode],
    }
    temporary = model_file.with_name('welder.json.new')
    temporary.write_text(json.dumps(payload, indent=2) + '\n', encoding='utf-8')
    temporary.replace(model_file)


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('mode', choices=('2d', '3d', 'status'))
    args = parser.parse_args()
    if args.mode != 'status':
        set_model(args.mode)
    current = selected_mode()
    print(f'Welder visual mode: {current.upper()}')
    print('This changes only the item model. Welding, unwelding and multiblock rules are unchanged.')
    if args.mode != 'status':
        print('Rebuild the JAR to use this choice, or use the optional 2D resource pack in an existing installation.')


if __name__ == '__main__':
    main()
