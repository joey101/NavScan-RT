# NavScan-RT: project and learning context

Last updated: 2026-10-05 (API organization). This is a snapshot; inspect the current source and `.ioc` before giving advice about their state.

## Latest change: ST API available in the build

At the user's request, a working copy of STSW-IMG009 v3.5.5's API was added to
`Drivers/VL53L1X/`: public headers in `include/`, API and calibration C sources in
`src/`, and the MCU adaptation file in `platform/vl53l1_platform.c`. CMake now
compiles these files; the Debug build passed. The license is retained and the
active API is the only retained source copy. At the user's request, the duplicate
vendor tree and original ZIP were removed to keep the project lean and unpacked.
See `Drivers/VL53L1X/README.md`.

The platform functions remain ST's unimplemented placeholders and return failure.
No sensor API calls were added to the application, and nothing was flashed.
The user can learn by implementing the I2C/delay adaptation layer; do not assume
the request to organize the API authorizes completing that implementation.
The earlier learning milestones below still apply.

## Goal

Build an embedded-systems portfolio project aimed at an Embedded Software Engineer role at Advanced Navigation in Sydney. The purpose is to understand and explain the engineering, not merely assemble a working demonstration.

The first complete demo is a **rotating VL53L1X 2D room scanner**: acquire distance and angle on the STM32, send measurements to a PC, and visualize a point cloud in Python. Demonstrate C/C++, STM32, FreeRTOS, sensor integration, hardware bring-up, timing, diagnostics, and testing.

Possible later extensions are a second scanning axis, a mobile platform, wheel odometry, an IMU, localization, and mapping. These are future goals, not the current implementation. An IMU and Raspberry Pi are not confirmed parts of the current hardware inventory. PC simulation was an earlier proposed starting point, but actual progress has followed hardware bring-up; do not assume a simulation exists.

## How to help me learn

- Default to short explanations, documentation pointers, and one achievable next checkpoint.
- Read current files when asked to review code. Explain the issue without silently fixing it.
- Do not edit firmware, build configuration, or flash the board unless explicitly asked. The user wants to make changes and perform uploads personally. A previous unsolicited edit/upload was explicitly stopped.
- Show code in chat when requested; that does not authorize changing files.
- Distinguish language requirements from organizational preferences. For example, an `extern` declaration can live in a suitable `.h` or `.hpp`; placing it in `main.h` is a project convention, not a language rule.
- Explain the data flow and why a step matters. Avoid introducing UART, DMA, interrupts, multiple tasks, servos, and driver design all at once.
- Using HAL is acceptable. The learning goal is to understand its transactions, flags, and registers, and write the sensor-specific driver myself.
- Documentation edits are welcome when requested. Keep the README concise; use this file for project history and learning context.

## Current learning stage

**Basic hardware communication works. Sensor register access is the next step.** Successful experiments show practical progress, but do not imply mastery of the underlying concepts.

| Area | Progress and next learning need |
| --- | --- |
| Build and flashing | Has built Arm firmware with CMake/Ninja and flashed it through ST-LINK. Continue understanding compiler, linker, source lists, and build artifacts. |
| C/C++ across files | Has encountered declarations versus definitions, `extern`, headers, C linkage, and globals. These concepts still need reinforcement with small examples. |
| Buffers and pointers | Has used fixed-size UART buffers and corrected length mismatches. Reinforce capacity versus message length, initialized data, terminators, and status versus payload. |
| UART | User confirmed a greeting and character echo work. Understands UART is the PC diagnostic channel, not the sensor bus. |
| I²C | User confirmed VL53L1X address acknowledgement works. Next: understand an actual register read and returned bytes. |
| FreeRTOS | Runs application code inside one existing task and uses `osDelay`. Not yet demonstrating queues, task notifications, DMA, or a multi-task design. |
| Sensor driver | Wants to implement it personally. No distance measurement has been demonstrated. |
| PWM and encoders | Peripherals have been configured/reserved; physical servo control, motor control, and encoder operation have not been demonstrated. |

## What currently runs

Execution flows through `Core/Src/main.c`, board/peripheral initialization, the FreeRTOS scheduler, `StartDefaultTask()`, and then `App/src/app.cpp::app_run()`.

The current `app_run()`:

1. Sends `Hello` over UART.
2. Repeatedly calls `HAL_I2C_IsDeviceReady()` for `hi2c1`, using `0x52`, three trials, and a 1,000 ms HAL timeout.
3. Prints `Sensor Ready` once after an acknowledgement.

`0x29` is the sensor's 7-bit address; this STM32 HAL interface expects the shifted value `0x52`. Do not shift `0x52` again.

**Current code caveat:** `if (status == HAL_OK && counter < 1)` goes to its LED-blinking `else` after the first success even if subsequent probes succeed. Blinking therefore does not prove sensor failure. This was identified but not changed.

Acknowledgement confirms bus communication, not sensor initialization, data validity, or a distance reading. The earlier UART echo is a completed experiment, not the current loop.

## Hardware and saved pin assignments

Hardware on hand: NUCLEO-F446RE, PiicoDev VL53L1X (CE07741), breadboard adapter (CE07691), 50 mm cable (CE07772), Tower Pro SG90, Tower Pro SG-5010, two FIT0186 encoder motors, and Pololu TB6612FNG carrier (713). Specifications and links are in [README.md](README.md).

| Function | Peripheral / MCU pins |
| --- | --- |
| Sensor I²C | I2C1: PB8 SCL / PB9 SDA, exposed as Nucleo D15 / D14 |
| PC serial | USART2 asynchronous: PA2 TX / PA3 RX, through ST-LINK virtual COM port |
| Servo signals | TIM1 CH1 / CH2: PA8 / PA9 |
| Motor A encoder | TIM2 CH1 / CH2: PA0 / PA1 |
| Motor B encoder | TIM3 CH1 / CH2: PA6 / PA7 |
| Motor speed signals | TIM4 CH1 / CH2: PB6 / PB7 |
| Direction and standby | PC0–PC3 direction; PC4 standby |
| Debug / HAL timebase | SWD on PA13 / PA14; TIM6 timebase |

The saved system and APB timer clocks are 84 MHz. TIM1 has prescaler 83, period 19999, and initial pulses 1500: a 50 Hz period with 1.5 ms high time. Configuration does not start the PWM or encoder channels automatically. Recheck `.ioc` before relying on these assignments.

Motor work is deferred: FIT0186 stall current is 7 A per motor; the TB6612FNG carrier is rated for 1 A continuous / 3 A peak per channel. It is not a suitable unrestricted pairing. Servo power has not been resolved; the MCU's 3.3 V signal level is not the servo supply specification.

## Code ownership and organization

- `App/src/app.cpp`: application task and current experiments.
- `App/include/app.h`: declares the C-callable `app_run()` entry point.
- `Core/Src/main.c`: generated initialization and definitions of peripheral handles.
- `Core/Inc/main.h`: shared `extern` declarations for `hi2c1`, `htim1`–`htim4`, and `huart2`, within C-linkage guards.
- `Drivers/VL53L1X/src/Lidar.cpp` and `include/Lidar.hpp`: intended home of my own driver. Currently a C++ ownership exercise involving a name and dynamically allocated health value; it does not communicate with the sensor and is not a completed driver design.
- Other `Drivers/` directories: ST HAL, CMSIS, and board support.
- `Middlewares/`: FreeRTOS and the CMSIS-RTOS2 wrapper. `os...` calls use that wrapper; FreeRTOS still schedules the task.
- `Drivers/VL53L1X/`: active ST API sources and platform placeholders, included in the build. Duplicate vendor sources and the original ZIP have been removed; keep the project lean with no archive backups.
- `docs/datasheets/` and `docs/manuals/`: offline PDFs.

Keep CubeMX-managed edits inside user-code blocks where applicable. List application/driver source files explicitly in the root CMake file. A source directory in `target_sources()` does not automatically include its contents.

## Immediate next milestone

**Read the VL53L1X identification register and print the value over UART.** Guide the user through it rather than supplying a complete implementation.

1. Find `VL53L1X_GetSensorId` in ST's reference API source.
2. Trace the register definition and read helper: identify register-address width, data length, byte order, and expected ID.
3. Read the parameter documentation for `HAL_I2C_Mem_Read()` in the locally installed HAL source/manual.
4. Attempt that read, distinguish HAL status from returned data, and report both sensibly over UART.

After this: sensor boot/initialization, one valid distance reading, periodic distance reports, then a focused driver interface. Add servo scanning and Python visualization afterward. Introduce more RTOS mechanisms only when there is a concrete scheduling or communication problem to solve.

## Reading map

- [VL53L1X datasheet](docs/datasheets/VL53L1X.pdf): sensor interface and characteristics.
- [UM2510](docs/manuals/UM2510-VL53L1X-driver-guide.pdf): driver initialization and ranging workflow; not a complete register programming reference.
- [Vendor reference guide](references/README.md): source files to inspect for register definitions and sequences.
- UM1725 (`dm00105879.pdf`, previously downloaded to `~/Downloads/`): STM32F4 HAL API; search for the exact function being used.
- UM1724 (`dm00105823.pdf`, previously downloaded to `~/Downloads/`): Nucleo connectors, power, and ST-LINK.
- RM0390: STM32F446 peripheral registers; follow the I²C chapter when investigating what HAL does internally. Offline availability has not been confirmed.
- The earlier recommended C++ foundations sequence: compiler/linker → declarations/definitions → multiple source files → headers → external linkage. Links were supplied from LearnCpp; those concepts remain relevant.

For a deeper understanding, trace one successful `HAL_I2C_IsDeviceReady()` call and identify START, address transmission, acknowledgement handling, and STOP before attempting to replace HAL.

## Workflow reminders

The user performs builds and flashing. Build first and flash only after success; do not run those operations concurrently. The README currently contains a combined command with a single `&`, which backgrounds the build and can flash stale firmware. That line should not be copied as a sequential build-and-flash command.

The working PC terminal command has been `/usr/bin/python3 -m serial.tools.miniterm /dev/ttyACM0 115200`. The port can change. Open the terminal before pressing RESET to see startup messages. UART transmits bytes, not automatic lines; CR/LF and transfer lengths are explicit.

This context update did not re-test hardware or change firmware. Treat user-confirmed hardware milestones as historical results and verify current behavior when needed.
