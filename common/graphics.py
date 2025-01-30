from pygame import (
    init,
    display,
    time,
    FULLSCREEN,
    KEYDOWN,
    K_ESCAPE,
    event,
    draw,
    Color,
    Surface,
    SRCALPHA,
    font,
    quit as pygame_quit,
)
from .config import *

init()

# Set up the drawing window
screen = display.set_mode((0, 0), FULLSCREEN)
screen_width, screen_height = display.get_surface().get_size()

field_width, field_height = screen_width, screen_height

surfaces_size = (
    field_width,
    field_height,
)

nearest_plant_surface = Surface(surfaces_size, SRCALPHA)
dumb_body_surface = Surface(surfaces_size, SRCALPHA)
circle_arrow_surface = Surface(surfaces_size, SRCALPHA)
smart_body_surface = Surface(surfaces_size, SRCALPHA)

font = font.Font("common/Courier New.ttf", FONT_SIZE)


def display_texts(text1, text2, text3):
    global \
        text_surface1, \
        text_rect1, \
        text_surface2, \
        text_rect2, \
        text_surface3, \
        text_rect3
    text_surface1 = font.render(text1, True, (255, 255, 255))
    text_rect1 = text_surface1.get_rect(
        center=(field_width / 2, field_height - 3 * FONT_SIZE)
    )
    text_surface2 = font.render(text2, True, (255, 255, 255))
    text_rect2 = text_surface2.get_rect(
        center=(field_width / 2, field_height - 2 * FONT_SIZE)
    )
    text_surface3 = font.render(text3, True, (255, 255, 255))
    text_rect3 = text_surface3.get_rect(
        center=(field_width / 2, field_height - FONT_SIZE)
    )


clock = time.Clock()
screen.fill(Color("black"))


def display_surfaces():
    clock.tick(FPS)

    screen.blit(nearest_plant_surface, SURFACE_CORNER)
    screen.blit(dumb_body_surface, SURFACE_CORNER)
    screen.blit(circle_arrow_surface, SURFACE_CORNER)
    screen.blit(smart_body_surface, SURFACE_CORNER)

    screen.blit(text_surface1, text_rect1)
    screen.blit(text_surface2, text_rect2)
    screen.blit(text_surface3, text_rect3)

    # Field borders
    draw.rect(
        screen,
        Color("black"),
        (0, 0, field_width, field_height),
        EVOLUTION_FIELD_OUTLINE_WIDTH,
    )

    display.flip()


def clear_surfaces():
    # Clear the surfaces
    nearest_plant_surface.fill((0, 0, 0, 0))
    dumb_body_surface.fill((0, 0, 0, 0))
    circle_arrow_surface.fill((0, 0, 0, 0))
    smart_body_surface.fill((0, 0, 0, 0))

    screen.fill(Color("black"))
