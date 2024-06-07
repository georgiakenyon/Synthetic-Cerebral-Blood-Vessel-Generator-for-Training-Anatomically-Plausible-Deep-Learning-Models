import os
import numpy as np
import nibabel as nib
from config import get_config

config = get_config()
# ----------------------------------------------------------------------------------------------------------------
#                                 SAVING IMAGES FUNCTIONS
# ----------------------------------------------------------------------------------------------------------------

def save_pv_image(img, folder_path, timestamp):
    filename = f"PV_SYNTHETIC_VESSEL_iter_{config['N_ITERATIONS']}_VESS_REPUL_STRENGTH_{config['VESSEL_REPULSION_STRENGTH']}_BRAIN_REPUL_RAD_{config['BRAIN_REPULSION_RADIUS']}_BRAIN_REPUL_STRENGTH_{config['BRAIN_REPULSION_STRENGTH']}_{timestamp}.nii.gz"
    img_nifti = nib.Nifti1Image(img, affine=None)  # Create NIfTI image object
    voxel_size = (0.7, 0.7, 0.7)  # voxel dimensions in mm
    img_nifti.header.set_zooms(voxel_size)  # update header to include the voxel dimensions
    save_path = os.path.join(folder_path, filename)
    nib.save(img_nifti, save_path)  # Save the image
    # print("Saved PV Image after n_iterations:" + str(n_iterations))

def save_final_pv_image(img, folder_path, timestamp):
    filename = f"FINAL_PV_SYNTHETIC_VESSEL_iter_{config['N_ITERATIONS']}_VRR_{config['VESSEL_REPULSION_RADIUS']}_VESS_REPUL_STRENGTH_{config['VESSEL_REPULSION_STRENGTH']}_BRAIN_REPUL_RAD_{config['BRAIN_REPULSION_RADIUS']}_BRAIN_REPUL_STRENGTH_{config['BRAIN_REPULSION_STRENGTH']}_UNCONT_PARAM_{config['UNCONTINUOUS_PARAMETER']}_BIF_TRIF_TOTAL_PROB_{config['BIFURCATION_TRIFURCATION_TOTAL_PROB']}_REALISTIC_ANGLES_{config['REALISTIC_ANGLES_PARAMETER']}_LLL_RADII_{config['LOWER_LENGTH_RANGE_LOW_RADII']}_ULL_RADII_{config['UPPER_LENGTH_RANGE_LOW_RADII']}_LLH_RADII_{config['LOWER_LENGTH_RANGE_HIGH_RADII']}_ULH_RADII_{config['UPPER_LENGTH_RANGE_HIGH_RADII']}_RAD_T_{config['RADIUS_THRESHOLD']}_{timestamp}.nii.gz"
    img_nifti = nib.Nifti1Image(img, affine=None)  # Create NIfTI image object
    voxel_size = (0.7, 0.7, 0.7)  # voxel dimensions in mm
    img_nifti.header.set_zooms(voxel_size)  # update header to include the voxel dimensions
    save_path = os.path.join(folder_path, filename)
    nib.save(img_nifti, save_path)  # Save the image
    print("Saved Final PV Image")


def save_final_score_image(img, folder_path, timestamp):
    filename = f"FINAL_SCORE_SYNTHETIC_VESSEL_VRR_{config['VESSEL_REPULSION_RADIUS']}_VESS_REPUL_STRENGTH_{config['VESSEL_REPULSION_STRENGTH']}_BRAIN_REPUL_RAD_{config['BRAIN_REPULSION_RADIUS']}_BRAIN_REPUL_STRENGTH_{config['BRAIN_REPULSION_STRENGTH']}_UNCONT_PARAM_{config['UNCONTINUOUS_PARAMETER']}_BIF_TRIF_TOTAL_PROB_{config['BIFURCATION_TRIFURCATION_TOTAL_PROB']}_REALISTIC_ANGLES_{config['REALISTIC_ANGLES_PARAMETER']}_LLL_RADII_{config['LOWER_LENGTH_RANGE_LOW_RADII']}_ULL_RADII_{config['UPPER_LENGTH_RANGE_LOW_RADII']}_LLH_RADII_{config['LOWER_LENGTH_RANGE_HIGH_RADII']}_ULH_RADII_{config['UPPER_LENGTH_RANGE_HIGH_RADII']}_RAD_T_{config['RADIUS_THRESHOLD']}_{timestamp}.nii.gz"
    img_nifti = nib.Nifti1Image(img, affine=None)  # Create NIfTI image object
    voxel_size = (0.7, 0.7, 0.7, 0.7)  # voxel dimensions in mm
    img_nifti.header.set_zooms(voxel_size)  # update header to include the voxel dimensions
    save_path = os.path.join(folder_path, filename)
    nib.save(img_nifti, save_path)  # Save the image
    print("Saved Final Score Image")


def save_image(img, n_iterations, folder_path, timestamp):
    filename = f"SYNTHETIC_VESSEL_VRS_{config['VESSEL_REPULSION_STRENGTH']}_BRR_{config['BRAIN_REPULSION_RADIUS']}_BRS_{config['BRAIN_REPULSION_STRENGTH']}_iter_{n_iterations}_{timestamp}.nii.gz"
    img_nifti = nib.Nifti1Image(img, affine=None)  # Create NIfTI image object
    voxel_size = (0.35, 0.35, 0.35, 0.35)  # voxel dimensions in mm
    img_nifti.header.set_zooms(voxel_size)  # update header to include the voxel dimensions
    save_path = os.path.join(folder_path, filename)
    nib.save(img_nifti, save_path)  # Save the image
    print("Saved Image after n_iterations:" + str(n_iterations))
    return img

def save_score_function(img, n_iterations, folder_path, timestamp):
    filename = f"SCORE_FN_SYNTHETIC_VESSEL_VRS_{config['VESSEL_REPULSION_STRENGTH']}_BRR_{config['BRAIN_REPULSION_RADIUS']}_BRS_{config['BRAIN_REPULSION_STRENGTH']}_iter_{n_iterations}_{timestamp}.nii.gz"
    img = np.float32(img)
    img_nifti = nib.Nifti1Image(img, affine=None)  # Create NIfTI image object
    voxel_size = (0.35, 0.35, 0.35, 0.35)
    img_nifti.header.set_zooms(voxel_size)  # update header to include the voxel dimensions
    save_path = os.path.join(folder_path, filename)
    nib.save(img_nifti, save_path)  # Save the image
    print("Saved Score 4d Image after n_iterations:" + str(n_iterations) + "for radius image (0.35 voxel size)")
    return img
