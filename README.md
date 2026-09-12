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

Writing to the STM32
```sh
STM32_Programmer_CLI -c port=SWD -w build/Debug/NavScan-RT.elf -v -rst
python3 build.py & STM32_Programmer_CLI -c port=SWD -w build/Debug/NavScan-RT.elf -v -rst
```

Firmware output: `build/Debug/NavScan-RT.elf` or `build/Release/NavScan-RT.elf`.

## Hardware

| Hardware | SKU / model | Purpose | Documentation |
| --- | --- | --- | --- |
| NUCLEO-F446RE (STM32F446RE) | WS-11147 | MCU board running FreeRTOS | [Board manual — UM1724](https://www.st.com/resource/en/user_manual/dm00105823.pdf) |
| PiicoDev Laser Distance Sensor | CE07741 / VL53L1X | ToF distance measurements | [Board and schematic](https://core-electronics.com.au/piicodev-laser-distance-sensor-vl53l1x.html), [sensor datasheet](https://www.st.com/resource/en/datasheet/vl53l1x.pdf) |
| Tower Pro Micro Servo 9g | SG90 | Rotate the distance sensor | [Manufacturer specifications](https://towerpro.com.tw/product/sg90-analog/) |
| PiicoDev Cable 50mm | CE07772 | Connect sensor to adapter | [Connector and wire colours](https://core-electronics.com.au/piicodev-cable-50mm.html) |
| PiicoDev Adapter for Breadboards | CE07691 | Break out sensor power and I²C | [Adapter resources](https://core-electronics.com.au/piicodev-breadboard-adapter.html) |
| 2 × metal DC geared motors with encoders, 12 V, 251 RPM | FIT0186 | Future mobile platform | [Specifications](https://wiki.dfrobot.com/fit0186/), [encoder wiring](https://wiki.dfrobot.com/fit0186/docs/18380) |
| TB6612FNG Dual Motor Driver Carrier | POLOLU-713 | Available driver; unsuitable for the FIT0186 motors at full load | [Specifications and wiring](https://www.pololu.com/product/713) |

The SG90 on hand has yellow, red, and black wires; verify the connector pinout before powering it. The linked SG90 page is the manufacturer's analog model reference.

Motor work is deferred: the FIT0186 is rated at 7 A stalled per motor, while this driver supports 1 A continuous / 3 A peak per channel (see specifications above).

## Documentation

This project uses FreeRTOS through CMSIS-RTOS2 (`osThreadNew`, `osDelay`, etc.).

| Resource | What to look for |
| --- | --- |
| [Nucleo-F446RE board manual — UM1724](https://www.st.com/resource/en/user_manual/dm00105823.pdf) | Board connectors, LEDs, buttons, power options, and ST-LINK. |
| [CMSIS-RTOS2 API](https://arm-software.github.io/CMSIS_6/main/RTOS2/group__CMSIS__RTOS.html) | Threads, delays, queues, and mutexes. |
| [Mastering the FreeRTOS Real Time Kernel](https://github.com/FreeRTOS/FreeRTOS-Kernel-Book) | Task management and scheduling; examples use the native FreeRTOS API. |
| [PiicoDev VL53L1X board](https://core-electronics.com.au/piicodev-laser-distance-sensor-vl53l1x.html) | Electrical specifications and Resources → Schematic for wiring. |
| [VL53L1X datasheet](https://www.st.com/resource/en/datasheet/vl53l1x.pdf) | I²C, ranging modes, timing, and measurement limitations. |
| [Ultra Lite Driver guide — UM2510](https://www.st.com/resource/en/user_manual/um2510-a-guide-to-using-the-vl53l1x-ultra-lite-driver-stmicroelectronics.pdf) | Initialization, measurements, and adapting the platform layer. |
| [C driver download — STSW-IMG009](https://www.st.com/en/embedded-software/stsw-img009.html) | Driver source and examples; connect its platform layer to STM32 I²C. |

Start with CMSIS thread management and the PiicoDev board page, then read UM2510.
