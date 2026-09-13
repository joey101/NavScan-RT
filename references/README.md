# Sensor driver reference

We are writing our own VL53L1X driver in `Drivers/VL53L1X/src/Lidar.cpp`, with its interface in `Drivers/VL53L1X/include/Lidar.hpp`.

`vendor/STSW-IMG009_v3.5.5/` contains the unmodified ST reference package. It is not included in our CMake build. The original ZIP is retained in `archives/STSW-IMG009.zip`.

Read these alongside UM2510:

- [API implementation](vendor/STSW-IMG009_v3.5.5/API/core/VL53L1X_api.c): register access and initialization/ranging sequences.
- [API header](vendor/STSW-IMG009_v3.5.5/API/core/VL53L1X_api.h): register definitions and function declarations.
- [Platform layer](vendor/STSW-IMG009_v3.5.5/API/platform/vl53l1_platform.c): the boundary between sensor operations and MCU I²C access.
- [License](vendor/STSW-IMG009_v3.5.5/API/LICENSE.txt): retain applicable notices if reusing source.

The bundled `Example/` is ST's example project, not our firmware entry point.
