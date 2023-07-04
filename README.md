# ColocalizePuncta
Spatial colocalization analysis is implemented using Python 3.5.1 (Anaconda distribution). 
Imaging features of the scikit-image module are used for loading and saving of image files. 
The masks created by FindFoci (DOI: 10.1371/journal.pone.0114749) or any mask serve as input for this program. 
Masks of the corresponding co-stained markers in an immunolabeling are then processed pairwise. 
Every selection area in the first mask (A) is checked for a corresponding area in the second mask (B). 
If such an overlap is found, both signals are considered as spatially colocalizing. 
Subsequently, the distances between the centre of masses of identified pairs is measured to infer the degree of association. 
Colocalizing and non-colocalizing selections are separated and saved as new output masks (e.g. A_coloc, A_non-coloc, B_coloc, B_non-coloc). 
These new masks can also be used as input masks for FindFoci in order to re-analyze colocalizing and non-colocalizing signals separately. 
Additionally, a GUI is provided for selection of the necessary folders.
