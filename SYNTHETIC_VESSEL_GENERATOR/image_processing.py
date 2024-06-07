import os
import numpy as np
import nibabel as nib
from config import get_config

config = get_config()

# ----------------------------------------------------------------------------------------------------------------
#                                 DOWNSAMPLING IMAGES FUNCTIONS
# ----------------------------------------------------------------------------------------------------------------

def downsample_radius_image(folder_path, timestamp, radius_vessel_arr, save_img):
    # print(radius_vessel_arr.shape)
    radius_vessel_arr = radius_vessel_arr.squeeze()  # remove 4th dimension
    downsampling_factor = (2, 2, 2)
    new_shape = tuple(np.array(radius_vessel_arr.shape) // np.array(downsampling_factor))  # Calculate the new shape after downsampling

    # Reshape the original array for easier max-pooling
    reshaped_array = radius_vessel_arr.reshape(
        new_shape[0], downsampling_factor[0],
        new_shape[1], downsampling_factor[1],
        new_shape[2], downsampling_factor[2]
    )

    downsampled_array = np.max(reshaped_array,
                               axis=(1, 3, 5))  # Use np.max to perform max-pooling along the specified dimensions
    downsampled_array /= 2  # Divide every value in the downsampled array by 2

    if save_img == True:
        filename = f"DOWNSAMPLED_RADIUS_IMG_SYNTHETIC_VESSSEL_iter_{config['N_ITERATIONS']}_VESS_REPUL_STRENGTH_{config['VESSEL_REPULSION_STRENGTH']}_BRAIN_REPUL_RAD_{config['BRAIN_REPULSION_RADIUS']}_BRAIN_REPUL_STRENGTH_{config['BRAIN_REPULSION_STRENGTH']}_{timestamp}.nii.gz"
        # img_nifti = nib.Nifti1Image(mag_grad_vessel_map, affine=np.eye(4))  # Create NIfTI image object
        img_nifti = nib.Nifti1Image(downsampled_array, affine=None)  # Create NIfTI image object
        voxel_size = (0.7, 0.7, 0.7)  # voxel dimensions in mm
        img_nifti.header.set_zooms(voxel_size)  # update header to include the voxel dimensions
        save_path = os.path.join(folder_path, filename)
        nib.save(img_nifti, save_path)  # Save the image
    return downsampled_array


def downsample_radius_score_image(folder_path, timestamp, radius_score_vessel_arr, save_img):
    score_image_shape = radius_score_vessel_arr.shape
    downsampling_factor = (2, 2, 2)
    downsampled_data = np.empty((score_image_shape[0] // downsampling_factor[0],
                                 score_image_shape[1] // downsampling_factor[1],
                                 score_image_shape[2] // downsampling_factor[2],
                                 score_image_shape[3]))

    for i in range(score_image_shape[3]):
        radius_score_3d = radius_score_vessel_arr[:, :, :, i]
        new_shape = tuple(np.array(radius_score_3d.shape) // np.array(
            downsampling_factor))  # Calculate the new shape after downsampling
        reshaped_array = radius_score_3d.reshape(new_shape[0], downsampling_factor[0], new_shape[1],
                                                 downsampling_factor[1], new_shape[2], downsampling_factor[
                                                     2])  # Reshape the original array for easier max-pooling
        downsampled_array_3d = np.max(reshaped_array, axis=(
        1, 3, 5))  # Use np.max to perform max-pooling along the specified dimensions
        downsampled_data[:, :, :, i] = downsampled_array_3d

    if save_img == True:
        filename = f"DOWNSAMPLED_RADIUS_SCORE_IMG_SYNTHETIC_VESSSEL_iter_{config['N_ITERATIONS']}_VESS_REPUL_STRENGTH_{config['VESSEL_REPULSION_STRENGTH']}_BRAIN_REPUL_RAD_{config['BRAIN_REPULSION_RADIUS']}_BRAIN_REPUL_STRENGTH_{config['BRAIN_REPULSION_STRENGTH']}_{timestamp}.nii.gz"
        # img_nifti = nib.Nifti1Image(mag_grad_vessel_map, affine=np.eye(4))  # Create NIfTI image object
        img_nifti = nib.Nifti1Image(downsampled_data, affine=None)  # Create NIfTI image object
        voxel_size = (0.7, 0.7, 0.7, 0.7)  # voxel dimensions in mm
        img_nifti.header.set_zooms(voxel_size)  # update header to include the voxel dimensions
        save_path = os.path.join(folder_path, filename)
        nib.save(img_nifti, save_path)  # Save the image
    return downsampled_data


def downsample_pv_image(folder_path, timestamp, pv_vessel_arr, save_img):
    print(f'Downsampling the original pv image of size: {pv_vessel_arr.shape}')
    pv_vessel_arr = pv_vessel_arr.squeeze()  # remove 4th dimension
    downsampling_factor = (2, 2, 2)
    new_shape = tuple(
        np.array(pv_vessel_arr.shape) // np.array(downsampling_factor))  # Calculate the new shape after downsampling

    # Reshape the original array for easier max-pooling
    reshaped_array = pv_vessel_arr.reshape(
        new_shape[0], downsampling_factor[0],
        new_shape[1], downsampling_factor[1],
        new_shape[2], downsampling_factor[2]
    )

    downsampled_pv_array = np.max(reshaped_array,
                                  axis=(1, 3, 5))  # Use np.max to perform max-pooling along the specified dimensions
    # downsampled_pv_array /= 2 # Divide every value in the downsampled array by 2

    if save_img == True:
        filename = f"DOWNSAMPLED_PV_SYNTHETIC_VESSSEL_iter_{config['N_ITERATIONS']}_VESS_REPUL_STRENGTH_{config['VESSEL_REPULSION_STRENGTH']}_BRAIN_REPUL_RAD_{config['BRAIN_REPULSION_RADIUS']}_BRAIN_REPUL_STRENGTH_{config['BRAIN_REPULSION_STRENGTH']}_{timestamp}.nii.gz"
        # img_nifti = nib.Nifti1Image(mag_grad_vessel_map, affine=np.eye(4))  # Create NIfTI image object
        img_nifti = nib.Nifti1Image(downsampled_pv_array, affine=None)  # Create NIfTI image object
        voxel_size = (0.7, 0.7, 0.7)  # voxel dimensions in mm
        img_nifti.header.set_zooms(voxel_size)  # update header to include the voxel dimensions
        save_path = os.path.join(folder_path, filename)
        nib.save(img_nifti, save_path)  # Save the image
    return downsampled_pv_array

