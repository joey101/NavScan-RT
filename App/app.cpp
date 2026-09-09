#include "app.h"
#include "cmsis_os2.h"

// The declaration in app.h gives this definition C linkage for main.c.
// Keep application code here; CubeMX continues to manage hardware setup in C.
void app_run(void)
{
    // Initialize application objects here when they need initialized hardware
    // or RTOS services. Global constructors run before main(), before HAL setup.
    for (;;) {
        // Add application work here. Blocking yields the CPU to other tasks.
        // CMSIS-RTOS2 measures this delay in kernel ticks, not milliseconds.
        osDelay(1U);
    }
}
