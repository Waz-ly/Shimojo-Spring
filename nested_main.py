import pygame
from nested_gui import Nested
from GLOBAL import *

if __name__ == "__main__":

    window = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Preference")

    mode = "near" #near vs far

    test = Nested(window, WIDTH, HEIGHT, mode)
    test.gui()
    test.save()