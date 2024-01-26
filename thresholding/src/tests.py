import timeit
import os
from single_node import threshold_image
from parallel import parallel_thresholding

import cv2
import pandas as pd
#import seaborn as sns
#import matplotlib.pyplot as plt

def _measure_func_time(func):
    start_time = timeit.default_timer()
    func
    end_time = timeit.default_timer()
    elapsed_time = start_time - end_time
    return elapsed_time


def _get_file_name(file_path: str):
    return os.path.basename(file_path)


def benchmark(img_paths: list[str], 
              img_sizes:list[tuple] = [(300, 300), (900, 900), (2700, 2700)]) -> list[pd.DataFrame]:
    results = []
    for path in img_paths:
        img = cv2.imread(path, cv2.IMREAD_GRAYSCALE)
        total_times = []
        for size in img_sizes:
            img = cv2.resize(img, size)
            threshold_single_node_time: float = _measure_func_time(threshold_image(img))
            voting_parallel_thresholding_time:float = _measure_func_time(parallel_thresholding(img, False))
            non_voting_parallel_thresholding_time: float = _measure_func_time(parallel_thresholding(img, True))
            times_taken = [threshold_single_node_time,
                            voting_parallel_thresholding_time,
                            non_voting_parallel_thresholding_time,
                            size]
            total_times.append(times_taken)
        time_df = pd.DataFrame(columns=["threshold_single_node_time", "voting_parallel_thresholding_time", "non_voting_parallel_thresholding_time", "size"] ,data= total_times)
        time_df["file_name"] = _get_file_name(path)
        results.append(time_df)
    return results





if __name__ == "__main__":
    df = benchmark(["C:\\Users\\puert\\OneDrive\\Escritorio\\thresholding\\img\\person.jpeg"])[0]
    sns.lineplot(data=df, x=df.index, y="threshold_single_node_time")
    plt.show() 
        





