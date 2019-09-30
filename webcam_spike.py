import imutils
from imutils.video import VideoStream
import argparse
import numpy as np
import cv2
import serial
import time
import datetime
import os


# ser = serial.Serial('COM3', 9600)


def construct_file():
    dt = datetime.datetime.now()
    # https://tecadmin.net/get-current-date-time-python/
    # https://docs.python.org/3/library/datetime.html
    # print(dt)
    # print ("Current Year is: %d" % dt.year)
    # print ("Current Month is: %d" % dt.month)
    # print ("Current Day is: %d" % dt.day)
    # print ("Current Hour is: %d" % dt.hour)
    # print ("Current Minute is: %d" % dt.minute)
    # print ("Current Second is: %d" % dt.second)

    camtime = str(dt.year) + "_"\
        +str(dt.month) + "_"\
        +str(dt.day) + "_"\
        +str(dt.hour) + "_"\
        +str(dt.minute) + "_"\
        +str(dt.second)

    fileloc = os.getcwd()
    camfile = os.path.join(fileloc,camtime)
    return camfile


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
# get the base image time stamp
filename = construct_file()
out_filename = filename + ".avi"
base_image_filename = filename + ".jpg"
# set up the video to be saved
out = cv2.VideoWriter(out_filename, fourcc, 20.0, (640,480))
# save the base image
cv2.imwrite(base_image_filename, base_image)


# set boundary boxes for movement tracking
cam_width = 640
cam_height = 480
# top left of image: [x = 0, y = 0]
# bottom right of image: [x = 640, y = 480]
boundary_box_1 = [0,0,210,480]
boundary_box_2 = [211,0,420,480]
boundary_box_3 = [421,0,640,480]


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