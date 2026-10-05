#ifndef NAVSCAN_APP_H
#define NAVSCAN_APP_H

// C linkage for the task entry called by CubeMX's main.c.
#ifdef __cplusplus
extern "C" {
#endif

#include "stm32f4xx_nucleo.h"
#include "stm32f4xx_hal_uart.h"
#include "stm32f4xx_hal_i2c.h"
#include "VL53L1X_api.h"

// Runs in the default FreeRTOS task and must not return.
void app_run(void);

#ifdef __cplusplus
}
#endif

#endif // NAVSCAN_APP_H
