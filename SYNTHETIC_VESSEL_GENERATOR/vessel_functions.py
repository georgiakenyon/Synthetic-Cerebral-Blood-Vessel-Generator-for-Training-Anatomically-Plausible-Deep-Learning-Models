import numpy as np
from simulation_utils import normalise_vector, check_image_bounds, draw_in_image
from scoring_functions import (
    branching_score_fn,
    radius_threshold_score_fn,
    uncontinuous_score_fn,
    overlapping_score_fn,
    length_radius_ratio_score_fn,
    angle_constrained_score_fn
)
import random
from random import randrange
from config import get_config

config = get_config()

def new_particle(location, velocity, length, radius):
    """Create a new particle with defined location and velocity and return it"""
    new_p = {'location': location.copy(), 'velocity': velocity.copy(),
             'length': length, 'radius': radius, 'event': 'branch'}
    return new_p

def update_velocity(particle, particle_list, vessel_repulsion_radius, vessel_repulsion_strength, brain_repulsion_radius,
                    brain_repulsion_strength, brain_edge_kernel_vector):
    vessel_overlap_repulsion_force_vec = overlap_repulsion_force(particle, particle_list, vessel_repulsion_radius,
                                                                 vessel_repulsion_strength)
    # print(f'vessel overlap force vector: {vessel_overlap_repulsion_force_vec}')
    brain_edge_repulsion_force_vec = brain_edge_force(particle, brain_repulsion_strength, brain_edge_kernel_vector)
    # print(f'brain edge repulsion force vector: {brain_edge_repulsion_force_vec}')
    new_velocity = normalise_vector(particle['velocity'] + vessel_overlap_repulsion_force_vec + brain_edge_repulsion_force_vec)
    # print(f'new_velocity after both repulsion forces = {new_velocity}')
    return new_velocity

def overlap_repulsion_force(particle, particle_list, vessel_repulsion_radius, vessel_repulsion_strength):
    force = np.zeros((3,))  # VESSEL REPULSION FORCE (prevent overlap of vessels)
    for other_particle in particle_list:
        if np.any(particle['location'] != other_particle['location']):
            dist = np.linalg.norm(particle['location'] - other_particle['location'])
            if dist < vessel_repulsion_radius:
                direction = normalise_vector(particle['location'] - other_particle['location'])
                force += vessel_repulsion_strength * direction

    return force


def brain_edge_force(particle, brain_repulsion_strength, brain_edge_kernel_vector):
    location = particle['location']
    x, y, z = int(location[0]), int(location[1]), int(location[2])
    if (brain_edge_kernel_vector[x, y, z] == (0, 0, 0)).all():
        # print(brain_edge_kernel_vector[x, y, z])
        force = np.zeros((3,))
        # print("Vessel not in range of brain mask")
    else:
        # print(brain_edge_kernel_vector[x, y, z])
        force = -brain_edge_kernel_vector[x, y, z] * brain_repulsion_strength
    # print(f'brain edge force: {force}')
    return force

def new_branch_properties(parent_velocity, num_branches, main_particle_list, scoring_function, radius_threshold, parent_radius, location, implausible_threshold):
    """Create velocities, lengths and radii for multiple branches"""
    x, y, z = location
    props = []
    if num_branches != 1:
        # prop = {}
        daughter_radii, angles = update_radius(parent_radius, num_branches, location, scoring_function, radius_threshold)
        if all(r > radius_threshold for r in daughter_radii):  # Ensures all radii are above the threshold
            if num_branches > 3:  #and (daughter_radii >= implausible_threshold).all()
                print(f'Scoring branching as implausible branches') #and vessel radii are above the threshold: {daughter_radii}')
                branching_score_fn(scoring_function, x, y, z, num_branches, parent_radius)  # BRANCHING SCORING FUNCTION
            # print(f'daughter radii = {daughter_radii}, angles = {angles}')
            daughter_vector = constrain_angle_vectors(angles, parent_velocity, num_branches)
            # print(f'daughter vector = {daughter_vector}')
            for i in range(num_branches):
                prop = {}
                # print(f'i in new_branch_properties function: {i}')
                prop['radius'] = daughter_radii[i]
                radius = prop['radius']
                prop['velocity'] = daughter_vector[i]
                prop['length'] = 2 * update_length(prop['radius'], parent_radius, particle_list=main_particle_list)  # 2x upsampled
                # print(f'props = {prop} when 2 or more branches')
                props.append(prop)
        else:
            print(f'Branch not created as not all radii are above the threshold at location ({x}, {y}, {z}).')
    else:  # if one branch
        # prop = {}
        daughter_radii = update_radius(parent_radius, num_branches, location, scoring_function, radius_threshold)
        if all(r > radius_threshold for r in daughter_radii):  # Ensures all radii are above the threshold
            for i in range(num_branches):
                prop = {}
                weight = np.random.uniform(low=config['LOWER_WIGGLE_RANGE'], high=config['UPPER_WIGGLE_RANGE'],
                                           size=num_branches)  # WEIGHT FOR THE WIGGLE OF THE VESSEL
                prop['radius'] = daughter_radii[i]
                radius = prop['radius']
                prop['length'] = 2 * update_length(prop['radius'], parent_radius, particle_list=main_particle_list)  # 2x upsampled
                prop['velocity'] = normalise_vector(
                    weight[i] * parent_velocity + (1 - weight[i]) * np.random.standard_normal((3,)))
                props.append(prop)
        else:
            print(f'Branch not created as radii is above the threshold at location ({x}, {y}, {z}).')
    # print(f'OVERALL PROPERTY LIST FOR SPECIFIC BRANCH POINT (1, 2, 3 ETC DEPENDANT ON HOW MANY BRANCHES SET: {props}')
    return props

def update_length(proximal_radii, parent_radius, particle_list):
    # Length to radius ratio = length_of_artery / proximal radius
    if proximal_radii > parent_radius - 2:  # if the vessels have radii 2 or less smaller than the largest initial parent vessel radii, use these bounds
        realistic_lower_lr, realistic_upper_lr = 4, 7  # KEEP SAME (BASED ON ANATOMY)
        lower_lr, upper_lr = config['LOWER_LENGTH_RANGE_LOW_RADII'], config['UPPER_LENGTH_RANGE_LOW_RADII']  # CHANGABLE PARAMETER BASED ON ANATOMICAL PLAUSIBILITY
        lr = float(np.random.uniform(upper_lr,
                                     lower_lr))  # LOWER_LENGTH_RANGE, UPPER_LENGTH_RANGE # Based on LR = 10.79 (Dissection), 6.82 (7T MRI), 4.24 (9.4T MRI) (LARGE RANGE)
        length = lr * proximal_radii
        # length_radius_ratio_score_fn(scoring_function, lr, realistic_upper_lr, realistic_lower_lr, particle_list)
    else:  # if the vessels have radii more than 2 below the largest initial parent vessel radii, use these bounds
        realistic_lower_lr, realistic_upper_lr = 7, 12  # KEEP SAME (BASED ON ANATOMY)
        lower_lr, upper_lr = config['LOWER_LENGTH_RANGE_HIGH_RADII'], config['UPPER_LENGTH_RANGE_HIGH_RADII'] # CHANGABLE PARAMETER BASED ON ANATOMICAL PLAUSIBILITY
        lr = float(np.random.uniform(upper_lr,
                                     lower_lr))  # Based on LR = 10.79 (Dissection), 6.82 (7T MRI), 4.24 (9.4T MRI) (LARGE RANGE)
        length = lr * proximal_radii
        # length_radius_ratio_score_fn(scoring_function, lr, realistic_upper_lr, realistic_lower_lr, particle_list)

    return length


def length_of_particle():
    # length = randrange(22, 36) #The mean length of the ICA from the proximal cavernous segment to the ICA terminus was 33.1 ± 6.1 mm. mean MCA length was 22.5 ± 8.1 mm. https://pubmed.ncbi.nlm.nih.gov/22490430/
    length = config['INITIAL_VESSEL_LENGTH']
    return length



#-----------------------------------------------------BRANCHING---------------------------------------------------------

def num_branches(bifurcation_trifurcation_total_prob):  # Number of branches (30% trifurcation + 70% bifurcation or no branching)
    bifurcation_prob = 0.7
    # IF NOT EQUAL TO 1, THERE WILL BE UNREALISTIC VESSELS PRESENT.
    for i in range(randrange(1, 5)):  # random value between 1 and 5 (20% chance of only having a branch number = 1)
        if i == 1:
            num_branches = 1  # no bifurcation or trifurcation
        else:
            random_integer = random.random()
            if random_integer < bifurcation_prob:
                num_branches = 2  # 70% chance of bifurcation
            elif random_integer < bifurcation_trifurcation_total_prob:
                num_branches = 3  # 30% chance of trifurcation
            else:
                num_branches = randrange(config['UNREALISTIC_BRANCHING_RANGE_LOWER'], config['UNREALISTIC_BRANCHING_RANGE_UPPER'])  # UNREALISTIC BRANCHING PATTERNS between a range

    return num_branches



def update_radius(parent_radius, num_branches, location, scoring_function, radius_threshold, tolerance=1e-3, max_iterations=100):
    """Calculate the radii of daughter particles based on the parent radius"""
    x, y, z = location
    while True:
        parent_radius_cubed = np.power(parent_radius, 3)
        iterations = 0
        while iterations < max_iterations:
            random_radii = np.random.uniform(parent_radius * 0.1, parent_radius, size=num_branches - 1)
            extra_radius = np.random.uniform(parent_radius * 0.1, parent_radius, size=1)
            extra_radius = np.array([extra_radius])
            daughter_radii = np.append(random_radii, extra_radius)
            sum_of_daughters_cubed = np.sum(np.power(daughter_radii, 3))
            if abs(sum_of_daughters_cubed - parent_radius_cubed) < tolerance:
                print("Parent radius value: " + str(parent_radius))
                print("Daughter radii values: " + str(daughter_radii))
                if len(daughter_radii) == 1:
                    return daughter_radii
                else:  # if more than one daughter branch
                    angles = []
                    for i in range(num_branches - 1):
                        print(f'i = {i}')
                        #print(f'Angles: {angles}')
                        print(f'Daughter radii being applied to generate angles: {daughter_radii[i]} and {daughter_radii[i + 1]}')
                        valid_angle_found = False
                        while not valid_angle_found:
                            if num_branches <= 3: #changed from 4...
                                angle_pair = constrain_angles(i, location, parent_radius, daughter_radii, angles, scoring_function, radius_threshold,
                                                              config['REALISTIC_ANGLES_PARAMETER'])
                                if angle_pair:
                                    # print(f'length of the angle pairs are: {len(angle_pair)}')
                                    angles.append(angle_pair)
                                    # print(f'length of the angles are: {len(angles)}')
                                    valid_angle_found = True
                                    print(f'Angles at i={i} are {angles}')
                                else:
                                    # print('Invalid angles found, regenerating daughter radii.')
                                    break
                            else: #SORT THIS FOR UNREALISTIC BRANCHING.
                                # print(f'Invalid angles found at i={i}, reattempting.')
                                random_angle_pair = (np.random.uniform(0, np.pi), np.random.uniform(0, np.pi))
                                angles.append(random_angle_pair)
                                #angle_constrained_score_fn(scoring_function, x, y, z)
                                # print(f'Daughter branches are: {daughter_radii}. Angles at i={i} are {angles}, These are implaussible angles, but it is OKAY as the score image will highlight this.')
                                valid_angle_found = True

                        if not valid_angle_found:
                            # Break out of the for-loop if max attempts for angle generation are reached
                            break

                    if len(angles) == num_branches - 1:
                        # print(f'length of angles: {len(angles)}')
                        # print(f'daughter_radii = {daughter_radii} and angles = {angles}')
                        return daughter_radii, angles
                    else:
                        # print('Invalid angles found. Reiterating.')
                        break  # Restart the loop
            iterations += 1

        # print("Reached maximum iterations. Restarting the loop.")

def constrain_angle_vectors(angles, parent_velocity, num_branches):
    # print(f'Number of branches are: {num_branches}')
    # print(f'Angle values are: {angles}')
    # print(f'There are {len(angles)} pairs of angles, which means {len(angles)+1} daughter vessels')
    daughter_vectors = []
    for i in range(len(angles)):
        # print(f'i = {i}')
        theta1, theta2 = angles[i]
        # print(f'theta1 and theta 2: {theta1}, {theta2}')
        u0 = parent_velocity
        u1 = np.array([np.cos(theta1), np.sin(theta1), 0])  # Construct vectors u1 and u2 in the 2D plane (z=0)
        u2 = np.array([np.cos(theta2), np.sin(theta2), 0])
        # print(f'u0 = {u0}, u1 = {u1} and u2 = {u2}')

        while True:
            v1 = np.random.normal(size=(3, 1))  # Generate a random vector v1 (3x1 vector with Gaussian random values)
            v = v1 - (v1 * np.dot(v1.T, u0) / np.sqrt(np.dot(v1.T, v1)))
            # print(f'theta1 = {theta1}, theta2 = {theta2}, u0 = {parent_velocity}, u1 = {u1}, u2 = {u2}, v1 = {v1}, v = {v}')
            if not np.allclose(v, np.zeros_like(v)):
                # go back to v1 random generator
                w1 = normalise_vector(v)  # Normalize the length of v1 to get w1 (orthogonal, unit direction vector)
                # print(f'w1 = {w1}')
                w2 = np.cross(u0.T,
                              w1.T)  # Calculate w2 as the cross product of u0 and w1 (third orthogonal direction vector)
                # print(f'w2 = {w2}')
                R = np.column_stack((u0, w1, w2.T))  # Construct the rotation matrix R using u0, w1, and w2
                # print(f'R = {R}')
                if i == 0:  # working with first two daughters
                    daughter_vector1 = np.dot(R,
                                              u1)  # Apply the rotation matrix to vectors u1 and u2 to get the final direction vectors for the children
                    daughter_vectors.append(daughter_vector1)
                    daughter_vector2 = np.dot(R, u2)
                    # print(f'Daughter Vector 1 = {daughter_vector1}, Daughter Vector 2: {daughter_vector2}')
                    daughter_vectors.append(daughter_vector2)
                    # daughter_vectors.append((daughter_vector1, daughter_vector2))
                    # print(f' COMPLETE DAUGHTER VECTORS ARE: {daughter_vectors}')
                    break
                else:  # more than 2 daughters, e.g.2nd and 3rd daughter - already have the 2nd daughter vector.
                    # daughter_vector1 = daughter_vectors[i - 1][i]
                    daughter_vector1 = daughter_vectors[i]
                    # print(f'daughter vector 1 (e.g. 2nd and 3rd daughter) = {daughter_vector1}')
                    daughter_vector2 = np.dot(R, u2)
                    # print(f'Daughter Vector 1 = {daughter_vector1}, Daughter Vector 2: {daughter_vector2}')
                    daughter_vectors.append((daughter_vector2))
                    # print(f' COMPLETE DAUGHTER VECTORS ARE: {daughter_vectors}')
                    # print(f'daughter vectors shape= {daughter_vectors}')
                    break

    return daughter_vectors


def constrain_angles(i, location, parent_radius, daughter_radii, angles, scoring_function,  radius_threshold, realistic_angles_parameter):
    x, y, z = location
    if random.random() <= realistic_angles_parameter:  # generate invalid angles based on the the parameter
        cos_theta_l, cos_theta_r = calculate_cosines(parent_radius, daughter_radii, i)
        # print(f'cos_theta_l: {cos_theta_l}, cos_theta_r: {cos_theta_r}')
        if -1 <= cos_theta_l <= 1 and -1 <= cos_theta_r <= 1:
            theta_l = np.arccos(cos_theta_l)
            theta_r = np.arccos(cos_theta_r)
            print(f'Angles between the paired vessels are: angle l: {np.degrees(theta_l):.2f}° and angle r: {np.degrees(theta_r):.2f}° with daughter radii: {daughter_radii[i]} and {daughter_radii[i + 1]}')
            # print('Angles between the paired vessels are: angle l:' + str(theta_l) + ' angle r:' + str(theta_r) + ' with daughter radii:' + str(daughter_radii[i]) + ' and ' + str(daughter_radii[i + 1]))
            return (theta_l, theta_r)
        else:
            print('Invalid angles found (not -1 <= cos_theta_l <= 1 and -1 <= cos_theta_r <= 1). Providing empty angle list.')
            return None

    else: #Generate unrealistic angles
        print(f'Generating unrealistic angles for pair of vessels')
        realistic_cos_theta_l, realistic_cos_theta_r = calculate_cosines(parent_radius, daughter_radii, i)
        if -1 <= realistic_cos_theta_l <= 1 and -1 <= realistic_cos_theta_r <= 1: #Generate realistic angles for the vessels, to then generate unrealistic vessels and score differences
            realistic_theta_l = np.arccos(realistic_cos_theta_l)
            realistic_theta_r = np.arccos(realistic_cos_theta_r)
            print(f'Realistic angles between the paired vessels are: angle l: {realistic_theta_l} and angle r: {realistic_theta_r} with daughter radii: {daughter_radii[i]} and {daughter_radii[i + 1]}')

            print(f'Realistic angles between the paired vessels are: angle l: {np.degrees(realistic_theta_l):.2f}° and angle r: {np.degrees(realistic_theta_r):.2f}° with daughter radii: {daughter_radii[i]} and {daughter_radii[i + 1]}')
            print(f'Generating unrealistic angles that do not obey Murrays laws (still within 0 to 180 degrees as cosine between -1 and 1.)')
            cos_theta_l = random.uniform(-1, 1)  # should i make this slighly less than 1 or -1 so not directly inline with original parent vessel? # Avoid exactly -1 or 1 to prevent undefined behavior in arccos
            cos_theta_r = random.uniform(-1, 1)
            theta_l = np.arccos(cos_theta_l)
            theta_r = np.arccos(cos_theta_r)

            if (cos_theta_l != realistic_cos_theta_l) or (cos_theta_r != realistic_cos_theta_r):
                #if daughter_radii[i] or daughter_radii[i + 1] < radius_threshold: #Only produce if within the radius threshold
                if all(r > radius_threshold for r in daughter_radii):  # Ensures all radii are above the threshold
                    # cos_theta_l and cos_theta_r could feasibly be between 0 and 180 degrees (0 or pi).
                    #print(f'Realistic angle values are: {realistic_cos_theta_l} and {realistic_cos_theta_r}. {realistic_theta_l} and {realistic_theta_r}  ')
                    #print(f'Angle values are outside of range for plausibility: {theta_l} and {theta_r}  and radii are within threshold: {daughter_radii[i]} and {daughter_radii[i + 1]}, adding score to unrealistic angle score img')
                    #print(f'Realistic angle cosines are: {np.degrees(realistic_cos_theta_l):.2f}° and {np.degrees(realistic_cos_theta_r):.2f}°.')
                    print(f'Implausible angles detected: {theta_l} and {theta_r} with radii: {daughter_radii[i]}, {daughter_radii[i + 1]}, adding score to unrealistic angle score img')
                    print(f'Implausible angles detected: {np.degrees(theta_l):.2f}° and {np.degrees(theta_r):.2f}° with radii: {daughter_radii[i]}, {daughter_radii[i + 1]}, adding score to unrealistic angle score img')
                    angle_constrained_score_fn(np.degrees(theta_l), np.degrees(theta_r), np.degrees(realistic_theta_l), np.degrees(realistic_theta_r),
                                               scoring_function, x, y, z)
                else:
                    print(
                        f"Angle values are incorrect but don't save implausibility value as one (or more) of the radii will not be saved in image as below threshold, with radii: {daughter_radii[i]}, {daughter_radii[i + 1]}")
                # print(f'Angle values are outside of range for plausibility: {angles}, adding score to unrealistic angle score img')
            return (theta_l, theta_r)
        else:
            print('Invalid angles (not -1 <= realistic_cos_theta_l <= 1 and -1 <= realistic_cos_theta_r <= 1)  found. Providing empty angle list.')
            return None

def calculate_cosines(parent_radius, daughter_radii, index):
    """Calculate cosine values for angle constraints based on radii."""
    cos_theta_l = ((parent_radius ** 4 + daughter_radii[index] ** 4 - daughter_radii[index + 1] ** 4) /
                   (2 * parent_radius ** 2 * daughter_radii[index] ** 2))
    cos_theta_r = ((parent_radius ** 4 + daughter_radii[index + 1] ** 4 - daughter_radii[index] ** 4) /
                   (2 * parent_radius ** 2 * daughter_radii[index + 1] ** 2))
    return cos_theta_l, cos_theta_r


def update_all_particles(particle_list, vessel_repulsion_radius, vessel_repulsion_strength, brain_repulsion_radius,
                         brain_repulsion_strength, img, radius_threshold, n_iterations, brain_edge_kernel_vector, image_bounds_brain_mask, scoring_function, bifurcation_trifurcation_total_prob, main_particle_list, implausible_threshold=0.2):
    new_particle_list = []
    for part in particle_list:
        # print(f' particle list: {particle_list}')
        # print(f'new particle list: {new_particle_list}')
        if part['radius'] > 1.0:  # calculate the stepsize based on the radii
            stepsize = config['UPPER_STEPSIZE']
            n_iterations += 1
        else:
            stepsize = config['LOWER_STEPSIZE']
            n_iterations += 1
            # stepsize = 0.1 * stepsize_factor * part['radius'] #calculate the stepsize based on the radii
        # print(f'PARTS_DURING_UPDATE_ALL_PARTICLES FUNC: {part}')
        delta_pos = stepsize * part['velocity']
        # print(f'delta_pos = {delta_pos} and the shape is {delta_pos.shape}')
        part['length'] -= np.linalg.norm(delta_pos)
        if part['length'] > 0:
            # print(f'part if length is > 0: {part}')
            # print(f'delta_pos if length > 0: {delta_pos}')
            # print("location:", part['location'])
            part['location'] += delta_pos
            # print(f'velocity and location = {part}')
            part['velocity'] = update_velocity(part, particle_list, vessel_repulsion_radius, vessel_repulsion_strength,
                                               brain_repulsion_radius, brain_repulsion_strength, brain_edge_kernel_vector)
            # print("Before radius update:", part['radius'])  # Print the radius before update
            part['radius'] = part['radius']
            # print("After radius update:", part['radius'])  # Print the radius after update
            if check_image_bounds(part['location'], img, image_bounds_brain_mask):
                new_particle_list += [part]
                # print(f'new particle list: {new_particle_list}')
        else:
            # print(f'MAKING A BRANCH POINT')
            x, y, z = part['location']
            # print(f'location of new branch point: {x}, {y}, {z}')
            radius = part['radius']
            overlapping_score_fn(scoring_function, x, y, z)  # FOR OVERLAPPING SCORE FUNCTION
            branches = num_branches(bifurcation_trifurcation_total_prob)
            proplist = new_branch_properties(part['velocity'], branches, main_particle_list, scoring_function, radius_threshold, parent_radius=part['radius'],
                                             location=part['location'], implausible_threshold=0.2)
            # print('Generated list of properties for the branch')
            for prop in proplist:
                radius = prop['radius']
                if radius < implausible_threshold:
                    if radius > radius_threshold:
                        radius_threshold_score_fn(scoring_function, radius, x, y, z)
                        # print(f"Branch radius {radius} below implausible threshold but above radius threshold at location ({x}, {y}, {z}). NOT Skipping update but saving as implausibility score.")
                    else:  # if radius < radius threshold and implausibility threshold
                        # print(f"Branch radius {radius} below threshold and implausible threshold at location ({x}, {y}, {z}). Skipping update and making new branch point. Not saving score as not saving radius")
                        continue
                new_part = new_particle(part['location'], prop['velocity'], prop['length'], prop[
                    'radius'])  # only start particle growth if the vessels have a radius above the threshold
                # print("New branch radius:", prop['radius'], "New branch velocity:", prop['velocity'])  # Print the new branch radius
                new_particle_list += [new_part]
            # print(f'NEW PARTICLE LIST AFTER BRANCHING OCCURS: {new_particle_list}')
    return new_particle_list



# def new_branch_properties(parent_velocity, num_branches, main_particle_list, scoring_function, radius_threshold, parent_radius, location, implausible_threshold):
#     """Create velocities, lengths and radii for multiple branches"""
#     x, y, z = location
#     props = []
#
#     if num_branches != 1:
#         # prop = {}
#         daughter_radii, angles = update_radius(parent_radius, num_branches, location, scoring_function, radius_threshold)
#         if num_branches > 3 and (daughter_radii >= implausible_threshold).all():  # Assuming 0.35 is the threshold
#             print(f'Scoring branching as implausible branches and vessel radii are above the threshold: {daughter_radii}')
#             branching_score_fn(scoring_function, x, y, z, num_branches, parent_radius)  # BRANCHING SCORING FUNCTION
#         # print(f'daughter radii = {daughter_radii}, angles = {angles}')
#         daughter_vector = constrain_angle_vectors(angles, parent_velocity, num_branches)
#         # print(f'daughter vector = {daughter_vector}')
#         for i in range(num_branches):
#             prop = {}
#             # print(f'i in new_branch_properties function: {i}')
#             prop['radius'] = daughter_radii[i]
#             radius = prop['radius']
#             # if radius < implausible_threshold and scoring_function[int(x), int(y), int(z), 5] = 1:
#             #     scoring_function[int(x), int(y), int(z), 5] = 0
#             # if radius < implausible_threshold:
#             #     radius_threshold_score_fn(scoring_function, radius, x, y, z)
#             prop['velocity'] = daughter_vector[i]
#             prop['length'] = 2 * update_length(prop['radius'], parent_radius, particle_list=main_particle_list)  # 2x upsampled
#             # print(f'props = {prop} when 2 or more branches')
#             props.append(prop)
#
#     else:  # if one branch
#         # prop = {}
#         daughter_radii = update_radius(parent_radius, num_branches, location, scoring_function, radius_threshold)
#         for i in range(num_branches):
#             prop = {}
#             weight = np.random.uniform(low=config['LOWER_WIGGLE_RANGE'], high=config['UPPER_WIGGLE_RANGE'],
#                                        size=num_branches)  # WEIGHT FOR THE WIGGLE OF THE VESSEL
#             prop['radius'] = daughter_radii[i]
#             radius = prop['radius']
#             # if radius < 0.35 and scoring_function[int(x), int(y), int(z), 5] = 1:
#             #     scoring_function[int(x), int(y), int(z), 5] = 0
#             # if radius < implausible_threshold:
#             #     radius_threshold_score_fn(scoring_function, radius, x, y, z)
#             prop['length'] = 2 * update_length(prop['radius'], parent_radius, particle_list=main_particle_list)  # 2x upsampled
#             # prop['velocity'] = normalise_vector(weight[i] * parent_velocity + (1 - weight[i]) * np.random.standard_normal((3, 1)))
#             prop['velocity'] = normalise_vector(
#                 weight[i] * parent_velocity + (1 - weight[i]) * np.random.standard_normal((3,)))
#             props.append(prop)
#     # print(f'OVERALL PROPERTY LIST FOR SPECIFIC BRANCH POINT (1, 2, 3 ETC DEPENDANT ON HOW MANY BRANCHES SET: {props}')
#     return props

#
# def constrain_angles(i, location, parent_radius, daughter_radii, angles, scoring_function,  radius_threshold, realistic_angles_parameter):
#     x, y, z = location
#     if random.random() <= realistic_angles_parameter:  # generate invalid angles based on the the parameter
#         cos_theta_l, cos_theta_r = calculate_cosines(parent_radius, daughter_radii, i)
#         # print(f'cos_theta_l: {cos_theta_l}, cos_theta_r: {cos_theta_r}')
#         if -1 <= cos_theta_l <= 1 and -1 <= cos_theta_r <= 1:
#             theta_l = np.arccos(cos_theta_l)
#             theta_r = np.arccos(cos_theta_r)
#             print(f'Angles between the paired vessels are: angle l: {np.degrees(theta_l):.2f}° and angle r: {np.degrees(theta_r):.2f}° with daughter radii: {daughter_radii[i]} and {daughter_radii[i + 1]}')
#             # print('Angles between the paired vessels are: angle l:' + str(theta_l) + ' angle r:' + str(theta_r) + ' with daughter radii:' + str(daughter_radii[i]) + ' and ' + str(daughter_radii[i + 1]))
#             return (theta_l, theta_r)
#         else:
#             print('Invalid angles found (not -1 <= cos_theta_l <= 1 and -1 <= cos_theta_r <= 1). Providing empty angle list.')
#             return None
#
#     else: #Generate unrealistic angles
#         print(f'Generating unrealistic angles for pair of vessels')
#         realistic_cos_theta_l, realistic_cos_theta_r = calculate_cosines(parent_radius, daughter_radii, i)
#         if -1 <= realistic_cos_theta_l <= 1 and -1 <= realistic_cos_theta_r <= 1: #Generate realistic angles for the vessels, to then generate unrealistic vessels and score differences
#             realistic_theta_l = np.arccos(realistic_cos_theta_l)
#             realistic_theta_r = np.arccos(realistic_cos_theta_r)
#             print(f'Realistic angles between the paired vessels are: angle l: {realistic_theta_l} and angle r: {realistic_theta_r} with daughter radii: {daughter_radii[i]} and {daughter_radii[i + 1]}')
#
#             print(f'Realistic angles between the paired vessels are: angle l: {np.degrees(realistic_theta_l):.2f}° and angle r: {np.degrees(realistic_theta_r):.2f}° with daughter radii: {daughter_radii[i]} and {daughter_radii[i + 1]}')
#             print(f'Generating unrealistic angles that do not obey Murrays laws (still within 0 to 180 degrees as cosine between -1 and 1.)')
#             cos_theta_l = random.uniform(-1, 1)  # should i make this slighly less than 1 or -1 so not directly inline with original parent vessel? # Avoid exactly -1 or 1 to prevent undefined behavior in arccos
#             cos_theta_r = random.uniform(-1, 1)
#             theta_l = np.arccos(cos_theta_l)
#             theta_r = np.arccos(cos_theta_r)
#
#             if (cos_theta_l != realistic_cos_theta_l) or (cos_theta_r != realistic_cos_theta_r):
#                 if daughter_radii[i] and daughter_radii[i + 1] > radius_threshold: #Only produce if within the radius threshold
#                     # cos_theta_l and cos_theta_r could feasibly be between 0 and 180 degrees (0 or pi).
#                     #print(f'Realistic angle values are: {realistic_cos_theta_l} and {realistic_cos_theta_r}. {realistic_theta_l} and {realistic_theta_r}  ')
#                     #print(f'Angle values are outside of range for plausibility: {theta_l} and {theta_r}  and radii are within threshold: {daughter_radii[i]} and {daughter_radii[i + 1]}, adding score to unrealistic angle score img')
#                     #print(f'Realistic angle cosines are: {np.degrees(realistic_cos_theta_l):.2f}° and {np.degrees(realistic_cos_theta_r):.2f}°.')
#                     print(f'Implausible angles detected: {theta_l} and {theta_r} with radii: {daughter_radii[i]}, {daughter_radii[i + 1]}, adding score to unrealistic angle score img')
#                     print(f'Implausible angles detected: {np.degrees(theta_l):.2f}° and {np.degrees(theta_r):.2f}° with radii: {daughter_radii[i]}, {daughter_radii[i + 1]}, adding score to unrealistic angle score img')
#                     angle_constrained_score_fn(np.degrees(theta_l), np.degrees(theta_r), np.degrees(realistic_theta_l), np.degrees(realistic_theta_r),
#                                                scoring_function, x, y, z)
#                 else:
#                     print(
#                         f"Angle values are incorrect but don't save implausibility value as one (or more) of the radii will not be saved in image as below threshold.")
#                 # print(f'Angle values are outside of range for plausibility: {angles}, adding score to unrealistic angle score img')
#             return (theta_l, theta_r)
#         else:
#             print('Invalid angles (not -1 <= realistic_cos_theta_l <= 1 and -1 <= realistic_cos_theta_r <= 1)  found. Providing empty angle list.')
#             return None
