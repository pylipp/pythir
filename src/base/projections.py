import numpy as np 
from phantom import Phantom

class Projections(object):
    """
    Represents all projections available to reconstruction. 
    Holds data container with line integral values. 
    """
    def __init__(self, views, nrBins):
        """
        :param      views | int 
                    nrBins | int 
        :attrib     __data | numpy.2darray
        """
        self.__views = views 
        self.__nrBins = nrBins 
        self.__data = np.zeros((views, nrBins))

    @property 
    def nrBins(self):
        """ :return     int """
        return self.__nrBins 

    @property
    def data(self):
        """ :return     numpy.2darray """
        return self.__data

    @property 
    def data1d(self):
        """ :return     numpy.1darray """
        return np.ravel(self.__data)

    @property
    def totalSize(self):
        """ :return     int """
        return np.product(self.__data.shape)

    @property 
    def views(self):
        """ :return     int """
        return self.__views

    def project(self, view, phantom):
        """
        Adds up each column of the given phantom and writes the sum into the
        corresponding bin of view. 

        :param      view | int 
                    phantom | np.2darray or Phantom 
        """
        if isinstance(phantom, Phantom):
            phantom = phantom.data
        self.__data[view, :] = np.sum(phantom, axis=0)
