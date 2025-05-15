/*
 * motor.h
 *
 *  Created on: May 15, 2025
 *      Author: KMS
 */

#ifndef INC_MOTOR_H_
#define INC_MOTOR_H_


#include "main.h"

// 모터 함수
void motor_init(void);
void motor_forward(void);
void motor_backward(void);
void motor_stop(void);
void set_motor_speed(uint8_t duty);


#endif /* INC_MOTOR_H_ */
