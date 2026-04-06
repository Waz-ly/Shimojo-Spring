import numpy as np
import pygame
import os
from GLOBAL import *
import random
from copy import deepcopy

pygame.init()

class GameInformation:
    def __init__(self):
        self.stimuli = []
        for f in os.listdir("stimuli"):
            if not f[0] == '.':
                self.stimuli.append("stimuli/" + f)
        num_stimuli = len(self.stimuli)

        self.songOrder = []

        for i in range(num_stimuli):
            for j in range(i):
                self.songOrder.append([i, j])
                random.shuffle(self.songOrder[-1])

        random.shuffle(self.songOrder)

        self.testing_completed = False
        self.pair_number = 0
        self.similarityArray = np.zeros((num_stimuli, num_stimuli))
        self.similarityScore = SENTIMENT_INITIAL

        self.started_listening = False
        self.listened = False
        self.rated = False

        self.playing_A = False
        self.playing_B = False

class Game:
    def __init__(self, window, width, height):
        self.width = width
        self.height = height
        self.window = window

        self.gameInfo = GameInformation()
        self.whitesTurn = True

        pygame.mixer.init()

    def additional_mode(self, original_labels):
        try:
            results = np.loadtxt('additional_results.csv', delimiter=',', dtype=str)
            labels = results[11:,0]
        except:
            labels = []
    
        self.gameInfo.stimuli = deepcopy(original_labels)
        for f in os.listdir("additional_stimuli"):
            if not f[0] == '.' and not os.path.splitext(f)[0] in labels:
                self.gameInfo.stimuli.append("additional_stimuli/" + f)

        self.gameInfo.songOrder = []

        for i in np.arange(len(original_labels)):
            for j in np.arange(len(self.gameInfo.stimuli) - len(original_labels)):
                self.gameInfo.songOrder.append([i, j + len(original_labels)])
                random.shuffle(self.gameInfo.songOrder[-1])

        random.shuffle(self.gameInfo.songOrder)

        self.gameInfo.similarityArray = np.zeros((len(self.gameInfo.stimuli), len(self.gameInfo.stimuli)))

    def draw(self):
        self.window.fill(BLACK)

        if self.gameInfo.playing_A:
            button_A_file = 'pause.webp'
        else:
            button_A_file = 'play.webp'

        button_A_image = pygame.image.load(os.path.join('assets', button_A_file))
        button_A_image = pygame.transform.scale(button_A_image, (BUTTON_SIZE, BUTTON_SIZE))
        self.window.blit(button_A_image, (BUTTON_A_X, BUTTON_A_Y))
        
        if self.gameInfo.playing_B:
            button_B_file = 'pause.webp'
        else:
            button_B_file = 'play.webp'

        button_B_image = pygame.image.load(os.path.join('assets', button_B_file))
        button_B_image = pygame.transform.scale(button_B_image, (BUTTON_SIZE, BUTTON_SIZE))
        self.window.blit(button_B_image, (BUTTON_B_X, BUTTON_A_Y))

        if self.gameInfo.rated:
            pygame.draw.rect(self.window, WHITE, (NEXT_BOX_X, NEXT_BOX_Y, NEXT_WIDTH, NEXT_HEIGHT))
            pygame.draw.rect(self.window, BLACK, (NEXT_BOX_X + 5, NEXT_BOX_Y + 5, NEXT_WIDTH - 10, NEXT_HEIGHT - 10))
            LARGE_FONT.render_to(self.window, (NEXT_TEXT_X, NEXT_TEXT_Y), f"next", WHITE)

        SMALL_FONT.render_to(self.window, (EXPERIMENT_TEXT_X, EXPERIMENT_TEXT_Y1), f"Click the play buttons to listen to the stimuli.", WHITE)
        SMALL_FONT.render_to(self.window, (EXPERIMENT_TEXT_X, EXPERIMENT_TEXT_Y2), f"Move the slider on the right based on the stimuli's similarity.", WHITE)
        SMALL_FONT.render_to(self.window, (EXPERIMENT_TEXT_X, EXPERIMENT_TEXT_Y3), f"Click next when complete. Try to use the full range of the scale.", WHITE)

        # scale
        pygame.draw.rect(self.window, WHITE, (SCALE_X, SCALE_Y, SCALE_WIDTH, SCALE_HEIGHT))

        for i in range(SENTIMENT_OPTIONS):
            tab_center = self.height//2 - (i-SENTIMENT_OPTIONS//2)*SCALE_HEIGHT//(SENTIMENT_OPTIONS-1)

            tab_y = tab_center - TAB_HEIGHT//2
            text_y = tab_center - SMALL_FONT_SIZE//2

            pygame.draw.rect(self.window, WHITE, (TAB_X, tab_y, TAB_WIDTH, TAB_HEIGHT))

            SMALL_FONT.render_to(self.window, (SCALE_NUMBER_X, text_y), f'{i+1}', WHITE)

        pygame.draw.circle(self.window, WHITE,
                           (SCALE_CENTER, self.height//2 - (self.gameInfo.similarityScore-5)*SCALE_HEIGHT//(SENTIMENT_OPTIONS-1)),
                           SIMILARITY_INDICATOR_SIZE)

        SMALL_FONT.render_to(self.window, (SCALE_LABEL_X, SCALE_LABEL_Y_1), f"most similar", WHITE)
        SMALL_FONT.render_to(self.window, (SCALE_LABEL_X, SCALE_LABEL_Y_2), f"least similar", WHITE)

        LARGE_FONT.render_to(self.window, (20, 10), f"{self.gameInfo.pair_number}", WHITE)

    def loop(self, mouse_pressed, mouse_pos):
        if mouse_pressed:
            self.gameInfo.similarityScore = max(min((self.height//2 - mouse_pos)*(SENTIMENT_OPTIONS-1)/SCALE_HEIGHT + 5, 9), 1)
            self.gameInfo.rated = True

        if not pygame.mixer.music.get_busy():
            self.gameInfo.playing_A = False
            self.gameInfo.playing_B = False

        self.draw()

        return self.gameInfo
 
    def next_pair(self):
        if not self.gameInfo.rated:
            return None

        self.gameInfo.rated = False
        pygame.mixer.music.stop()

        song_pair = self.gameInfo.songOrder[self.gameInfo.pair_number]
        self.gameInfo.similarityArray[song_pair[0], song_pair[1]] = self.gameInfo.similarityScore
        self.gameInfo.similarityArray[song_pair[1], song_pair[0]] = self.gameInfo.similarityScore

        self.gameInfo.similarityScore = SENTIMENT_INITIAL
        self.gameInfo.pair_number += 1

        # check game end
        if self.gameInfo.pair_number >= len(self.gameInfo.songOrder):
            self.gameInfo.testing_completed = True

    def play_A(self):
        pygame.mixer.music.load(self.gameInfo.stimuli[self.gameInfo.songOrder[self.gameInfo.pair_number][0]])
        pygame.mixer.music.set_volume(0.7)
        pygame.mixer.music.play()

        if self.gameInfo.playing_A:
            pygame.mixer.music.stop()

        self.gameInfo.playing_A = True
        self.gameInfo.playing_B = False
    
    def play_B(self):
        pygame.mixer.music.load(self.gameInfo.stimuli[self.gameInfo.songOrder[self.gameInfo.pair_number][1]])
        pygame.mixer.music.set_volume(0.7)
        pygame.mixer.music.play()

        if self.gameInfo.playing_B:
            pygame.mixer.music.stop()

        self.gameInfo.playing_B = True
        self.gameInfo.playing_A = False