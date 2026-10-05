# Sensor driver reference

The active STSW-IMG009 v3.5.5 API is in `Drivers/VL53L1X/` and included in the firmware build. Its platform functions still need implementing. See the [driver guide](../Drivers/VL53L1X/README.md).

Read these alongside UM2510:

- [API implementation](../Drivers/VL53L1X/src/VL53L1X_api.c): initialization and ranging sequences.
- [API header](../Drivers/VL53L1X/include/VL53L1X_api.h): register definitions and declarations.
- [Platform layer](../Drivers/VL53L1X/platform/vl53l1_platform.c): I2C and delay functions to implement.
- [License](../Drivers/VL53L1X/LICENSE.txt): ST's terms and notices.

Only the active API and the PDFs under `docs/` are retained. The duplicate vendor tree, bundled example project, and ZIP archive have been removed.
