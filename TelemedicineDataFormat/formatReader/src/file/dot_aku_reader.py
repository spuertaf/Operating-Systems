import os
import struct
from file.dot_aku_metadata import DotAkuMetadata
from typing import Union
from services.pdf_creator import PdfCreator

from numpy import (
    ndarray,
    zeros
)


class DotAkuReader:
    """Reads DotAku files and parses image data and metadata."""
    def __init__(self, proyect_parent_folder: str):
        """Initialize DotAkuReader instance.

        Args:
            proyect_parent_folder (str): Path to the parent folder of the project.
        """
        self._proyect_parent_folder = os.path.abspath(proyect_parent_folder)
        self.FILE_EXTENSION = ".bin"
        self._img: Union[None, ndarray] = None
        self._metadata: Union[None, DotAkuMetadata] = None
    
    def _get_dot_bin_file_path(self) -> str:
        """Find and return the path of the DotAku binary file.

        Raises:
            ValueError: If no DotAku binary file is found.

        Returns:
            str: Path of the DotAku binary file.
        """
        for root, _, files in os.walk(self._proyect_parent_folder):
            for file in files:
                if file.endswith(self.FILE_EXTENSION):
                    return os.path.abspath(os.path.join(root, file))
        raise ValueError("")
    
    def _read_image(self, dot_bin_file_path: str) -> ndarray:
        """Read and return the image data from the DotAku binary file.

        Args:
            dot_bin_file_path (str): Path of the DotAku binary file.

        Returns:
            ndarray: Image data extracted from the binary file.
        """
        with open(dot_bin_file_path, "rb") as bin_file:
            rows, cols, dims = struct.unpack("IIc", bin_file.read(9))
            DTYPE_BYTES, dims = 1, dims[0]
            img_data: ndarray = zeros((rows, cols, dims))
            
            for i in range(rows):
                for j in range(cols):
                    for k in range(dims):
                        bin_number = bin_file.read(DTYPE_BYTES)
                        img_data[i,j,k] = struct.unpack("c", bin_number)[0][0]
        
        bin_file.close()
        return img_data.astype('uint8')
    
    def _read_metadata(self, dot_bin_file_path: str) -> DotAkuMetadata:
        """Read and return metadata from the DotAku binary file.

        Args:
            dot_bin_file_path (str): Path of the DotAku binary file.

        Returns:
            DotAkuMetadata: Metadata extracted from the binary file.
        """
        with open(dot_bin_file_path, "rb") as bin_file:
            rows, cols, dims = struct.unpack("IIc", bin_file.read(9))
            dims = dims[0]
            ####
            
            bin_file.seek(9 + (rows*cols*dims))  # search the metadata after looping all headers and image data
            metadata = DotAkuMetadata(bin_file)
            
            bin_file.close()     
        return metadata
         
    def parse(self) -> None:
        """Parse DotAku binary file and create a PDF document with image and metadata."""
        bin_file_path: str = self._get_dot_bin_file_path()
        img: ndarray = self._read_image(bin_file_path)
        metadata: DotAkuMetadata = self._read_metadata(bin_file_path)
        PdfCreator(self._proyect_parent_folder).create(img, metadata)