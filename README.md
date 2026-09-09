# Build

Install dependencies on Ubuntu 24.04:

```sh
sudo apt update
sudo apt install python3 python3-venv cmake ninja-build gcc-arm-none-eabi libnewlib-arm-none-eabi libstdc++-arm-none-eabi-newlib
```

The [Ubuntu Arm toolchain package](https://packages.ubuntu.com/noble/gcc-arm-none-eabi) supplies the cross-compilers.

From the project root, run:

```sh
python3 -m venv .venv                # First-time setup; skip if already created
source .venv/bin/activate            # Activate in each new terminal
python3 build.py                     # Debug build
python3 build.py --preset Release    # Release build
```

Firmware output: `build/Debug/NavScan-RT.elf` or `build/Release/NavScan-RT.elf`.
