'''
Determine the time period for the propogation stage.

Author: YANG Gengchao (The University of Hong Kong)
'''

import cv2
import numpy as np
import os
import pickle
from matplotlib import pyplot as plt

print('Determine the time period for the propogation stage.')

## Find the time corresponding to 0.95Ltilde_f
t95 = np.interp(0.95*Ltilde[-1], Ltilde, t)

# plot the runout evolution with the stopage point
plt.plot(t, Ltilde)
plt.plot(t95, 0.95*Ltilde[-1], '.')
plt.xlabel('$t$ (s)')
plt.ylabel('$(L-L_i)/L_i$')
plt.show()

# output the running time
tRun = t95-tTrigger
print('******Running time: {0:.3f} s'.format(tRun))