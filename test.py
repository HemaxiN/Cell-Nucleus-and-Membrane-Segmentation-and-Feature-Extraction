# -*- coding: utf-8 -*-
"""
Created on Tue Mar 26 15:20:50 2019

@author: hemaxi
"""

'''Obtain the features for each nucleus in the DAPI images and save the pandas dataframe.'''


#import the packages
import nuclei_features
import pandas as pd
import os

#images directory
images_path = r'C:\Users\hemax\Desktop\Imagens_Membrana\CHO_blue'
#predictions directory (folder with pickle objects containing the nuclei segmentation masks given by predict.py)
#predictions_path = r'D:\Ambiente_de_Trabalho\Tese\Clones\predictions_clones'
predictions_path = r'C:\Users\hemax\Desktop\Imagens_Membrana\predictions\CHO'

# =============================================================================
# images_path = r'D:\Ambiente_de_Trabalho\Tese\Images\CellImages\Blue_Channel_SF'
# predictions_path = r'D:\Ambiente_de_Trabalho\Tese\SF\predictions'
# 
# =============================================================================

##AGS
types = ['Branco','WT','Mock','Del3846','Dup4146','Mut394']

##CHO
types = ['Branco','WT','Mock','Del3846','Dup4146','Mut394']


features = nuclei_features.obtain_features(images_path, predictions_path, types, True)


# =============================================================================
# average_performance = features.groupby("Image").agg({'Area': np.mean, 'BBox_Area': np.mean, 
#                                      'Perimeter': np.mean, 'Eccentricity': np.mean, 'Total Intensity': np.mean, 'Mean Intensity': np.mean})
# 
# 
# #aux = average_performance
# #a = aux[aux.Image.str.startswith('Del 38_46')]
# 
# 
# def histogram(df, string):
#     aux = df[df.Image.str.startswith(string)]
#     hist = aux.hist()
#     return hist
# 
# 
# =============================================================================






