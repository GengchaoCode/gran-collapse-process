'''
Image and video processing of the experimental data from granular collapses.

Author: YANG Gengchao (The University of Hong Kong)
'''
import os
import pickle
import cv2
os.system('cls')                    # clear the screen

## Specify the parameters for video processing and free-surface detection
# parameters related to file naming and location
folderName = 'D:\\Experimental_Results\\2019_HKU_PRFluids_columnSizeEffects\\T1b_AR0.50W18_GB1.44mm_Li3.0cm_Hi1.50cm_SP80Cw_20190325\\'   # folder where the video exists
fileName = 'IMG_1694.MOV'           # video name
paramName = 'input_parameters.dat'  # name for the saved input parameters
newVidName = 'video_calibrated.avi' # name of the output video

# parameters related to video processing
if os.path.isfile(folderName+paramName):
    print('Input parameters have been saved previously, so import them. ')
    fid = open(folderName+paramName, 'rb')
    input_list = pickle.load(fid)
    fid.close()
    
    # unpack the input list
    caliBoxHeight, caliBoxLength, cropVidHeight, cropVidLength, axisInterval, newVidFrameRate, frameStart, frameEnd = input_list
else:
    print('Input parameters have not been saved previously, so specify them.')
    # specify the size of the calibration box
    caliBoxHeight = 9.6             # unit: cm
    caliBoxLength = 15.2            # unit: cm

    # specify the size of the cropped video
    cropVidHeight = 6               # unit: cm
    cropVidLength = 2*cropVidHeight # unit: cm
    axisInterval = int(cropVidHeight/3) # unit: cm

    # specify the control parameters for the output video
    newVidFrameRate = 12            # unit: FPS
    frameStart = 1                  # first frame, set to 1 if not sure
    frameEnd = frameStart+60        # final frame, set to 1 if not sure

    # save the input parameters
    input_list = [caliBoxHeight, caliBoxLength,
                  cropVidHeight, cropVidLength, axisInterval,
                  newVidFrameRate, frameStart, frameEnd]
    fid = open(folderName+paramName, 'wb')
    pickle.dump(input_list, fid)
    fid.close()

## Capture the video and create the video object for output
# capture the video
capVid = cv2.VideoCapture(folderName+fileName)
capVidWidth = capVid.get(cv2.CAP_PROP_FRAME_WIDTH)
capVidHeight = capVid.get(cv2.CAP_PROP_FRAME_HEIGHT)

# define the codec and create video writer object
fourcc = cv2.VideoWriter.fourcc(*'DIVX')
newVid = cv2.VideoWriter(folderName+newVidName, fourcc, newVidFrameRate, (int(capVidWidth), int(capVidHeight)))

# process the raw video and save to the new video frame-by-frame
if not capVid.isOpened():
    print('Error capturing the video. Check the folder name and file name.')
else:
    while(True):                    # cycle through all the frames
        ret, frame = capVid.read()  # read frame-by-frame, note unpacking the tuple here

        if ret == True:
            # convert to the grey scale images
            frameGray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

            # display the frame
            cv2.namedWindow('frame', cv2.WINDOW_NORMAL)
            cv2.imshow('frame', frameGray)
            cv2.resizeWindow('frame', 960, 540) # shrink the window do show the whole frame

            # write the processed frame - write BGR frames only!!!!!!!!
            newVid.write(frame)

            # wait key input to slow down the video and end the job if wanted
            if cv2.waitKey(1) & 0xFF == 27:     # increase the wait time in milliseconds to slow down the play
                break
        else:
            break                   # end of the video

# release all video objects if job is finished
capVid.release()                    # release the raw video after processing
newVid.release()                    # release the new video after processing
cv2.destroyAllWindows()             # close all the windows