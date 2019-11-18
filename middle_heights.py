'''
Extract the heights of the final deposit at 1/3, 1/2 and 2/3 of the final runout distance.

Author: YANG Gengchao (The University of Hong Kong)
'''

import cv2
import numpy as np
import os
import pickle
from matplotlib import pyplot as plt

## Import the final deposit
finalDeposit = cv2.imread(folderName+depositFigName, 0)   # read in the grey scale image

## Manually pick the free surface of the final deposit
if os.path.isfile(folderName+depositName):
    print('Free surface data have been saved previously. So import them.')
    fid = open(folderName+depositName, 'rb')
    surfCoords = pickle.load(fid)
    fid.close()
else:
    print('Free surface data have not been saved previously. So select them.')

    # initialize a list to store the coordinates of the granular free-surface
    surfCoords = []

    # create a mouse callback function
    def pick_surface(event, x, y, flag, param):
        if event == cv2.EVENT_LBUTTONDOWN:
            cv2.circle(finalDeposit, (x,y), 6, (0,0,0), -1)
            surfCoords.append((x, y))       # mutable object can be changed in functions!!!
            cv2.destroyAllWindows()                     # close the window by left click

    # select the free surface points
    print('Press the ESC key to end the selection for free-surface points.')
    while True:
        # create a window and bind it to the mouse callback function
        cv2.namedWindow('deposit', cv2.WINDOW_NORMAL)
        cv2.setMouseCallback('deposit', pick_surface)   # the binding is lost if the window is closed
        cv2.resizeWindow('deposit', (newVidWidth, newVidHeight))

        # display the final deposit
        cv2.imshow('deposit', finalDeposit)

        # hold the image for action
        if cv2.waitKey(0) & 0xFF == 27:
            break

    # dump the free surface data
    fid = open(folderName+depositName, 'wb')
    pickle.dump(surfCoords, fid)
    fid.close()

## Calculate the heights in the middle of the final deposit
surfCoords = np.array(surfCoords)
surfCoordsX = surfCoords[:, 0]
surfCoordsY = surfCoords[:, 1]

locs = np.array([runout[-1]/3, runout[-1]/2, 2*runout[-1]/3])*cm2px
h = np.interp(locs, surfCoordsX, surfCoordsY)

# convert to integer piixels
locs = locs.astype(int)
h = h.astype(int)

## Display the original image together with the heights
cv2.line(finalDeposit, (locs[0], newVidHeight), (locs[0], h[0]), (0,0,0), 2)
cv2.line(finalDeposit, (locs[1], newVidHeight), (locs[1], h[1]), (0,0,0), 2)
cv2.line(finalDeposit, (locs[2], newVidHeight), (locs[2], h[2]), (0,0,0), 2)

cv2.imshow('deposit', finalDeposit)
cv2.waitKey(0)
cv2.destroyAllWindows()

## Output the heights
print('******Height of final deposit when x = 1/3L_f: '+str((newVidHeight-h[0])/cm2px)+' cm')
print('******Height of final deposit when x = 1/2L_f: '+str((newVidHeight-h[1])/cm2px)+' cm')
print('******Height of final deposit when x = 2/3L_f: '+str((newVidHeight-h[2])/cm2px)+' cm')