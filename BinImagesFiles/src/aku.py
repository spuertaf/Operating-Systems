from numpy import ndarray
from interfaces.file import AbstractFile
import os
from dtypes import Dtypes
import struct

import cv2
from numpy import ndarray, zeros

class Aku(AbstractFile): 
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
    
    def read_meta_data(self):
        AbstractFile.is_valid_file_path(self._img_path)
        with open(os.path.abspath(f"..\\Operating-Systems\\BinImagesFiles\\src\\bin\\{self._get_img_dot_bin()}"), "rb") as bin_file:
            rows, cols, dims = struct.unpack("IIc", bin_file.read(9))
            dims = dims[0]

            bin_file.seek(9 + rows*cols*dims)

            id = struct.unpack("H", bin_file.read(2))[0]
            print(id)

            gender_and_age = '{0:08b}'.format(struct.unpack("c", bin_file.read(1))[0][0])
            gender = "M" if int(gender_and_age[0],2) == 1 else "F"
            age = int(gender_and_age[1:],2)

            date = '{0:016b}'.format(struct.unpack("H", bin_file.read(2))[0])
            date_day = int(date[:4],2)
            date_month = int(date[4:9],2)
            date_year = int(date[9:],2)
            
            num_bytes_other = struct.unpack("c", bin_file.read(1))[0][0]
            other = struct.unpack("<" + str(num_bytes_other) + "s",\
                                   bin_file.read(num_bytes_other))[0].decode("utf-8")
            
            bin_file.close()
    
        #TODO: Mejorar esto, es mejor guardar en al archivo el tipo de dato y luego aqui leer el tipo de dato y pasarlo a bytes.
        return [id, gender, age, date_day, date_month, date_year, other]
    
    def _write_meta_data(self, bin_file, file_content: list, keep_open = False):
        # TODO: check if the given path is valid or not
        id = int(file_content[0])

        gender = "1" if file_content[1] == "M" else "0"
        age = int(file_content[2])
        gender_and_age = bytes([int(gender + '{0:07b}'.format(age), 2)])

        date_day = int(file_content[3])
        date_month = int(file_content[4])
        date_year = int(file_content[5])
        date = int(\
                    '{0:04b}'.format(date_day) +\
                    '{0:05b}'.format(date_month) +\
                    '{0:07b}'.format(date_year),\
                     2)

        other = bytes(file_content[6], "utf-8")
        num_bytes_other = bytes([len(other)])
            
        bin_file.write(struct.pack("H", id))
        bin_file.write(struct.pack("c", gender_and_age))
        bin_file.write(struct.pack("H", date))
        bin_file.write(struct.pack("c", num_bytes_other))
        bin_file.write(struct.pack("<" + str(len(other)) + "s", other))
        
        if(not keep_open):
            bin_file.close()
        
        return self
    
    def _write_image(self, bin_file, keep_open = False):
        AbstractFile.is_valid_file_path(self._img_path)
        img_array: ndarray = cv2.imread(self._abs_img_path)
        
        rows, cols, dims = img_array.shape
        
        bin_file.write(struct.pack("IIc", rows, cols, bytes([dims])))
        
        for i in range(rows):
            for j in range(cols):
                for k in range(dims):
                    bin_file.write(struct.pack("c", bytes([img_array[i,j,k]])))
        
        if(not keep_open):
            bin_file.close()
            
        return self

    def write_file(self, file_content: list):
        AbstractFile.is_valid_file_path(self._img_path)
    
        with open(os.path.abspath(f"..\\Operating-Systems\\BinImagesFiles\\src\\bin\\{self._get_img_dot_bin()}"), "wb") as bin_file:
            self._write_image(bin_file, keep_open= True)
            self._write_meta_data(bin_file, file_content, keep_open= True)
            bin_file.close()
            
        return self
    
    def show(self):
        img_array: ndarray = self.read_image()
        cv2.imshow(self._get_img_dot_bin(), img_array)
        cv2.waitKey(0)
        cv2.destroyAllWindows()
        