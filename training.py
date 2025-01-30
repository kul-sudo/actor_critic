from for_training.learning_config import *
import common.plants

common.plants.PLANT_SPAWN_PROBABILITY = PLANT_SPAWN_PROBABILITY
common.plants.MAX_N_PLANTS = MAX_N_PLANTS

import common.body

common.body.BODY_INITIAL_ENERGY = BODY_INITIAL_ENERGY
common.body.PLANT_ENERGY = PLANT_ENERGY

from common.config import *
from common.graphics import (
    display_texts,
    display_surfaces,
    clear_surfaces,
    smart_body_surface,
)
from common.body import SmartBody
from common.plants import (
    plants,
    update_plants,
    new_plant,
    flip_plants,
)
from common.get_keys import *
from common.brains import Actor, Critic
from for_training.agent import Agent
from statistics import fmean
from math import inf
from torch import save


# Global
def initialize_global_var():
    global \
        body, \
        agent, \
        lives_n, \
        current_life_duration, \
        life_durations, \
        last_learning_n_tested, \
        learning_n, \
        max_deaths_n, \
        saved

    body = SmartBody(smart_body_surface, 0, 0, Actor())
    body.set_random_position()
    agent = Agent(body.actor)
    lives_n = 1  # Current life
    current_life_duration = 0  # Ticks since the beginning of the current life
    life_durations = []  # The durations of the previous lives
    last_learning_n_tested = -1  # learning_n when the last automatic testing happened.
    learning_n = 0
    max_deaths_n = MAX_DEATHS_N
    saved = False


initialize_global_var()

test_on = False  # If a test is happening
test_on_request = False
attempts_n = 1

# Initial plant spawning
for _ in range(MAX_N_PLANTS):
    new_plant(1, body)

update_plants(body)

while True:
    if body.bounced or body.dead:
        if not test_on:
            flip_plants()

        body.set_random_position()  # Makes the learning process more effective by avoiding moving around the same place
        update_plants(body)

    # Handle the key presses
    match get_keys():
        case Keys.save_model:
            save(body.actor.state_dict(), "actor.pt")
        case Keys.test_toggle:
            test_on = not test_on
            if test_on:
                test_on_request = True
                deaths_n = 0
                directions = set()

    # Whether it's time for automatic testing
    if (
        learning_n >= MIN_LEARNING_N_FOR_AUTOMATIC_TESTING
        and (learning_n - MIN_LEARNING_N_FOR_AUTOMATIC_TESTING)
        % STEP_FOR_AUTOMATIC_TESTING
        == 0
        and learning_n != last_learning_n_tested
    ):
        test_on = True
        test_on_request = False
        testing_step = 0
        deaths_n = 0
        last_learning_n_tested = learning_n
        directions = set()

    # Testing
    if test_on:
        direction, _ = body.one_move()
        directions.add(direction)
        update_plants(body)
        if not test_on_request:
            if testing_step == MAX_TEST_STEPS:  # The test is successful
                save(
                    body.actor.state_dict(),
                    f"{PATH}{attempts_n}-{learning_n}-{deaths_n}.pt",
                )
                saved = True
                max_deaths_n = deaths_n
                test_on = False
                continue

            testing_step += 1
    else:
        energy_before_move = body.energy
        state = body.get_state()
        _, weight = body.one_move()
        update_plants(body)
        next_state = None if body.bounced else body.get_state()
        reward = body.energy - energy_before_move
        agent.train(state, weight, next_state, reward)
        learning_n += 1

    # Display the info
    current_life_duration += 1
    if test_on:
        if test_on_request:
            test_text = "A test is on."
        else:
            test_text = (
                f"Automatic testing. Step: {testing_step}, maximum: {MAX_TEST_STEPS}."
            )
        texts_to_display = (
            test_text + f" Current energy: {body.energy}, {len(plants)} plants.",
            f"Current life: number {deaths_n + 1}"
            + ("." if test_on_request else f" (maximum lives {max_deaths_n + 1})."),
            "",
        )

    else:
        texts_to_display = (
            f"{lives_n} lives.",
            f"Life duration: {current_life_duration}. {len(plants)} plants."
            f" {learning_n} fits.",
            (
                ""
                if lives_n == 1
                else f"Average duration of previous lives: {average_life_duration}."
            ),
        )
    display_texts(*texts_to_display)

    display_surfaces()
    clear_surfaces()

    # Death
    if body.dead:
        body.energy = BODY_INITIAL_ENERGY  # Born again
        life_durations.append(current_life_duration)
        average_life_duration = round(fmean(life_durations))
        current_life_duration = 0
        lives_n += 1
        if test_on:
            deaths_n += 1
            if not test_on_request:
                if deaths_n == max_deaths_n + 1:  # Unsuccessful
                    if (
                        len(directions) <= MIN_DIRECTIONS_N
                        or not saved
                        and learning_n >= MAX_BAD_LEARNING_N
                    ):
                        initialize_global_var()
                        update_plants(body)
                        attempts_n += 1
                    test_on = False
