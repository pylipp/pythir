import numpy as np 
import matplotlib.pyplot as plt 
from sectorMask import sector_mask

def createPhantom(radius, plot=False):
    size = 2*radius+1
    maxValue = 1.0
    tissue = 0.2*maxValue 
    bone = 0.9*maxValue
    phantom = np.zeros((size, size))
    
    body = sector_mask(phantom.shape, (radius,radius), radius)
    phantom[body] = tissue

    for m in [int(x) for x in [0.5*radius, radius, 1.5*radius]]:
        inlet = sector_mask(phantom.shape, (m,radius), 0.1*radius)
        phantom[inlet] = bone

    if plot:
        plt.imshow(phantom, cmap="gray")
        plt.show()

    return phantom
