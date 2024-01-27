import timeit
import os
from single_node import threshold_image
from custom_thresholding import simple_image_thresholding
from parallel import parallel_thresholding

import cv2
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

def _measure_func_time(func) -> float:
    start_time = timeit.default_timer()
    func
    end_time = timeit.default_timer()
    elapsed_time = (end_time - start_time) * 1000 #Miliseconds
    return elapsed_time


def _get_file_name(file_path: str):
    return os.path.basename(file_path)


def benchmark(img_paths: list[str], 
              img_sizes:list[tuple] = [(300, 300), (900, 900), (2700, 2700)],
              use_cv2: bool = False) -> list[pd.DataFrame]:
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
    
    def plot_results(images_metrics: list[pd.DataFrame], figure_axes):
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