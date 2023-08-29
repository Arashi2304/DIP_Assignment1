import numpy as np
import matplotlib.pyplot as plt
import skimage.io as io

def get_histogram(path):
    img = io.imread(path, as_gray=True).flatten()
    histogram = np.zeros(256)
    for i in range(0, 256):
        histogram[i] = np.sum(img == i)
        #histogram[i] = histogram[i] / img.size
    plt.bar(np.arange(0, 256), histogram)
    plt.title(' Image Histogram')
    plt.xlabel('Intensity levels')
    plt.ylabel('Frequency')
    plt.show()
    avg_intensity = np.sum(np.arange(0, 256) * histogram) / np.sum(histogram)
    print('Average intensity of the image (Using the histogram): ', avg_intensity)    
    print('Average intensity of the image (Using the image): ', np.sum(img) / img.size)
    return histogram