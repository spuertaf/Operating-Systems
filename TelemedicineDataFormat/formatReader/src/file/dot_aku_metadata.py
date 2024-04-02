from io import BufferedWriter
import struct

class DotAkuMetadata:
    """Represents metadata extracted from a binary file.

    This class parses binary data to extract patient information.

    Attributes:
        _id (int): Patient ID.
        _gender_n_age (str): Binary representation of gender and age.
        _gender (str): Gender of the patient ('M' for male, 'F' for female).
        _age (int): Age of the patient.
        _date (str): Date of the patient record.
        _description (list): Description of the patient.

    Methods:
        __init__: Initialize DotAkuMetadata instance.
        __str__: Return a formatted string representation of patient information.
        get_metadata: Return metadata as a list.
    """
    def __init__(self, bin_file: BufferedWriter):
        """Initialize DotAkuMetadata instance.

        Args:
            bin_file (BufferedWriter): Binary file stream.
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
        """Return a formatted string representation of patient information.

        Returns:
            str: Formatted patient information.
        """
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
        """Return metadata as a list.

        Returns:
            list: List containing patient metadata.
        """
        return [
            self._date, 
            self._id, 
            self._age,
            self._gender
        ] + self._description