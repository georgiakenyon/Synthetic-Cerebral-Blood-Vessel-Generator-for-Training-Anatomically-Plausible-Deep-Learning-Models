import argparse


def get_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('--N_ITERATIONS', type=int, default=5000, help='N_ITERATIONS')
    parser.add_argument('--N_ITERATIONS_SAVED', type=int, default=1000, help='Number of iterations to wait before saving')

    parser.add_argument('--IMAGE_SHAPE_X', type=int, default=520, help='Size of image (x coord)')
    parser.add_argument('--IMAGE_SHAPE_Y', type=int, default=622, help='Size of image (y coord)')
    parser.add_argument('--IMAGE_SHAPE_Z', type=int, default=520, help='Size of image (z coord)')

    parser.add_argument('--INITIAL_VESSEL_X_COORD', type=int, default=254, help='Starting x coordinate for largest parent vessel growth')
    parser.add_argument('--INITIAL_VESSEL_Y_COORD', type=int, default=342, help='Starting y coordinate for largest parent vessel growth')
    parser.add_argument('--INITIAL_VESSEL_Z_COORD', type=int, default=158, help='Starting z coordinate for largest parent vessel growth')

    parser.add_argument('--UPPER_STEPSIZE', type=float, default=0.5, help='UPPER STEPSIZE FOR RADIUS ABOVE 1')
    parser.add_argument('--LOWER_STEPSIZE', type=float, default=0.1, help='UPPER STEPSIZE FOR RADIUS ABOVE 1')

    parser.add_argument('--INITIAL_PARENT_RADIUS', type=int, default=5, help='INITIAL_PARENT_RADIUS')
    parser.add_argument('--VESSEL_REPULSION_RADIUS_LOWER', type=int, default=40, help='VESSEL_REPULSION_RADIUS_LOWER')
    parser.add_argument('--VESSEL_REPULSION_RADIUS_UPPER', type=int, default=70, help='VESSEL_REPULSION_RADIUS_UPPER')
    parser.add_argument('--VESSEL_REPULSION_STRENGTH', type=int, default=1000, help='VESSEL_REPULSION_STRENGTH')
    parser.add_argument('--BRAIN_REPULSION_RADIUS', type=int, default=5, help='BRAIN_REPULSION_RADIUS')
    parser.add_argument('--BRAIN_REPULSION_STRENGTH', type=int, default=1000, help='BRAIN_REPULSION_STRENGTH')
    parser.add_argument('--THRESHOLD', type=int, default=70, help='THRESHOLD')
    parser.add_argument('--LOWER_WIGGLE_RANGE', type=int, default=7, help='LOWER_WIGGLE_RANGE')
    parser.add_argument('--UPPER_WIGGLE_RANGE', type=int, default=11, help='UPPER_WIGGLE_RANGE')
    parser.add_argument('--RADIUS_THRESHOLD', type=float, default=0.2, help='RADIUS_THRESHOLD')
    parser.add_argument('--INITIAL_VESSEL_LENGTH_LOWER', type=int, default=44, help='INITIAL_VESSEL_LENGTH_LOWER')
    parser.add_argument('--INITIAL_VESSEL_LENGTH_UPPER', type=int, default=72, help='INITIAL_VESSEL_LENGTH_UPPER')
    #PLAUSIBLE VESSEL PARAMETERS
    parser.add_argument('--LOWER_LENGTH_RANGE_LOW_RADII', type=int, default=4, help='LOWER_LENGTH_RANGE_LOW_RADII')
    parser.add_argument('--UPPER_LENGTH_RANGE_LOW_RADII', type=int, default=7, help='UPPER_LENGTH_RANGE_LOW_RADII')
    parser.add_argument('--LOWER_LENGTH_RANGE_HIGH_RADII', type=int, default=7, help='LOWER_LENGTH_RANGE_HIGH_RADII')
    parser.add_argument('--UPPER_LENGTH_RANGE_HIGH_RADII', type=int, default=12, help='UPPER_LENGTH_RANGE_HIGH_RADII')
    parser.add_argument('--UNCONTINUOUS_PARAMETER', type=float, default=1.0, help='UNCONTINUOUS_PARAMETER') #1 = CONTINUOUS
    parser.add_argument('--BIFURCATION_TRIFURCATION_TOTAL_PROB', type=float, default=1.0, help='BIFURCATION_TRIFURCATION_TOTAL_PROB') #1 = NO IMPLAUSIBLE BRANCH NUMBERS
    parser.add_argument('--UNREALISTIC_BRANCHING_RANGE_LOWER', type=int, default=4, help='UNREALISTIC_BRANCHING_RANGE_LOWER')
    parser.add_argument('--UNREALISTIC_BRANCHING_RANGE_UPPER', type=int, default=10, help='UNREALISTIC_BRANCHING_RANGE_UPPER')
    parser.add_argument('--REALISTIC_ANGLES_PARAMETER', type=float, default=1.0, help='REALISTIC_ANGLES_PARAMETER')  # 1 = REALISTIC ANGLES
    return parser.parse_args()

