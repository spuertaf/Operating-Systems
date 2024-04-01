from file import FlatFile
from image import Image
from text import Text
from aku import Aku

import numpy as np

#data = np.array([[1, 2, 3], [4, 18, 6], [7, 8, 9]])
#print(FlatFile(".\\BinImagesFiles\\src\\bin\\sample.bin").write_file(data).read_file())

#Image("..\\Operating-Systems\\BinImagesFiles\\img\\sampleImg.jpg").write_file().show()

meta_data = ['666', 'M', '69', '13', '07', '23', 'Picture of a messed up asshole']
#print(Text("..\\Operating-Systems\\BinImagesFiles\\text\\patient_info.bin").write_file(lines).read_file())

aku_file = Aku("..\\Operating-Systems\\BinImagesFiles\\img\\culo.png")
aku_file.write_file(meta_data)
print(aku_file.read_meta_data())
aku_file.show()