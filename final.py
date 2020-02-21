# -*- coding: utf-8 -*-
"""
Created on Sat Dec 14 13:59:52 2019

@author: hemaxi
"""


'''Membrane Segmentation using Hough Transform'''

import os
import numpy as np
import cv2
import matplotlib.pyplot as plt
from skimage import data, color
from skimage.transform import hough_circle, hough_circle_peaks
from skimage.feature import canny
from skimage.draw import circle_perimeter
from skimage.util import img_as_ubyte
import pickle
from skimage.color import label2rgb
import skimage

imgs_dir = r'C:\Users\hemax\Desktop\Imagens_Membrana\CHO'
predictions_path = r'C:\Users\hemax\Desktop\Imagens_Membrana\predictions\CHO'



for img, pkl in zip(os.listdir(imgs_dir), os.listdir(predictions_path)):
    
    # Load picture and detect edges
    
    image = cv2.imread(os.path.join(imgs_dir, img))
    or_img = image
    
    image = image[:,:,-1]
    
    
    #normalize the image
    
    minn = np.min(image)
    maxx = np.max(image)
    
    ones = np.ones(np.shape(image))
    ones = ones * minn
    
    image = (image - ones) /(maxx - minn)
    image = image*255.0
    image = image.astype('uint8')
    
    
    #detect the edges
    
    edges = canny(image, sigma=3, low_threshold=10, high_threshold=50)
    
    
    # Detect between a range of radii (from 40 pixels to 80 pixels)
    hough_radii = np.arange(40, 80, 1)
    hough_res = hough_circle(edges, hough_radii)
    
    # Select the most prominent 500 circles
    accums, cx, cy, radii = hough_circle_peaks(hough_res, hough_radii, min_xdistance=60, 
                                               min_ydistance=60, total_num_peaks=500)



    
    
    
    ## remove overlapping circles

    #put all the predicted circles in an array
    v=[]
    for center_y, center_x, radius in zip(cy, cx, radii):
        v.append((0,center_y, center_x, radius))
    
    
    #convert a list to array

    v = np.array(v)

    out = []


    for i in range(0,np.shape(v)[0]):
        a=[]
        if(v[i][0]!=10000):
            a.append(v[i])
            for j in range(0,np.shape(v)[0]):
                if(v[j][0]!=10000 and i!=j):
                    if(np.abs(v[i][1]-v[j][1])<=60 and np.abs(v[i][2]-v[j][2])<=60):
                        a.append(v[j])
                        v[j][0] = 10000
            v[i][0]=10000
                
                    
        if(a != []):
            out.append(np.mean(a, axis=0))
        
        
    
    


   ## segmentation mask

    pickle_in = open(os.path.join(predictions_path, pkl), "rb")
    masks = pickle.load(pickle_in)
    
    prediction = np.zeros(np.shape(masks[:,:,0]))
    
    for i in range(len(masks[0,0,:])):
        prediction[masks[:,:,i]==1] = i + 1
        
        
    masks_labelled = prediction.astype(np.int64)
    masks = skimage.morphology.remove_small_objects(masks_labelled, min_size = 400)  
    
    prediction = masks    

    I = label2rgb(prediction, bg_label =0, bg_color=(1,1,1))

    with open(os.path.join(r'C:\Users\hemax\Desktop\Centers\CHO', img + '.pkl'),'wb') as f:
        pickle.dump(out, f)

    #plot
    
    fig, (ax1,ax2, ax3) = plt.subplots(ncols=3, nrows=1)
    image = color.gray2rgb(image)
    for a,center_y, center_x, radius in out:
        circy, circx = circle_perimeter(np.int(center_y), np.int(center_x), np.int(radius),
                                    shape=image.shape)
        I[circy, circx] = (0,0,0)
        image[circy, circx] = (255,0,0)

    ax1.imshow(or_img)
    ax1.set_title('Original Image')
    ax2.imshow(image)
    ax2.set_title('Membrane')
    ax3.imshow(I)
    ax3.set_title('Segmentation Mask (nucleus + membrane)')
    plt.show()


    #save the plot
    cv2.imwrite(os.path.join(r'C:\Users\hemax\Desktop\Masks\AGS', img + '.jpg'), I*255.0)












