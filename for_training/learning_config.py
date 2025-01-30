GAMMA = 0.99
MIN_LEARNING_N_FOR_AUTOMATIC_TESTING = 20000
STEP_FOR_AUTOMATIC_TESTING = 10000  # Test every STEP_FOR_AUTOMATIC_TESTING training
MAX_TEST_STEPS = 35000
MAX_DEATHS_N = 6  # How many times the smart body is allowed to die during the first automatic testing
PATH = "auto/"  # Where to save the automatically created weights. The case when the directory doesn't exist isn't handled
MIN_DIRECTIONS_N = 3
MAX_BAD_LEARNING_N = 60000

# The effectiveness of the model depends on: body speed, energy for moving, vision distance, plant energy, screen size
MAX_N_PLANTS = 1200  # Choose a value that guarantees the smart body learns well
PLANT_SPAWN_PROBABILITY = 0.1

BODY_INITIAL_ENERGY = 200
PLANT_ENERGY = 15  # How much energy a plant gives when eaten
