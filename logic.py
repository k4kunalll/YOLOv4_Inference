
from os import X_OK
from statistics import mean, median
from cv2 import cv2
import collections
import time
# from numba import jit, vectorize

# @jit(forceobj=True)
def analyse(frame, rois, frame_no):
    # rois = [[xmin, ymin, xmax, ymax, class_id]]
    analysis = {}
    roi_upper = 200  # upper ROI line  600
    roi_lower = 300  # lower ROI line  700
    roi_left = 0  # vertical          10
    roi_right = 800  # vertical       2000


    cv2.line(frame, (roi_left, roi_upper), (roi_right, roi_upper), (0, 255, 0), 1)  # green roi
    cv2.line(frame, (roi_left, roi_lower), (roi_right, roi_lower), (0, 255, 0), 1)  # blue roi
    
    cv2.line(frame, (roi_left, roi_upper), (roi_left, roi_lower), (0, 0, 255), 1)  # red roi
    cv2.line(frame, (roi_right, roi_upper), (roi_right, roi_lower), (0, 0, 255), 1)  # red roi

    for roi in rois:
        # creating the centroid
        centroid = (int((roi[0] + roi[2]) / 2), int((roi[1] + roi[3]) / 2))
        # if centroid is inside the roi region
        if (roi[4] == 0 or roi[4] == 1) and roi_upper < centroid[1] < roi_lower and roi_left < centroid[0] < roi_right:
            pass
        
    """
    Write YOUR LOGIC HERE
    """

    analysis2 = 0
    analysis["total_count"] = 0
    analysis["frame_no"] = frame_no

    return analysis, frame, rois, frame_no
    
def increment(y, flag):
    if flag == 'data':
        y += 30
    elif flag == 'data2':
        y += 10
    elif flag == 'line':
        y += 40
    return y

def write_analysis(frame,analysis):
    font = cv2.FONT_HERSHEY_SIMPLEX
    start_y = 20

    # boxes Count 
    cv2.putText(frame, "Total Counted" + ":" + str(analysis["total_count"] ), (20, 20), font, 0.75, (255, 255, 255), 3)
    cv2.putText(frame, "Total Counted" + ":" + str(analysis["total_count"] ), (20, 20), font, 0.75, (0, 0 ,0), 2)
    start_y = increment(start_y, 'data')

    cv2.putText(frame, "Frames" + ":" + str(analysis["frame_no"]), (20, 60), font, 0.75, (255, 255, 255), 3)
    cv2.putText(frame, "Frames" + ":" + str(analysis["frame_no"]), (20, 60), font, 0.75, (0, 0 ,0), 2)
    start_y = increment(start_y, 'data')
