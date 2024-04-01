from abc import ABC, abstractmethod
import os


from numpy import ndarray



class AbstractFile(ABC):
    @abstractmethod
    def read_image() -> ndarray: ...

    @abstractmethod
    def write_file(): ...

    @classmethod
    def is_valid_file_path(cls, abs_file_path: str):
        if not os.path.exists(abs_file_path): raise ValueError()