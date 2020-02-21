# -*- coding: utf-8 -*-
"""
Created on Wed Dec 18 14:45:35 2019

@author: hemaxi
"""

import pandas as pd
import numpy as np

#df = pd.read_csv(r'C:\Users\hemax\Desktop\Imagens_Membrana\final_all_grouped.csv') ## AGS
df = pd.read_pickle(r'C:\Users\hemax\Desktop\Imagens_Membrana\final_AGS.pickle') ## CHO

new_column = []

for index, row in df.iterrows():
        nucleus_area = row['Area']


        radius = row['radius']
        
        circle_area = np.pi*radius**2
        
        ratio = circle_area/nucleus_area
        
        new_column.append(ratio)

df['circle_area/nucleus_area'] = new_column