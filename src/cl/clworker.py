import pyopencl as pcl 
import numpy as np


class ClWorker(object):
    def __init__(self, **kwargs):
        self._taskName = kwargs.get('taskName')
        self._task = None
        self._program = None 
        self._context = None 
        self._queue = None 
        self._ready = False 

    def init(self):
        platform = pcl.get_platforms()
        my_gpu = platform[0].get_devices(device_type=pcl.device_type.GPU)
        self._context = pcl.Context(devices=my_gpu)
        self._queue = pcl.CommandQueue(self._context)

        if self._taskName == 'rotate_img':
            try:
                kernelFile = open("src/cl/rotate_img.cl", 'r')
            except IOError as e:
                import pdb; import PyQt4.QtCore; PyQt4.QtCore.pyqtRemoveInputHook();
                pdb.set_trace()
                print str(e)
            kernelStr = kernelFile.read()
            self._program = pcl.Program(self._context, kernelStr).build()
            self._task = getattr(self._program, self._taskName)
        self._ready = True

    def process(self, img, *args):
        if not self._ready:
            return
        mf = pcl.mem_flags 
        clImgIn = pcl.Buffer(self._context, mf.READ_ONLY|mf.USE_HOST_PTR, hostbuf=img)
        clImgOut = pcl.Buffer(self._context, mf.WRITE_ONLY, size=img.nbytes)

        event = self._task(self._queue, img.shape,
                None, clImgIn, clImgOut, *args).wait()
        self._queue.finish()
        imgOut = np.empty_like(img)
        pcl.enqueue_copy(self._queue, imgOut, clImgOut)
        self._queue.finish()
        return imgOut
