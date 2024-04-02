from io import BufferedWriter
import struct

class DotAkuMetadata:
    def __init__(self, bin_file: BufferedWriter):
        """_summary_

        Args:
            bin_file (BufferedWriter): _description_
        """
        self._id = struct.unpack("H", bin_file.read(2))[0]
        self._gender_n_age = '{0:08b}'.format(struct.unpack("c", bin_file.read(1))[0][0])
        self._gender = "M" if int(self._gender_n_age[0],2) == 1 else "F"
        self._age = int(self._gender_n_age[1:],2)
        self._num_bytes_date = struct.unpack("c", bin_file.read(1))[0][0]
        self._date = struct.unpack("<" + str(self._num_bytes_date) + "s",\
                                   bin_file.read(self._num_bytes_date))[0].decode("utf-8")
        self._num_bytes_description = struct.unpack("c", bin_file.read(1))[0][0]
        self._description: list = struct.unpack("<" + str(self._num_bytes_description) + "s",\
                                   bin_file.read(self._num_bytes_description))[0].decode("utf-8").split(".") 
        
    
    def __str__(self) -> str:
        return f"""
        Patient Information:
        Date: {self._date}
        --------------------
        ID: {self._id}
        Age: {self._age}
        Gender: {self._gender}
        Description: {self._description}
        """
        
    def get_metadata(self) -> list:
        """_summary_

        Returns:
            list: _description_
        """
        return [
            self._date, 
            self._id, 
            self._age,
            self._gender
        ] + self._description