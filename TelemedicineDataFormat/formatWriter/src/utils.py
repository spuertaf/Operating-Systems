import os


def get_file_name_from_abs_path(abs_path: str) -> str: 
    """
    Get the file name from an absolute path.

    Args:
        abs_path (str): The absolute path of the file.

    Returns:
        str: The file name extracted from the absolute path.
    """
    return os.path.basename(abs_path)