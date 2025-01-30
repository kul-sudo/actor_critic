from pygame import (
    KEYDOWN,
    K_ESCAPE,
    KMOD_LCTRL,
    K_s,
    K_t,
    event,
    quit as pygame_quit,
)
from .config import *


class Keys:
    save_model = 0
    test_toggle = 1


def get_keys():
    for e in event.get():
        if e.type == KEYDOWN:
            if e.key == K_ESCAPE:
                pygame_quit()
                exit()
            elif e.key == KMOD_LCTRL | K_s:
                return Keys.save_model
            elif e.key == KMOD_LCTRL | K_t:
                return Keys.test_toggle
