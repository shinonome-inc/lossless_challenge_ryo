from collections import Counter
import matplotlib.pyplot as plt
import filter
import numpy as np
def load_mnist(path, kind='train'):
    import os
    import gzip
    import numpy as np


    """Load MNIST data from `path`"""
    labels_path = os.path.join(path,
                               '%s-labels-idx1-ubyte.gz'
                               % kind)
    images_path = os.path.join(path,
                               '%s-images-idx3-ubyte.gz'
                               % kind)

    with gzip.open(labels_path, 'rb') as lbpath:
        labels = np.frombuffer(lbpath.read(), dtype=np.uint8,
                               offset=8)

    with gzip.open(images_path, 'rb') as imgpath:
        images = np.frombuffer(imgpath.read(), dtype=np.uint8,
                               offset=16).reshape(len(labels), 784)

    return images, labels

X_train, y_train = load_mnist('', kind='train')

sub_pixels = np.zeros((60000, 784), dtype = np.uint8)
up_pixels = np.zeros((60000, 784), dtype = np.uint8)
average_pixels = np.zeros((60000, 784), dtype = np.uint8)
peath_pixels = np.zeros((60000, 784), dtype = np.uint8)

for raw in range(60000):
    pixel_raw = filter.Filter(X_train[raw, :].reshape(28, 28))
    sub_pixels[raw, :] = pixel_raw.sub().reshape(-1,)
    up_pixels [raw, :] = pixel_raw.up().reshape(-1,)
    average_pixels[raw, :] = pixel_raw.average().reshape(-1,)
    peath_pixels[raw, :] = pixel_raw.peath().reshape(-1,)

fig = plt.figure()
axis1 = fig.add_subplot(5, 1, 1)
axis1.hist(np.ravel(X_train), range=(0, 255))
plt.title("元画像群")
axis2 = fig.add_subplot(5, 1, 2)
axis2.hist(np.ravel(sub_pixels), range=(0, 255))
plt.title("Subフィルター後")
axis3 = fig.add_subplot(5, 1, 3)
axis3.hist(np.ravel(up_pixels), range=(0, 255))
plt.title("Upフィルター後")
axis4 = fig.add_subplot(5, 1, 4)
axis4.hist(np.ravel(average_pixels), range=(0, 255))
plt.title("Averageフィルター後")
axis5 = fig.add_subplot(5, 1, 5)
axis5.hist(np.ravel(peath_pixels), range=(0, 255))
plt.title("Peathフィルター後")
plt.show()
























                            








