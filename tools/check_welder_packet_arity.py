#!/usr/bin/env python3
"""Reject calls to the seven-field WelderClickRequest with stale argument counts."""
from pathlib import Path
import re

root = Path(__file__).resolve().parents[1] / 'src/main/java'
needle = re.compile(r'\bnew\s+(?:net\.createindustrialteam\.createindustrial\.network\.)?WelderClickRequest\s*\(')
count = 0
for path in sorted(root.rglob('*.java')):
    content = path.read_text(encoding='utf-8')
    for match in needle.finditer(content):
        opening = match.end() - 1
        depth = 1
        commas = 0
        pos = opening + 1
        in_string = None
        escaped = False
        while pos < len(content) and depth:
            char = content[pos]
            if in_string:
                if escaped: escaped = False
                elif char == chr(92): escaped = True
                elif char == in_string: in_string = None
            elif char in (chr(34), chr(39)):
                in_string = char
            elif char in '([{': depth += 1
            elif char in ')]}': depth -= 1
            elif char == ',' and depth == 1: commas += 1
            pos += 1
        lineno = content.count('\n', 0, opening) + 1
        if depth != 0: raise AssertionError(f'{path}:{lineno}: unclosed constructor')
        if commas != 6:
            raise AssertionError(f'{path}:{lineno}: WelderClickRequest requires seven arguments, found {commas + 1}')
        count += 1
assert count >= 4, f'expected multiple WelderClickRequest callers, found {count}'
print(f'PASS: all {count} WelderClickRequest calls pass seven arguments')
