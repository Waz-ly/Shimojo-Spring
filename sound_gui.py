import pygame
from sound_game import Game
from GLOBAL import *

class SoundGUI:
    def __init__(self, window, width, height, points):
        self.game = Game(window, width, height, points)

    # function used to play against one's self
    def play_self(self):
        clock = pygame.time.Clock()
        run = True
        pressed = False
        self.game.loop()

        while run:
            clock.tick(60)

            for event in pygame.event.get():

                if event.type == pygame.QUIT:

                    run = False
                    break

                elif event.type == pygame.MOUSEBUTTONDOWN:
                    
                    if (15 <= pygame.mouse.get_pos()[0] <= HEIGHT - 15
                        and 15 <= pygame.mouse.get_pos()[1] <= HEIGHT - 15):

                        self.game.new_selection_point(pygame.mouse.get_pos())
                
            self.game.loop()
            pygame.display.update()

        pygame.quit()