#!/usr/bin/env python3
"""Run executable pure-Java logic tests plus source/resource checks using JDK 21."""
from pathlib import Path
import shutil
import re
import subprocess
import sys
import tempfile
import contextlib

root = Path(__file__).resolve().parents[1]
java = root / "src/main/java/net/createindustrialteam/createindustrial"
for executable in ("java", "javac"):
    if shutil.which(executable) is None:
        raise SystemExit(f"{executable} is required. Install JDK 21 and put its bin directory on PATH.")

def run(*args):
    subprocess.run([str(a) for a in args], check=True, cwd=root)

try:
    run(sys.executable, root / "tools/verify_resources.py")
    run(sys.executable, root / "tools/verify_welder_v23.py")
    run(sys.executable, root / "tools/verify_welder_orange.py")
    run(sys.executable, root / "tools/verify_welder_model_switch.py")
    run(sys.executable, root / "tools/verify_v20_assets.py")
    run(sys.executable, root / "tools/verify_v22_recipes.py")
    run(sys.executable, root / "tools/check_gametest_player_rotation.py")
    run(sys.executable, root / "tools/check_welder_packet_arity.py")
    run(sys.executable, root / "tools/check_v20_architecture.py")
    # Keep compiler output inside the checkout (also works in restricted Windows hosts).
    test_output = root / "build/offline-tests"
    test_output.mkdir(parents=True, exist_ok=True)
    with contextlib.nullcontext(str(test_output)) as tmp:
        run("javac", "-d", tmp, root / "tools/JavaSyntaxCheck.java")
        run("java", "-cp", tmp, "JavaSyntaxCheck", root / "src/main/java")
        production = [java / p for p in (
            "multiblock/VoxelPattern.java", "multiblock/PatternGeometry.java", "multiblock/BlastFurnaceLayout.java",
            "multiblock/LargeBlastFurnaceLayout.java",
            "multiblock/FurnaceCellMatcher.java", "multiblock/FurnaceControllerOffsets.java",
            "items/SelectionPolicy.java", "foundry/FurnaceRules.java",
            "foundry/FurnaceTransferRules.java")]
        tests = sorted((root / "tests").glob("*.java"))
        run("javac", "-d", tmp, *production, *tests)
        for test in tests:
            package = re.search(r"(?m)^package\s+([\w.]+);", test.read_text())
            name = (package.group(1) + "." if package else "") + test.stem
            run("java", "-cp", tmp, name)
except subprocess.CalledProcessError as exc:
    raise SystemExit(exc.returncode)
print("Offline logic checks passed. Minecraft-linked GameTests and client playtesting are separate checks.")
