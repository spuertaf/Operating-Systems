from file import FlatFile
from image import Image


import numpy as np


data = np.array([[1, 2, 3], [4, 18, 6], [7, 8, 9]])

print(FlatFile(".\\BinImagesFiles\\src\\bin\\sample.bin").write_file(data).read_file())
#Image("..\\Operating-Systems\\BinImagesFiles\\img\\sampleImg.jpg").write_file().show()

#"C:\Users\PC\OneDrive - Universidad EAFIT\Eafit\2024-1\OS\Operating-Systems\BinImagesFiles\img\sampleImg.jpg"