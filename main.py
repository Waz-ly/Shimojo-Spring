import pygame
from Game import Game
import numpy as np
from GLOBAL import *

class SimilarityTest:
    def __init__(self, window, width, height):
        self.game = Game(window, width, height)
        self.lastMoves = []
        self.lastLastMoves = []

    # function used to play against one's self
    def play_self(self):
        clock = pygame.time.Clock()
        run = True
        pressed = False
        clicked = False
        moveMade = False
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

                    if (pygame.mouse.get_pos()[0] < BUTTON_B_X + BUTTON_SIZE
                        and pygame.mouse.get_pos()[1] < BUTTON_B_Y + BUTTON_SIZE
                        and pygame.mouse.get_pos()[1] > BUTTON_B_Y
                        and pygame.mouse.get_pos()[0] > BUTTON_B_X):

                        self.game.play_B()

                    if (pygame.mouse.get_pos()[0] < SCALE_X + SCALE_WIDTH
                        and pygame.mouse.get_pos()[1] < HEIGHT//2 - (self.game.gameInfo.similarityScore-5)*SCALE_HEIGHT//(SENTIMENT_OPTIONS-1) + SIMILARITY_INDICATOR_SIZE
                        and pygame.mouse.get_pos()[1] > HEIGHT//2 - (self.game.gameInfo.similarityScore-5)*SCALE_HEIGHT//(SENTIMENT_OPTIONS-1) - SIMILARITY_INDICATOR_SIZE
                        and pygame.mouse.get_pos()[0] > SCALE_X - SCALE_WIDTH):

                        pressed = True

                elif event.type == pygame.MOUSEBUTTONUP:
                    pressed = False
                
            gameInfo = self.game.loop(pressed, pygame.mouse.get_pos()[1])

            if gameInfo.testing_completed:
                run = False
                break

            pygame.display.update()

        stimuli_modification = []
        stimuli_files = self.game.gameInfo.stimuli
        for file in stimuli_files:
            stimuli_modification.append(file[file.find('(')+1:file.find(')')])

        output = np.empty((11, 11), dtype=object)
        output[0, 0] = ""
        output[0, 1:] = stimuli_modification
        output[1:, 0] = stimuli_modification
        output[1:, 1:] = np.round(self.game.gameInfo.similarityArray, 2)

        np.savetxt('test.csv', output, fmt="%s", delimiter=',')

        pygame.quit()