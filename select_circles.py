# -*- coding: utf-8 -*-
"""
Created on Fri Dec 13 21:04:30 2019

@author: hemaxi
"""

if 'CHO' in name:

    image = cv2.imread(os.path.join(r'C:\Users\hemax\Desktop\Imagens_Membrana\CHO', name + '.tif'))

else:
    image = cv2.imread(os.path.join(r'C:\Users\hemax\Desktop\Imagens_Membrana\AGS', name + '.tif'))
    

or_img = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
#image = cv2.imread(r'C:\Users\hemax\Desktop\Imagens_Membrana\CHO\9-3IF_CHO_Branco_Alt.tif')
image = image[:,:,-1]

import numpy as np


v=[]
for center_y, center_x, radius in zip(cy, cx, radii):
    v.append((0,center_y, center_x, radius))
    

v = np.array(v)

out = []


for i in range(0,np.shape(v)[0]):
    a=[]
    if(v[i][0]!=10000):
        a.append(v[i])
        for j in range(0,np.shape(v)[0]):
            if(v[j][0]!=10000 and i!=j):
                if(np.abs(v[i][1]-v[j][1])<=50 and np.abs(v[i][2]-v[j][2])<=50):
                    a.append(v[j])
                    v[j][0] = 10000
        v[i][0]=10000
            
                
    if(a != []):
        out.append(np.mean(a, axis=0))
        
        
import pickle
from skimage.color import label2rgb
import skimage


if 'CHO' in name:
    
    pickle_in = open(os.path.join(r'C:\Users\hemax\Desktop\Imagens_Membrana\predictions\CHO', name + '.tif.pickle'), "rb")
else:

    pickle_in = open(os.path.join(r'C:\Users\hemax\Desktop\Imagens_Membrana\predictions\AGS', name + '.tif.pickle'), "rb")
masks = pickle.load(pickle_in)

prediction = np.zeros(np.shape(masks[:,:,0]))

for i in range(len(masks[0,0,:])):
    prediction[masks[:,:,i]==1] = i + 1
    
    
masks_labelled = prediction.astype(np.int64)
masks = skimage.morphology.remove_small_objects(masks_labelled, min_size = 400)  

prediction = masks    

I = label2rgb(prediction, bg_label =0, bg_color=(1,1,1))

    
    
# Draw them
fig, (ax1,ax2) = plt.subplots(ncols=2, nrows=1)
#image = color.gray2rgb(image)
for a,center_y, center_x, radius in out:
    circy, circx = circle_perimeter(np.int(center_y), np.int(center_x), np.int(radius),
                                    shape=image.shape)
    #image[circy, circx] = (220, 20, 20)
    I[circy, circx] = (0,0,0)

import matplotlib.pyplot as plt

plt.figure()
plt.imshow(I)

plt.figure()
plt.imshow(or_img)

# =============================================================================
# ax1.imshow(or_img)
# ax1.set_title('Original Image')
# ax2.imshow(I)
# ax2.set_title('Segmentation Mask (nucleus + membrane)')
# plt.show()
# =============================================================================
