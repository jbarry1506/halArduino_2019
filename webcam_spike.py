import numpy as np
import cv2
import serial
import time


# ser = serial.Serial('COM3', 9600)

# function to get the initial image to compare for motion detection
def get_base_image(camera):
    retimage, im = camera.read()
    return im


# camera 1 is the external camera
cap = cv2.VideoCapture(1)
# capture the base image for comparison
base_image = get_base_image(cap)
# set up the video codec
fourcc = cv2.VideoWriter_fourcc(*'DIVX')
# set up the video to be saved
out = cv2.VideoWriter('output.avi', fourcc, 20.0, (640,480))
# save the base image
cv2.imwrite('baseimage.jpg', base_image)


while(True):
    # Capture frame-by-frame
    ret, frame = cap.read()

    out.write(frame)

    # Our operations on the frame come here
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    # Display the resulting frame
    cv2.imshow('frame',gray)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

    # ser.write(b'H')
    # time.sleep(1)
    # ser.write(b'L')
    # time.sleep(1)
# When everything done, release the capture
cap.release()
out.release()
cv2.destroyAllWindows()