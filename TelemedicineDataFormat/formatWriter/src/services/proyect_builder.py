from typing import Union
from datetime import datetime
import os
import shutil
from utils import get_file_name_from_abs_path


class ProyectBuilder:
    def __init__(self, proyect_name: Union[None, str] = None):
        self._proyect_name = (datetime.now()).strftime("%Y-%m-%d-%H-%M-%S") if proyect_name is None else proyect_name
        self._proyect_parent_folder: Union[None, str] = None
        self._proyect_data_folder: Union[None, str] = None
        self._proyect_bin_folder: Union[None, str] = None
        self._proyect_img_path: Union[None, str] = None
        self._proyect_text_path: Union[None, str] = None
    
    @property
    def bin_folder(self) -> Union[None, str]:
        return self._proyect_bin_folder
    
    @property
    def img_path(self) -> Union[None, str]:
        return self._proyect_img_path

    @property
    def text_path(self) -> Union[None, str]: 
        return self._proyect_text_path
        
    def build_parent_folder(self, output_folder_path = None):
        output_folder_path = "..\\proyects" if output_folder_path is None else output_folder_path
        output_folder_path = os.path.abspath(output_folder_path)
        self._proyect_parent_folder = os.path.abspath(os.path.join(output_folder_path, self._proyect_name))
        return self
        
    def build_data_folder(self, data_folder_name = None):
        assert self._proyect_parent_folder is not None, ...
        data_folder_name = "data" if data_folder_name is None else data_folder_name
        self._proyect_data_folder = os.path.join(self._proyect_parent_folder, data_folder_name)
        return self
            
    def build_bin_folder(self, bin_folder_name = None):
        assert self._proyect_parent_folder is not None, ...
        bin_folder_name = "bin" if bin_folder_name is None else bin_folder_name
        self._proyect_bin_folder = os.path.abspath(os.path.join(self._proyect_parent_folder, bin_folder_name))
        return self
    
    def _validate_built_stages(self):
        assert self._proyect_parent_folder is not None, ""
        assert self._proyect_data_folder is not None, ""
        assert self._proyect_bin_folder is not None, ""

    def create_proyect(self):
        self._validate_built_stages()
        os.mkdir(self._proyect_parent_folder)
        os.mkdir(self._proyect_data_folder)
        os.mkdir(self._proyect_bin_folder)
        return self
    
    def copy_img_2_proyect(self, img_path: str):
        abs_img_path = os.path.abspath(img_path)
        assert os.path.exists(abs_img_path), ""
        assert self._proyect_data_folder is not None, ""
        self._proyect_img_path = os.path.abspath(os.path.join(self._proyect_data_folder, get_file_name_from_abs_path(abs_img_path)))
        shutil.copy(
            abs_img_path,  # origin path
            self._proyect_img_path  # destiny path
        )
        return self
    
    def copy_text_2_proyect(self, text_path: str):  # TODO: Boilerplate code, this could be improved handling files dynamically
        if text_path is None:
            return self  # text_path optional
        abs_text_path = os.path.abspath(text_path)
        assert os.path.exists(abs_text_path), ""
        assert self._proyect_data_folder is not None, ""
        self._proyect_text_path = os.path.abspath(os.path.join(self._proyect_data_folder, get_file_name_from_abs_path(abs_text_path)))
        shutil.copy(
            abs_text_path,  # origin path
            self._proyect_text_path  # destiny path
        )
        return self    


if __name__ == "__main__":
    ProyectBuilder().build_parent_folder()