import pygame
from nested_gui import Nested
from GLOBAL import *

if __name__ == "__main__":

    window = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Preference")

    test = Nested(window, WIDTH, HEIGHT)
    test.gui()
    test.save()