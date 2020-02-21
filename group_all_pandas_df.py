# -*- coding: utf-8 -*-
"""
Created on Tue Dec 17 13:34:59 2019

@author: hemaxi
"""

'''Convert pickle objects to pandas df for easier processing'''


import os
import pickle
import pandas as pd


#group points clicked by me

ags_points = pd.DataFrame(columns = ["Image", "x", "y"])

pkl_dir = r'C:\Users\hemax\Desktop\Masks\CHO\pkl'

for pkl in os.listdir(pkl_dir):
    pickle_in = open(os.path.join(pkl_dir, pkl), 'rb')
    points = pickle.load(pickle_in)
    
    out = pd.concat([ags_points, points])
    
    ags_points = out


ags_points.to_csv(r'C:\Users\hemax\Desktop\Imagens_Membrana\cho_points.csv')


#group all circles

pkl_dir = r'C:\Users\hemax\Desktop\Centers\CHO'

circle_points = pd.DataFrame(columns = ["Image", "x", "y", "radius"])


for pkl in os.listdir(pkl_dir):
    with open(os.path.join(pkl_dir, pkl),'rb') as f:
        loading = pickle.load(f)
        
        for i in range(0, len(loading)):
            a = loading[i]
            x = a[2]
            y = a[1]                
            radius = a[3]
            
            aux = pkl.replace('.pkl', '')
            
            res = {"Image": aux, "x": x , "y": y, "radius": radius}
            row = len(circle_points)
            circle_points.loc[row] = res
            
            
circle_points.to_csv(r'C:\Users\hemax\Desktop\Imagens_Membrana\circle_points_CHO.csv')
            