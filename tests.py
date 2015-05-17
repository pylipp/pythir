import unittest
import numpy as np

from src.base.phantom import Phantom 


class EmptyInitPhantomTestCase(unittest.TestCase):
    def setUp(self):
        self.phantom = Phantom()

    def runTest(self):
        self.assertIsNone(self.phantom.create())

class SizeInitPhantomTestCase(unittest.TestCase):
    def setUp(self):
        self.size = 33
        self.phantom = Phantom(size=self.size)
        self.phantom.create()

    def test_shape(self):
        self.assertEqual(self.phantom.size, self.size)

    def test_fileName(self):
        self.assertIsNone(self.phantom.fileName)

    def test_data(self):
        self.assertIsInstance(self.phantom.data, np.ndarray)

class FileNameInitPhantomTestCase(unittest.TestCase):
    def setUp(self):
        self.phantom = Phantom(fileName="./src/images/shepp-logan512.png")
        self.phantom.create()

    def test_size(self):
        self.assertEqual(self.phantom.size, 512)
