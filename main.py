'''
Major routine and plot figures.

Author: Yang Gengchao (The University of Hong Kong)
'''

import os
import pickle
os.system('cls')                            # clear the screen

## Which file to process
folderName = 'C:\\Users\\gengc\Desktop\\2019_HKU_PRFluids_columnSizeEffects\\T1b_AR0.50W18_GB1.44mm_Li3.0cm_Hi1.50cm_SP80Cw_20190325\\'   # folder where the video exists
fileName = 'IMG_1694.MOV'                   # video name

## Import and calibrate the video and then save it
# specify the parameters for video processing
paramName = 'input_parameters.dat'          # name for the saved input parameters
calibName = 'calib_corners.dat'             # name foor the saved calibration points (corners of a rectangle)
newVidName = 'video_calibrated.avi'         # name of the output video
runoutName = 'runout.dat'                   # name for the runout data
heightName = 'height.dat'                   # name for the height data
depositFigName = 'final_deposit.png'        # name for the final deposit image
depositName = 'deposit_profile.dat'         # name for the final deposit profile data

# parameters related to video processing
if os.path.isfile(folderName+paramName):
    print('Input parameters have been saved previously, so import them.')
    fid = open(folderName+paramName, 'rb')
    input_list = pickle.load(fid)
    fid.close()
    
    # unpack the input list
    calibBoxHeight, calibBoxWidth, cropVidHeight, cropVidWidth, axisInterval,\
         cm2px, newVidFrameRate, frameStart, vidFrameTotal, frameEnd = input_list
else:
    print('Input parameters have not been saved previously, so specify them.')
    # specify the size of the calibration box
    calibBoxHeight = 9.6                    # unit: cm
    calibBoxWidth = 15.2                    # unit: cm

    # specify the size of the cropped video
    cropVidHeight = 3                       # unit: cm
    cropVidWidth = 2*cropVidHeight          # unit: cm
    axisInterval = int(cropVidHeight/3)     # unit: cm
    cm2px = 200                             # number of pixels per cm in video

    # specify the control parameters for the output video
    newVidFrameRate = 12                    # unit: FPS
    frameStart = 166                        # first frame, set to 1 if not sure
    vidFrameTotal = 60                      # total frame counts for the calibrate video
    frameEnd = frameStart+vidFrameTotal     # final frame, set to 1 if not sure

    # save the input parameters
    input_list = [calibBoxHeight, calibBoxWidth,
                  cropVidHeight, cropVidWidth, axisInterval, cm2px,
                  newVidFrameRate, frameStart, vidFrameTotal, frameEnd]
    fid = open(folderName+paramName, 'wb')
    pickle.dump(input_list, fid)
    fid.close()

exec(open('video_process.py').read())

## Extract the runout evolution during granular collapses
# input parameters required to plot the runout evolution
dt = 0.05                                   # grap the front position every dt seconds
exec(open('runout_detection.py').read())

## Extract the height evolution during granular collapses
exec(open('height_detection.py').read())

## Extract the heights in the middle of the final deposit
exec(open('middle_heights.py').read())

## Find the triggering time
exec(open('trigger_time.py').read())