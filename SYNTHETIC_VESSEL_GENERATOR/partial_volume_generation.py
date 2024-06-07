import numpy as np
from scipy.interpolate import griddata
import numpy as np
import pandas as pd
import nibabel as nib
from io_operations import save_pv_image, save_final_pv_image, save_final_score_image
from image_processing import downsample_radius_image, downsample_radius_score_image, downsample_pv_image

# ----------------------------------------------------------------------------------------------------------------
#                                 PARTIAL VOLUME FUNCTIONS OF VESSELS WITH RADII
# ----------------------------------------------------------------------------------------------------------------

def interpolate_mean_pv(data, radius, distance):
    radii = data['radius'].values
    distances = data['distance'].values
    mean_pvs = data['mean_pv'].values
    interpolated_mean_pvs = griddata((radii, distances), mean_pvs, (radius, distance), method='linear')
    return interpolated_mean_pvs


def calculate_partial_volume_image_upsampled(pv_csv_data, radius_img, img_shape):
    partial_volume_img = np.zeros(img_shape)  # EMPTY PV volume of same size of vessel image
    distances_to_interpolate = [0.0, 1.0, 2.0, 3.0, 4.0, 5.0, 6.0, 8.0, 9.0, 12.0]

    for z0 in range(radius_img.shape[2]):
        for y0 in range(radius_img.shape[1]):
            for x0 in range(radius_img.shape[0]):
                r0 = radius_img[x0, y0, z0]
                if 4 >= r0 > 0:
                    # print(f"radius value: {r0}, x: {x0} y: {y0}, z: {z0}")
                    # if have radius, what are the mean_pvs for all distances before get into for dx, dy, dz loops?
                    pvs = {}
                    for dist in distances_to_interpolate:
                        pvs[dist] = interpolate_mean_pv(pv_csv_data, r0, dist)
                        # print(f'For radius: {r0}, and distance: {dist}, the mean pv is: {pvs[dist]}')
                    for dx in [-2.0, -1.0, 0.0, 1.0, 2.0]:
                        for dy in [-2.0, -1.0, 0.0, 1.0, 2.0]:
                            for dz in [-2.0, -1.0, 0.0, 1.0, 2.0]:
                                x1, y1, z1 = int(x0 + dx), int(y0 + dy), int(z0 + dz)
                                if 0 <= x1 < radius_img.shape[0] and 0 <= y1 < radius_img.shape[1] and 0 <= z1 < \
                                        radius_img.shape[2]:
                                    distance = (x1 - x0) * (x1 - x0) + (y1 - y0) * (y1 - y0) + (z1 - z0) * (z1 - z0)
                                    # print(f'Distance is: {distance}')
                                    mean_pv = pvs[distance]  # get precomputed pvs from dist value
                                    # print(f'mean_pv = {mean_pv}')
                                    partial_volume_img[x1, y1, z1] += mean_pv

    partial_volume_img[partial_volume_img > 1] = 1  # Convert any values above 1 to 1 in PV image.
    return partial_volume_img


def calculate_partial_volume_image_downsampled(pv_csv_data, radius_img, img_shape):
    partial_volume_img = np.zeros(img_shape)  # EMPTY PV volume of same size of vessel image
    distances_to_interpolate = [0.0, 1.0, 2.0, 3.0, 4.0, 5.0, 6.0, 8.0, 9.0, 12.0]

    for z0 in range(radius_img.shape[2]):
        for y0 in range(radius_img.shape[1]):
            for x0 in range(radius_img.shape[0]):
                r0 = radius_img[x0, y0, z0]
                if r0 > 2.0:
                    # print(f"radius value: {r0}, x: {x0} y: {y0}, z: {z0}")
                    # if have radius, what are the mean_pvs for all distances before get into for dx, dy, dz loops?
                    pvs = {}
                    for dist in distances_to_interpolate:
                        pvs[dist] = interpolate_mean_pv(pv_csv_data, r0, dist)
                        # print(f'For radius: {r0}, and distance: {dist}, the mean pv is: {pvs[dist]}')
                    for dx in [-2.0, -1.0, 0.0, 1.0, 2.0]:
                        for dy in [-2.0, -1.0, 0.0, 1.0, 2.0]:
                            for dz in [-2.0, -1.0, 0.0, 1.0, 2.0]:
                                x1, y1, z1 = int(x0 + dx), int(y0 + dy), int(z0 + dz)
                                if 0 <= x1 < radius_img.shape[0] and 0 <= y1 < radius_img.shape[1] and 0 <= z1 < \
                                        radius_img.shape[2]:
                                    distance = (x1 - x0) * (x1 - x0) + (y1 - y0) * (y1 - y0) + (z1 - z0) * (z1 - z0)
                                    # print(f'Distance is: {distance}')
                                    mean_pv = pvs[distance]  # get precomputed pvs from dist value
                                    # print(f'mean_pv = {mean_pv}')
                                    partial_volume_img[x1, y1, z1] += mean_pv

    partial_volume_img[partial_volume_img > 1] = 1  # Convert any values above 1 to 1 in PV image.
    return partial_volume_img



# ----------------------------------PARTIAL VOLUME IMAGE GENERATION--------------------------------------------------------------------

def generate_partial_volume_images(radius_image, score_image, pv_csv_file, folder_path, timestamp):

    radius_vessel_arr = radius_image
    radius_score_arr = score_image
    pv_csv_data = pd.read_csv(pv_csv_file)

    downsampled_radius_image = downsample_radius_image(folder_path, timestamp, radius_vessel_arr, save_img=True)  # downsample whole  image, just to extract the information about the vessels with a larger than 4 radii.
    downsampled_score_image = downsample_radius_score_image(folder_path, timestamp, radius_score_arr, save_img=True)

    partial_volume_img_downsampled = calculate_partial_volume_image_downsampled(pv_csv_data,
                                                                            radius_img=downsampled_radius_image,
                                                                            img_shape=(
                                                                                downsampled_radius_image.shape))  # pv of radius values that are larger than 2.
    save_pv_image(partial_volume_img_downsampled, folder_path, timestamp)

    radius_img = np.copy(radius_vessel_arr)

    partial_volume_img_upsampled = calculate_partial_volume_image_upsampled(pv_csv_data, radius_img=radius_img, img_shape=(radius_img.shape))  # pv image of original upsampled radii image, but only radius less than 2

    partial_volume_img_new_downsampled = downsample_pv_image(folder_path, timestamp, pv_vessel_arr=partial_volume_img_upsampled, save_img=True)  # downsample the pv array that is focussed on smaller vessels
    final_pv_image = partial_volume_img_new_downsampled + partial_volume_img_downsampled

    save_final_pv_image(final_pv_image, folder_path, timestamp)

    adjust_score_images(downsampled_score_image, final_pv_image, folder_path, timestamp)


def adjust_score_images(score_image, final_pv_image, folder_path, timestamp):
    # Adjusting score images based on conditions
    # Remove the angle scores where there is no longer a vessel due to pvs removing small radii.
    angle_condition = (score_image[:, :, :, 5] > 0) & (final_pv_image[:, :, :] == 0)
    score_image[angle_condition, 5] = 0

    # Remove the uncontinuous scores if the partial volume is present in the voxel
    uncontinuous_condition = (score_image[:, :, :, 2] == 1) & (final_pv_image[:, :, :] > 0)
    score_image[uncontinuous_condition, 2] = 0

    # Remove the angle scores where there is branching more than 3 as overconstrained
    branching_condition = (score_image[:, :, :, 0] > 0) & (score_image[:, :, :, 5] > 0)
    score_image[branching_condition, 5] = 0

    save_final_score_image(score_image, folder_path, timestamp)

