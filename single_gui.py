import pygame
from single_game import Game
import numpy as np
from GLOBAL import *
import os

class ScoreTest:
    def __init__(self, window, width, height):
        self.game = Game(window, width, height)

    def gui(self):
        clock = pygame.time.Clock()
        run = True
        pressed = False
        gameInfo = self.game.loop(False, 0)

        while run:
            clock.tick(60)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    run = False
                    break
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    if (pygame.mouse.get_pos()[0] < NEXT_CENTER_X + NEXT_WIDTH//2
                        and pygame.mouse.get_pos()[1] < NEXT_CENTER_Y + NEXT_HEIGHT//2
                        and pygame.mouse.get_pos()[1] > NEXT_CENTER_Y - NEXT_HEIGHT//2
                        and pygame.mouse.get_pos()[0] > NEXT_CENTER_X - NEXT_WIDTH//2):
                        
                        self.game.next_pair()

                    if (pygame.mouse.get_pos()[0] < BUTTON_A_X + BUTTON_SIZE
                        and pygame.mouse.get_pos()[1] < BUTTON_A_Y + BUTTON_SIZE
                        and pygame.mouse.get_pos()[1] > BUTTON_A_Y
                        and pygame.mouse.get_pos()[0] > BUTTON_A_X):
                        
                        self.game.play_A()

                    if (pygame.mouse.get_pos()[0] < SCALE_X + SIMILARITY_INDICATOR_SIZE*2
                        and pygame.mouse.get_pos()[1] < HEIGHT//2 + SCALE_HEIGHT//2
                        and pygame.mouse.get_pos()[1] > HEIGHT//2 - SCALE_HEIGHT//2
                        and pygame.mouse.get_pos()[0] > SCALE_X - SIMILARITY_INDICATOR_SIZE*2):

                        pressed = True

                elif event.type == pygame.MOUSEBUTTONUP:
                    pressed = False
                
            gameInfo = self.game.loop(pressed, pygame.mouse.get_pos()[1])

            if gameInfo.testing_completed:
                run = False
                break

            pygame.display.update()

    def save(self):
        stimuli_modification = []
        stimuli_files = self.game.gameInfo.stimuli
        for file in stimuli_files:
            file_name = os.path.basename(file)
            file_name = os.path.splitext(file_name)[0]

            stimuli_modification.append(file_name)
        
        similarity_array_size = self.game.gameInfo.similarityArray.shape[0]

        output = np.empty((2, similarity_array_size + 1), dtype=object)
        output[0, 0] = ""
        output[0, 1:] = stimuli_modification
        output[1, 1:] = np.round(self.game.gameInfo.similarityArray, 2)

        np.savetxt('test.csv', output, fmt="%s", delimiter=',')

        pygame.quit()