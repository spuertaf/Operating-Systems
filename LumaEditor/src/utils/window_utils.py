from os import path


def get_luma_file_path(file_path: str):
    """Generate a path for a luma file based on the given file path.

    Args:
        file_path (str): The path of the original file.

    Returns:
        str: The path for the luma file.
    """
    extension = path.splitext(file_path)[1]
    return file_path.replace(extension, ".luma")
        