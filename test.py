from phantom import Phantom
from projectionsimulator import ProjectionSimulator

import matplotlib.pyplot as plt
import numpy as np 

def plot(data):
    plt.imshow(data, "gray")
    plt.show()

def createSinogram(size, start, stop, views):
    p = Phantom(size)
    p.create(False)

    ps = ProjectionSimulator(p)
    ps.projectAll(size, start, stop, views)
    return ps

size = 101
views = 400
#ps = createSinogram(size, 0, 360, views)
##plot(ps.projections.data)
#H = ps.systemMatrix.data 
#f = ps.phantom.data
#g = ps.projections.data #sinogram
#
##import pdb; pdb.set_trace()
#Hrs = H.reshape(views, size*size)
#plot(f)
##plot(Hrs)
##plot(H[1,:,:])
#frs = f.reshape(size*size)
#s = Hrs*frs
#srs = s.reshape(views, size, size)


from program import Program 
p = Program()
p.compute()
#plot(np.sum(srs, axis=1))
