import cv2
import numpy as np


def calibration_points(frameGray, cornerCoords):
    """Select four calibration points from the image and store them in a list"""
    # mouse callback function
    def select_points(event, x, y, flags, param):
        if event == cv2.EVENT_LBUTTONDOWN:
            cv2.circle(frameGray, (x,y), 10, (0,0,255), -1)
            cornerCoords.append((x,y))      # mutable object can be changed in functions!!!

    # create a window and bind it to the callback function
    cv2.namedWindow('frame', cv2.WINDOW_NORMAL)
    cv2.setMouseCallback('frame', select_points)

    # display the image and select the points
    info = ['first', 'second', 'third', 'forth']
    for i in range(0,4):
        print('Press any key to log the {} calibration point'.format(info[i]))
        cv2.imshow('frame', frameGray)
        cv2.resizeWindow('frame', 1280, 720) # shrink the window do show the whole frame

        # hold the frame for key input
        cv2.waitKey(0) & 0xFF
    
    # close the current window
    cv2.destroyAllWindows()


def perspective_transform(frameGray, cornerCoords, calibBoxWidth, calibBoxHeight, cm2px):
    """Calibrate the distorted frame due to the perspective effects."""

    # convert list of calibration points to a numpy array
    pts_src = np.array(cornerCoords, dtype=np.float32)

    # define the destination points according to the dimension of calibration box
    col_left = cm2px
    col_right = cm2px*(calibBoxWidth+1)
    row_top = cm2px
    row_bottom = cm2px*(calibBoxHeight+1)
    pts_dst = np.float32([[col_left, row_top], [col_right, row_top], [col_left, row_bottom], [col_right, row_bottom]])

    # calculate the transformation matrix and correct the perspective distortion
    calibWidth = int(cm2px*(calibBoxWidth+2))       # width of the calibrated frame
    calibHeight = int(cm2px*(calibBoxHeight+2))     # height of the calibrated frame
    transformM = cv2.getPerspectiveTransform(pts_src, pts_dst)
    frameCalib = cv2.warpPerspective(frameGray, transformM, (calibWidth, calibHeight))
    
    return frameCalib


def crop_frame(frameCalib, cropVidWidth, cropVidHeight, calibBoxHeight, cm2px):
    """Crop the frame to the region of interest"""

    # determine the bound of the cropped image
    col_left = int(cm2px)
    col_right = col_left+int(cm2px*cropVidWidth)

    calibHeight = int(cm2px*(calibBoxHeight+2))     # height of the calibrated frame
    row_top = calibHeight-int(cm2px)-int(cm2px*cropVidHeight)
    row_bottom = row_top+int(cm2px*cropVidHeight)

    # crop the image using numpy slicing
    frameCrop = frameCalib[row_top:row_bottom, col_left:col_right]

    return frameCrop


def add_info(img, frameID, frameStart, orgVidFrameRate, newVidFrameRate):
    """Add text information to the processed video"""

    # information to show
    time = (frameID-frameStart)/newVidFrameRate
    info1 = 'Time: '+'{:.3f}'.format(time)+' s'
    info2 = 'Current frame ID: '+str(frameID)
    info3 = 'Original video frame rate: '+str(orgVidFrameRate)+' fps'
    info4 = 'Output video frame rate: '+str(newVidFrameRate)+' fps'
    info = [info1, info2, info3, info4]

    # size of the image
    height, width = img.shape           # image is store as numpy arrays
    linespace = 0.05*height

    # basic parameters for drawing texts
    font = cv2.FONT_HERSHEY_COMPLEX     # font type
    fs = 0.7                            # font scale
    fc = (255, 255, 0)                  # font color = yellow
    thick = 1                           # thickness of the strokes
    lt = cv2.FILLED                     # line type
    
    # loop 4 times to write four lines of information
    orgX = int(0.63*width)
    for i in range(4):
        orgY = int(0.05*height+i*linespace)
        frameOut = cv2.putText(img, info[i], (orgX, orgY), font, fs, fc, thick, lt)

    return frameOut