import pygame
from single_gui import ScoreTest
from GLOBAL import *

if __name__ == "__main__":

    window = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("familiarity")

    test = ScoreTest(window, WIDTH, HEIGHT)
    test.gui()
    test.save()