from src.base.phantom import Phantom
from src.base.projectionsimulator import ProjectionSimulator
from src.base.program import Program 

import matplotlib.pyplot as plt
import numpy as np 

def plot(data):
    plt.imshow(data, "gray", interpolation="nearest")
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


ph = Phantom(fileName="src/images/shepp-logan512.png")
ph.create()
p = Program(ph)
#p = Program()
p.setUp(nrIter=1, views=360)
p.compute()
p.computeRmse()

#plt.subplot(131)
#p.plot(p.result)
#plt.subplot(132)
#plt.imshow(p._Program__phantom.data, "gray", interpolation="nearest")
#plt.subplot(133)
#plt.imshow(p._Program__phantom.data - p.result, "gray", interpolation="nearest")
