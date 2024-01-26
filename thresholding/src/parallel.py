import os
from concurrent.futures import ProcessPoolExecutor
from single_node import _find_optimal_threshold, threshold_image
from functools import partial

from numpy import array, ndarray, mean, vstack


def _get_or_check_processes(num_processes: int = None):
    """
    Retrieves or checks the specified number of processes for a task.

    Args:
        num_processes (int, optional): Number of processes to use for the task. 
            If not provided, it will use the number of available cores.
            Defaults to None.

    Returns:
        int: The validated number of processes.

    Raises:
        AssertionError: If the provided `num_processes` is not an integer.
    """
    if num_processes is None:
        num_processes = find_available_cores()
    assert isinstance(num_processes, int), "Number of processes for thresholding the image must be an int"
    return num_processes



def find_available_cores() -> int:
    """
    Returns the number of available CPU cores on the current system.

    Returns:
        int: The number of available CPU cores.
    """
    return os.cpu_count()


def split_image(img: ndarray, num_parts: int = None) -> ndarray[ndarray]:
    """
    Splits an image matrix into a specified number of parts.

    Args:
        img (ndarray): Matrix representation of the image
        num_parts (int, optional): Number of parts to split the image. 
        If not provided, it will use the number of available cores.
        Defaults to None.

    Returns:
        ndarray[ndarray]: List of image parts.
    """
    if num_parts is None:
        num_parts = find_available_cores()
    assert isinstance(num_parts, int), "Number of parts for splitting the image must be int"
    height, width = img.shape[:2]
    one_part_height = height // num_parts
    img_parts = [img[i*one_part_height:(i+1)*one_part_height] for i in range(num_parts)]
    return array(img_parts)


def _find_parallel_optimal_threshold(img: ndarray, num_processes: int = None) -> int:
    """
    Finds the optimal threshold for image thresholding using parallel processing.
    The optimal threshold is found for every image partition then the mean of all will 
    be considered as the optimal threshold.

    Args:
        img (ndarray): Matrix representation of the image.
        num_processes (int, optional): Number of processes to use for parallelization. 
            If not provided, it will use the number of available cores.
            Defaults to None.

    Returns:
        int: The optimal threshold for image thresholding.
    """
    num_processes:int = _get_or_check_processes(num_processes)
    img_parts: ndarray = split_image(img) 
    with ProcessPoolExecutor(max_workers=num_processes) as executor:
        optimal_threshold_votes: list = list(executor.map(_find_optimal_threshold, img_parts))
    print(f"The optimal thresholds for each partition are: {optimal_threshold_votes}")
    optimal_threshold = int(mean(optimal_threshold_votes))
    print(f"The optimal threshold is: {optimal_threshold}")
    return optimal_threshold


def _merge_img_parts(img_parts: ndarray[ndarray]) -> ndarray:
    """
    Merges a list of image parts into a single image matrix.

    Args:
        img_parts (ndarray[ndarray]): List of image parts to be merged.

    Returns:
        ndarray: Merged image matrix.
    """
    return vstack(img_parts)


def parallel_thresholding(img,
                          optimal_threshold_per_partition: bool = False, 
                          num_processes: int = None):
    """
    Applies thresholding to an image using parallel processing.

    Args:
        img (ndarray): Matrix representation of the image.
        optimal_threshold_per_partition (bool, optional): 
            If True, uses a different optimal threshold for each partition.
            If False, uses a single optimal threshold for the entire image.
            Defaults to False.
        num_processes (int, optional): Number of processes to use for parallelization. 
            If not provided, it will use the number of available cores.
            Defaults to None.

    Returns:
        ndarray: Thresholded image matrix.
    """
    num_processes:int = _get_or_check_processes(num_processes)
    optimal_threshold = _find_parallel_optimal_threshold(img)
    img_parts: ndarray = split_image(img)
    if optimal_threshold_per_partition is False:
        threshold_n_img = partial(threshold_image, optimal_threshold=optimal_threshold)
    else: 
        threshold_n_img = threshold_image
    with ProcessPoolExecutor(max_workers=num_processes) as executor:
        thresholded_images: list = list(executor.map(threshold_n_img, img_parts))
    return _merge_img_parts(thresholded_images)

         

