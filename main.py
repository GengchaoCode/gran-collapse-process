'''
Image and video processing of the experimental data from granular collapses.

Author: YANG Gengchao (The University of Hong Kong)
'''
# python libraries
import os
import pickle
import cv2
os.system('cls')                    # clear the screen

# user-defined functioons
from camera_calibration import *    # import the class to correct the perspectives

## Specify the parameters for video processing and free-surface detection
# parameters related to file naming and location
folderName = 'D:\\Experimental_Results\\2019_HKU_PRFluids_columnSizeEffects\\T1b_AR0.50W18_GB1.44mm_Li3.0cm_Hi1.50cm_SP80Cw_20190325\\'   # folder where the video exists
fileName = 'IMG_1694.MOV'                   # video name
paramName = 'input_parameters.dat'          # name for the saved input parameters
calibName = 'calib_corners.dat'             # name foor the saved calibration points (corners of a rectangle)
newVidName = 'video_calibrated.avi'         # name of the output video

# parameters related to video processing
if os.path.isfile(folderName+paramName):
    print('Input parameters have been saved previously, so import them.')
    fid = open(folderName+paramName, 'rb')
    input_list = pickle.load(fid)
    fid.close()
    
    # unpack the input list
    calibBoxHeight, calibBoxWidth, cropVidHeight, cropVidWidth, axisInterval, cm2px, newVidFrameRate, frameStart, frameEnd = input_list
else:
    print('Input parameters have not been saved previously, so specify them.')
    # specify the size of the calibration box
    calibBoxHeight = 9.6                    # unit: cm
    calibBoxWidth = 15.2                    # unit: cm

    # specify the size of the cropped video
    cropVidHeight = 3                       # unit: cm
    cropVidWidth = 2*cropVidHeight          # unit: cm
    axisInterval = int(cropVidHeight/3)     # unit: cm
    cm2px = 100                             # number of pixels per cm in video

    # specify the control parameters for the output video
    newVidFrameRate = 12                    # unit: FPS
    frameStart = 120                        # first frame, set to 1 if not sure
    frameEnd = frameStart+60                # final frame, set to 1 if not sure

    # save the input parameters
    input_list = [calibBoxHeight, calibBoxWidth,
                  cropVidHeight, cropVidWidth, axisInterval, cm2px,
                  newVidFrameRate, frameStart, frameEnd]
    fid = open(folderName+paramName, 'wb')
    pickle.dump(input_list, fid)
    fid.close()

## Capture the video and create the video object for output
# capture the video
capVid = cv2.VideoCapture(folderName+fileName)

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
                fid = open(folderName+calibName, 'rb')
                cornerCoords = pickle.load(fid)
                fid.close()
            else:
                cornerCoords = []           # a list to store the corners
                calibration_points(frameGray, cornerCoords)
                # store the calibration points
                fid = open(folderName+calibName, 'wb')
                pickle.dump(cornerCoords, fid)
                fid.close()
 
        # calibrate the frame regarding camera distortions
        frameCalib = perspective_transform(frameGray, cornerCoords, calibBoxWidth, calibBoxHeight, cm2px)
        print(frameCalib.shape[:2])

        # crop the image to the region of interest
        frameCrop = crop_frame(frameCalib, cropVidWidth, cropVidHeight, calibBoxHeight, cm2px)

        # convert the image to black and white - thresholding
        

        # display the processed image
        cv2.imshow('frameCrop', frameCrop)
      
        # write the processed frame - write BGR frames only!!!!!!!!
        frameCalib = cv2.cvtColor(frameCrop, cv2.COLOR_GRAY2BGR)
        newVid.write(frameCrop)

        # wait key input to slow down the video and end the job if wanted
        if cv2.waitKey(1) & 0xFF == 27:     # increase the wait time in milliseconds to slow down the play
            break
    else:
        break                   # end of the video

# release all video objects if job is finished
capVid.release()                    # release the raw video after processing
newVid.release()                    # release the new video after processing
cv2.destroyAllWindows()             # close all the windows