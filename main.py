#Load the class
from screen_grab import screen_grab

#initiate the class
sg  = screen_grab()

#Fix the ROI from the screeen
sg.get_focus_area()

#Let it play
sg.grap_roi()