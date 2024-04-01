import os
import imghdr

def get_file_name_from_abs_path(abs_path: str) -> str: 
    return os.path.basename(abs_path)

def is_path_an_img(abs_path: str) -> bool:
    return bool(imghdr.what(abs_path))


if __name__ == "__main__":
    path = "C:\\Users\\Admin\\Desktop\\Operating-Systems\\TelemedicineDataFormat\\formatWriter\\img\\sample1.png"
    print(is_path_an_img(path))