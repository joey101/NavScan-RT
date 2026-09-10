# Build

Install dependencies on Ubuntu 24.04:

Installing the usb

```sh
sudo apt-get install libusb-1.0.0-dev

```
When using ST-LINK/J-Link probes or USB DFU to connect to a target, copy the rules files located under the Driver/rules folder to /etc/udev/rules.d/ on Ubuntu:
```sh
sudo cp *.* /etc/udev/rules.d
```
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

## Documentation

This project uses FreeRTOS through CMSIS-RTOS2 (`osThreadNew`, `osDelay`, etc.).

| Resource | What to look for |
| --- | --- |
| [CMSIS-RTOS2 API](https://arm-software.github.io/CMSIS_6/main/RTOS2/group__CMSIS__RTOS.html) | Threads, delays, queues, and mutexes. |
| [Mastering the FreeRTOS Real Time Kernel](https://github.com/FreeRTOS/FreeRTOS-Kernel-Book) | Task management and scheduling; examples use the native FreeRTOS API. |
| [PiicoDev VL53L1X board](https://core-electronics.com.au/piicodev-laser-distance-sensor-vl53l1x.html) | Electrical specifications and Resources → Schematic for wiring. |
| [VL53L1X datasheet](https://www.st.com/resource/en/datasheet/vl53l1x.pdf) | I²C, ranging modes, timing, and measurement limitations. |
| [Ultra Lite Driver guide — UM2510](https://www.st.com/resource/en/user_manual/um2510-a-guide-to-using-the-vl53l1x-ultra-lite-driver-stmicroelectronics.pdf) | Initialization, measurements, and adapting the platform layer. |
| [C driver download — STSW-IMG009](https://www.st.com/en/embedded-software/stsw-img009.html) | Driver source and examples; connect its platform layer to STM32 I²C. |

Start with CMSIS thread management and the PiicoDev board page, then read UM2510.
