import os
from file.dot_aku_metadata import DotAkuMetadata
from fpdf import FPDF
from typing import Union

from numpy import ndarray
from cv2 import imwrite, cvtColor, COLOR_RGB2BGR


class PdfCreator:
    def __init__(self, proyect_parent_folder: str):
        self.OUT_FOLDER_NAME = "out"
        self.IMG_EXTENSION = ".jpg"
        self._out_folder_path = os.path.abspath(os.path.join(proyect_parent_folder, self.OUT_FOLDER_NAME))
        self._proyect_name = os.path.basename(proyect_parent_folder)
        self._out_img_path = os.path.abspath(os.path.join(self._out_folder_path, f"{self._proyect_name}{self.IMG_EXTENSION}"))
        self._pdf_path = os.path.abspath(os.path.join(self._out_folder_path, f"{self._proyect_name}.pdf"))
      
    def _create_out_dir(self):
        os.mkdir(self._out_folder_path)
        return self   
        
    def _save_img(self, img: ndarray):
        imwrite(self._out_img_path, cvtColor(img, COLOR_RGB2BGR))
        return self
      
    def _create_file(self, 
                     metadata: Union[DotAkuMetadata, None]):
        pdf_file = FPDF()
        pdf_file.add_page()
        pdf_file.image(self._out_img_path, x = 30, y = 30, w = 100)
        pdf_file.add_page()
        pdf_file.set_font("Arial", size=12)
        if metadata is not None:
            for field in metadata.get_metadata():
                print(field)
                pdf_file.cell(200, 10, txt=str(field), ln=True)    
        pdf_file.output(self._pdf_path)
        return self
        
    def create(self, 
               img: ndarray, 
               metadata: Union[DotAkuMetadata, None]):
        (
            self
            ._create_out_dir()
            ._save_img(img)
            ._create_file(metadata)
        )
        
    
    