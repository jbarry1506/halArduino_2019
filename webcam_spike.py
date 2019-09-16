import numpy as np
import cv2
import serial
import time

ser = serial.Serial('COM3', 9600)
cap = cv2.VideoCapture(0)

while(True):
    # Capture frame-by-frame
    ret, frame = cap.read()

    # Our operations on the frame come here
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    # Display the resulting frame
    cv2.imshow('frame',gray)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

    ser.write(b'H')
    time.sleep(1)
    ser.write(b'L')
    time.sleep(1)
# When everything done, release the capture
cap.release()
cv2.destroyAllWindows()