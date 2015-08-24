Welcome to 

#### PYTHIR ####

a PYTHon project dedicated to Iterative Reconstruction as it is used in the
field of computed tomography. 

Feel free to browse and/or clone the code yet keep in mind that this project
currently can be considered a 'sandbox' of mine for several programming techniques
such as
- GUI programming using PyQt and pyqtgraph
- GPGPU programming using PyOpenCl
- general pythonic coding (using Python 3 at some point...)
- testing using the unittest module
- experimenting with Cython or PyPy (maybe)
and for several aspects of X-ray computed tomography such as
- definition of phantom data
- simulation of X-ray scans
- algebraic and statistical reconstruction methods 
- forward/backprojection, system matrix
My goal is to get self-taught in the techniques and principles listed above
while keeping the overall project simple. F.i. I don't plan on implementing
something fancier than a parallel beam geometry. But who knows.

As you can guess, this repo has some dependencies:
- pyqt4
- pyqtgraph
- numpy, scipy, matplotlib
- pyopencl


I browsed the web to find related work:
- CTSim: Appears to be abandoned. Clear and detailed documentation though.
  Comes with GUI. 
- STIR: Actively developed C++ framework for iterative reconstruction of
  SPECT/PET data. Currently not funded anymore. Good documentation. Command
  line use only.
- GATE: Simulation package for PET/SPECT/CT. No reconstruction. 

### TODO ###
+ DESIGN
- consistent backend data container for simulation
- cleanup QThread handling
- consistent handling of properties and pythonic methods
- introduce Forward/Backprojector methods
- handling of global settings like PyOpenCl usage
+ COMPUTATIONAL METHODS
- ray tracing algorithm
- ML algorithm 
