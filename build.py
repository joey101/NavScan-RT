#!/usr/bin/env python3

import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent
BUILD_DIR = ROOT / "build"


def run(command):
    print(f"\n> {' '.join(map(str, command))}")

    result = subprocess.run(
        command,
        cwd=ROOT
    )

    if result.returncode != 0:
        print("\nBuild failed.")
        sys.exit(result.returncode)


def main():
    BUILD_DIR.mkdir(exist_ok=True)

    # Configure CMake
    run([
        "cmake",
        "-S", str(ROOT),
        "-B", str(BUILD_DIR),
        "-DCMAKE_EXPORT_COMPILE_COMMANDS=ON",
    ])

    # Build project
    run([
        "cmake",
        "--build", str(BUILD_DIR),
        "-j",
    ])

    # Make compile_commands.json available to clangd / Neovim
    compile_commands = BUILD_DIR / "compile_commands.json"
    root_compile_commands = ROOT / "compile_commands.json"

    if compile_commands.exists():

        if (
            root_compile_commands.exists()
            or root_compile_commands.is_symlink()
        ):
            root_compile_commands.unlink()

        root_compile_commands.symlink_to(
            compile_commands
        )

    print("\nBuild successful.")


if __name__ == "__main__":
    main()
