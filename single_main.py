import pygame
from single_gui import ScoreTest
from GLOBAL import *

if __name__ == "__main__":

    keyword = "attractive"

    window = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption(keyword)

    test = ScoreTest(window, keyword, WIDTH, HEIGHT)
    test.gui()
    test.save()