import numpy as np 
from scipy.ndimage import interpolation

TISSUES = {'fat': 0.2, 'bone': 0.9, 'max': 1.0}

class Phantom(object):

    def __init__(self, size):
        self.__size = size if size%2==1 else size+1
        self.__shape = (self.__size, self.__size)
        self.__data = np.zeros(self.__shape)

    @property
    def data(self):
        return self.__data

    @property
    def size(self):
        return self.__size 

    @property
    def shape(self):
        return self.__shape 

    def __getitem__(self, index):
        return self.__data[index]

    def create(self, withInlets=True):
        radius = self.size/2-1 
        #body = self.createCircularMask(self.shape, (radius,radius), radius)
        #self.__data[body] = TISSUES['fat']
        x = np.floor(np.sqrt(0.5)*self.size)/2
        self.__data[x:self.size-x,x:self.size-x] = TISSUES['fat']
        
        if withInlets:
            for m in [int(x) for x in [0.5*radius, radius, 1.5*radius]]:
                inlet = self.createCircularMask(self.shape, (m,radius), 0.1*radius)
                self.__data[inlet] = TISSUES['bone']

    def createCircularMask(self, shape, centre, radius, angle_range=(0,360)):
        """
        Return a boolean mask for a circular sector. The start/stop angles in  
        `angle_range` should be given in clockwise order.
        http://stackoverflow.com/questions/18352973/mask-a-circular-sector-in-a-numpy-array 
        """
        x,y = np.ogrid[:shape[0],:shape[1]]
        cx,cy = centre
        tmin,tmax = np.deg2rad(angle_range)

        # ensure stop angle > start angle
        if tmax < tmin:
                tmax += 2*np.pi

        # convert cartesian --> polar coordinates
        r2 = (x-cx)*(x-cx) + (y-cy)*(y-cy)
        theta = np.arctan2(x-cx,y-cy) - tmin

        # wrap angles between 0 and 2*pi
        theta %= (2*np.pi)
        # circular mask
        circmask = r2 <= radius*radius
        # angular mask
        anglemask = theta <= (tmax-tmin)
        return circmask*anglemask

    def reshape(self, shape):
        assert(np.product(self.data.shape) == np.product(shape))
        return np.reshape(self.data, shape).copy()

    def rotate(self, angle):
         return interpolation.rotate(self.__data, angle, reshape=False)
