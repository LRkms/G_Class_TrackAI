/*
 * uart.h
 *
 *  Created on: May 15, 2025
 *      Author: KMS
 */

#ifndef INC_UART_H_
#define INC_UART_H_


#include "main.h"

extern uint8_t rx_data;
void uart_receive_start(void);
void process_uart_command(uint8_t cmd);


#endif /* INC_UART_H_ */
