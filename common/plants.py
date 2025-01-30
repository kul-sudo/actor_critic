from .config import *
from .graphics import surfaces_size, screen, nearest_plant_surface
from random import random, uniform, choice
from math import dist
from pygame import draw, Color


class Plant:
    def __init__(self, x, y):
        self.x = x
        self.y = y


plants = {}
total_plants_n = 0
nearest_plant = None


def get_nearest_plant():
    global nearest_plant
    return nearest_plant


def new_plant(probability, body):
    global total_plants_n
    if (len(plants) == MAX_N_PLANTS or random() > probability) and len(plants) != 0:
        return
    while True:
        centre_x = uniform(PLANT_SIDE / 2, surfaces_size[0] - PLANT_SIDE / 2)
        centre_y = uniform(PLANT_SIDE / 2, surfaces_size[1] - PLANT_SIDE / 2)
        if dist([centre_x, centre_y], [body.x, body.y]) > REACH_LENGTH:
            # If a plant is put right on the body, it is unclear how the learning
            # process will be affected
            plants[total_plants_n] = Plant(centre_x, centre_y)
            total_plants_n += 1
            return


def draw_plant(plant, surface, color):
    bottom_left_x = plant.x - PLANT_SIDE / 2
    bottom_left_y = plant.y - PLANT_SIDE / 2
    draw.rect(surface, color, (bottom_left_x, bottom_left_y, PLANT_SIDE, PLANT_SIDE))


def update_plants(body):
    global nearest_plant
    new_plant(PLANT_SPAWN_PROBABILITY, body)
    nearest_plant = None
    min_dist = float("inf")
    for plant in plants.values():
        d = dist([body.x, body.y], [plant.x, plant.y])
        if d < min_dist:
            if nearest_plant is not None:
                draw_plant(nearest_plant, screen, Color("green"))
            nearest_plant = plant
            min_dist = d
        else:
            draw_plant(plant, screen, Color("green"))
    draw_plant(nearest_plant, nearest_plant_surface, Color("red"))


def flip_plants():  # Flip either horizontally or vertically
    if choice((True, False)):
        for plant in plants.values():
            plant.x = surfaces_size[0] - plant.x
    else:
        for plant in plants.values():
            plant.y = surfaces_size[1] - plant.y
