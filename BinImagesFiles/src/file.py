import os
import struct
from dtypes import Dtypes
from interfaces.file import AbstractFile


from numpy import ndarray, zeros, random
        

class FlatFile(AbstractFile):
    def __init__(self, file_path: str):
        self._file_path = file_path
        self._abs_file_path = os.path.abspath(self._file_path)


    def read_file(self):
        AbstractFile.is_valid_file_path(self._file_path)
        with open(self._abs_file_path, "rb") as bin_file:
            rows, cols, dtype_bytes = struct.unpack("ccc", bin_file.read(3))
            rows = rows[0]
            cols = cols[0]
            dtype_bytes = len(dtype_bytes)
            data = zeros((rows, cols))

            for i in range(rows):
                for j in range(cols):
                    bin_number = bin_file.read(dtype_bytes)
                    data[i,j] = struct.unpack("c", bin_number)[0][0]
            
            bin_file.close()
        return data
        

    def write_file(self, file_content: ndarray):
        # TODO: check if the given path is valid or not
        rows, cols = file_content.shape  
        dtype_bytes = Dtypes.get_dtype_bytes(str(file_content.dtype))
        with open(self._abs_file_path, "wb") as bin_file:
            bin_file.write(struct.pack("ccc", bytes([rows]), bytes([cols]), bytes([dtype_bytes])))
            #bin_file.write(struct.pack("III", rows, cols, dtype_bytes))

            for i in range(rows):
                for j in range(cols):
                    bin_file.write(struct.pack("c", bytes([file_content[i,j]])))
            
            bin_file.close()
        
        return self 