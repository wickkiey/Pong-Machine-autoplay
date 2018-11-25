import cv2 as cv
import numpy

def show_img(image):
    cv.imshow('imagem',image)
    cv.waitKey(0)
    cv.destroyAllWindows()

img = cv.imread("pong.JPG",-1)
img.shape

#Shape based detection

#Find countour
gray = cv.cvtColor(img,cv.COLOR_BGR2GRAY)
blurred = cv.GaussianBlur(gray,(3,3),0)
_, thresh = cv.threshold(blurred,127,255,cv.THRESH_BINARY)
im2, contours, hierarchy = cv.findContours(thresh.copy(),cv.RETR_EXTERNAL,cv.CHAIN_APPROX_SIMPLE)

ball = []
left =[]
right =[]
board = []

for c in contours:
    # compute the center of the contour, then detect the name of the
    # shape using only the contour
    M = cv.moments(c)
    cX = int((M["m10"] / M["m00"]))
    cY = int((M["m01"] / M["m00"]))
    peri = cv.arcLength(c, True)
    approx = cv.approxPolyDP(c, 0.04 * peri, True)

    if len(approx) == 4:
    # compute the bounding box of the contour and use the
    # bounding box to compute the aspect ratio
        (x, y, w, h) = cv.boundingRect(approx)
        ar = w / float(h)
        cv.circle(img,(cX,cY),5,(0,0,255))
        # a square will have an aspect ratio that is approximately
        # equal to one, otherwise, the shape is a rectangle
        if ar >=0.95 and ar <= 1.05:
            print("square")
            ball=[cX,cY]
        else:
            board.append([cX,cY])

    if (len(board) > 1):
        board = sorted(board)
        left = board[0]
        right = board[1]
    board = []


import time
import pyautogui as pg

for i in range(10):
    time.sleep(.5)
    pg.keyUp('up')
    time.sleep(.03)
    pg.keyDown('up')
    pg.keyUp('down')
    time.sleep(.03)
    pg.keyDown('down')