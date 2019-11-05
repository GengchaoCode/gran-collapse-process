import cv2


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


def perspective_transform():
    """Calibrate the distorted frame due to the perspective effects."""

    print('hello world')