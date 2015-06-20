import numpy as np 
from phantom import Phantom
from . import enum

class Projections(object):
    """
    Represents all projections available to reconstruction. 
    Holds data container with a certain data type (either representing
    attenuation line integrals or photon counts). 
    A 2D plot of this container yields the projection sinogram.
    """

    DataType = enum(
            LINE_INTEGRAL=0,
            PHOTON_COUNT=1 )

    def __init__(self, views, nrBins, dataType=DataType.LINE_INTEGRAL):
        """
        :param      views | int 
                    nrBins | int 
                    dataType | Projections.DataType
        :attrib     __data | numpy.2darray
        """
        self.__views = views 
        self.__nrBins = nrBins 
        self.__data = np.zeros((views, nrBins))
        self._dataType = dataType
        self._maxPhotons = 100000

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

    def convertDataType(self):
        """
        Converts the projection data to line integral values if the current
        data type is PHOTON_COUNT and vice versa.
        """
        if self._dataType == Projections.DataType.LINE_INTEGRAL:
            self.__data[:,:] = self._maxPhotons * np.exp( - self.data[:,:] )
            self._dataType = Projections.DataType.PHOTON_COUNT
        elif self._dataType == Projections.DataType.PHOTON_COUNT:
            # assert positive arguments for logarithm
            self.__data[self.data <= 0] = 1.e-9
            self.__data[:,:] = np.log( self._maxPhotons / self.data[:,:] )
            self._dataType = Projections.DataType.LINE_INTEGRAL

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
        if self._dataType == Projections.DataType.PHOTON_COUNT:
            self.__data[view, :] = self._maxPhotons * np.exp( - self.__data[view, :] )
