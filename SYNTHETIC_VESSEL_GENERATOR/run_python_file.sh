#!/bin/bash -l

#SBATCH --job-name=Synthetic_Vessels_Generation_2

#SBATCH --partition=highmem
#SBATCH --nodes=1
#SBATCH --ntasks-per-node=1 	# number of tasks (sequential job starts 1 task) (check this if your job unexpectedly uses 2 nodes)
#SBATCH --time=09:00:00 # time allocation, which has the format (D-HH:MM:SS)
#SBATCH --mem=256GB                                             # specify memory required per node (here set to 16 GB)


# Configure notifications
#SBATCH --mail-type=END                                         # Send a notification email when the job is done (=END)
#SBATCH --mail-type=FAIL                                        # Send a notification email when the job fails (=FAIL)
#SBATCH --mail-user=georgia.kenyon@adelaide.ac.uk         # Email to which notifications will be sent

# Execute your script (due to sequential nature, please select proper compiler as your script corresponds to)                                       # bash script used here for demonstration purpose, you should select proper compiler for your needs

#module load Anaconda3/2020.07
conda activate /gpfs/users/a1836131/CONDA_ENVS/SEG_ENV


echo "$(date) Starting main script"

#nvidia-smi -q -d MEMORY,COMPUTE,UTILIZATION

#output_file="Synthetic_image_iterations_${N_ITERATIONS}_radius_${VESSEL_REPULSION_RADIUS}_channels_${channels}_loss_fn_${loss_fns}_lr_${lrs}.out"

#SBATCH --output="${output_file}-%j.out"



python -u main.py \
    --N_ITERATIONS 2500 \
    --N_ITERATIONS_SAVED 2500 \
    --IMAGE_SHAPE_X 520 \
    --IMAGE_SHAPE_Y 622 \
    --IMAGE_SHAPE_Z 520 \
    --INITIAL_VESSEL_X_COORD 254 \
    --INITIAL_VESSEL_Y_COORD 342 \
    --INITIAL_VESSEL_Z_COORD 158 \
    --INITIAL_PARENT_RADIUS 7 \
    --VESSEL_REPULSION_RADIUS_LOWER 40 \
    --VESSEL_REPULSION_RADIUS_UPPER 70 \
    --VESSEL_REPULSION_STRENGTH 5000 \
    --BRAIN_REPULSION_RADIUS 5 \
    --BRAIN_REPULSION_STRENGTH 1000 \
    --THRESHOLD 70 \
    --LOWER_WIGGLE_RANGE 7 \
    --UPPER_WIGGLE_RANGE 11 \
    --RADIUS_THRESHOLD 2e-1 \
    --INITIAL_VESSEL_LENGTH_LOWER 44 \
    --INITIAL_VESSEL_LENGTH_UPPER 72 \
    --LOWER_LENGTH_RANGE_LOW_RADII 4 \
    --UPPER_LENGTH_RANGE_LOW_RADII 7 \
    --LOWER_LENGTH_RANGE_HIGH_RADII 7 \
    --UPPER_LENGTH_RANGE_HIGH_RADII 12 \
    --UPPER_STEPSIZE 0.1 \
    --LOWER_STEPSIZE 0.1 \
    --UNCONTINUOUS_PARAMETER 1 \
    --BIFURCATION_TRIFURCATION_TOTAL_PROB 1 \
    --UNREALISTIC_BRANCHING_RANGE_LOWER 4 \
    --UNREALISTIC_BRANCHING_RANGE_UPPER 7 \
    --REALISTIC_ANGLES_PARAMETER 0.9

echo "$(date) Finished running main script"

#    --N_ITERATIONS 5000 \
#    --N_ITERATIONS_SAVED 250 \
#    --IMAGE_SHAPE_X 520 \
#    --IMAGE_SHAPE_Y 622 \
#    --IMAGE_SHAPE_Z 520 \
#    --INITIAL_VESSEL_X_COORD 254 \
#    --INITIAL_VESSEL_Y_COORD 342 \
#    --INITIAL_VESSEL_Z_COORD 158 \
#    --INITIAL_PARENT_RADIUS 5 \
#    --VESSEL_REPULSION_RADIUS_LOWER 40 \
#    --VESSEL_REPULSION_RADIUS_UPPER 70 \
#    --VESSEL_REPULSION_STRENGTH 1000 \
#    --BRAIN_REPULSION_RADIUS 5 \
#    --BRAIN_REPULSION_STRENGTH 1000 \
#    --THRESHOLD 70 \
#    --LOWER_WIGGLE_RANGE 7 \
#    --UPPER_WIGGLE_RANGE 11 \
#    --RADIUS_THRESHOLD 2e-1 \
#    --INITIAL_VESSEL_LENGTH_LOWER 44 \
#    --INITIAL_VESSEL_LENGTH_UPPER 72 \
#    --LOWER_LENGTH_RANGE_LOW_RADII 4 \
#    --UPPER_LENGTH_RANGE_LOW_RADII 7 \
#    --LOWER_LENGTH_RANGE_HIGH_RADII 7 \
#    --UPPER_LENGTH_RANGE_HIGH_RADII 12 \
#    --UNCONTINUOUS_PARAMETER 1 \
#    --BIFURCATION_TRIFURCATION_TOTAL_PROB 1 \
#    --UNREALISTIC_BRANCHING_RANGE_LOWER 4 \
#    --UNREALISTIC_BRANCHING_RANGE_UPPER 10 \
#    --REALISTIC_ANGLES_PARAMETER 1