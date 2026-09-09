#!/usr/bin/env python3

"""Build the STM32 firmware with the CubeMX CMake presets.

Examples:
    python3 build.py
    python3 build.py --preset Release --jobs 4

Requires CMake, Ninja, and the Arm GNU bare-metal toolchain on PATH.
"""

import argparse
import os
import shlex
import shutil
import subprocess
import sys
from pathlib import Path

# Resolve paths from this script, so it also works when called from another folder.
ROOT = Path(__file__).resolve().parent


def run(command):
    # Flush before starting CMake so its output appears after the command line.
    print(f"\n> {shlex.join(command)}", flush=True)
    # cwd lets CMake find CMakePresets.json. A list avoids shell interpretation;
    # check=True stops the script if configuration or compilation fails.
    subprocess.run(command, cwd=ROOT, check=True)


def main(argv=None):
    parser = argparse.ArgumentParser(
        description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    # These names correspond to both configurePresets and buildPresets in JSON.
    parser.add_argument("--preset", choices=("Debug", "Release"), default="Debug")
    parser.add_argument(
        "--jobs", type=int, default=os.cpu_count() or 1,
        help="maximum parallel build jobs (default: CPU count)",
    )
    args = parser.parse_args(argv)
    if args.jobs < 1:
        parser.error("--jobs must be at least 1")

    # Check the tools used by our Ninja + GCC presets before creating a cache.
    # Desktop gcc/g++ cannot compile firmware for the STM32's Cortex-M4 core.
    required = ("cmake", "ninja", "arm-none-eabi-gcc", "arm-none-eabi-g++")
    missing = [tool for tool in required if shutil.which(tool) is None]
    if missing:
        print("Missing build tools on PATH: " + ", ".join(missing), file=sys.stderr)
        print("Install Ninja and the Arm GNU bare-metal toolchain, and ensure "
              "CMake and the toolchain's bin directory are on PATH.", file=sys.stderr)
        return 1

    # Match binaryDir = ${sourceDir}/build/${presetName} in CMakePresets.json.
    # Each preset gets its own cache; the old build/CMakeCache.txt is not reused.
    build_dir = ROOT / "build" / args.preset
    try:
        # Configuration selects Ninja and loads the Arm toolchain BEFORE CMake
        # identifies compilers. Plain `cmake -S ... -B ...` omitted that selection.
        run(["cmake", "--preset", args.preset])

        # CMake emits the exact include paths, defines, and compiler flags here.
        # Publish it before compilation so clangd can help even if code has errors.
        compile_commands = build_dir / "compile_commands.json"
        if not compile_commands.is_file():
            raise FileNotFoundError(f"CMake did not generate {compile_commands}")
        root_compile_commands = ROOT / "compile_commands.json"
        # Replace the previous generated file/link; a relative link survives moves.
        root_compile_commands.unlink(missing_ok=True)
        root_compile_commands.symlink_to(compile_commands.relative_to(ROOT))

        # --build selects build mode; this preset points to the SAME configured
        # directory. --parallel bounds the number of simultaneous compiler jobs.
        run(["cmake", "--build", "--preset", args.preset,
             "--parallel", str(args.jobs)])
    except subprocess.CalledProcessError as error:
        print(f"\nBuild failed (exit status {error.returncode}).", file=sys.stderr)
        return error.returncode
    except OSError as error:
        print(f"\nBuild failed: {error}", file=sys.stderr)
        return 1

    print(f"\nBuild successful. Firmware output: {build_dir}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
