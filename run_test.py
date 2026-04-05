import pygame
from similarity_gui import SimilarityTest
from GLOBAL import *

if __name__ == "__main__":

    window = pygame.display.set_mode((WIDTH, HEIGHT))

    test = SimilarityTest(window, WIDTH, HEIGHT)
    test.play_self()