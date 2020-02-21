# -*- coding: utf-8 -*-
"""
Created on Sat Dec 14 10:29:57 2019

@author: Hemaxi
"""

'''Extract features from each nucleus in the DAPI image and save in a pandas dataframe.'''

#import the packages
import cv2
import os
import pickle
import pandas as pd
import numpy as np 
from skimage.segmentation import clear_border
from skimage.measure import regionprops, shannon_entropy
import matplotlib.pyplot as plt
from skimage.feature import local_binary_pattern, greycomatrix
from skimage import exposure
import skimage
from skimage.measure import label


def obtain_features(images_path, predictions_path, types, pickle_obj):
	#create the dataframe
    features = pd.DataFrame(columns = ["Image", "Area", "BBox_Area", "Perimeter", "Eccentricity", "Total Intensity", "Mean Intensity", "Solidity",
                                      "Local Binary Pattern", "Entropy", "Shannon Entropy", "Centroid_x", "Centroid_y"])

	#for each image and prediction, read the image, load the pickle object
    for img, pred in zip(os.listdir(images_path), os.listdir(predictions_path)):
		#read the image
        image = cv2.imread(os.path.join(images_path, img), cv2.IMREAD_GRAYSCALE)
		#image = exposure.equalize_hist(image)
		######image = aux_percentile(img, image, types, values)     
		#image = exposure.rescale_intensity(image, in_range=(p2, p98))    

        if (pickle_obj):

			#load the pickle
            pickle_in = open(os.path.join(predictions_path, pred), "rb")
            masks = pickle.load(pickle_in)
            
            prediction = np.zeros(np.shape(masks[:,:,0]))          

            for i in range(len(masks[0,0,:])):
                prediction[masks[:,:,i]==1] = i+1     
            
            
            masks_labelled = prediction      

            masks_labelled = masks_labelled.astype(np.int64)
			#create a labelled images containing predictions, and remove the objects located at the boundaries
			#masks_labelled = lbl(masks)
            masks = skimage.morphology.remove_small_objects(masks_labelled , min_size = 400)
            masks_labelled = lbl2(masks)	      
            masks_labelled = masks_labelled.astype(np.int64)
            
			#plt.figure()
			#plt.imshow(masks_labelled)   

        else:
		
            masks = cv2.imread(os.path.join(predictions_path, pred), cv2.IMREAD_GRAYSCALE)
            
            masks = skimage.morphology.remove_small_objects(masks , min_size = 20)        
            masks_labelled = lbl2(masks)	        



		#compute features for each nuclei and add to the features dataframe
        features = compute_props(image, masks_labelled, features, img)

    return features


def aux_percentile(img, image, types, values):
    found = False
    i = 0
    while (not found and i<len(types)):
        if(types[i] in img):
            found = True
            subset = values[values.Image.str.startswith(types[i])]
            p2 = subset.iat[0,2]
            p98 = subset.iat[0,3]
            image_rescaled = exposure.rescale_intensity(image, in_range=(p2, p98))  
        else:
            i=i+1
    return image_rescaled


def lbl(masks):
	prediction = np.zeros(np.shape(masks[:,:,0]))

	#create the labelled image, read each mask and give a label on the prediction image
	for i in range(len(masks[0,0,:])):
		prediction[masks[:,:,i]==1] = i+1

	#remove objects located at boundaries
	finalotp = clear_border(prediction, buffer_size=1)
	return finalotp


def lbl2(masks):
	#label the masks when we are talking about images and then clear the borders 
	prediction = label(masks)
	prediction = clear_border(prediction, buffer_size=1)

	return prediction



from scipy import ndimage as ndi
from skimage.filters import gabor_kernel

# prepare filter bank kernels
# =============================================================================
# kernels = []
# for theta in range(4):
#     theta = theta / 4. * np.pi
#     for sigma in (1, 3):
#         for frequency in (0.05, 0.25):
#             kernel = gabor_kernel(frequency, theta=theta,
#                                           sigma_x=sigma, sigma_y=sigma)
#             kernels.append(kernel)
# 
# =============================================================================

def compute_props(image, masks_labelled, features, img):
	properties = regionprops(masks_labelled, intensity_image = image)
	#for each nuclei, save the corresponding features 
	for region in properties:
		area = float(region.area)
		bboxarea = float(region.bbox_area) 
		perimeter = region.perimeter 
		eccentricity = region.eccentricity
		total_intensity = float(np.sum(region.intensity_image))
		mean_intensity = region.mean_intensity
		solidity = region.solidity
		centroid = region.centroid       
        
		#feats = compute_feats(region.intensity_image,kernels)
		#pw = power(region.intensity_image, kernels[0])      
		lbp = local_binary_pattern(region.intensity_image, 3, 3, method = 'ror')      
		entr = compute_entropy(region.intensity_image)      
		shannon_entr = shannon_entropy(region.intensity_image)              
# =============================================================================
# 		res = {"Image": img, "Area": area, "BBox_Area": bboxarea, "Perimeter": perimeter, "Eccentricity": eccentricity, 
# 				"Total Intensity": total_intensity, "Mean Intensity": mean_intensity, "Solidity": solidity, "Gabor Mean":
#              feats[0,0], "Gabor Var": feats[0,1], "Gabor Amplitude": np.mean(pw), "Gabor Energy": np.sum(pw**2),
#              "Local Binary Pattern": compute_energy(lbp), "Entropy": compute_energy(entr)}
# =============================================================================
		res = {"Image": img, "Area": area, "BBox_Area": bboxarea, "Perimeter": perimeter, "Eccentricity": eccentricity, 
				"Total Intensity": total_intensity, "Mean Intensity": mean_intensity, "Solidity": solidity,
             "Local Binary Pattern": compute_energy(lbp), "Entropy": compute_amplitude(entr),
             "Shannon Entropy": shannon_entr, "Centroid_y": centroid[0], "Centroid_x": centroid[1]}
		row = len(features)
		features.loc[row] = res
	return features


def compute_feats(image, kernels):
	#compute mean and var of filtered images
    feats = np.zeros((len(kernels), 2), dtype=np.double)
    for k, kernel in enumerate(kernels):
        filtered = ndi.convolve(image, kernel, mode='wrap')
        feats[k, 0] = filtered.mean()
        feats[k, 1] = filtered.var()
    return feats

def power(image, kernel):
    # Normalize images for better comparison.
    image = (image - image.mean()) / image.std()
    return np.sqrt(ndi.convolve(image, np.real(kernel), mode='wrap')**2 +
                   ndi.convolve(image, np.imag(kernel), mode='wrap')**2)

def compute_entropy(image):
	from skimage.filters.rank import entropy
	from skimage.morphology import disk
	im_aux = image / np.max(image)
	filtered = entropy(im_aux, disk(3))
	return filtered

def compute_power(image):
	return np.sqrt((np.real(image)**2) + (np.imag(image)**2))

def compute_energy(image):
	aux = compute_power(image)
	return np.sum(aux**2)

def compute_amplitude(image):
	aux = compute_power(image)
	return np.mean(aux)
