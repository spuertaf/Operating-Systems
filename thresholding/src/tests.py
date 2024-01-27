import timeit
import os
from single_node import threshold_image
from custom_thresholding import simple_image_thresholding
from parallel import parallel_thresholding

import cv2
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from numpy import ndarray


def _measure_func_time(func) -> float:
    """
    Measures the execution time of a given function.

    Args:
        func (Callable): The function for which the execution time needs to be measured.

    Returns:
        float: The elapsed time in milliseconds for the execution of the provided function.
    """
    start_time = timeit.default_timer()
    func
    end_time = timeit.default_timer()
    elapsed_time = (end_time - start_time) * 1000 #Miliseconds
    return elapsed_time


def _get_file_name(file_path: str):
    """
    Extracts the file name from the given file path.

    Args:
        file_path (str): A string representing the full path of the file.

    Returns:
        str: The file name extracted from the provided file path.
    """
    return os.path.basename(file_path)


def benchmark(img_paths: list[str], 
              img_sizes:list[tuple] = [(300, 300), (900, 900), (2700, 2700)],
              use_cv2: bool = False) -> list[pd.DataFrame]:
    """
    Benchmarks image processing algorithms on a set of images with different sizes.
    In case the use_cv2 argument is False the custom_thresholding simple_image_thresholding algorithm
    is used.

    Args:
        img_paths (list[str]): A list of file paths to the images for benchmarking.
        img_sizes (list[tuple], optional): A list of tuples representing different image sizes to be tested.
            Defaults to [(300, 300), (900, 900), (2700, 2700)].
        use_cv2 (bool, optional): A flag indicating whether to use the OpenCV library for image processing.
            Defaults to False.

    Returns:
        list[pd.DataFrame]: A list of Pandas DataFrames containing benchmarking results for each image.
    """
    thresholding_algorithm = simple_image_thresholding if use_cv2 is False else threshold_image
    results = []
    for path in img_paths:
        img = cv2.imread(path, cv2.IMREAD_GRAYSCALE)
        total_times = []
        for size in img_sizes:
            img = cv2.resize(img, size)
            threshold_single_node_time: float = _measure_func_time(thresholding_algorithm(img))
            voting_parallel_thresholding_time:float = _measure_func_time(parallel_thresholding(img, False, use_cv2=use_cv2))
            non_voting_parallel_thresholding_time: float = _measure_func_time(parallel_thresholding(img, True, use_cv2=use_cv2))
            times_taken = [threshold_single_node_time,
                            voting_parallel_thresholding_time,
                            non_voting_parallel_thresholding_time,
                            size]
            total_times.append(times_taken)
        time_df = pd.DataFrame(columns=["threshold_single_node_time", "voting_parallel_thresholding_time", "non_voting_parallel_thresholding_time", "size"],
                               data= total_times)
        time_df["file_name"] = _get_file_name(path)
        results.append(time_df)
    return results


def plot_benchmarking(img_paths: list[str], 
                     img_sizes:list[tuple] = [(1000, 1000), (2000, 2000), (3000, 3000), (4000, 4000), (5000, 5000)],
                     use_cv2: bool = False) -> list[pd.DataFrame]:
    """
    Performs benchmarking on a set of images and plots the results.

    Args:
        img_paths (List[str]): A list of file paths to the images for benchmarking.
        img_sizes (List[Tuple[int, int]], optional): A list of tuples representing different image sizes to be tested.
            Defaults to [(1000, 1000), (2000, 2000), (3000, 3000), (4000, 4000), (5000, 5000)].
        use_cv2 (bool, optional): A flag indicating whether to use the OpenCV library for image processing.
            Defaults to False.

    Returns:
        List[pd.DataFrame]: A list of Pandas DataFrames containing benchmarking results for each image.
    """
    
    def plot_results(images_metrics: list[pd.DataFrame], 
                     figure_axes: ndarray) -> ndarray:
        """
        Plots benchmarking results for different image processing metrics.

        Args:
            images_metrics (list[pd.DataFrame]): A list of Pandas DataFrames containing benchmarking results for each image.
            figure_axes (ndarray): The figure axes or subplot layout for displaying the plots.

        Returns:
            ndarray: The modified figure axes with the plotted results.
        """
        metrics_cols = ["threshold_single_node_time", 
                        "voting_parallel_thresholding_time", 
                        "non_voting_parallel_thresholding_time"]
        flag = True if len(images_metrics) == 1 else False
        for i, image_metric in enumerate(images_metrics):
            for metric_col in metrics_cols:
                if flag:
                    sns.lineplot(data=image_metric, 
                                x=image_metric["size"].apply(lambda x: x[0]), 
                                y=metric_col,
                                label=metric_col)
                else:
                    sns.lineplot(data=image_metric, 
                                x=image_metric["size"].apply(lambda x: x[0]), 
                                y=metric_col,
                                label=metric_col,
                                ax= figure_axes[i])
            if flag: 
                figure_axes.set_title(image_metric["file_name"][0]) 
                return figure_axes
            figure_axes[i].set_title(image_metric["file_name"][0])
        return figure_axes
        
    results: list[pd.DataFrame] = benchmark(img_paths, img_sizes, use_cv2)
    print(results)
    _, axes = plt.subplots(ncols=len(results), 
                           figsize=(12, 5))
    axes = plot_results(results, axes)
    plt.show()