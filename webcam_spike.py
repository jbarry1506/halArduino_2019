# currently working tutorials
# https://buildmedia.readthedocs.org/media/pdf/opencv-python-tutroals/latest/opencv-python-tutroals.pdf
# https://www.nongnu.org/avr-libc/user-manual/group__avr__sleep.html
# https://makezine.com/2014/04/23/arduinos-servo-library-angles-microseconds-and-optional-command-parameters/

import imutils
from imutils.video import VideoStream
import argparse
import numpy as np
import cv2
import serial
import time
import datetime
import os
# local import
from ItFuncs import *

# set up the serial port to receive data
    # com3 is test arduino - duemillanove
# ser = serial.Serial('COM3', 115200)
    # com4 is production arduino - UNO
ser = serial.Serial('COM4', 115200)

# camera 1 is the external camera
cap = cv2.VideoCapture(0)
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

def clock_diff(cl_end, cl_begin):
    cl_diff = cl_end - cl_begin
    return cl_diff


def find_center(lb, rb):
    center = rb - ((rb - lb)/2)
    center = int(center)
    return center


def head_angle(cp):
    if cp > 0:
        angle = cp/3.55
    else:
        angle = 0
    # add 210 for the frequency of the servo
    angle = int(angle)+210
    return angle


def eye_angle(cp):
    if cp > 0:
        e_angle = cp/7
    else:
        e_angle = 0
    e_angle = int(e_angle)+260
    return e_angle


# function to reverse head angle for correct rotation of servo
def arduino_head_angle(ha, paha):
    # 300 is approximate middle
    if ha > 300:
        aha = ha - ((ha-300)*2)
    elif ha < 300:
        aha = ha + ((300-ha)*2)
    else:
        # head angle = 300
        aha = ha

    if paha > aha:
        change = paha - aha
    elif paha < ha:
        change = aha - paha
    else:
        change = 0

    print("aha = ",aha,"\tpha = ",paha)
        
    if change > 5:
        if aha > paha:
            aha = paha + 5
        elif aha < paha:
            aha = paha -5

    return aha


# function to send serial data
def send_serial(data, part):
    for i in str(data):
        ser.write(b'{%d}'%int(i))
        time.sleep(0.025)
    if part == 'head':
        ser.write(b's')
    elif part == 'eyes':
        ser.write(b'e')


#----------------------------------------------------------------------
# set boundary boxes for movement tracking
cam_width = 640
cam_height = 480
# top left of image: [x = 0, y = 0]
# bottom right of image: [x = 640, y = 480]
boundary_box_1 = [0,0,204,480]
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

bb1_active = False
bb2_active = False
bb3_active = False
end_clock_difference = 0
start_clock = time.clock()
previous_arduino_head_point = 210

while(True):
    diff = cv2.absdiff(frame1, frame2)
    gray = cv2.cvtColor(diff, cv2.COLOR_BGR2GRAY)
    blur = cv2.GaussianBlur(gray, (5,5), 0)
    _, thresh = cv2.threshold(blur, 20, 255, cv2.THRESH_BINARY)
    dilated = cv2.dilate(thresh, None, iterations=3)
    contours, _ = cv2.findContours(dilated, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

    # cv2.drawContours(frame1, contours, -1, (0,255,0), 2)
    for contour in contours:
        current_clock = time.clock()
        (x, y, w, h) = cv2.boundingRect(contour)

        if cv2.contourArea(contour) < 8000:
            continue

        left_bound = x
        right_bound = x+w
        cv2.rectangle(frame1, (x, y), (x+w, y+h), (0,255,0), 2)
        # print testing for boundaries
        print("left_bound = ",left_bound,"\t right_bound = ",right_bound)

        # find the center of the object detected        
        center_point = find_center(left_bound,right_bound)
        print("center_point = ",center_point)

        # find the angle the head should be pointed to
        head_point = head_angle(center_point)
        print("head_point = ",head_point)


        # recalculate for the arduino head point
        arduino_head_point = arduino_head_angle(head_point, previous_arduino_head_point)
        print("arduino_head_point = ",arduino_head_point)
        previous_arduino_head_point = arduino_head_point

        # get the current frame number - this code is not being used - reference
        # current_frame = cap.get(cv2.CAP_PROP_POS_FRAMES)
        # print("CAP_PROP_POS_FRAMES = ",current_frame)
        # time_diff = int(clock_diff(current_clock,start_clock))


        eyes = eye_angle(center_point)

        send_serial(eyes,'eyes')

        send_serial(arduino_head_point,'head')


        if boundary_box_1[0] < x < boundary_box_3[2]:
            if boundary_box_1[0] < x < boundary_box_2[0]:
                if bb1_active == True:
                    clock_difference = clock_diff(current_clock, start_clock_1)
                    if clock_difference > 1:
                        print(clock_difference)
                else:
                    print("Activate region 1")
                    start_clock_1 = time.clock()
                    bb1_active = True
                    bb2_active = False
                    bb3_active = False
            elif boundary_box_2[0] < x < boundary_box_3[0]:
                if bb2_active == True:
                    clock_difference = clock_diff(current_clock, start_clock_2)
                    if clock_difference > 1:
                        print(clock_difference)
                else:
                    print("Activate region 2")
                    start_clock_2 = time.clock()
                    bb1_active = False
                    bb2_active = True
                    bb3_active = False
            elif boundary_box_3[0] < x < boundary_box_3[2]:
                if bb3_active == True:
                    clock_difference = clock_diff(current_clock, start_clock_3)
                    if clock_difference > 1:
                        print(clock_difference)
                else:
                    print("Activate region 3")
                    start_clock_3 = time.clock()
                    bb1_active = False
                    bb2_active = False
                    bb3_active = True
            else:
                pass
        else:
            end_clock = time.clock()
            end_clock_difference = clock_diff(end_clock, current_clock)
            
    if end_clock_difference > 15:
        # put the arduino to sleep
        print("Putting the arduino to sleep.")

    # Display the resulting frames
    cv2.imshow('frame1',gray)
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