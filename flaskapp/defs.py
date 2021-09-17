import pandas as pd
import numpy as np
import os
import sys
from PIL import Image
import scipy.ndimage.interpolation as interp
import cv2

from matplotlib import colors
from matplotlib.ticker import PercentFormatter
import matplotlib.pyplot as plt

def ofromt(path1, path2, mode=0, root='static/'):
    image1 = Image.open(path1)
    image2 = Image.open(path2)
    width1, height1 = image1.size
    width2, height2 = image2.size

    x = 0
    y = 0
    height = 0
    width = 0

    if mode == 0:
        coeff = height1 / height2
        height2 = int(height2 * coeff)
        width2 = int(width2 * coeff)

        height = height1
        width = width1 + width2
        x = width1

    elif mode == 1:
        coeff = width1 / width2
        height2 = int(height2 * coeff)
        width2 = int(width2 * coeff)

        height = height1 + height2
        width = width1
        y = height1

    image2 = image2.resize((width2, height2), Image.ANTIALIAS)

    img = Image.new('RGB', (width, height))
    img.paste(image1, (0, 0))
    img.paste(image2, (x, y))
    img.save(root + 'timages_joined.png')

def GRAPHS(path, root, name):
    from skimage import io
    import matplotlib.pyplot as plt
    image = io.imread(path)

    _ = plt.hist(image.ravel(), bins = 64, color = 'Orange', )
    _ = plt.hist(image[:, :, 0].ravel(), bins = 64, color = 'Red', alpha = 0.7)
    _ = plt.hist(image[:, :, 1].ravel(), bins = 64, color = 'Green', alpha = 0.7)
    _ = plt.hist(image[:, :, 2].ravel(), bins = 64, color = 'Blue', alpha = 0.7)
    _ = plt.xlabel('Intensity Value')
    _ = plt.ylabel('Count')
    _ = plt.legend(['Total', 'Red Channel', 'Green Channel', 'Blue Channel'])
    _ = plt.title(name)

    plt.savefig(root)
