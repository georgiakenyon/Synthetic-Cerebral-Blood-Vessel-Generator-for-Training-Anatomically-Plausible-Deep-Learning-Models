import os
import nibabel as nib
import numpy as np
import matplotlib.pyplot as plt

def calculate_average_score(patch_folder, label_folder):
    patch_files = os.listdir(patch_folder)

    total_score = 0
    total_patches = 0
    zero_sum_count = 0
    non_zero_count = 0
    less_two_sum_count = 0
    above_two_count = 0
    above_ten_count = 0
    above_twenty_count = 0
    above_thirty_count = 0
    above_fourty_count = 0
    above_fifty_count = 0
    above_sixty_count = 0
    above_seventy_count = 0
    above_eighty_count = 0
    above_ninety_count = 0
    above_one_hundred_count = 0
    above_two_hundred_count = 0
    above_four_hundred_count = 0
    total_score_above_two = 0
    branching_score = 0
    radius_threshold_score = 0
    uncontinuous_score = 0
    overlapping_score = 0
    length_radius_ratio_score = 0
    angle_constraint_score = 0
    label_value= {}

    no_patches_angle_constraint_score = 0
    no_patches_branching_score = 0
    no_patches_overlapping_score = 0
    no_patches_uncontinuous_score = 0

    # Dictionaries to hold scores for each sub-label
    scores = {
        "branching_score": [],
        #"radius_threshold_score": [],
        "uncontinuous_score": [],
        "overlapping_score": [],
        #"length_radius_ratio_score": [],
        "angle_constraint_score": []
    }

    for patch_file in patch_files:
        if patch_file.startswith('patch_') and patch_file.endswith('.nii.gz'):
            label_file = f"label_patch_{patch_file[6:-7]}.nii.gz"
            patch_path = os.path.join(patch_folder, patch_file)
            label_path = os.path.join(label_folder, label_file)
            #print(f"Patch file: {patch_file} and Patch label: {label_file}")

            if os.path.exists(label_path):
                # Load NIfTI files
                label_data = nib.load(label_path).get_fdata()
                label_score = np.sum(label_data)

                label_value[patch_file] = np.sum(label_data)

                if label_score == 0:
                    zero_sum_count += 1
                if label_score != 0:
                    non_zero_count += 1
                if label_score <= 2:
                    less_two_sum_count += 1
                if label_score > 2:
                    above_two_count += 1
                    total_score_above_two += np.sum(label_data)
                if label_score > 10:
                    above_ten_count += 1
                if label_score > 20:
                    above_twenty_count += 1
                if label_score > 30:
                    above_thirty_count += 1
                if label_score > 40:
                    above_fourty_count += 1
                if label_score > 50:
                    above_fifty_count += 1
                if label_score > 60:
                    above_sixty_count += 1
                if label_score > 70:
                    above_seventy_count += 1
                if label_score > 80:
                    above_eighty_count += 1
                if label_score > 90:
                    above_ninety_count += 1
                if label_score > 100:
                    above_one_hundred_count += 1
                if label_score > 200:
                    above_two_hundred_count += 1
                if label_score > 400:
                    above_four_hundred_count += 1

                # Accumulate scores for each sub-label
                scores["branching_score"].append(np.sum(label_data[:, :, :, 0]))
                #scores["radius_threshold_score"].append(np.sum(label_data[:, :, :, 1]))
                scores["uncontinuous_score"].append(np.sum(label_data[:, :, :, 2]))
                scores["overlapping_score"].append(np.sum(label_data[:, :, :, 3]))
                #scores["length_radius_ratio_score"].append(np.sum(label_data[:, :, :, 4]))
                scores["angle_constraint_score"].append(np.sum(label_data[:, :, :, 5]))

                patch_branching_score = np.sum(label_data[:, :, :, 0])
                patch_uncontinuous_score = np.sum(label_data[:, :, :, 2])
                patch_overlapping_score = np.sum(label_data[:, :, :, 3])
                patch_angle_constraint_score = np.sum(label_data[:, :, :, 5])
                # print(f"patch_branching_score: {patch_branching_score}")
                # print(f"patch_uncontinuous_score: {patch_uncontinuous_score}")
                # print(f"patch_overlapping_score: {patch_overlapping_score}")
                # print(f"patch_angle_constraint_score: {patch_angle_constraint_score}")

                if patch_branching_score == 0 and patch_uncontinuous_score == 0 and patch_overlapping_score == 0:
                    if max_display_score > patch_angle_constraint_score > min_display_score:
                        no_patches_angle_constraint_score += 1

                if patch_branching_score == 0 and patch_uncontinuous_score == 0 and patch_angle_constraint_score == 0:
                    if max_display_score > patch_overlapping_score > min_display_score:
                        no_patches_overlapping_score += 1

                if patch_branching_score == 0 and patch_angle_constraint_score == 0 and patch_overlapping_score == 0:
                    if max_display_score > patch_uncontinuous_score > min_display_score:
                        no_patches_uncontinuous_score += 1

                if patch_angle_constraint_score == 0 and patch_uncontinuous_score == 0 and patch_overlapping_score == 0:
                    if max_display_score > patch_branching_score > min_display_score:
                        no_patches_branching_score += 1


                #print(label_score)
                # Assuming voxel values represent scores, sum the voxel values across channels
                total_score += np.sum(label_data)
                total_patches = zero_sum_count + non_zero_count

                branching_score += np.sum(label_data[:, :, :, 0])
                radius_threshold_score += np.sum(label_data[:, :, :, 1])
                uncontinuous_score += np.sum(label_data[:, :, :, 2])
                overlapping_score += np.sum(label_data[:, :, :, 3])
                length_radius_ratio_score += np.sum(label_data[:, :, :, 4])
                angle_constraint_score += np.sum(label_data[:, :, :, 5])


                average_branching_score = branching_score / total_patches
                average_radius_threshold_score = radius_threshold_score / total_patches
                average_uncontinuous_score = uncontinuous_score / total_patches
                average_overlapping_score = overlapping_score / total_patches
                average_length_radius_ratio_score = length_radius_ratio_score / total_patches
                average_angle_constraint_score = angle_constraint_score / total_patches

    if total_patches > 0:
        max_label_value = max(label_value.values())

        # Calculate and print the total scores for each category
        total_branching_score = sum(scores["branching_score"])
        total_uncontinuous_score = sum(scores["uncontinuous_score"])
        total_overlapping_score = sum(scores["overlapping_score"])
        total_angle_constraint_score = sum(scores["angle_constraint_score"])

        print(f"Total branching score: {total_branching_score}")
        print(f"Total uncontinuous score: {total_uncontinuous_score}")
        print(f"Total overlapping score: {total_overlapping_score}")
        print(f"Total angle constraint score: {total_angle_constraint_score}")

        average_score = total_score / total_patches
        average_total_score_above_two = total_score_above_two / above_two_count
        print(f"Number of patches with zero sum labels: {zero_sum_count}")
        print(f"Number of patches with non-zero sum labels: {non_zero_count}")
        print(f"Number of patches with less than or equal to 2 sum labels: {less_two_sum_count}")
        print(f"Number of patches with more than 2 sum labels: {above_two_count}")

        print(f"Number of patches with more than 10 sum labels: {above_ten_count}")
        print(f"Number of patches with more than 20 sum labels: {above_twenty_count}")
        print(f"Number of patches with more than 30 sum labels: {above_thirty_count}")
        print(f"Number of patches with more than 40 sum labels: {above_fourty_count}")
        print(f"Number of patches with more than 50 sum labels: {above_fifty_count}")
        print(f"Number of patches with more than 60 sum labels: {above_sixty_count}")
        print(f"Number of patches with more than 70 sum labels: {above_seventy_count}")
        print(f"Number of patches with more than 80 sum labels: {above_eighty_count}")
        print(f"Number of patches with more than 90 sum labels: {above_ninety_count}")
        print(f"Number of patches with more than 100 sum labels: {above_one_hundred_count}")
        print(f"Number of patches with more than 200 sum labels: {above_two_hundred_count}")
        print(f"Number of patches with more than 400 sum labels: {above_four_hundred_count}")

        print(f"Total Score: {total_score}")
        print(f"Total Patches: {total_patches}")
        print(f"Average Score: {average_score}")
        print(f"Average Score for count above 2 : {average_total_score_above_two}")

        print(f"Average branching score: {average_branching_score}")
        print(f"Average radius threshold score: {average_radius_threshold_score}")
        print(f"Average uncontinuous score: {average_uncontinuous_score}")
        print(f"Average overlapping score: {average_overlapping_score}")
        print(f"Average length radius ratio score: {average_length_radius_ratio_score}")
        print(f"Average angle constraint score: {average_angle_constraint_score}")

        print(f"Maximum Label Value: {max_label_value}")

        print(f"Number of patches with just a branching score between the max and min display score : {no_patches_branching_score}")
        print(f"Number of patches with just a uncontinuous score between the max and min display score : {no_patches_uncontinuous_score}")
        print(f"Number of patches with just a overlapping score between the max and min display score : {no_patches_overlapping_score}")
        print(f"Number of patches with just a angle constraint score between the max and min display score : {no_patches_angle_constraint_score}")


        return label_value, scores
    else:
        print("No valid patches found.")
        return None

def calculate_and_print_averages_within_range(scores, min_display_score=25, max_display_score=100):
    # Initialize sums and counts for scores within the specified range
    averages_within_range = {
        "branching_score": [],
        "uncontinuous_score": [],
        "overlapping_score": [],
        "angle_constraint_score": []
    }

    # Loop through each score type and filter values within the specified range
    for score_label, values in scores.items():
        filtered_values = [value for value in values if min_display_score <= value <= max_display_score]
        if filtered_values:  # Ensure there are values to prevent division by zero
            average = sum(filtered_values) / len(filtered_values)
            averages_within_range[score_label] = average
        else:
            averages_within_range[score_label] = None  # Indicate no data for this score within the range

    # Print out the averages
    for score_label, average in averages_within_range.items():
        if average is not None:
            print(f"Average {score_label} within {min_display_score}-{max_display_score}: {average}")
        else:
            print(f"No {score_label} data within {min_display_score}-{max_display_score}")

    return averages_within_range

def plot_label_histogram(label_value, save_path=None):
    # Plotting the histogram
    plt.hist(label_value.values(), bins=100, color='blue', edgecolor='black', alpha=0.7)
    plt.title('Label Value Distribution')
    plt.xlabel('Label Value')
    plt.ylabel('Frequency')

    # Save the histogram as a JPEG if save_path is provided
    if save_path:
        plt.savefig(save_path)
        print(f"Histogram saved as {save_path}")
    plt.show()

def plot_histograms(scores, base_folder, min_display_score, max_display_score):
    for label, values in scores.items():
        plt.figure()  # Start a new figure for each histogram
        plt.hist(values, bins=100, color='blue', edgecolor='black', alpha=0.7,
                 range=(min_display_score, max_display_score))
        plt.title(f'{label} Distribution ({min_display_score} to {max_display_score})')
        plt.xlabel('Score Value')
        plt.ylabel('Frequency')
        save_path = os.path.join(base_folder, f"{label}_histogram_{min_display_score}_to_{max_display_score}.jpg")
        plt.savefig(save_path)
        plt.show()
        print(f"Histogram for {label} displayed from {min_display_score} to {max_display_score} saved as {save_path}")

if __name__ == "__main__":
    base_folder = "/gpfs/users/a1836131/FINAL_HPC_SYNTHETIC_VESSEL_GENERATION_CODE/SYNTHETIC_GENERATOR/SYNTHETIC_DATA/UNREALISTIC_BRANCHING_NUM/UNREALISTIC_BRANCHING_NUM_PATCHES/"

    patch_folder = os.path.join(base_folder, "IMAGES")
    label_folder = os.path.join(base_folder, "LABELS")
    min_display_score = 1
    max_display_score = 50
    label_value, scores = calculate_average_score(patch_folder, label_folder)
    if label_value:
        plot_label_histogram(label_value, save_path=os.path.join(base_folder, "label_histogram.jpg"))
        plot_histograms(scores, base_folder, min_display_score=min_display_score, max_display_score=max_display_score)
        calculate_and_print_averages_within_range(scores, min_display_score=min_display_score, max_display_score=max_display_score)
#base_folder = "/gpfs/users/a1836131/FINAL_HPC_SYNTHETIC_VESSEL_GENERATION_CODE/SYNTHETIC_VESSELS/PATCHES/30_30_30/"
