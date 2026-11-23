# physics constants
UNIVERSAL_GRAVITATIONAL_CONSTANT = 6.67430e-11
MASS_OF_SUN = 1.9885e30

# game constants
FPS = 60
SIMULATION_TIME_SCALE = 3 * 86400.0  # simulated seconds per real second 

ORIGIN_X = 0 # Sun position
ORIGIN_Y = 0

BASE_BODY_SCALE_DOWN = 3e5  # reference body scale used for the configured display diameters.
BODY_SCALE_DOWN = BASE_BODY_SCALE_DOWN  # current body scale. zoom changes this value.
ZOOM_BODY_SCALE = 1e4 # amount by which BODY_SCALE_DOWN changes on a zoom
TARGET_BODY_SCALE_DOWN = BODY_SCALE_DOWN # keep changing the scale till it is equal to the target so that zooming is smooth

DISTANCE_FROM_SUN_SCALE = 1e9 # distance of a planet from sun is divided by this
ZOOM_DISTANCE_FROM_SUN_SCALE = 1e8 # amount by which DISTANCE_FROM_SUN_SCALE changes on a zoom
TARGET_DISTANCE_FROM_SUN_SCALE = DISTANCE_FROM_SUN_SCALE # keep changing the scale till it is equal to the target so that zooming is smooth

DRAG_FACTOR = DISTANCE_FROM_SUN_SCALE # amount by which origin (sun poisition) is shifted on a drag
ZOOM_DRAG_FACTOR = ZOOM_DISTANCE_FROM_SUN_SCALE
TARGET_DRAG_FACTOR = DRAG_FACTOR # keep chaning the drag factor till it is equal to the target so that zooming is smooth

ZOOM_SMOOTHING_RATE = 10.0  # easing speed per second; higher values reach the target faster

MAX_DEQUE_POINTS_FOR_TRACE = 20000