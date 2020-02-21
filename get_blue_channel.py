# -*- coding: utf-8 -*-
"""
Created on Sat Dec 14 10:20:57 2019

@author: Hemaxi
"""

'''Extract the blue channel from the RGB images.'''

#import the packages
import os
import numpy as np
import cv2

#image directory
imgs_dir = r'C:\Users\hemax\Desktop\Imagens_Membrana\CHO'
#directory to save the blue component of the images
save_dir = r'C:\Users\hemax\Desktop\Imagens_Membrana\CHO_blue'

# run through the directory
for img in os.listdir(imgs_dir):
    #read the image
    image = cv2.imread(os.path.join(imgs_dir, img))
    #extract the blue channel
    image_blue = image[:,:,0]
    #save the image corresponding to the blue channel
    cv2.imwrite(os.path.join(save_dir, img), image_blue)