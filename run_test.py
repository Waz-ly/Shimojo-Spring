import pygame
from main import SimilarityTest
from GLOBAL import *

window = pygame.display.set_mode((WIDTH, HEIGHT))

test = SimilarityTest(window, WIDTH, HEIGHT)
test.play_self()