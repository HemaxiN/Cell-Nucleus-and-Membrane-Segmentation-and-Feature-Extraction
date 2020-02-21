# -*- coding: utf-8 -*-
"""
Created on Tue Dec 17 13:44:10 2019

@author: hemaxi
"""

'''Assign a membrane to each nucleus '''


import pandas as pd
from scipy.spatial import distance

#manually clicked points
ags_points = pd.read_csv(r'C:\Users\hemax\Desktop\Imagens_Membrana\ags_points.csv') 

#nuclei features extracted from DAPI images
features_ags = pd.read_csv(r'C:\Users\hemax\Desktop\Imagens_Membrana\featuresAGS.csv')

#membrane information
circle_points = pd.read_csv(r'C:\Users\hemax\Desktop\Imagens_Membrana\circle_points_AGS.csv')

images_name = ['13_3IF_AGS_WT_Alt.tif',
'17_3IF_AGS_WT_Alt.tif',
'19_3IF_AGS_WT_Alt.tif',
'1_62_3IF_AGS_Branco_Alt.tif',
'22_3IF_AGS_Mock_Alt.tif',
'24_3IF_AGS_Mock_Alt.tif',
'28_3IF_AGS_Mock_Alt.tif',
'32_3IF_AGS_Del3846_Alt.tif',
'34_3IF_AGS_Del3846_Alt.tif',
'38_3IF_AGS_Del3846_Alt.tif',
'44_3IF_AGS_Dup4146_Alt.tif',
'46_3IF_AGS_Dup4146_Alt.tif',
'48_3IF_AGS_Dup4146_Alt.tif',
'50_3IF_AGS_Mut394_Alt.tif',
'56_3IF_AGS_Mut394_Alt.tif',
'58_3IF_AGS_Mut394_Alt.tif',
'5_3IF_AGS_Branco_Alt.tif',
'6_3IF_AGS_Branco_Alt.tif']



# =============================================================================
# images_name = ['13-3IF_CHO_Branco_Alt.tif',
# '17-3IF_CHO_WT_Alt.tif',
# '19-3IF_CHO_WT_Alt.tif',
# '21-3IF_CHO_WT_Alt.tif',
# '25-3IF_CHO_WT_Alt.tif',
# '27-3IF_CHO_WT_Alt.tif',
# '29-3IF_CHO_Mock_Alt.tif',
# '31-3IF_CHO_Mock_Alt.tif',
# '33-3IF_CHO_Mock_Alt.tif',
# '35-3IF_CHO_Mock_Alt.tif',
# '52-3IF_CHO_Del384_Alt.tif',
# '54-3IF_CHO_Del384_Alt.tif',
# '56-3IF_CHO_Del384_Alt.tif',
# '58-3IF_CHO_Del384_Alt.tif',
# '62-3IF_CHO_Dup4146_Alt.tif',
# '64-3IF_CHO_Dup4146_Alt.tif',
# '66-3IF_CHO_Dup4146_Alt.tif',
# '7-3IF_CHO_Branco_Alt.tif',
# '70_3IF_CHO_Dup4146_Alt.tif',
# '79-3IF_CHO_Mut394_Alt.tif',
# '83-3IF_CHO_Mut394_Alt.tif',
# '85-3IF_CHO_Mut394_Alt.tif',
# '9-3IF_CHO_Branco_Alt.tif',
# '94-3IF_CHO_Mut394_Alt.tif']
# =============================================================================


intermediate_df = pd.DataFrame(columns = ["Image", "x_manual", "y_manual", "Area", 
                                   "BBox_Area", "Perimeter", "Eccentricity", "Total Intensity", 
                                   "Mean Intensity", "Solidity", "Local Binary Pattern", 
                                   "Entropy", "Shannon Entropy", "Centroid_x", "Centroid_y"])

for img_name in images_name: 
    
    
    aux_ags_points = ags_points[ags_points.Image.str.contains(img_name)]
    
    aux_features_ags = features_ags[features_ags.Image.str.contains(img_name)]
    
    for index, row in aux_ags_points.iterrows():
        x_manual = row['x']
        y_manual = row['y']
        dis = 10**10
        
        for index1, row1 in aux_features_ags.iterrows():
            centroid_x = row1['Centroid_x']
            centroid_y = row1['Centroid_y']
          
            
            new_dist = distance.euclidean((x_manual, y_manual),(centroid_x, centroid_y))
            
            if (new_dist < dis):
                dis = new_dist
                res = {"Image": img_name, "x_manual": x_manual , "y_manual": y_manual, 
                       "Area": row1['Area'] ,"BBox_Area": row1['BBox_Area'], 
                       "Perimeter": row1['Perimeter'], "Eccentricity": row1['Eccentricity'], 
                       "Total Intensity": row1['Total Intensity'], 
                       "Mean Intensity": row1['Mean Intensity'], "Solidity": row1['Solidity'], 
                       "Local Binary Pattern": row1['Local Binary Pattern'], 
                       "Entropy": row1['Entropy'], "Shannon Entropy": row1['Shannon Entropy'], 
                       "Centroid_x": row1['Centroid_x'], "Centroid_y": row1['Centroid_y']}
                
                print(dis)
    
        location = len(intermediate_df)
        intermediate_df.loc[location] = res
    
    

final_df = pd.DataFrame(columns = ["Image", "x_manual", "y_manual", "Area", 
                                   "BBox_Area", "Perimeter", "Eccentricity", "Total Intensity", 
                                   "Mean Intensity", "Solidity", "Local Binary Pattern", 
                                   "Entropy", "Shannon Entropy", "Centroid_x", "Centroid_y",
                                   "Circle_x", "Circle_y", "radius"])


for img_name in images_name: 
    
    
    aux_intermediate = intermediate_df[intermediate_df.Image.str.contains(img_name)]
    
    aux_circle_points = circle_points[circle_points.Image.str.contains(img_name)]
    
    for index1, row1 in aux_intermediate.iterrows():
        x_manual = row1['x_manual']
        y_manual = row1['y_manual']
        dis = 10**10
        
        for index, row in aux_circle_points.iterrows():
            centroid_x = row['x']
            centroid_y = row['y']
          
            
            new_dist = distance.euclidean((x_manual, y_manual),(centroid_x, centroid_y))
            
            if (new_dist < dis):
                dis = new_dist
                res = {"Image": img_name, "x_manual": x_manual , "y_manual": y_manual, 
                       "Area": row1['Area'] ,"BBox_Area": row1['BBox_Area'], 
                       "Perimeter": row1['Perimeter'], "Eccentricity": row1['Eccentricity'], 
                       "Total Intensity": row1['Total Intensity'], 
                       "Mean Intensity": row1['Mean Intensity'], "Solidity": row1['Solidity'], 
                       "Local Binary Pattern": row1['Local Binary Pattern'], 
                       "Entropy": row1['Entropy'], "Shannon Entropy": row1['Shannon Entropy'], 
                       "Centroid_x": row1['Centroid_x'], "Centroid_y": row1['Centroid_y'], 
                       "Circle_x": row['x'], "Circle_y": row['y'], "radius": row['radius']}
                
                print(dis)
    
        location = len(final_df)
        final_df.loc[location] = res
    
    
    
distances = []


for index, row in final_df.iterrows():
        x_nucleus = row['Centroid_x']
        y_nucleus = row['Centroid_y']
        
        x_circle = row['Circle_x']
        y_circle = row['Circle_y']
        
        dist = distance.euclidean((x_nucleus, y_nucleus),(x_circle, y_circle))
        
        distances.append(dist)
        

final_df['Distance_nucleus_circle'] = distances
    
    