import numpy as np
import os
import nibabel as nib


def process_patches(base_folder):
    patch_folder = os.path.join(base_folder, "IMAGES")
    label_folder = os.path.join(base_folder, "LABELS")

    for label_file in os.listdir(label_folder):
        label_path = os.path.join(label_folder, label_file)
        # Assuming the corresponding image file has the same name
        image_base_name = label_file.replace('label_patch', 'patch')
        image_path = os.path.join(patch_folder, image_base_name)
        label_nii = nib.load(label_path) # Load the label
        label = label_nii.get_fdata()

        # Calculate the scores again
        branching_score = np.sum(label[:, :, :, 0])
        radius_thrshold_score =  np.sum(label[:, :, :, 1])
        uncontinuous_score = np.sum(label[:, :, :, 2])
        overlapping_score = np.sum(label[:, :, :, 3])
        length_radius_ratio_score =  np.sum(label[:, :, :, 4])
        angle_constraint_score = np.sum(label[:, :, :, 5])


        initial_label_sum = branching_score + radius_thrshold_score + uncontinuous_score + overlapping_score\
                            + length_radius_ratio_score + angle_constraint_score
        #if initial_label_sum != 0:

        # Set the entire fourth channel of other labels to 0
        # label[:, :, :, 0] = 0 #BRANCHING NUMBER
        label[:, :, :, 1] = 0 #RADIUS THRESHOLD
        label[:, :, :, 2] = 0 #GAPS
        label[:, :, :, 3] = 0 #OVERLAPPING
        label[:, :, :, 4] = 0 #LENGTH RADIUS RATIO
        label[:, :, :, 5] = 0 #BRANCHING ANGLES

        # Calculate the scores again
        branching_score = np.sum(label[:, :, :, 0])
        radius_thrshold_score = np.sum(label[:, :, :, 1])
        uncontinuous_score = np.sum(label[:, :, :, 2])
        overlapping_score = np.sum(label[:, :, :, 3])
        length_radius_ratio_score = np.sum(label[:, :, :, 4])
        angle_constraint_score = np.sum(label[:, :, :, 5])


        # Calculate the new label sum
        label_sum = branching_score + radius_thrshold_score + uncontinuous_score + overlapping_score\
                        + length_radius_ratio_score + angle_constraint_score

        # Check if label_sum is zero
        if label_sum == 0:
            # Delete both the label and image files
            os.remove(label_path)
            if os.path.exists(image_path):
                os.remove(image_path)
        else:
            # Save the modified label back
            new_label_nii = nib.Nifti1Image(label, affine=label_nii.affine, header=label_nii.header)
            nib.save(new_label_nii, label_path)


# Define your base folder
base_folder = "/gpfs/users/a1836131/FINAL_HPC_SYNTHETIC_VESSEL_GENERATION_CODE/SYNTHETIC_GENERATOR/SYNTHETIC_DATA/UNREALISTIC_BRANCHING_NUM/UNREALISTIC_BRANCHING_NUM_PATCHES"

# Process the patches
process_patches(base_folder)