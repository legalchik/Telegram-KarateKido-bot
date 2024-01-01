import mss
import cv2
import numpy
from time import sleep
import pyautogui
import random


pyautogui.PAUSE = 0
sct = mss.mss()

sleep(2)

right = False
x = 1045
y = 990

dimensions_left = {
    'left': 805,
    'top': 600,
    'width': 135,
    'height': 130
}

dimensions_right = {
    'left': 988,
    'top': 600,
    'width': 135,
    'height': 130
}

short_right = cv2.imread("short_right.jpg")
short_left = cv2.imread("short_left.jpg")
long_right = cv2.imread("long_right.jpg")
long_left = cv2.imread("long_left.jpg")

w = long_left.shape[1]
h = long_left.shape[0]


scr = numpy.array(sct.grab(dimensions_right))

while True:

    if right:
        scr = numpy.array(sct.grab(dimensions_left))
        short_wood = short_left
        long_wood = long_left
    else:
        scr = numpy.array(sct.grab(dimensions_right))
        short_wood = short_right
        long_wood = long_right

    scr_remove = scr[:,:,:3]

    short_result = cv2.matchTemplate(scr_remove, short_wood, cv2.TM_CCOEFF_NORMED)
    long_result = cv2.matchTemplate(scr_remove, long_wood, cv2.TM_CCOEFF_NORMED)

    _, max_val_short, _, max_loc_short = cv2.minMaxLoc(short_result)
    _, max_val_long, _, max_loc_long = cv2.minMaxLoc(long_result)

    src = scr.copy()

    if max_val_short > .77 or max_val_long > .77:
        right = not right
        if right:
            sleep(random.uniform(0.03, 0.05))
            x=860
        else:
            sleep(random.uniform(0.03, 0.05))
            x=1045
        sleep(0.1)
            

        cv2.rectangle(scr, max_loc_short, (max_loc_short[0] + w, max_loc_short[1] + h), (0,255,255), 2)
        cv2.rectangle(scr, max_loc_long, (max_loc_long[0] + w, max_loc_long[1] + h), (0,255,255), 2)

    key = cv2.waitKey(1) & 0xFF
    if key == ord('q'):
        cv2.destroyAllWindows()
        exit()


    cv2.imshow('Screen Shot', scr)
    cv2.setWindowProperty("Screen Shot", cv2.WND_PROP_TOPMOST, 1)
    pyautogui.click(x=x, y=y)
    sleep(0.02)
