class DotAkuMetadata:
    """Represents metadata for DotAku.

    This class stores metadata information for DotAku.

    Attributes:
        _id (int): The ID of the metadata.
        _gender (str): The gender of the person associated with the metadata.
        _age (int): The age of the person associated with the metadata.
        _gender_n_age (bytes): The binary representation of gender and age.
        _date (bytes): The date associated with the metadata.
        _description (bytes): The description associated with the metadata.
        _num_bytes_date (bytes): The number of bytes in the date.
        _num_bytes_description (bytes): The number of bytes in the description.
    """
    def __init__(self,
                 id: str, 
                 gender: str, 
                 age: str,
                 date: str, 
                 description: str):
        """Initializes a DotAkuMetadata object.

        Args:
            id (str): The ID of the metadata.
            gender (str): The gender of the person.
            age (str): The age of the person.
            date (str): The date associated with the metadata.
            description (str): The description associated with the metadata.
        """
        self._id = int(id)
        self._gender = "1" if gender == "M" else "0"
        self._age = int(age)
        self._gender_n_age =  bytes([int(self._gender + '{0:07b}'.format(self._age), 2)])
        self._date = bytes(date, "utf-8")
        self._description = bytes(description, "utf-8")
        self._num_bytes_date = bytes([len(self._date)])
        self._num_bytes_description = bytes([len(self._description)])
        
    @property
    def id(self) -> str:
        """Gets the ID of the metadata.

        Returns:
            str: The ID of the metadata.
        """
        return self._id
    
    @property
    def gender_n_age(self) -> str:
        """Gets the binary representation of gender and age.

        Returns:
            str: The binary representation of gender and age.
        """
        return self._gender_n_age
    
    @property
    def num_bytes_date(self) -> str:
        """Gets the number of bytes in the date.

        Returns:
            str: The number of bytes in the date.
        """
        return self._num_bytes_date
    
    @property
    def date(self) -> str:
        """Gets the date associated with the metadata.

        Returns:
            str: The date associated with the metadata.
        """
        return self._date
    
    @property
    def num_bytes_description(self) -> str:
        """Gets the number of bytes in the description.

        Returns:
            str: The number of bytes in the description.
        """
        return self._num_bytes_description    
    
    @property
    def description(self) -> str:
        """Gets the description associated with the metadata.

        Returns:
            str: The description associated with the metadata.
        """
        return self._description