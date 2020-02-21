# -*- coding: utf-8 -*-
"""
Created on Thu Dec 19 10:43:39 2019

@author: hemaxi
"""

import pandas as pd
import numpy as np

#df = pd.read_csv(r'C:\Users\hemax\Desktop\Imagens_Membrana\final_all_grouped.csv') ## AGS
df = pd.read_pickle(r'C:\Users\hemax\Desktop\Imagens_Membrana\final_final_CHO.pickle') ## CHO

perimeter_circle = []
area_circle = []

for index, row in df.iterrows():

        radius = row['radius']
        
        circle_perimeter = 2*np.pi*radius
        
        circle_area = np.pi*radius**2
        
        perimeter_circle.append(circle_perimeter)
        area_circle.append(circle_area)

df['circle_perimeter'] = perimeter_circle
df['circle_area'] = area_circle