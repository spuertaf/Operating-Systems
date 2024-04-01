import os
import struct

import cv2
from numpy import ndarray


class DotAkuWriter:
    """
    A class for writing .aku files.

    Attributes:
        _img_path (str): The path to the image file.
        _text_path (str): The path to the text file.
        _bin_folder_path (str): The path to the binary folder.
        BIN_FILE_NAME (str): The name of the .aku file.
        _aku_file_path (str): The path to the .aku file.
    """
    def __init__(self,
                 img_path: str,
                 text_path: str,
                 bin_file_path: str):
        """
        Initializes a DotAkuWriter.

        Args:
            img_path (str): The path to the image file.
            text_path (str): The path to the text file.
            bin_file_path (str): The path to the binary folder.
        """
        self._img_path = os.path.abspath(img_path)
        self._text_path = os.path.abspath(text_path) if text_path is not None else None  # text_path is optional
        self._bin_folder_path = os.path.abspath(bin_file_path)
        self.BIN_FILE_NAME = "aku.bin"  # TODO: Make this dynamic according to the users needs
        self._aku_file_path = os.path.abspath(os.path.join(self._bin_folder_path, self.BIN_FILE_NAME))
    
    def _write_image(self, aku_file, keep_open = False) -> 'DotAkuWriter':
        """
        Write image data to the .aku file.

        Args:
            aku_file (file): The .aku file object.
            keep_open (bool, optional): Whether to keep the file open after writing. Defaults to False.

        Returns:
            DotAkuWriter: The DotAkuWriter instance.
        """
        assert self._img_path is not None, ""
        img_array: ndarray = cv2.imread(self._img_path)
        rows, cols, dims = img_array.shape
        
        aku_file.write(struct.pack("IIc", rows, cols, bytes([dims])))
        
        for i in range(rows):
            for j in range(cols):
                for k in range(dims):
                    aku_file.write(struct.pack("c", bytes([img_array[i,j,k]])))

        if not keep_open:
            aku_file.close()
        
        return self
                 
    def _write_metadata(self, aku_file, keep_open = False) -> 'DotAkuWriter':
        """
        Write metadata to the .aku file.

        Args:
            aku_file (file): The .aku file object.
            keep_open (bool, optional): Whether to keep the file open after writing. Defaults to False.

        Returns:
            DotAkuWriter: The DotAkuWriter instance.
        """
        if self._text_path is None:
            return self
        
    def write_file(self) -> 'DotAkuWriter':
        """
        Write data to the .aku file.

        Returns:
            DotAkuWriter: The DotAkuWriter instance.
        """
        with open(self._aku_file_path, "wb") as aku_file:
            (
                self
                ._write_image(aku_file, keep_open=True)
                #._write_metadata(aku_file, keep_open=True)
            )
            aku_file.close()
        return self
            