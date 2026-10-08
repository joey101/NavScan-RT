#include "app.h"
#include "main.h"
#include "cmsis_os2.h"

void app_run(void)
{
    uint8_t pData[7] = "Hello\n";

    uint16_t size = 6;
    uint32_t timeout = 1000;
    HAL_StatusTypeDef status;

    uint32_t Trials = 3;
    uint16_t devAddress = 0x52;
    uint8_t state = 0;
    VL53L1X_ERROR Status;

    status = HAL_UART_Transmit(&huart2, pData, size, timeout);

    if (status != HAL_OK) {
        BSP_LED_Off(LED2);
        osDelay(100U);
        BSP_LED_On(LED2);
        osDelay(1000U);
    }

    status = HAL_I2C_IsDeviceReady(&hi2c1, devAddress, Trials, timeout);

    if (status == HAL_OK) {
        uint8_t pDataTx[16] = "Sensor Ready\r\n";
        status = HAL_UART_Transmit(&huart2, pDataTx, 14, timeout);
    } else {
        uint8_t pDataTx[16] = "Sensor Failed\r\n";
        status = HAL_UART_Transmit(&huart2, pDataTx, 15, timeout);
    }

    while (!state) {
        Status = VL53L1X_BootState(devAddress, &state);
        HAL_Delay(2);
    }

    Status = VL53L1X_SensorInit(devAddress);

    if (Status != VL53L1X_ERROR_NONE) {
        uint8_t pDataFailed[22] = "Failed Initalization\n";
        BSP_LED_Off(LED2);
        osDelay(100U);
        BSP_LED_On(LED2);
        osDelay(1000U);

        HAL_UART_Transmit(&huart2, pDataFailed, 21, timeout);
    } else {
        uint8_t pDataFailed[26] = "Successful Initalization\n";

        HAL_UART_Transmit(&huart2, pDataFailed, 25, timeout);
    }

    for (;;) {
        if (Status != VL53L1X_ERROR_NONE) {
            BSP_LED_Off(LED2);
            osDelay(100U);
            BSP_LED_On(LED2);
            osDelay(100U);
        } else {
            BSP_LED_On(LED2);
        }
    }
}
