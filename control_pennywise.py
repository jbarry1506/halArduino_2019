# virtualenv path
# ~/Documents/PROGRAMMING_2019/HALLOWEEN_2019/halloween_2019/Scripts/activate
# activate this virtualenv before working, deactivate at the end

import serial
import time

ser = serial.Serial('COM3', 9600)

for i in range(10):
    time.sleep(0.5)
    ser.write(b'H')
    time.sleep(0.5)
    ser.write(b'L')

