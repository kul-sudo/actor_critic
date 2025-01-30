from .config import *
from .plants import plants, get_nearest_plant
from .graphics import (
    circle_arrow_surface,
    surfaces_size,
)
from math import dist, pi, cos, sin
from random import uniform, random
from pygame import draw, Color
from torch import argmax, FloatTensor


class DumbBody:
    def __init__(self, body_surface, x, y):
        global base_color
        self.x = x
        self.y = y
        self.energy = BODY_INITIAL_ENERGY
        self.bounced = None  # Whether it bounced off a wall during the last step
        self.dead = False  # Whether it died during the last step
        self.angle = None  # By instinct
        self.color = Color("yellow")

        self.surface_width = surfaces_size[0]
        self.surface_height = surfaces_size[1]
        self.body_surface = body_surface

    def draw_body(self):
        draw.circle(  # The body itself
            self.body_surface, self.color, (self.x, self.y), BODY_RADIUS
        )

    def to_new_pos(self):
        self.bounced = False

        # Vertical walls
        new_x = self.x + BODY_SPEED * cos(self.angle)
        if self.x < BODY_RADIUS or self.x > self.surface_width - BODY_RADIUS:
            self.angle = pi - self.angle
            new_x = max(min(new_x, self.surface_width - BODY_RADIUS), BODY_RADIUS)
            self.bounced = True

        self.x = new_x

        # Horizontal walls
        new_y = self.y - BODY_SPEED * sin(self.angle)
        if self.y < BODY_RADIUS or self.y > self.surface_height - BODY_RADIUS:
            self.angle = -self.angle
            new_y = max(min(new_y, self.surface_height - BODY_RADIUS), BODY_RADIUS)
            self.bounced = True

        self.y = new_y

        # Eating
        for plant_id in plants:
            plant = plants[plant_id]
            if dist([self.x, self.y], [plant.x, plant.y]) < REACH_LENGTH:
                del plants[plant_id]
                self.energy += PLANT_ENERGY
                break

        # Energy
        self.energy -= ENERGY_FOR_MOVING
        self.dead = self.energy <= 0

        # Drawing
        self.draw_body()

    def one_move(self):
        if self.angle is None or random() <= CHANGE_INSTINCT_ANGLE_PROBABILITY:
            self.angle = uniform(0, 2 * pi)
        self.to_new_pos()

    def set_random_position(self):
        while True:
            self.x = uniform(BODY_RADIUS, self.surface_width - BODY_RADIUS)
            self.y = uniform(BODY_RADIUS, self.surface_height - BODY_RADIUS)
            if all(
                [
                    dist([self.x, self.y], [plant.x, plant.y]) > REACH_LENGTH
                    for plant in plants.values()
                ]
            ):
                return


class SmartBody(DumbBody):
    def __init__(self, body_surface, x, y, actor):
        super().__init__(body_surface, x, y)
        self.color = Color("deepskyblue")

        self.actor = actor

    def get_state(self):  # Get the state of what it sees
        nearest_plant = get_nearest_plant()  # The method is only called when there's a visible plant, so the variable can't be None
        # Prepare the data for the agent
        dx = nearest_plant.x - self.x
        dy = nearest_plant.y - self.y
        return FloatTensor([dx, dy])

    def one_move(self):
        nearest_plant = get_nearest_plant()
        state = self.get_state()
        q_values = self.actor(state)
        direction = argmax(
            q_values
        ).item()  # Choose the direction with the maximum weight
        self.angle = direction * ((2 * pi) / N_DIRECTIONS)
        self.to_new_pos()
        return direction, q_values[direction]

    def to_new_pos(self):
        super().to_new_pos()
        self.draw_arrow()

    def draw_arrow(self):  # Angle of movement
        arrow_end = [
            self.x + ARROW_LENGTH * cos(self.angle),
            self.y - ARROW_LENGTH * sin(self.angle),
        ]

        draw.line(
            circle_arrow_surface,
            Color("darkorchid1"),
            [self.x, self.y],
            arrow_end,
            ARROW_WIDTH,
        )

        arrowhead_point1 = (
            arrow_end[0] - ARROWHEAD_LENGTH * cos(-self.angle - ANGLE_RAD_HALF),
            arrow_end[1] - ARROWHEAD_LENGTH * sin(-self.angle - ANGLE_RAD_HALF),
        )
        arrowhead_point2 = (
            arrow_end[0] - ARROWHEAD_LENGTH * cos(-self.angle + ANGLE_RAD_HALF),
            arrow_end[1] - ARROWHEAD_LENGTH * sin(-self.angle + ANGLE_RAD_HALF),
        )
        draw.polygon(
            circle_arrow_surface,
            Color("darkorchid1"),
            [arrow_end, arrowhead_point1, arrowhead_point2],
        )
