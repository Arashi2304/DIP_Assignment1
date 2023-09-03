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

def connected_components(image):
    labelled = np.zeros(image.shape)
    components = 1
    eq = {}
    for j in range(1,image.shape[0]):
        if (image[0,j] != image[0,j-1]):
            labelled[0,j] = components
            components += 1
        else:
            labelled[0,j] = labelled[0,j-1]
    
    for i in range(1,image.shape[0]):
        if image[i, 0] != image[i - 1, 0]:
            labelled[i, 0] = components
            components += 1
        else:
            labelled[i, 0] = labelled[i - 1, 0]
            
        for j in range(1, image.shape[1]):
            if image[i, j] != image[i - 1, j] and image[i, j] != image[i, j - 1]:
                labelled[i, j] = components
                components += 1
            elif image[i, j] != image[i - 1, j] and image[i, j] == image[i, j - 1]:
                labelled[i, j] = labelled[i, j - 1]
            elif image[i, j] == image[i - 1, j] and image[i, j] != image[i, j - 1]:
                labelled[i, j] = labelled[i - 1, j]
            else:
                labelled[i, j] = labelled[i, j - 1]
                if labelled[i - 1, j] != labelled[i, j - 1]:
                    temp = labelled[i - 1, j]
                    for key, value in eq.items():
                        if value == temp:
                            eq[key] = labelled[i, j - 1]

                    eq[labelled[i - 1, j]] = labelled[i, j - 1]
    for i in range(image.shape[0]):
        for j in range(image.shape[1]):
            if labelled[i, j] in eq:
                labelled[i, j] = eq[labelled[i, j]]
    plt.imshow(labelled, cmap='gray')
    plt.title('Connected Components')
    plt.axis('off')
    plt.show()
    
    character_count = 0
    min_pixel_count = 275
    
        
    for label in np.unique(labelled):
        
        pixel_count = np.sum(labelled == label)
        
        if label == 0:
            continue
        
        if pixel_count >= min_pixel_count:
            character_count += 1
            
    print("Total characters excluding punctuations:", character_count)
    
    return character_count

def count_characters(path):
    image = io.imread(path)
    binarized_image = otsu(image)
    total_components = connected_components(binarized_image)
    return total_components 