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

ROOT = Path(__file__).resolve().parent


def run(command):
    print(f"\n> {shlex.join(command)}", flush=True)
    subprocess.run(command, cwd=ROOT, check=True)


def main(argv=None):
    parser = argparse.ArgumentParser(
        description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    parser.add_argument("--preset", choices=("Debug", "Release"), default="Debug")
    parser.add_argument(
        "--jobs", type=int, default=os.cpu_count() or 1,
        help="maximum parallel build jobs (default: CPU count)",
    )
    args = parser.parse_args(argv)
    if args.jobs < 1:
        parser.error("--jobs must be at least 1")

    required = ("cmake", "ninja", "arm-none-eabi-gcc", "arm-none-eabi-g++")
    missing = [tool for tool in required if shutil.which(tool) is None]
    if missing:
        print("Missing build tools on PATH: " + ", ".join(missing), file=sys.stderr)
        print("Install Ninja and the Arm GNU bare-metal toolchain, and ensure "
              "CMake and the toolchain's bin directory are on PATH.", file=sys.stderr)
        return 1

    # Keep this path aligned with binaryDir in CMakePresets.json.
    build_dir = ROOT / "build" / args.preset
    try:
        run(["cmake", "--preset", args.preset])

        # Expose compiler flags to clangd even if compilation later fails.
        compile_commands = build_dir / "compile_commands.json"
        if not compile_commands.is_file():
            raise FileNotFoundError(f"CMake did not generate {compile_commands}")
        root_compile_commands = ROOT / "compile_commands.json"
        root_compile_commands.unlink(missing_ok=True)
        root_compile_commands.symlink_to(compile_commands.relative_to(ROOT))

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
