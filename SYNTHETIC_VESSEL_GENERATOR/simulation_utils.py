import numpy as np
import random

def normalise_vector(vec):
    """Normalise vector to unit norm"""
    newvec = vec / np.linalg.norm(vec)
    return newvec


def check_image_bounds(location, img, image_bounds_brain_mask):
    """In-bounds check for coordinate within image"""
    voxel_value = image_bounds_brain_mask[int(location[0] - 1), int(location[1] - 1), int(location[2] - 1)]
    retval = False
    if 0 <= location[0] <= img.shape[0] - 1:
        if 0 <= location[1] <= img.shape[1] - 1:
            if 0 <= location[2] <= img.shape[2] - 1:
                if voxel_value < 1:
                    retval = True
    return retval


def draw_in_image(particle_list, img, uncontinuous_parameter, image_bounds_brain_mask):  # DRAW VESSELS WITH THE RADII AS THE 4TH DIMENSION FOR ANY VESSEL VOXEL - 2D LINE DRAWING OF VESSELS BUT CONSIDERING THE RADII TO PREVENT OVERLAP
    """Draw current particle positions in image (taking into account size/thickness)"""
    for part in particle_list:
        if check_image_bounds(part['location'], img, image_bounds_brain_mask):
            if random.random() <= uncontinuous_parameter:  # Save particle based on uncontinuous_parameter
                radius = part['radius']
                x, y, z = part['location']
                for i in range(int(x - radius), int(x + radius) + 1):
                    for j in range(int(y - radius), int(y + radius) + 1):
                        for k in range(int(z - radius), int(z + radius) + 1):
                            if check_image_bounds([i, j, k], img, image_bounds_brain_mask):
                                dist = np.linalg.norm([i - x, j - y, k - z])
                                if dist <= radius:
                                    img[int(x), int(y), int(z)] = radius  # drawing radius just for central voxel
            else:
                x, y, z = part['location']
                radius = part['radius']
                for i in range(int(x - radius), int(x + radius) + 1):
                    for j in range(int(y - radius), int(y + radius) + 1):
                        for k in range(int(z - radius), int(z + radius) + 1):
                            if check_image_bounds([i, j, k], img, image_bounds_brain_mask):
                                dist = np.linalg.norm([i - x, j - y, k - z])
                                if dist <= radius:
                                    uncontinuous_score_fn(scoring_function, x, y, z, radius)  # drawing radius just for central voxel
