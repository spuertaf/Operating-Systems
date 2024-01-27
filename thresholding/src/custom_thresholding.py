from numpy import (
    ndarray,
    where,
    histogram,
    sum,
    arange,
    uint8
)

def _find_optimal_threshold_otsu(img: ndarray):
    """
    Finds the optimal threshold for image segmentation using Otsu's method.

    Args:
        img (ndarray): The input image as a NumPy array.

    Returns:
        int: The optimal threshold value for image segmentation.
    """
    # Obtain image's histogram
    hist, _ = histogram(img.flatten(), bins=256, range=[0,256])
    # Normalize the histogram
    norm_hist = hist / hist.sum()
    
    total_sum = sum(arange(256) * norm_hist)
    sumB, wB, threshold = (0, 0, 0)
    max_variance = 0 # Max variance between classes
    
    # Iterate over all grays for finding the optimal threshold
    for i in range(256):
        wB += norm_hist[i]
        if wB == 0: continue
        
        wF = 1 - wB
        if wF == 0: break
        
        sumB += i * norm_hist[i]
        mB = sumB / wB
        mF = (total_sum - sumB) / wF

        variance = wB * wF * (mB - mF)**2
        
        if variance > max_variance:
            max_variance = variance
            threshold = i
    
    print(f"The optimal threshold is: {threshold}")
    return threshold
    

def simple_image_thresholding(img: ndarray, 
                              optimal_threshold: int = None):
    """
    Applies simple image thresholding to the input image.
    For every pixel value where the value is greater than the optimal threshold
    the said pixel value is set to 255 (white), for the opposite case,
    where the pixel value is lesser than the optimal threshold the pixel value
    is set to 0 (black).

    Args:
        img (ndarray): The input image as a NumPy array.
        optimal_threshold (int, optional): The threshold value for image segmentation.
            If None, the optimal threshold is calculated using Otsu's method.
            Defaults to None.

    Returns:
        ndarray: The thresholded image as a NumPy array.
    """
    if optimal_threshold is None:        
        optimal_threshold = _find_optimal_threshold_otsu(img)
    
    thresholded_image = where(img > optimal_threshold, 255, 0)
    return thresholded_image.astype(uint8)