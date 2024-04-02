import argparse
from argparse import Namespace
from typing import Union
from copy import deepcopy


class FlagsParser:
    """
    A class for parsing flags.

    Attributes:
        _description (str): The description of the flags parser.
        parser (argparse.ArgumentParser): The ArgumentParser instance.
        _args (Namespace): The parsed arguments.
    """
    def __init__(self, description: str = None):
        """
        Initializes a FlagsParser.

        Args:
            description (str, optional): The description of the flags parser. Defaults to None.
        """
        self._description = """
        Flags parser for .med format writter. The following are allowed flags: \n
        
        """ if description is None else description
        self.parser = argparse.ArgumentParser(description=self._description)
        self._args: Union[None, Namespace] = None
    
    def get_flags(self) -> dict[str, str]:
        """
        Get all parsed flags.

        Returns:
            dict[str, str]: A dictionary containing all parsed flags.
        """
        return deepcopy(vars(self._args))  # deepcopy due to if any of the values in vars is modified the value in the object gets modified
    
    def build(self) -> 'FlagsParser':
        """
        Build the flags parser.

        Returns:
            FlagsParser: The FlagsParser instance.
        """
        self.parser.add_argument("-proyect", "--proyect_parent_folder", type=str, help="Path to the folder where the project was saved.")
        self._args = (self.parser).parse_args()
        return self
    
    def existent_flags(self) -> bool:
        """
        Check if any flag exists.

        Returns:
            bool: True if any flag exists, False otherwise.
        """
        return any(vars(self._args).values())