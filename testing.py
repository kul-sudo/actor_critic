from for_testing.testing_config import *
import common.plants

common.plants.PLANT_SPAWN_PROBABILITY = PLANT_SPAWN_PROBABILITY
common.plants.MAX_N_PLANTS = MAX_N_PLANTS

import common.body

common.body.BODY_INITIAL_ENERGY = BODY_INITIAL_ENERGY
common.body.PLANT_ENERGY = PLANT_ENERGY

from common.graphics import (
    display_texts,
    surfaces_size,
    display_surfaces,
    clear_surfaces,
    smart_body_surface,
    dumb_body_surface,
)
from common.body import SmartBody, DumbBody
from common.plants import update_plants, new_plant, plants
from common.get_keys import *
from common.brains import Actor
from torch import load

current_life_duration = 0
lives_n = 1
dumb_bodies = []
dumb_bodies_death_n = 0

# Create the smart body
actor = Actor()
actor.load_state_dict(load(f"{MODELS_PATH}/{FNAME}.pt", weights_only=True))
actor.eval()
smart_body = SmartBody(smart_body_surface, 0, 0, actor)
smart_body.set_random_position()

# Spawn the plants
for _ in range(MAX_N_PLANTS):
    new_plant(1, smart_body)

# Create the dumb bodies
for _ in range(DUMB_BODIES_N):
    dumb_body = DumbBody(dumb_body_surface, 0, 0)
    dumb_body.set_random_position()
    dumb_bodies.append(dumb_body)


update_plants(smart_body)

# Testing
while True:
    get_keys()

    # One step for each dumb body
    for dumb_body in dumb_bodies:
        if dumb_body.dead:
            dumb_bodies_death_n += 1
            dumb_body.set_random_position()
            dumb_body.energy = BODY_INITIAL_ENERGY

        dumb_body.one_move()

    if smart_body.dead:  # If dead, move into a random position
        lives_n += 1
        current_life_duration = 0
        smart_body.energy = BODY_INITIAL_ENERGY
        smart_body.set_random_position()
        update_plants(smart_body)

    smart_body.one_move()
    current_life_duration += 1
    update_plants(smart_body)

    texts_to_display = (
        f"Currently: energy of smart body: {smart_body.energy}, {lives_n} lives, "
        f"duration: {current_life_duration}, {len(plants)} plants.",
        f"{dumb_bodies_death_n} deaths of dumb body(ies) | {lives_n - 1} deaths of smart body",
        "",
    )

    display_texts(*texts_to_display)

    display_surfaces()
    clear_surfaces()
