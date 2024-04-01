from numpy import ndarray
from interfaces.file import AbstractFile
import os
from dtypes import Dtypes
import struct

import cv2
from numpy import ndarray, zeros

class Text(AbstractFile): 
    def __init__(self, txt_path: str):
        self._txt_path = txt_path
        self._abs_txt_path = os.path.abspath(self._txt_path)
    
    def read_image(self):
        AbstractFile.is_valid_file_path(self._txt_path)
        with open(self._abs_txt_path, "rb") as bin_file:
            id = struct.unpack("H", bin_file.read(2))[0]

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
        

    def write_file(self, file_content: list):
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

        with open(self._abs_txt_path, "wb") as bin_file:
            
            bin_file.write(struct.pack("H", id))
            bin_file.write(struct.pack("c", gender_and_age))
            bin_file.write(struct.pack("H", date))
            bin_file.write(struct.pack("c", num_bytes_other))
            bin_file.write(struct.pack("<" + str(len(other)) + "s", other))
            
            bin_file.close()
        
        return self 
        
            

if __name__ == "__main__":
    print(Text("C:\\Users\\Admin\\Desktop\\Operating-Systems\\BinImagesFiles\\img\\sampleImg.jpg").show())
        