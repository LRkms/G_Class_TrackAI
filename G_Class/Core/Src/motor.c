/*
 * motor.c
 *
 *  Created on: May 15, 2025
 *      Author: KMS
 */

#include "motor.h"

// === 사용할 타이머 핸들러 및 채널 정의 ===
extern TIM_HandleTypeDef htim2;

#define ENA_PWM &htim2, TIM_CHANNEL_1  // PA0
#define ENB_PWM &htim2, TIM_CHANNEL_2  // PA1
#define ENA_CHANNEL TIM_CHANNEL_1
#define ENB_CHANNEL TIM_CHANNEL_2
// === 초기화 함수 (PWM 스타트용) ===
void motor_init(void)
{
    HAL_TIM_PWM_Start(ENA_PWM);  // ENA (좌측)
    HAL_TIM_PWM_Start(ENB_PWM);  // ENB (우측)
}
// === 속도 설정 함수 수정 ===
void set_motor_speed(uint8_t duty)
{
    uint32_t pwm = (duty * (__HAL_TIM_GET_AUTORELOAD(&htim2))) / 100;
    __HAL_TIM_SET_COMPARE(&htim2, ENA_CHANNEL, pwm);  // 좌측
    __HAL_TIM_SET_COMPARE(&htim2, ENB_CHANNEL, pwm);  // 우측
}

// === 전진 ===
void motor_forward(void)
{
    HAL_GPIO_WritePin(GPIOC, GPIO_PIN_5, GPIO_PIN_SET);   // IN1
    HAL_GPIO_WritePin(GPIOC, GPIO_PIN_6, GPIO_PIN_RESET); // IN2

    HAL_GPIO_WritePin(GPIOB, GPIO_PIN_8, GPIO_PIN_SET);   // IN3
    HAL_GPIO_WritePin(GPIOB, GPIO_PIN_9, GPIO_PIN_RESET); // IN4

    set_motor_speed(30);  // 기본 속도 70%
}

// === 후진 ===
void motor_backward(void)
{
    HAL_GPIO_WritePin(GPIOC, GPIO_PIN_5, GPIO_PIN_RESET); // IN1
    HAL_GPIO_WritePin(GPIOC, GPIO_PIN_6, GPIO_PIN_SET);   // IN2

    HAL_GPIO_WritePin(GPIOB, GPIO_PIN_8, GPIO_PIN_RESET); // IN3
    HAL_GPIO_WritePin(GPIOB, GPIO_PIN_9, GPIO_PIN_SET);   // IN4

    set_motor_speed(30);  // 기본 속도 70%
}

// === 정지 ===
void motor_stop(void)
{
    HAL_GPIO_WritePin(GPIOC, GPIO_PIN_5, GPIO_PIN_RESET);
    HAL_GPIO_WritePin(GPIOC, GPIO_PIN_6, GPIO_PIN_RESET);
    HAL_GPIO_WritePin(GPIOB, GPIO_PIN_8, GPIO_PIN_RESET);
    HAL_GPIO_WritePin(GPIOB, GPIO_PIN_9, GPIO_PIN_RESET);

    //set_motor_speed(0);
}

// === 좌회전 ===
void motor_turn_left(void)
{
    HAL_GPIO_WritePin(GPIOC, GPIO_PIN_5, GPIO_PIN_RESET); // IN1 LOW
    HAL_GPIO_WritePin(GPIOC, GPIO_PIN_6, GPIO_PIN_RESET); // IN2 LOW

    HAL_GPIO_WritePin(GPIOB, GPIO_PIN_8, GPIO_PIN_SET);   // IN3 HIGH
    HAL_GPIO_WritePin(GPIOB, GPIO_PIN_9, GPIO_PIN_RESET); // IN4 LOW

    __HAL_TIM_SET_COMPARE(&htim2, ENA_CHANNEL, 0);        // 좌측 속도 0%
    __HAL_TIM_SET_COMPARE(&htim2, ENB_CHANNEL, (__HAL_TIM_GET_AUTORELOAD(&htim2) * 30) / 100);
}

// === 우회전 ===
void motor_turn_right(void)
{
    HAL_GPIO_WritePin(GPIOC, GPIO_PIN_5, GPIO_PIN_SET);   // IN1 HIGH
    HAL_GPIO_WritePin(GPIOC, GPIO_PIN_6, GPIO_PIN_RESET); // IN2 LOW

    HAL_GPIO_WritePin(GPIOB, GPIO_PIN_8, GPIO_PIN_RESET); // IN3 LOW
    HAL_GPIO_WritePin(GPIOB, GPIO_PIN_9, GPIO_PIN_RESET); // IN4 LOW

    __HAL_TIM_SET_COMPARE(&htim2, ENA_CHANNEL, (__HAL_TIM_GET_AUTORELOAD(&htim2) * 30) / 100);
    __HAL_TIM_SET_COMPARE(&htim2, ENB_CHANNEL, 0);        // 우측 속도 0%
}

