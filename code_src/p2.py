import numpy as np
import matplotlib.pyplot as plt
from skimage import io
import time as time

def binarize(image, threshold):
    return (image > threshold).astype(int) * 255

def within_class_variance(image, threshold):
    binary_image = image > threshold
    background = image[~binary_image]
    foreground = image[binary_image]
    
    var_background = np.var(background) if len(background) > 0 else 0
    var_foreground = np.var(foreground) if len(foreground) > 0 else 0
    
    within_class_var = (
        (len(background) / image.size) * var_background +
        (len(foreground) / image.size) * var_foreground
    )
    
    return within_class_var

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

def otsu(path):
    image = io.imread(path, as_gray=True)
    shape = image.shape
    image = image.flatten()
    threshold_values = np.arange(1, 255)
    within_class_variances = np.zeros(254)
    between_class_variances = np.zeros(254)
    for i in range(len(threshold_values)):
        within_class_variances[i] = within_class_variance(image, threshold_values[i])
        between_class_variances[i] = between_class_variance(image, threshold_values[i])
    print(f'Minimum of within-class variance: {np.argmin(within_class_variances)}')
    print(f'Maximum of between-class variance: {np.argmax(between_class_variances)}')
    plt.figure(1)
    plt.plot(threshold_values, within_class_variances, label='Within-class variance')
    plt.plot(threshold_values, between_class_variances, label='Between-class variance')
    plt.legend()
    plt.title('Within-class and between-class variance')
    plt.xlabel('Threshold value')
    plt.ylabel('Variance')
    plt.show()
    
    start_time = time.time()
    within_class_threshold = np.argmin(within_class_variances)
    bin_image_within = binarize(image, within_class_threshold)
    bin_image_within = bin_image_within.reshape(shape)
    within_class_runtime = time.time() - start_time
    threshold = np.argmax(between_class_variances)
    binary_image = binarize(image, threshold)
    binary_image = binary_image.reshape(shape)
    
    start_time = time.time()
    between_class_threshold = np.argmax(between_class_variances)
    bin_image_between = binarize(image, between_class_threshold)
    bin_image_between = bin_image_between.reshape(shape)
    between_class_runtime = time.time() - start_time

    print(f"Runtime of within-class variance method: {within_class_runtime:.6f}")
    print(f"Runtime of between-class variance method: {between_class_runtime:.6f}")
     
    threshold = np.argmax(between_class_variances)
    binary_image = binarize(image, threshold)
    binary_image = binary_image.reshape(shape)
    plt.figure(2)
    plt.imshow(binary_image, cmap='gray')
    plt.axis('off')
    plt.title(f'Binarized image with threshold: {threshold}')
    plt.show()
    
    return binary_image          