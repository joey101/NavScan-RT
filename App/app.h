#ifndef NAVSCAN_APP_H
#define NAVSCAN_APP_H

// C linkage lets the generated main.c call a function implemented in C++.
// The guard keeps this header valid when included by either language.
#ifdef __cplusplus
extern "C" {
#endif

#include "stm32f4xx_hal.h"

#include "stm32f4xx_nucleo.h"


// Runs inside the default FreeRTOS task, after the scheduler has started.
// Like other task entry functions, this function must not return.
void app_run(void);

#ifdef __cplusplus
}
#endif

#endif // NAVSCAN_APP_H
