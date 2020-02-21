# -*- coding: utf-8 -*-
"""
Created on Wed Dec 18 12:04:03 2019

@author: hemaxi
"""


import pandas as pd
import numpy as np
from scipy.spatial import distance
from skimage.draw import circle_perimeter


#df = pd.read_csv(r'C:\Users\hemax\Desktop\Imagens_Membrana\final_all_grouped.csv') ## AGS
df = pd.read_csv(r'C:\Users\hemax\Desktop\Imagens_Membrana\final_results_CHO.csv') ## CHO

new_column = []

for index, row in df.iterrows():
        x_nucleus = row['Centroid_x']
        y_nucleus = row['Centroid_y']
        
        x_circle = row['Circle_x']
        y_circle = row['Circle_y']
        radius = row['radius']
        
        
        circy, circx = circle_perimeter(np.int(y_circle), np.int(x_circle), np.int(radius),
                                    shape=(1040, 1388))
        
        distances = []
        #image[circy, circx] = (220, 20, 20)
        for (circunfy, circunfx) in zip(circy, circx):
        
            dist = distance.euclidean((x_nucleus, y_nucleus),(circunfx, circunfy))
        
            distances.append(dist)
            
        
        
        distances = np.asarray(distances)
        new_column.append(distances)

df['dist_centr_circle_pts'] = new_column