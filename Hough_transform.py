# -*- coding: utf-8 -*-
"""
Created on Sat Dec  7 16:53:49 2019

@author: hemaxi
"""

import numpy as np
import matplotlib.pyplot as plt

from skimage import data, color
from skimage.transform import hough_circle, hough_circle_peaks
from skimage.feature import canny
from skimage.draw import circle_perimeter
from skimage.util import img_as_ubyte

import cv2
import os


name = '85-3IF_CHO_Mut394_Alt'

# Load picture and detect edges

if 'CHO' in name:

    image = cv2.imread(os.path.join(r'C:\Users\hemax\Desktop\Imagens_Membrana\CHO', name + '.tif'))
#image = cv2.imread(r'C:\Users\hemax\Desktop\Imagens_Membrana\CHO\9-3IF_CHO_Branco_Alt.tif')
    
else:
    image = cv2.imread(os.path.join(r'C:\Users\hemax\Desktop\Imagens_Membrana\AGS', name + '.tif'))

image = image[:,:,-1]

minn = np.min(image)
maxx = np.max(image)

ones = np.ones(np.shape(image))
ones = ones * minn

image = (image - ones) /(maxx - minn)
image = image*255.0
image = image.astype('uint8')

edges = canny(image, sigma=3, low_threshold=10, high_threshold=50)


# Detect two radii

if 'CHO' :

    hough_radii = np.arange(40, 60, 1)
    
else:
    hough_radii = np.arange(40, 80, 1)
    
hough_res = hough_circle(edges, hough_radii)

# Select the most prominent 3 circles
accums, cx, cy, radii = hough_circle_peaks(hough_res, hough_radii, min_xdistance=60, 
                                           min_ydistance=60, total_num_peaks=500)

# Draw them
fig, ax = plt.subplots(ncols=1, nrows=1, figsize=(10, 4))
image = color.gray2rgb(image)
for center_y, center_x, radius in zip(cy, cx, radii):
    circy, circx = circle_perimeter(center_y, center_x, radius,
                                    shape=image.shape)
    image[circy, circx] = (220, 20, 20)

ax.imshow(image, cmap=plt.cm.gray)
plt.show()


