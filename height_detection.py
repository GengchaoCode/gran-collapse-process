'''
Manually pick the residual height and save them in a list of height.

Author: YANG Gengchao (The University of Hong Kong)
'''

import cv2
import numpy as np
import os
import pickle
from matplotlib import pyplot as plt

## Capture the video and define the data acquisition frequency and initialize the height list
# create a video capture object to access files containing video data
newVid = cv2.VideoCapture(folderName+newVidName)

# time and frames
time = np.arange(vidFrameTotal)/orgVidFrameRate
df = int(dt*orgVidFrameRate)
t = time[0:vidFrameTotal:df]                        # numpy slicing - start:end:step

# create a 1d numpy array to store the front position
height = []

## Detect and save the front positions
# load the front position if saved previously
if os.path.isfile(folderName+heightName):
    print('Height data have been saved previously. So import them.')
    fid = open(folderName+heightName, 'rb')
    height = pickle.load(fid)
    fid.close()
else:
    print('Height data have not been saved previously. So select them.')

    # Cycle through all the frames and pick the front position
    for frameID in np.arange(vidFrameTotal):
        ret, frame = newVid.read()
        
        if ret == True:
            if frameID%df == 0:
                # create a mouse callback function
                def pick_height(event, x, y, flag, param):
                    if event == cv2.EVENT_LBUTTONDOWN:
                        height.append(newVidHeight-y)
                        cv2.destroyAllWindows()         # close the window after left click
                
                # create a window and bind it to the callback function
                cv2.namedWindow('frame', cv2.WINDOW_NORMAL)
                cv2.setMouseCallback('frame', pick_height)

                # display the image and select the front
                cv2.imshow('frame', frame)
                cv2.waitKey(0) & 0xFF                   # hold the frame for key or click input
        
    # dump the height data
    fid = open(folderName+heightName, 'wb')
    pickle.dump(height, fid)
    fid.close()

# release the video when the job is finished
newVid.release()

# conver pixcels to centi-meters
height = np.array(height)
height = height/cm2px
print('******Final residual height: '+str(height[-1])+' cm')

## Plot the normalized height against the time
# calculate the normalized height
H_tilde = (height)/runout[0]
plt.plot(t, H_tilde)
plt.xlabel('$t$ (s)')
plt.ylabel('$H/L_i$')
plt.show()