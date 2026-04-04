import pygame
from main import SimilarityTest
from GLOBAL import *

window = pygame.display.set_mode((WIDTH, HEIGHT))

# for similarity set to False, for preference set to true
preference = True

test = SimilarityTest(window, WIDTH, HEIGHT)
test.play_simple_preference(preference)