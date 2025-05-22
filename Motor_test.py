import serial
import time

ser = serial.Serial('/dev/ttyTHS1', 115200, timeout=1)

while True:
    cmd = input("명령 입력 (F/B/L/R/S): ").strip()
    if cmd in ['F', 'B', 'L', 'R', 'S']:
        ser.write(cmd.encode())
        print(f"전송: {cmd}")
    else:
        print("유효하지 않은 명령")