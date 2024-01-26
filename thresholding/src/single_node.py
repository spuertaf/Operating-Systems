from numpy import ndarray
import cv2

def _find_optimal_threshold(img: ndarray) -> float:
    """
    Finds the optimal threshold using Otsu's method.

    Args:
        img (ndarray): Matrix representation of the image.

    Returns:
        float: The optimal threshold for image thresholding.
    """
    optimal_threshold, _ = cv2.threshold(img, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
    print(f"The optimal threshold is: {optimal_threshold}")
    return optimal_threshold


def threshold_image(img: ndarray,
                    optimal_threshold: float = None) -> ndarray:
    """
    Applies thresholding to an image using a specified or optimal threshold.

    Args:
        img (ndarray): Matrix representation of the image.
        optimal_threshold (float, optional): 
            If provided, uses the specified threshold for image thresholding.
            If not provided, it finds the optimal threshold using Otsu's method.
            Defaults to None.

    Returns:
        ndarray: Thresholded image matrix.
    """
    if optimal_threshold is None:
        optimal_threshold =_find_optimal_threshold(img)

    _, thresholded_image = cv2.threshold(img, optimal_threshold, 255, cv2.THRESH_BINARY)
    return thresholded_image