#include "app.h"
#include "cmsis_os2.h"
#include "stm32f4xx_nucleo.h"

void app_run(void)
{
    for (;;) {
        BSP_LED_Off(LED2);
        osDelay(1000U);
        BSP_LED_On(LED2);
        osDelay(1000U);
    }
}
