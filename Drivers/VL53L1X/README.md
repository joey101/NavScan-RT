# VL53L1X driver

Working copy of ST's STSW-IMG009 v3.5.5 Ultra Lite Driver (ULD).
Only the active, unpacked API is retained; duplicate vendor copies and archives were removed.
ST's license and source notices are retained.

- `include/`: public API, calibration, platform, and type headers.
- `src/VL53L1X_api.c`: ST's sensor initialization and ranging operations.
- `src/VL53L1X_calibration.c`: ST's calibration operations.
- `platform/vl53l1_platform.c`: MCU-specific I2C and delay functions to implement.
- `src/Lidar.cpp` and `include/Lidar.hpp`: existing C++ learning code; currently
  independent of the ST API.

CMake compiles these sources and exposes `include/` to the application, so C++
code can include `VL53L1X_api.h`. The supplied headers have C-linkage guards.

**Not hardware-ready:** the platform functions are ST's original placeholders
and return failure. Building successfully does not mean the API can communicate
with the sensor. Implement that layer before using the API for measurements.
No API calls have been added to `app_run()`.
