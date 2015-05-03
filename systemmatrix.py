import numpy as np 

class SystemMatrix(object):
    """
    Represents system matrix of reconstruction problem. 
    The data member contains information about the contribution of each pixel
    in each projection. 
    """

    def __init__(self, dimensions):
        """
        :param      dimensions | 3-tuple[int]
        :attrib     __data | numpy.3darray
        """
        self.__dimensions = dimensions 
        self.__data = np.zeros(dimensions)

    @property
    def data(self):
        """ :return     numpy.3darray """
        return self.__data

    @property 
    def data2d(self):
        """
        Convenient for algebraic computations. 

        :return     numpy.2darray
        """
        a,b,c = self.__dimensions
        return self.__data.reshape(a, b*c)

    @property
    def shape(self):
        """ :return     2-tuple[int] """
        a,b,c = self.__dimensions 
        return (a, b*c)

    def add(self, view, data):
        """
        Convenient setter method. 
        Fills slice (of index 'view') with elements of 'data'. 
        Called in projection simulation.

        :param      view | int 
                    data | numpy.2darray
        """
        self.data[view,:,:] = data

    def reshape(self, shape):
        assert(np.product(shape) == np.product(self.__dimensions))
        return np.reshape(self.data, shape).copy()
