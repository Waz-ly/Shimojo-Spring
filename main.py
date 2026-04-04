import pygame
from Game import Game
import numpy as np
from GLOBAL import *

class SimilarityTest:
    def __init__(self, window, width, height):
        self.game = Game(window, width, height)
        self.lastMoves = []
        self.lastLastMoves = []

    def run_familiarity(self):
        clock = pygame.time.Clock()
        run = True
        gameInfo = self.game.loop(False, 0)

        while run:
            clock.tick(60)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    if (pygame.mouse.get_pos()[0] < NEXT_CENTER_X + NEXT_WIDTH//2
                        and pygame.mouse.get_pos()[1] < NEXT_CENTER_Y + NEXT_HEIGHT//2
                        and pygame.mouse.get_pos()[1] > NEXT_CENTER_Y - NEXT_HEIGHT//2
                        and pygame.mouse.get_pos()[0] > NEXT_CENTER_X - NEXT_WIDTH//2
                        and self.game.gameInfo.familiarity_completed):
                        
                        run = False
                        self.game.gameInfo.familiarity_ended = True
                        break

                    if (pygame.mouse.get_pos()[0] < BUTTON_C_X + BUTTON_SIZE
                        and pygame.mouse.get_pos()[1] < BUTTON_C_Y + BUTTON_SIZE
                        and pygame.mouse.get_pos()[1] > BUTTON_C_Y
                        and pygame.mouse.get_pos()[0] > BUTTON_C_X
                        and not self.game.gameInfo.familiarity_started):
                        
                        self.game.start_familiarity()

            gameInfo = self.game.loop(False, 0)

            pygame.display.update()

    def run_conditioning(self):
        clock = pygame.time.Clock()
        run = True
        gameInfo = self.game.loop(False, 0)

        while run:
            clock.tick(60)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    if (pygame.mouse.get_pos()[0] < NEXT_CENTER_X + NEXT_WIDTH//2
                        and pygame.mouse.get_pos()[1] < NEXT_CENTER_Y + NEXT_HEIGHT//2
                        and pygame.mouse.get_pos()[1] > NEXT_CENTER_Y - NEXT_HEIGHT//2
                        and pygame.mouse.get_pos()[0] > NEXT_CENTER_X - NEXT_WIDTH//2
                        and self.game.gameInfo.conditioning_completed):
                        
                        run = False
                        self.game.gameInfo.conditioning_ended = True
                        break

                    if (pygame.mouse.get_pos()[0] < BUTTON_C_X + BUTTON_SIZE
                        and pygame.mouse.get_pos()[1] < BUTTON_C_Y + BUTTON_SIZE
                        and pygame.mouse.get_pos()[1] > BUTTON_C_Y
                        and pygame.mouse.get_pos()[0] > BUTTON_C_X
                        and not self.game.gameInfo.conditioning_started):
                        
                        self.game.start_conditioning()

            gameInfo = self.game.loop(False, 0)

            pygame.display.update()

    def play_preference(self):
        self.game.gameInfo.preference = True

        self.run_familiarity()

        clock = pygame.time.Clock()
        run = True
        pressed = False
        gameInfo = self.game.loop2(False, 0)

        while run:
            clock.tick(60)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    run = False
                    break
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    if (pygame.mouse.get_pos()[0] < NEXT_CENTER2_X + NEXT_WIDTH//2
                        and pygame.mouse.get_pos()[1] < NEXT_CENTER2_Y + NEXT_HEIGHT//2
                        and pygame.mouse.get_pos()[1] > NEXT_CENTER2_Y - NEXT_HEIGHT//2
                        and pygame.mouse.get_pos()[0] > NEXT_CENTER2_X - NEXT_WIDTH//2):
                        
                        self.game.next_pair()

                    if (pygame.mouse.get_pos()[0] < BUTTON_A2_X + BUTTON_SIZE
                        and pygame.mouse.get_pos()[1] < BUTTON_A2_Y + BUTTON_SIZE
                        and pygame.mouse.get_pos()[1] > BUTTON_A2_Y
                        and pygame.mouse.get_pos()[0] > BUTTON_A2_X):
                        
                        self.game.play_A()

                    if (pygame.mouse.get_pos()[0] < BUTTON_B2_X + BUTTON_SIZE
                        and pygame.mouse.get_pos()[1] < BUTTON_B2_Y + BUTTON_SIZE
                        and pygame.mouse.get_pos()[1] > BUTTON_B2_Y
                        and pygame.mouse.get_pos()[0] > BUTTON_B2_X):

                        self.game.play_B()

                    if (pygame.mouse.get_pos()[0] < WIDTH//2 + SCALE_HEIGHT//2
                        and pygame.mouse.get_pos()[1] < SCALE_CENTER2 + SIMILARITY_INDICATOR_SIZE*2
                        and pygame.mouse.get_pos()[1] > SCALE_CENTER2 - SIMILARITY_INDICATOR_SIZE*2
                        and pygame.mouse.get_pos()[0] > WIDTH//2 - SCALE_HEIGHT//2):

                        pressed = True

                elif event.type == pygame.MOUSEBUTTONUP:
                    pressed = False
                
            gameInfo = self.game.loop2(pressed, pygame.mouse.get_pos()[0])

            if gameInfo.testing_completed:
                run = False
                break

            pygame.display.update()

        stimuli_modification = []
        stimuli_files = self.game.gameInfo.stimuli
        for file in stimuli_files:
            stimuli_modification.append(file[file.find('(')+1:file.find(')')])

        similarity_array_size = self.game.gameInfo.similarityArray.shape[0]

        output = np.empty((similarity_array_size + 1, similarity_array_size + 1), dtype=object)
        output[0, 0] = ""
        output[0, 1:] = stimuli_modification
        output[1:, 0] = stimuli_modification
        output[1:, 1:] = np.round(self.game.gameInfo.similarityArray, 2)

        np.savetxt('test.csv', output, fmt="%s", delimiter=',')

        pygame.quit()

    def play_simple_preference(self, preference=True):
        self.game.gameInfo.preference = preference

        self.run_familiarity()

        if not preference:
            self.run_conditioning()

        clock = pygame.time.Clock()
        run = True
        pressed = False
        gameInfo = self.game.loop3(False, 0)

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
                        and pygame.mouse.get_pos()[0] > NEXT_CENTER_X - NEXT_WIDTH//2
                        and ((gameInfo.listened and gameInfo.playing_original) or gameInfo.rated)):
                        
                        self.game.next_pair_simple()

                    if (pygame.mouse.get_pos()[0] < BUTTON_A_X + BUTTON_SIZE
                        and pygame.mouse.get_pos()[1] < BUTTON_A_Y + BUTTON_SIZE
                        and pygame.mouse.get_pos()[1] > BUTTON_A_Y
                        and pygame.mouse.get_pos()[0] > BUTTON_A_X):
                        
                        self.game.play_C()

                    if (pygame.mouse.get_pos()[0] < SCALE_X + SIMILARITY_INDICATOR_SIZE*2
                        and pygame.mouse.get_pos()[1] < HEIGHT//2 + SCALE_HEIGHT//2
                        and pygame.mouse.get_pos()[1] > HEIGHT//2 - SCALE_HEIGHT//2
                        and pygame.mouse.get_pos()[0] > SCALE_X - SIMILARITY_INDICATOR_SIZE*2):

                        pressed = True

                elif event.type == pygame.MOUSEBUTTONUP:
                    pressed = False
                
            gameInfo = self.game.loop3(pressed, pygame.mouse.get_pos()[1])

            if gameInfo.testing_completed:
                run = False
                break

            pygame.display.update()

        stimuli_modification = []
        stimuli_files = self.game.gameInfo.stimuli
        for file in stimuli_files:
            stimuli_modification.append(file[file.find('(')+1:file.find(')')])

        similarity_array_size = self.game.gameInfo.similarityArray.shape[0]

        output = np.empty((similarity_array_size + 1, similarity_array_size + 1), dtype=object)
        output[0, 0] = ""
        output[0, 1:] = stimuli_modification
        output[1:, 0] = stimuli_modification
        output[1:, 1:] = np.round(self.game.gameInfo.similarityArray, 2)

        np.savetxt('test.csv', output, fmt="%s", delimiter=',')

        pygame.quit()

    # function used to play against one's self
    def play_self(self):
        self.run_familiarity()
        self.run_conditioning()

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

                    if (pygame.mouse.get_pos()[0] < BUTTON_B_X + BUTTON_SIZE
                        and pygame.mouse.get_pos()[1] < BUTTON_B_Y + BUTTON_SIZE
                        and pygame.mouse.get_pos()[1] > BUTTON_B_Y
                        and pygame.mouse.get_pos()[0] > BUTTON_B_X):

                        self.game.play_B()

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

        stimuli_modification = []
        stimuli_files = self.game.gameInfo.stimuli
        for file in stimuli_files:
            stimuli_modification.append(file[file.find('(')+1:file.find(')')])

        similarity_array_size = self.game.gameInfo.similarityArray.shape[0]

        output = np.empty((similarity_array_size + 1, similarity_array_size + 1), dtype=object)
        output[0, 0] = ""
        output[0, 1:] = stimuli_modification
        output[1:, 0] = stimuli_modification
        output[1:, 1:] = np.round(self.game.gameInfo.similarityArray, 2)

        np.savetxt('test.csv', output, fmt="%s", delimiter=',')

        pygame.quit()