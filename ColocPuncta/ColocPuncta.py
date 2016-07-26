import numpy as np
import skimage.io
import skimage.viewer
import skimage.measure
from scipy import ndimage
import os
import os.path
import errno
import warnings
import math

#---- Configruation parameters below ----

# Requirements: Images in 8-bit/16-bit/32-bit format (non-color). 
#               You can convert them with ImageJ via Image -> Type -> 8-bit

# folder_one: Location of folder with the images of the first channel
folder_one = r"C:\Users\Christian Jacob\Documents\GitHub\ColocDots\ColocDots\ColocDots\vg1_mask"

# folder_two: Location of folder with the images of the second channel
folder_two = r"C:\Users\Christian Jacob\Documents\GitHub\ColocDots\ColocDots\ColocDots\sh2_mask"

# channel_one: A specific name of the first channel
channel_one = "vg1"
# channel_two: A specific name of the second channel
channel_two = "sh2"
# Remark:   This tool will infer the filename of the second image by replacing any occurence of the value of
#           channel_one with channel_two in the filename
#           
#           E.g. if channel_one is set to "sh3" and channel_two to "vg1": if a file is named "img_sh3.tif",
#           the matching partner is assumed to be named "img_vg1.tif". If files have the same name, just set
#           both variables to the same value

# output_folder_one: location where results of the first channel will be saved
output_folder_one = r"output_one"

# output_folder_one: location where results of the second channel will be saved
output_folder_two = r"output_two"

# original_extension: the original extensions of your files (e.g. ".png", ".jpg", ".tif", etc.)
original_extension = ".tif"

# a new extension, if you want a different type (e.g. ".mask.tif", ".png", etc.). If you save images
# as non-tif, the image might only be visible in ImageJ due to low contrast.
new_extension = ".tif"

# background_level: the value of your background. Will be 0 in most cases. Everything above this value is
#                   regarded as signal
background_level = 1

# save_masks_instead_of_images: masks will be saved, if set to true
save_masks_instead_of_images = True

# statistics_save_file: The folder, where statistics will be saved. 
#                       Will create the following files:
#                           - overlapping_areas.csv: Contains relative amount of overlapping areas in pixel
statistics_save_folder = r"output_stats"

# ---- End of configuration parameters ----

_overlapping_area_filehandle = None
_distance_com_filehandle = None

def create_dir_if_not_exists(dir):
    try:
        os.makedirs(dir)
    except OSError as exception:
        if exception.errno != errno.EEXIST:
            raise

def _calculate_overlapping_area(threshold_one, threshold_two, mask, filename_ch_1):
    area_channel_one = np.sum(threshold_one)
    area_channel_two = np.sum(threshold_two)
    overlap = np.sum(mask)

    relative_channel_one = overlap/area_channel_one
    relative_channel_two = overlap/area_channel_two

    print(filename_ch_1, area_channel_one, area_channel_two, overlap, relative_channel_one, relative_channel_two, sep=";", file = _overlapping_area_filehandle)

def _distance(p0, p1):
    return math.sqrt((p0[0] - p1[0])**2 + (p0[1] - p1[1])**2)

def _calculate_distance_of_overlaying_pictures(labels_one, labels_two, max_label_one, filename_ch_1):
    for i in range(1, max_label_one):
        current_label_mask = labels_one == i
        overlapping_labels_two = labels_two[current_label_mask]

        overlaying_ids_channel_two = list(np.unique(overlapping_labels_two.ravel()))

        if 0 in overlaying_ids_channel_two:
            overlaying_ids_channel_two.remove(0)

        for id in overlaying_ids_channel_two:
            com_one = ndimage.center_of_mass(current_label_mask)
            com_two = ndimage.center_of_mass(labels_two == id)

            distance = _distance(com_one, com_two)
            print(filename_ch_1, i, id, distance, sep = ";", file = _distance_com_filehandle)


def open_statistic_files():
    global _overlapping_area_filehandle
    global _distance_com_filehandle

    create_dir_if_not_exists(statistics_save_folder)

    _overlapping_area_filehandle = open(os.path.join(statistics_save_folder, "overlapping_areas.csv"),'w')
    print('File Ch1;Area {0} in px;Area {1} in px;Overlap in px;Relative overlap {0};Relative overlap {1}'.format(channel_one.replace(";", "-"), channel_two.replace(";", "-")), file = _overlapping_area_filehandle)

    _distance_com_filehandle = open(os.path.join(statistics_save_folder, "distance_com.csv"), 'w')
    print('File Ch1;Label 1;Label 2;Distance in px', file = _distance_com_filehandle)

def close_statistic_files():
    global _overlapping_area_filehandle
    global _distance_com_filehandle

    _overlapping_area_filehandle.close()
    _distance_com_filehandle.close()

def colocalize_images(filename_one, filename_two):
    full_filename_one = os.path.join(folder_one, filename_one)
    full_filename_two = os.path.join(folder_two, filename_two)

    if not os.path.isfile(full_filename_two):
        print("Warning: no corresponding file found for {}".format(filename_one))
        return                                                                      # Return for non-existing files
    
    print("Processing file {}".format(filename_one))

    image_one = skimage.io.imread(full_filename_one)
    image_two = skimage.io.imread(full_filename_two)

    threshold_one = image_one > background_level
    threshold_two = image_two > background_level

    mask = np.logical_and(threshold_one, threshold_two)

    labels_one, max_label_one = skimage.measure.label(threshold_one, connectivity = 1, return_num = True)
    labels_two = skimage.measure.label(threshold_two, connectivity = 1)

    overlaying_one = labels_one[mask]
    overlaying_two = labels_two[mask]

    ids_one = np.unique(overlaying_one.ravel())
    ids_two = np.unique(overlaying_two.ravel())

    result_one = np.in1d(labels_one.ravel(), ids_one).reshape(image_one.shape)
    result_two = np.in1d(labels_two.ravel(), ids_two).reshape(image_two.shape)

    image_one[np.logical_not(result_one)] = 0
    image_two[np.logical_not(result_two)] = 0

    save_file_one = os.path.join(output_folder_one, filename_one.replace(original_extension, new_extension))
    save_file_two = os.path.join(output_folder_two, filename_two.replace(original_extension, new_extension))

    if statistics_save_folder != None:
        _calculate_overlapping_area(threshold_one, threshold_two, mask, filename_one.replace(";", "-"))
        _calculate_distance_of_overlaying_pictures(labels_one, labels_two, max_label_one, filename_one.replace(";", "-"))

    with warnings.catch_warnings():
        warnings.simplefilter("ignore")
        if save_masks_instead_of_images:
            mask_result_one = np.ones_like(image_one)
            mask_result_one[np.logical_not(result_one)] = 0
            mask_result_two = np.ones_like(image_two)
            mask_result_two[np.logical_not(result_two)] = 0

            skimage.io.imsave(save_file_one, mask_result_one)
            skimage.io.imsave(save_file_two, mask_result_two)
        else:
            skimage.io.imsave(save_file_one, image_one)
            skimage.io.imsave(save_file_two, image_two)

if __name__ == '__main__':
    open_statistic_files()
    input_files = os.listdir(folder_one)

    create_dir_if_not_exists(output_folder_one)
    create_dir_if_not_exists(output_folder_two)

    if len(input_files) != len(os.listdir(folder_two)):
        print("Warning: unequal number of input images. Maybe images are missing?")

    for file in input_files:
        file_two = file.replace(channel_one, channel_two)
        colocalize_images(file, file_two)
    close_statistic_files()