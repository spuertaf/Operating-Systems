import argparse
from argparse import Namespace
from typing import Union
from copy import deepcopy


class FlagsParser:
    def __init__(self, description: str = None):
        self._description = """
        Flags parser for .med format writter. The following are allowed flags: \n
        
        """ if description is None else description
        self.parser = argparse.ArgumentParser(description=self._description)
        self._args: Union[None, Namespace] = None
    
    def get_flag(self, flag_name: str) -> Union[str, None]:
        return getattr(self._args, flag_name, None)
    
    def get_flags(self) -> dict[str, str]:
        return deepcopy(vars(self._args))  # deepcopy due to if any of the values in vars is modified the value in the object gets modified
    
    def build(self) -> 'FlagsParser':
        self.parser.add_argument("-name", "--proyect_name", type=str, help="")
        self.parser.add_argument("-out", "--output_folder_path", type=str, help="")  # the proyect's parent folder
        self.parser.add_argument("-data_folder", "--proyect_data_folder", type=str, help="")
        self.parser.add_argument("-bin_folder", "--proyect_bin_folder", type=str, help="")
        self.parser.add_argument("-img", "--input_img_path", type=str, help="")
        self.parser.add_argument("-text", "--input_text_path", type=str, help="")
        self._args = (self.parser).parse_args()
        return self
    
    def existent_flags(self) -> bool:
        return any(vars(self._args).values())
        

if __name__ == "__main__":
    fg = FlagsParser().build()
    print(fg.get_flags())
    