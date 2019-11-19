'''
Determine the triggering time according to time evolution of runout distance.

Author: YANG Gengchao (The University of Hong Kong)
'''

import cv2
import numpy as np
import os
import pickle
from matplotlib import pyplot as plt

## Calculate the time evolution of front velocity
vel = np.gradient(Ltilde, dt)

# plot the time evolution of front velocity
plt.subplot(1,2,1)
plt.plot(t, Ltilde)
plt.xlabel('$t$ (s)')
plt.ylabel('($L-L_i)/L_i$')

## Calculate the triggering time
# find the maximum velocity and the corresponding time and runout
velMax = np.amax(vel)
indMax = np.where(vel==velMax)              # return a tuple of array with the index per axis
indMax = indMax[0][0]                       # we only have one axis here
LtildeMax = Ltilde[indMax]
tMax = t[indMax]

# back extrapolate to find the triggering time
tTrigger = tMax-LtildeMax/velMax

# plot the runout evolution together with the triggering line
triggerX = [tTrigger, tMax]
triggerY = [0, LtildeMax]

plt.subplot(1,2,2)
plt.plot(t, Ltilde, triggerX, triggerY)
plt.xlabel('$t$ (s)')
plt.ylabel('($L-L_i)/L_i$')
plt.show()

# print out the triggering time
print('******Triggering time: {0:.3f} s'.format(tTrigger))