from numpy import (
    ndarray,
    where,
    histogram,
    sum,
    arange,
    uint8
)

def _find_optimal_threshold_otsu(img: ndarray):
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
    if optimal_threshold is None:        
        optimal_threshold = _find_optimal_threshold_otsu(img)
    
    thresholded_image = where(img > optimal_threshold, 255, 0)
    return thresholded_image.astype(uint8)