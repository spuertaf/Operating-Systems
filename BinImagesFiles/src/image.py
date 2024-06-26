from numpy import ndarray
from interfaces.file import AbstractFile
import os
from dtypes import Dtypes
import struct

import cv2
from numpy import ndarray, zeros

class Image(AbstractFile): 
    def __init__(self, img_path: str):
        self._img_path = img_path
        self._abs_img_path = os.path.abspath(self._img_path)
    

    def _get_img_dot_bin(self) -> str:
        img_extension:str = os.path.splitext(self._img_path)[1]
        return (os.path.basename(self._img_path)).replace(img_extension, ".bin")
        
    def read_image(self) -> ndarray:
        with open(os.path.abspath(f"..\\Operating-Systems\\BinImagesFiles\\src\\bin\\{self._get_img_dot_bin()}"), "rb") as bin_file:
            rows, cols, dims = struct.unpack("IIc", bin_file.read(9))
            dims = dims[0]
            dtype_bytes = 1
            data = zeros((rows, cols, dims))
            
            for i in range(rows):
                for j in range(cols):
                    for k in range(dims):
                        bin_number = bin_file.read(dtype_bytes)
                        data[i,j,k] = struct.unpack("c", bin_number)[0][0]
            
            bin_file.close()
        
        # TODO: Mejorar esto, es mejor guardar en al archivo el tipo de dato y luego aqui leer el tipo de dato y pasarlo a bytes.
        return data.astype('uint8')
        

    def write_file(self):
        AbstractFile.is_valid_file_path(self._img_path)
        img_array: ndarray = cv2.imread(self._abs_img_path)
        
        rows, cols, dims = img_array.shape
        
        with open(os.path.abspath(f"..\\Operating-Systems\\BinImagesFiles\\src\\bin\\{self._get_img_dot_bin()}"), "wb") as bin_file:
            bin_file.write(struct.pack("IIc", rows, cols, bytes([dims])))
            
            for i in range(rows):
                for j in range(cols):
                    for k in range(dims):
                        bin_file.write(struct.pack("c", bytes([img_array[i,j,k]])))
            
            bin_file.close()
            
        return self
    
    def show(self):
        img_array: ndarray = self.read_image()
        cv2.imshow(self._get_img_dot_bin(), img_array)
        cv2.waitKey(0)
        cv2.destroyAllWindows()
        
            

if __name__ == "__main__":
    print(Image("C:\\Users\\Admin\\Desktop\\Operating-Systems\\BinImagesFiles\\img\\sampleImg.jpg").show())
        