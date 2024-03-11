from file import FlatFile
from image import Image


import numpy as np




data = np.array([[1, 2, 3], [4, 5, 6], [6, 7, 8]])

print(FlatFile(".\\bin\\sample.bin").write_file(data).read_file())

Image("..\\img\\sampleImg.jpg").write_file().show()