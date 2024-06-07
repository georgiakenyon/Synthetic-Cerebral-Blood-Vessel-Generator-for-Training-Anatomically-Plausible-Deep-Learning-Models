import numpy as np
# ----------------------------------------------------------------------------------------------------------
#                                SCORING FUNCTIONS (ONE HOT ENCODED ARRAY)
# ----------------------------------------------------------------------------------------------------------

def branching_score_fn(scoring_function, x, y, z, num_branches, parent_radius):
    """Set the branching score to number of branches * radius if the radius is above a threshold."""
    scoring_function[int(x), int(y), int(z), 0] = num_branches #* parent_radius

def radius_threshold_score_fn(scoring_function, x, y, z, radius):
    """Mark radius below a threshold in the scoring function."""
    scoring_function[int(x), int(y), int(z), 1] = 1
    print(f'Scoring where the radius ({radius}) is below the threshold at location [{x}, {y}, {z}]')

def uncontinuous_score_fn(scoring_function, x, y, z, radius):  # UNCONTINUOUS_SCORE_FN is within draw_image function (scoring_function[int(x), int(y), int(z), 2] = 1)
    """Flag uncontinuous regions in the scoring function."""
    scoring_function[int(x), int(y), int(z), 2] = 1
    # print(f'Score function found implausible voxel due to gaps at location: {int(x), int(y), int(z)} and allocated a value of radius {radius}')

def overlapping_score_fn(scoring_function, x, y, z):
    """Increment the overlap score at a given location."""
    scoring_function[int(x), int(y), int(z), 3] += 1

def length_radius_ratio_score_fn(scoring_function, lr, realistic_upper_lr, realistic_lower_lr, particle_list):
    """Score particles based on length to radius ratio being outside realistic bounds."""
    if lr > realistic_upper_lr or lr < realistic_lower_lr:
        for part in particle_list:
            x, y, z = part['location']
            scoring_function[int(x), int(y), int(z), 4] = 1

def angle_constrained_score_fn(theta_l, theta_r, realistic_theta_l, realistic_theta_r, scoring_function, x, y, z):
    """Score implausible angles based on how far they deviate from realistic angles."""
    deviation_l = abs(theta_l - realistic_theta_l)
    deviation_r = abs(theta_r - realistic_theta_r)

    score_l = deviation_l / 180
    score_r = deviation_r / 180

    average_score = (score_l + score_r) / 2

    print(f'Implausibility scores are: {score_l} and {score_r}')
    print(f'Average score: {average_score}')
    # Apply scores to a scoring function
    scoring_function[int(x), int(y), int(z), 5] += average_score
