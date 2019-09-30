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


#----------------------------------------------------------------------
# set boundary boxes for movement tracking
cam_width = 640
cam_height = 480
# top left of image: [x = 0, y = 0]
# bottom right of image: [x = 640, y = 480]
boundary_box_1_begin = (0,0)
boundary_box_1_end = (207,480)  # allow for 3 pixel border on each side
boundary_box_1_color = (255,0,0)

boundary_box_2 = [211,0,420,480]
boundary_box_2_begin = (211,0)
boundary_box_2_end = (417,480)  # allow for 3 pixel border on each side
boundary_box_2_color = (0,255,0)

boundary_box_3 = [421,0,640,480]
boundary_box_3_begin = (421,0)
boundary_box_3_end = (637,480)  # allow for 3 pixel border on each side
boundary_box_3_color = (0,0,255)

# draw the boundary boxes on the base image
img = cv2.imread(base_image_filename, cv2.IMREAD_COLOR)
cv2.rectangle(img, boundary_box_1_begin, boundary_box_1_end, \
    boundary_box_1_color, 3)
cv2.rectangle(img, boundary_box_2_begin, boundary_box_2_end, \
    boundary_box_2_color, 3)
cv2.rectangle(img, boundary_box_3_begin, boundary_box_3_end, \
    boundary_box_3_color, 3)

# cv2.imshow('base_image', img)

#----------------------------------------------------------------------
# Capture frame-by-frame
ret, frame1 = cap.read() # can i do this just comparing base image?
ret, frame2 = cap.read()

while(True):
    diff = cv2.absdiff(frame1, frame2)
    gray = cv2.cvtColor(diff, cv2.COLOR_BGR2GRAY)
    blur = cv2.GaussianBlur(gray, (5,5), 0)
    _, thresh = cv2.threshold(blur, 20, 255, cv2.THRESH_BINARY)
    dilated = cv2.dilate(thresh, None, iterations=3)
    contours, _ = cv2.findContours(dilated, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

    # cv2.drawContours(frame1, contours, -1, (0,255,0), 2)
    for contour in contours:
        (x, y, w, h) = cv2.boundingRect(contour)

        if cv2.contourArea(contour) < 3000:
            continue

        cv2.rectangle(frame1, (x, y), (x+w, x+h), (0,255,0), 2)

    # Our operations on the frame come here
    # gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    # Display the resulting frames
    # cv2.imshow('frame1',gray)
    cv2.imshow('frame1_feed', frame1)
    frame1 = frame2
    ret, frame2 = cap.read()

    out.write(frame1)

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