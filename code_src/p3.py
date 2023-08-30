import numpy as np
import matplotlib.pyplot as plt
import skimage.io as io

def binarize(image, threshold):
    return (image > threshold).astype(int) * 255

def between_class_variance(image, threshold):
    p1 = np.sum(image > threshold) / image.size
    p2 = 1 - p1
    
    sum_gt_threshold = np.sum(image * (image > threshold))
    count_gt_threshold = np.sum(image > threshold)
    m1 = sum_gt_threshold / count_gt_threshold if count_gt_threshold > 0 else 0
    
    sum_leq_threshold = np.sum(image * (image <= threshold))
    count_leq_threshold = np.sum(image <= threshold)
    m2 = sum_leq_threshold / count_leq_threshold if count_leq_threshold > 0 else 0
    
    return p1 * p2 * ((m1 - m2) ** 2)

def otsu(image):
    best_threshold = 0
    best_variance = 0
    for threshold in range(256):
        variance = between_class_variance(image, threshold)
        if variance > best_variance:
            best_variance = variance
            best_threshold = threshold
    binarized_image = binarize(image, best_threshold)
    
    return binarized_image

def superimpose(text_image_path,depth_image_path,background_image_path):
    text_image = io.imread(text_image_path)
    depth_image = io.imread(depth_image_path, as_gray=True)
    background_image = io.imread(background_image_path)
    
    bin_inverse_depth_map = otsu(depth_image)
    
    text_regions = text_image.copy()
    text_regions[bin_inverse_depth_map == 0] = 0
    
    final_img = background_image.copy()
    final_img[text_regions != 0] = text_regions[text_regions != 0]
    
    plt.imshow(final_img)
    plt.axis('off')
    plt.show()
    
    return final_img