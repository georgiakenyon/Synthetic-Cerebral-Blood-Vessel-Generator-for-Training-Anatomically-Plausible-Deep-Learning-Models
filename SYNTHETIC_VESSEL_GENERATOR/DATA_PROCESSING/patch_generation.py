import numpy as np
import os
from glob import glob
import nibabel as nib
import time

#PLAUSIBLE
DATA_DIR = '/gpfs/users/a1836131/FINAL_HPC_SYNTHETIC_VESSEL_GENERATION_CODE/SYNTHETIC_GENERATOR/SYNTHETIC_DATA/UNREALISTIC_BRANCHING_NUM/UNREALISTIC_BRANCHING_NUM_IMG_LABELS'
PATCHES_DIR = '/gpfs/users/a1836131/FINAL_HPC_SYNTHETIC_VESSEL_GENERATION_CODE/SYNTHETIC_GENERATOR/SYNTHETIC_DATA/UNREALISTIC_BRANCHING_NUM/UNREALISTIC_BRANCHING_NUM_PATCHES/IMAGES'
PATCHES_LABELS_DIR = '/gpfs/users/a1836131/FINAL_HPC_SYNTHETIC_VESSEL_GENERATION_CODE/SYNTHETIC_GENERATOR/SYNTHETIC_DATA/UNREALISTIC_BRANCHING_NUM/UNREALISTIC_BRANCHING_NUM_PATCHES/LABELS'
#IMPLAUSIBLE
# DATA_DIR = '/gpfs/users/a1836131/FINAL_HPC_SYNTHETIC_VESSEL_GENERATION_CODE/SYNTHETIC_VESSELS/IMPLAUSIBLE_VESSELS'
# PATCHES_DIR = '/gpfs/users/a1836131/FINAL_HPC_SYNTHETIC_VESSEL_GENERATION_CODE/SYNTHETIC_VESSELS/PATCHES/30_30_30/IMAGES'
# PATCHES_LABELS_DIR = '/gpfs/users/a1836131/FINAL_HPC_SYNTHETIC_VESSEL_GENERATION_CODE/SYNTHETIC_VESSELS/PATCHES/30_30_30/LABELS'

l_d_thresh = 0.01
u_d_thresh = 0.05
vessels = sorted(glob(os.path.join(DATA_DIR, 'IMAGES', '*.nii.gz')))
vessel_labels = sorted(glob(os.path.join(DATA_DIR, 'LABELS', '*.nii.gz')))

image_size = (260, 311, 260)
count = 0
patch_size = (32, 32, 32)

def split_image_into_patches(image, label, patch_size):
    depth, height, width = image.shape
    d_patch, h_patch, w_patch = patch_size
    patches = []
    label_patches = []

    for d in range(0, depth - d_patch + 1, d_patch):
        for h in range(0, height - h_patch + 1, h_patch):
            for w in range(0, width - w_patch + 1, w_patch):
                patch = image[d:d + d_patch, h:h + h_patch, w:w + w_patch]
                label_patch = label[d:d + d_patch, h:h + h_patch, w:w + w_patch]
                patches.append(patch)
                label_patches.append(label_patch)

    return patches, label_patches

def vessel_pv_density_check(image_patch, label_patch, l_d_thresh, u_d_thresh, patch_dir, label_patch_dir, original_filename):
    #depth, height, width = image_patch.shape
    #no_voxels_patch = depth * height * width
    #no_voxels_patch = patch_size[0]/2 * patch_size[1]/2 * patch_size[2]/2 #not sure why did this?
    no_voxels_patch = np.prod(patch_size)
    #print(no_voxels_patch)
    total_vessels = np.sum(image_patch)
    patch_density = total_vessels/no_voxels_patch

    density_patches = []
    label_density_patches = []

    if l_d_thresh < patch_density < u_d_thresh:
        patch = image_patch
        patch_label = label_patch
        density_patches.append(patch)
        label_density_patches.append(patch_label)
        #timestamp = time.strftime("%Y%m%d%H%M%S")

        filename = os.path.join(patch_dir, f"patch_{timestamp}_{count}_density_{patch_density}_dthresh_{l_d_thresh}_{u_d_thresh}_BRANCHING_NUM.nii.gz")
        img_nifti = nib.Nifti1Image(image_patch, affine=None)  # Create NIfTI image object
        voxel_size = (0.7, 0.7, 0.7)  # voxel dimensions in mm
        img_nifti.header.set_zooms(voxel_size)  # update header to include the voxel dimensions
        nib.save(img_nifti, filename)  # Save the image

        label_filename = os.path.join(label_patch_dir, f"label_patch_{timestamp}_{count}_density_{patch_density}_dthresh_{l_d_thresh}_{u_d_thresh}_BRANCHING_NUM.nii.gz")
        label_nifti = nib.Nifti1Image(patch_label, affine=None)  # Create NIfTI image object
        voxel_size = (0.7, 0.7, 0.7, 0.7)  # voxel dimensions in mm
        label_nifti.header.set_zooms(voxel_size)  # update header to include the voxel dimensions
        nib.save(label_nifti, label_filename)  # Save the image

        print("Saved image and label patch")
        return density_patches
# Define a function to extract the timestamp from the image filename
def extract_timestamp(filename):
    return filename.split('_')[-1]

# Define a function to find the matching label file for a given timestamp
def find_matching_label(label_files, timestamp):
    for label_file in label_files:
        if timestamp in label_file:
            return label_file
    return None


for image_path in vessels:
    images = nib.load(image_path)
    image_data = images.get_fdata()
    original_filename = os.path.splitext(os.path.basename(image_path))[0]  # Get original filename without extension
    if original_filename.endswith(".nii"):
        original_filename = original_filename[:-4]
    timestamp = extract_timestamp(original_filename)
    matching_label = find_matching_label(vessel_labels, timestamp)     # Find the matching label file
    #patches, label_patches = split_image_into_patches(image_data, label_data, patch_size)
    if matching_label is not None:
        label_images = nib.load(matching_label)
        label_data = label_images.get_fdata()
        # overlapping_score = label_data[:, :, :, 3] #changing how i monitor the overlapping vessels to only ever be 1.
        #  # Extract overlapping score
        # overlapping_score[overlapping_score > 1] = 1  # Set all values greater than 1 to 1
        # label_data[:, :, :, 3] = overlapping_score  # Update the label_data with modified scores

        patches, label_patches = split_image_into_patches(images.get_fdata(), label_data, patch_size)
        for patch, label_patch in zip(patches, label_patches):
            save_patches = vessel_pv_density_check(patch, label_patch, l_d_thresh=l_d_thresh, u_d_thresh=u_d_thresh, patch_dir=PATCHES_DIR, label_patch_dir=PATCHES_LABELS_DIR, original_filename=original_filename)

            count += 1
    else:
        print(f"No matching label found for image {image_path}")