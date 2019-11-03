'''
Image and video processing of the experimental data from granular collapses.

Author: YANG Gengchao (The University of Hong Kong)
'''
import os
import pickle
from pathlib import Path
os.system('cls')    # clear the screen

## Specify the parameters for video processing and free-surface detection
folderName = Path('D:/Experimental_Results/2019_HKU_PRFluids_columnSizeEffects/T1b_AR0.50W18_GB1.44mm_Li3.0cm_Hi1.50cm_SP80Cw_20190325/')   # folder where the video exists
fileName = 'IMG_1694.MOV'           # video name
saveName = 'input_parameters.dat'   # name for the saved input parameters

if os.path.isfile(folderName/saveName):
    print('Input parameters have been saved previously, so import them. ')
    fid = open(folderName/saveName, 'rb')
    input_list = pickle.load(fid)
    fid.close()
else:
    print('Input parameters have not been saved previously, so specify them.')
    # specify the size of the calibration box
    caliBoxHeight = 9.6             # unit: cm
    caliBoxLength = 15.2            # unit: cm

    # specify the size of the cropped video
    cropVidHeight = 6               # unit: cm
    cropVidLength = 2*cropVidHeight # unit: cm
    axisInterval = cropVidHeight/3  # unit: cm

    # specify the control parameters for the output video
    newVidFrameRate = 12            # unit: FPS
    frameStart = 1                  # first frame, set to 1 if not sure
    frameEnd = frameStart+60        # final frame, set to 1 if not sure

    # save the input parameters
    input_list = [caliBoxHeight, caliBoxLength,
                  cropVidHeight, cropVidLength, axisInterval,
                  newVidFrameRate, frameStart, frameEnd]
    fid = open(folderName/saveName, 'wb')
    pickle.dump(input_list, fid)
    fid.close()

print(input_list)