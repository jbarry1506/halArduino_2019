# timing algorithm to move servo along with movement on camera
import time
import random


def set_movement(microseconds):
    beg_micro = 0
    change = 0
    for micro in range(beg_micro,microseconds):
        if (micro%10 == 0):
            change += .01
    return change


servo_pos = 90
start_time = time.clock()
set_motion = 0
count_time = 0
while(count_time < 10):

    randnum = random.randint(-250, 250)
    print("randnum = ", randnum)
    servo_range = range(45,135)

    movement = set_movement(randnum)

    if (randnum < 0) and (servo_pos >= 45):
        set_motion -= movement
        print("set_motion = ", set_motion)
    elif (randnum > 0) and (servo_pos <= 135):
        set_motion += movement
        print("set_motion = ", set_motion)
    else:
        pass

    count_time = time.clock()
