Cell Nucleus and Membrane Segmentation and Feature Extraction


Code developed for the analysis of microscopy images of cells stained with DAPI and with a marker for the membrane.
Cell nuclei segmentation is performed using our previously proposed method: 

Narotamo, H., Sanches, J. M., & Silveira, M. (2019, July). Segmentation of Cell Nuclei in Fluorescence Microscopy Images Using Deep Learning. In Iberian Conference on Pattern Recognition and Image Analysis (pp. 53-64). Springer, Cham.

Membrane segmentation is performed based on the Hough Transform.


Correct order to run the files, in order to perform membrane segmentation, extract features from the nuclei and membrane

1) final.py --> performs membrane segmentation using Hough Transform
2) test.py --> by running this script features for the nuclei are extracted (these features are defined in "nuclei_features.py")
3) Hough_transform.py + select_circles.py --> manually select nuclei and membrane that are correctly segmented
4) group_all_pandas_df.py --> convert pickle objects to pandas dataframe
5) assignment --> assign each nucleus to a membrane

(If you want to extract additional features from both nuclei and membranes run:
feature_centr_circle_point.py
feat_relative_size.py
feat_perimeter_circularity.py
)

The files "final_19_12_CHO.pickle" and "final_19_12_AGS.pickle" are pandas dataframes which contain the membranes and nuclei features for each pair nucleus-membrane. These dataframes are used to obtain the box plots and statitical analysis, which is performed with the jupyter notebooks "jupyter_notebooks\Features_Comparison_MUT_vs_WT_AGS.ipynb" and "jupyter_notebooks\Features_Comparison_MUT_vs_WT_CHO.ipynb".
