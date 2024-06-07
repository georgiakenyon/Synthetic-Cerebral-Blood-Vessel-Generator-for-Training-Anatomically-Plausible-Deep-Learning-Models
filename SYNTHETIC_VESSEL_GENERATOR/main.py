from config import get_config
from vessel_functions import new_particle, update_all_particles
from io_operations import save_image, save_score_function
from simulation_utils import draw_in_image
from partial_volume_generation import generate_partial_volume_images
import nibabel as nib
import time
import os
import numpy as np
import pandas as pd

# ----------------------------------------------------------------------------------------------------------------
#                                SYNTHETIC VESSEL GENERATOR MAIN CODE : 3D RADIUS LINE IMAGE
# ----------------------------------------------------------------------------------------------------------------
def radius_simulation():
    #Load Config
    config = get_config()
    print("Simulation Configuration:", config)


    # Setup file paths and environment
    timestamp = time.strftime("%Y%m%d%H%M%S")
    FOLDER_NAME = f"VRR_{config['VESSEL_REPULSION_RADIUS']}_VRS_{config['VESSEL_REPULSION_STRENGTH']}_BRR_{config['BRAIN_REPULSION_RADIUS']}_BRS_{config['BRAIN_REPULSION_STRENGTH']}_UNCONT_PARAM_{config['UNCONTINUOUS_PARAMETER']}_BIF_TRIF_TOTAL_PROB_{config['BIFURCATION_TRIFURCATION_TOTAL_PROB']}_REALISTIC_ANGLES_{config['REALISTIC_ANGLES_PARAMETER']}_LLL_RADII_{config['LOWER_LENGTH_RANGE_LOW_RADII']}_ULL_RADII_{config['UPPER_LENGTH_RANGE_LOW_RADII']}_LLH_RADII_{config['LOWER_LENGTH_RANGE_HIGH_RADII']}_ULH_RADII_{config['UPPER_LENGTH_RANGE_HIGH_RADII']}_RAD_THRESH_{config['RADIUS_THRESHOLD']}_USTEP_{config['UPPER_STEPSIZE']}_LSTEP_{config['LOWER_STEPSIZE']}_{timestamp}"
    folder_path = os.path.join(config['SAVE_DIRECTORY'], FOLDER_NAME)
    os.makedirs(folder_path, exist_ok=True)  # Create the directory if it doesn't exist

    # Load and prepare data
    brain_edge_kernel_vector = nib.load(config['BRAIN_EDGE_KERNEL_VECTOR_PATH']).get_fdata()
    image_bounds_brain_mask = nib.load(config['IMAGE_BOUNDS_BRAIN_MASK']).get_fdata()
    brain_mask = nib.load(config['BRAIN_MASK']).get_fdata()

    # Set up the initial particle conditions
    initial_velocity = np.array([np.random.uniform(0.99, 1, 3)]).flatten()
    centre_location = np.array([config['INITIAL_VESSEL_X_COORD'], config['INITIAL_VESSEL_Y_COORD'], config['INITIAL_VESSEL_Z_COORD']])
    centre_location = centre_location.astype('float64')
    # Dynamic list of particles
    main_particle_list = [new_particle(centre_location, initial_velocity, config['INITIAL_VESSEL_LENGTH'],
                                       config['INITIAL_PARENT_RADIUS'])]

    # Initialize image array (4D with one channel (the binary image) to store the radius- Size of upsampled (2x) image)
    img = np.zeros((config['IMAGE_SHAPE_X'], config['IMAGE_SHAPE_Y'], config['IMAGE_SHAPE_Z'], 1))

    # Initialize image array (4D with one channel (the binary image) to store the radius- Size of upsampled (2x) image) and scoring function
    img = np.zeros((config['IMAGE_SHAPE_X'], config['IMAGE_SHAPE_Y'], config['IMAGE_SHAPE_Z'], 1))
    scoring_function = np.zeros((config['IMAGE_SHAPE_X'], config['IMAGE_SHAPE_Y'], config['IMAGE_SHAPE_Z'], 6))  # Assuming 6 scoring functions, # 4d so can save out additional info if multiple implausible parameters in one voxel


    # Simulation main loop
    for n in range(config['N_ITERATIONS']):
        main_particle_list = update_all_particles(main_particle_list,
                                                  config['VESSEL_REPULSION_RADIUS'],
                                                  config['VESSEL_REPULSION_STRENGTH'],
                                                  config['BRAIN_REPULSION_RADIUS'],
                                                  config['BRAIN_REPULSION_STRENGTH'],
                                                  img,
                                                  config['RADIUS_THRESHOLD'],
                                                  config['N_ITERATIONS'],
                                                  brain_edge_kernel_vector,
                                                  image_bounds_brain_mask,
                                                  scoring_function,
                                                  config['BIFURCATION_TRIFURCATION_TOTAL_PROB'],
                                                  main_particle_list)
        # print(f'Size of particle list = {len(main_particle_list)}')
        draw_in_image(main_particle_list, img, config['UNCONTINUOUS_PARAMETER'], image_bounds_brain_mask)  # not uncontinuous if = 1 = 100% of voxels are saved, 0.5 = 50% voxels saved to image

        if (n + 1) % config['N_ITERATIONS_SAVED'] == 0:  # Save image every _ iterations
            # Save the current state of the simulation
            radius_image = save_image(img, n + 1, folder_path, timestamp)
            overlapping_mask = scoring_function[:, :, :, 3] > 0
            scoring_function[:, :, :, 3][overlapping_mask] -= 1  # Subtract 1 from every voxel to find the overlapping vessels for the none realistic vessels.
            print("Applied overlapping function to score function image")
            score_image = save_score_function(scoring_function, n + 1, folder_path, timestamp)

    return radius_image, score_image, config, folder_path, timestamp

def pv_simulation(radius_image, score_image, pv_csv_file, folder_path, timestamp):
    generate_partial_volume_images(radius_image, score_image, pv_csv_file, folder_path, timestamp)

if __name__ == "__main__":
    #Create radius and radius score image at full resolution (0.35, 0.35, 0.35)
    radius_image, score_image, config, folder_path, timestamp = radius_simulation()
    # After simulation - create partial volumes and downsample images (0.7, 0.7, 0.7)
    pv_simulation(radius_image, score_image, config['PV_CSV_FILE'], folder_path, timestamp)