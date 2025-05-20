/*
 * uart.c
 *
 *  Created on: May 15, 2025
 *      Author: KMS
 */

#include "uart.h"
#include "motor.h"

extern UART_HandleTypeDef huart1;

void uart_receive_start(void)
{
    HAL_UART_Receive_IT(&huart1, &rx_data, 1);
}

void HAL_UART_RxCpltCallback(UART_HandleTypeDef *huart)
{
    if (huart->Instance == USART1)
    {
        HAL_UART_Transmit(&huart1, &rx_data, 1, 10); // ← 여기에 Breakpoint
        process_uart_command(rx_data);
        HAL_UART_Receive_IT(&huart1, &rx_data, 1);
    }
}


void process_uart_command(uint8_t cmd)
{
    switch(cmd)
    {
        case 'F':
            motor_forward();
            break;
        case 'B':
            motor_backward();
            break;
        case 'S':
            motor_stop();
            break;
        case 'L':
            motor_turn_left();
            break;
        case 'R':
            motor_turn_right();
            break;
        default:
            break;
    }
}

