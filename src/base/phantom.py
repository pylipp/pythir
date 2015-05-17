import numpy as np 
import matplotlib.pyplot as plt
from scipy.ndimage import interpolation

TISSUES = {'fat': 0.2, 'bone': 0.9, 'max': 1.0}

class Phantom(object):
    """
    Represents phantom slice. 
    First, this is the basis for the projection simulation. 
    Later it serves as reference image to the reconstructed image.
    The data (i.e. gray value intensities) is hold in a quadratic 2D-array. 
    """

    def __init__(self, **kwargs):
        """
        To initialize a phantom, one can either load an appropriate image file
        (note that the first channel of color images is selected) or
        create a simple circular shape with three inlets.
        Pass arguments using key words.

        :param      fileName | str
                    size | int 
        :attrib     __data | numpy.2darray
                    __size | int 
                    __shape | 2-tuple[int]
        """
        self.__size = None
        self.__fileName = None
        self.__data = None
        for key in kwargs.iterkeys():
            if key == 'fileName':
                self.__fileName = kwargs[key]
            elif key == 'size':
                self.__size = kwargs[key] 

    @property
    def data(self):
        return self.__data

    @property 
    def fileName(self):
        return self.__fileName 

    @property
    def size(self):
        return self.__size 

    @property
    def shape(self):
        return self.__data.shape 

    def __getitem__(self, index):
        return self.__data[index]

    def create(self):
        """
        This method should be called after the initialization of a phantom. 
        First it loads data from a file if a file name has been given. 
        Otherwise it creates a simple phantom. 
        """
        if self.__fileName is not None:
            try:
                inputData = plt.imread(self.__fileName)
                if len(inputData.shape) == 3:
                    self.__data = inputData[:,:,0]
                elif len(inputData.shape) == 2:
                    self.__data = inputData
                self.__size = np.max(self.data.shape)
                return
            except IOError as e:
                print str(e)
        if self.size is None:
            print "No phantom created."
            return

        radius = self.size/2-1 
        shape = (self.size, self.size)
        body = self.createCircularMask(shape, (radius,radius), radius)
        self.__data = np.zeros(shape)
        self.__data[body] = TISSUES['fat']
        
        #create the inlets
        for m in [int(x) for x in [0.5*radius, radius, 1.5*radius]]:
            inlet = self.createCircularMask(shape, (m,radius), 0.1*radius)
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
