'''
Image and video processing of the experimental data from granular collapses.

Author: YANG Gengchao (The University of Hong Kong)
'''

# python libraries
import os
import pickle
import cv2

# user-defined functioons
from process_functions import *    # import the class to correct the perspectives

## Capture the video and create the video object for output
# capture the video
capVid = cv2.VideoCapture(folderName+fileName)
orgVidFrameRate = capVid.get(cv2.CAP_PROP_FPS)

# define the codec and create video writer object
newVidWidth = int(cm2px*cropVidWidth)
newVidHeight = int(cm2px*cropVidHeight)
fourcc = cv2.VideoWriter.fourcc(*'DIVX')
newVid = cv2.VideoWriter(folderName+newVidName, fourcc, newVidFrameRate, (newVidWidth, newVidHeight), 0)

# find whether the video is captured coorrectly
if not capVid.isOpened():
    print('Error capturing the video. Check the folder name and file name.')

# determine the frame associated with the start of the column collapse
if frameStart != 1:
    for frameID in range(1, frameStart):
        _, frame = capVid.read()            # read the preparatioon stage

## Process the raw video and save to the new video frame-by-frame
# cycle through all frames
for frameID in range(frameStart, frameEnd):
    ret, frame = capVid.read()              # read frame-by-frame, note unpacking the tuple here

    if ret == True:
        # convert to the grey scale images
        frameGray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        # if the first frame, select the calibration points
        if frameID == frameStart:
            if os.path.isfile(folderName+calibName):
                # load the calibration points
                print('Calibration points have been selected previously, so import them.')
                fid = open(folderName+calibName, 'rb')
                cornerCoords = pickle.load(fid)
                fid.close()
            else:
                print('Select the calibration points to correct the perspective error.')
                cornerCoords = []           # a list to store the corners
                calibration_points(frameGray, cornerCoords)
                # store the calibration points
                fid = open(folderName+calibName, 'wb')
                pickle.dump(cornerCoords, fid)
                fid.close()
 
        # calibrate the frame regarding camera distortions
        frameCalib = perspective_transform(frameGray, cornerCoords, calibBoxWidth, calibBoxHeight, cm2px)

        # crop the image to the region of interest
        frameCrop = crop_frame(frameCalib, cropVidWidth, cropVidHeight, calibBoxHeight, cm2px)

        # put text on videos to show the basic information
        frameOut = add_info(frameCrop, frameID, frameStart, orgVidFrameRate, newVidFrameRate)

        # write the processed frame - write BGR frames only!!!!!!!!
        frameCalib = cv2.cvtColor(frameOut, cv2.COLOR_GRAY2BGR)
        cv2.imshow('frame', frameCalib)
        newVid.write(frameOut)

        # wait key input to slow down the video and end the job if wanted
        if cv2.waitKey(1) & 0xFF == 27:     # increase the wait time in milliseconds to slow down the play
            break
    else:
        break                   # end of the video

# save the last frame as the final deposit
print('Saving the final deposit...')
cv2.imwrite(folderName+depositFigName, frameOut)

# release all video objects if job is finished
capVid.release()                    # release the raw video after processing
newVid.release()                    # release the new video after processing
cv2.destroyAllWindows()             # close all the windows