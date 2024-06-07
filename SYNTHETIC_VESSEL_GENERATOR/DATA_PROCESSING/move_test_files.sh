#!/bin/bash

# Set the paths for the source and destination directories
source_dir="/gpfs/users/a1836131/FINAL_HPC_SYNTHETIC_VESSEL_GENERATION_CODE/SYNTHETIC_VESSELS/PATCHES/50_50_50/IMAGES"
dest_dir="/gpfs/users/a1836131/FINAL_HPC_SYNTHETIC_VESSEL_GENERATION_CODE/SYNTHETIC_VESSELS/PATCHES/50_50_50/TEST_IMAGES"
label_source_dir="/gpfs/users/a1836131/FINAL_HPC_SYNTHETIC_VESSEL_GENERATION_CODE/SYNTHETIC_VESSELS/PATCHES/50_50_50/LABELS"
label_dest_dir="/gpfs/users/a1836131/FINAL_HPC_SYNTHETIC_VESSEL_GENERATION_CODE/SYNTHETIC_VESSELS/PATCHES/50_50_50/TEST_LABELS"

# Randomly select 50 files from the source directory
selected_files=($(ls "$source_dir"/*patch_*.nii.gz | shuf -n 220))

# Move the selected files to the destination directory
for file in "${selected_files[@]}"; do
    # Extract the numerical value from the file name
    file_name=$(basename "$file")

    # Print debugging information
    echo "Moving $file to $dest_dir/"

    # Move the image file to the destination directory
    mv "$file" "$dest_dir/"

    # Find the corresponding label file with the same numerical value
    label_file=$(find "$label_source_dir" -name "label_${file_name}" | head -n 1)

    if [ -n "$label_file" ]; then
        # Print debugging information
        echo "Moving $label_file to $label_dest_dir/"

        # Move the corresponding label file to the destination label directory
        mv "$label_file" "$label_dest_dir/"
    else
        # Print an error message if the label file is not found
        echo "Error: Label file not found for $file_name."
    fi
done