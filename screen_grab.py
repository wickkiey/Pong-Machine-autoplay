import pyautogui
import cv2 as cv
import numpy as np
import pyautogui as pg
import time
import threading

class screen_grab:
    #Class variables
    roi = []
    ball = []
    last_ball = []
    left = []
    right = []
    board = []
    last_roi = None
    current_control = None
    def __init__(self):
        self.roi = [0,0,0,0]
        self.last_ball = [0,0]
        c = threading.Thread(target=self.control_up_down)
        c.start()

    def get_focus_area(self):
        dummy = input()
        scrn = pyautogui.screenshot()
        img = np.array(scrn)
        print("start screen grabbing")

        while 1:
            cv.imshow('iwin', img)
            if cv.waitKey(1) & 0xFF == ord('q'):
                break
            cv.setMouseCallback('iwin', self.onMouse)
            if ((self.roi[0] > 0) and (self.roi[2] > 0)):
                print(self.roi)
                cv.destroyAllWindows()
                # roi[3] = roi[3]-roi[1]
                # roi = [0,0,0,0]
                break;

    def onMouse(self, event, x, y, flags, param):
        # print(img[x,y]
        if event == cv.EVENT_LBUTTONDOWN:
            print('l dwn')
            print(x, y)
            self.roi[0:2] = [x, y]
        if event == cv.EVENT_LBUTTONUP:
            print('l up')
            print(x, y)
            self.roi[2:4] = [x, y]
            print(self.roi)

    def grap_roi(self):
        print("Capture ROI")
        #Change to height width from pixels
        self.roi[2] -= self.roi[0]
        self.roi[3] -= self.roi[1]
        while 1:
            scrn = pyautogui.screenshot(region=self.roi)
            img = np.array(scrn)
            self.get_objects(img)
            image = self.control_right_bar(img)
            #image = self.control_mouse(img)
            cv.imshow('ROI_region', image)
            if cv.waitKey(1) & 0xFF == ord('q'):
                break
        cv.destroyAllWindows()

    def get_objects(self,img):

        gray = cv.cvtColor(img, cv.COLOR_BGR2GRAY)
        gray_clone = gray.copy()
        if self.last_roi is None:
            self.last_roi = gray
        else:
            h, w = gray.shape[:2]
            gray[0:h,100:w-100] = cv.subtract(gray[0:h,100:w-100],self.last_roi[0:h,100:w-100])
            self.last_roi = gray_clone
        cv.imshow("subtracted_gray",gray)
        blurred = cv.GaussianBlur(gray, (3, 3), 0)
        _, thresh = cv.threshold(blurred, 127, 255, cv.THRESH_BINARY)
        im2, contours, hierarchy = cv.findContours(thresh.copy(), cv.RETR_EXTERNAL, cv.CHAIN_APPROX_SIMPLE)
        try:
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
                    cv.circle(img, (cX, cY), 5, (0, 0, 255))
                    # a square will have an aspect ratio that is approximately
                    # equal to one, otherwise, the shape is a rectangle
                    if ar >= 0.95 and ar <= 1.05:
                        print("Target position acquired")
                        self.ball = [cX, cY]
                    else:
                        self.board.append([cX, cY])
        except:
            print("Error in calculating moments")
        if (len(self.board) > 1):
            self.board = sorted(self.board)
            self.left = self.board[0]
            self.right = self.board[1]
        self.board = []

        print(self.ball,self.left,self.right)

    def control_right_bar(self, img):
        if(len(self.ball) >1 and len(self.right) > 1):
            cv.circle(img, (self.ball[0],self.ball[1]), 30, (255, 0, 0),3)
            cv.circle(img, (self.right[0],self.right[1]), 10, (255, 255, 0),5)
            if(self.last_ball[0] > self.ball[0]):
                self.current_control = 'idle'
                cv.putText(img, 'Target Moving ::Left', (20, 50), cv.FONT_HERSHEY_PLAIN, 2, (0, 255, 0), 2, cv.LINE_AA)
                cv.putText(img, 'Bar : Idle', (20, 80), cv.FONT_HERSHEY_PLAIN, 2, (0, 255, 0), 2, cv.LINE_AA)
            else:
                height_diff = abs(self.ball[1] - self.right[1])
                if (height_diff > 5):
                    if (abs(self.ball[0] - self.right[0]) < 70):
                        self.current_control = "idle"
                    elif (self.ball[1] < self.right[1]):
                        # print("move up")
                        self.current_control = 'up'
                        cv.putText(img, 'Bar : Move Up', (20, 80), cv.FONT_HERSHEY_PLAIN, 2, (0, 255, 0), 2, cv.LINE_AA)
                    else:
                        #print("move down")
                        self.current_control = 'down'
                        cv.putText(img, 'Bar : Move Down', (20, 80), cv.FONT_HERSHEY_PLAIN, 2, (0, 255, 0), 2, cv.LINE_AA)

                cv.putText(img, 'Target Moving ::Right', (20, 50), cv.FONT_HERSHEY_PLAIN, 2, (0, 255, 0), 2, cv.LINE_AA)
            self.last_ball = self.ball

        return img

    def control_mouse(self,img):
        if(len(self.ball) >1 and len(self.right) > 1):
            pg.moveTo(None,(self.ball[1]+self.roi[1]))

            cv.circle(img, (self.ball[0],self.ball[1]), 10, (0, 0, 255))
            cv.circle(img, (self.right[0],self.right[1]), 10, (0, 0, 255))

        return img

    def control_up_down(self):
        while(1):
            if self.current_control == 'idle':
                pg.keyUp('down')
                pg.keyUp('up')
            elif self.current_control == "up":
                print("up from thread")
                pg.keyUp('down')
                pg.keyDown('up')
                # time.sleep(.0001)
                # pg.keyUp('up')
            elif self.current_control == "down":
                print("down from thread")
                pg.keyUp('up')
                pg.keyDown('down')
                # time.sleep(.0001)
                # pg.keyUp('down')