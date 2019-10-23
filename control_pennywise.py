# virtualenv path
# ~/Documents/PROGRAMMING_2019/HALLOWEEN_2019/halloween_2019/Scripts/activate
# activate this virtualenv before working, deactivate at the end

import serial
import time
import random

ser = serial.Serial('COM3', 115200)

for i in range(10):
    #--- Spike for PennyComTest.ino
    # time.sleep(0.2)
    # ser.write(b'L')
    # time.sleep(0.2)
    # ser.write(b'M')
    # time.sleep(0.2)
    # ser.write(b'R')
    # time.sleep(0.2)
    # ser.write(b'M')
    # ser.write(b'%d'%int(i))
    # time.sleep(0.1)
    # ser.write(b's')
    # time.sleep(1.0)

    #--- Spike for PennyComTest_2.ino
        # working
    servoPos = random.randint(0,180)

    for i in str(servoPos):
        ser.write(b'{%d}'%int(i))
        time.sleep(0.2)
    ser.write(b's')
