import numpy as np
import skimage.io
import skimage.viewer
import skimage.measure
import os
import os.path
import errno
import warnings

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
output_folder_one = r"C:\Users\Christian Jacob\Documents\GitHub\ColocDots\ColocDots\ColocDots\output_one"

# output_folder_one: location where results of the second channel will be saved
output_folder_two = r"C:\Users\Christian Jacob\Documents\GitHub\ColocDots\ColocDots\ColocDots\output_two"

# original_extension: the original extensions of your files (e.g. ".png", ".jpg", ".tif", etc.)
original_extension = ".tiff"

# a new extension, if you want a different type (e.g. ".mask.tif", ".png", etc.). If you save images
# as non-tif, the image might only be visible in ImageJ due to low contrast.
new_extension = ".tif"

# background_level: the value of your background. Will be 0 in most cases. Everything above this value is
#                   regarded as signal
background_level = 0

# save_masks_instead_of_images: masks will be saved, if set to true
save_masks_instead_of_images = True

# ---- End of configuration parameters ----


def create_dir_if_not_exists(dir):
    try:
        os.makedirs(dir)
    except OSError as exception:
        if exception.errno != errno.EEXIST:
            raise

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

    labels_one = skimage.measure.label(threshold_one, connectivity = 1)
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
    input_files = os.listdir(folder_one)

    create_dir_if_not_exists(output_folder_one)
    create_dir_if_not_exists(output_folder_two)

    if len(input_files) != len(os.listdir(folder_two)):
        print("Warning: unequal number of input images. Maybe images are missing?")

    for file in input_files:
        file_two = file.replace(channel_one, channel_two)
        colocalize_images(file, file_two)