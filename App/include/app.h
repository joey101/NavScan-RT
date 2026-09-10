#ifndef NAVSCAN_APP_H
#define NAVSCAN_APP_H

// C linkage for the task entry called by CubeMX's main.c.
#ifdef __cplusplus
extern "C" {
#endif

// Runs in the default FreeRTOS task and must not return.
void app_run(void);

#ifdef __cplusplus
}
#endif

#endif // NAVSCAN_APP_H
