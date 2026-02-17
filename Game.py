import numpy as np
import pygame
import os
from GLOBAL import *
import random

pygame.init()

class GameInformation:
    def __init__(self):
        self.stimuli = []
        for f in os.listdir("stimuli"):
            if not f[0] == '.':
                self.stimuli.append("stimuli/" + f)
        num_stimuli = len(self.stimuli)

        self.conditioning_completed = False

        self.conditioning_order = self.stimuli.copy()
        random.shuffle(self.conditioning_order)
        self.conditioning_order = self.conditioning_order[0:5]
        
        self.conditioning_number = 0

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

        self.playing_A = False
        self.playing_B = False
        self.playing_C = False

class Game:
    def __init__(self, window, width, height):
        self.width = width
        self.height = height
        self.window = window

        self.gameInfo = GameInformation()
        self.whitesTurn = True

        pygame.mixer.init()

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

        pygame.draw.rect(self.window, WHITE, (NEXT_BOX_X, NEXT_BOX_Y, NEXT_WIDTH, NEXT_HEIGHT))
        pygame.draw.rect(self.window, BLACK, (NEXT_BOX_X + 5, NEXT_BOX_Y + 5, NEXT_WIDTH - 10, NEXT_HEIGHT - 10))
        next_text = NEXT_FONT.render(f"next", 1, WHITE)
        self.window.blit(next_text, (NEXT_TEXT_X, NEXT_TEXT_Y))

        # scale
        pygame.draw.rect(self.window, WHITE, (SCALE_X, SCALE_Y, SCALE_WIDTH, SCALE_HEIGHT))

        for i in range(SENTIMENT_OPTIONS):
            tab_center = self.height//2 - (i-SENTIMENT_OPTIONS//2)*SCALE_HEIGHT//(SENTIMENT_OPTIONS-1)

            tab_y = tab_center - TAB_HEIGHT//2
            text_y = tab_center - TEXT_SIZE//2

            pygame.draw.rect(self.window, WHITE, (TAB_X, tab_y, TAB_WIDTH, TAB_HEIGHT))

            scale_level = SCALE_FONT.render(f'{i+1}', 1, WHITE)
            self.window.blit(scale_level, (SCALE_TEXT_X, text_y))

        pygame.draw.circle(self.window, WHITE,
                           (SCALE_CENTER, self.height//2 - (self.gameInfo.similarityScore-5)*SCALE_HEIGHT//(SENTIMENT_OPTIONS-1)),
                           SIMILARITY_INDICATOR_SIZE)

        scale_question = SCALE_FONT.render(f"on a scale of 1-9 how", 1, WHITE)
        self.window.blit(scale_question, (SCALE_QUESTION_X, SCALE_QUESTION_Y_1))

        scale_question = SCALE_FONT.render(f"similar are these songs?", 1, WHITE)
        self.window.blit(scale_question, (SCALE_QUESTION_X, SCALE_QUESTION_Y_2))

        counter = NEXT_FONT.render(f"{self.gameInfo.pair_number}", 1, WHITE)
        self.window.blit(counter, (20, 10))

    def draw_conditioning(self):
        self.window.fill(BLACK)

        if self.gameInfo.playing_C:
            button_C_file = 'pause.webp'
        else:
            button_C_file = 'play.webp'

        button_C_image = pygame.image.load(os.path.join('assets', button_C_file))
        button_C_image = pygame.transform.scale(button_C_image, (BUTTON_SIZE, BUTTON_SIZE))
        self.window.blit(button_C_image, (BUTTON_C_X, BUTTON_C_Y))

        pygame.draw.rect(self.window, WHITE, (NEXT_BOX_X, NEXT_BOX_Y, NEXT_WIDTH, NEXT_HEIGHT))
        pygame.draw.rect(self.window, BLACK, (NEXT_BOX_X + 5, NEXT_BOX_Y + 5, NEXT_WIDTH - 10, NEXT_HEIGHT - 10))
        next_text = NEXT_FONT.render(f"next", 1, WHITE)
        self.window.blit(next_text, (NEXT_TEXT_X, NEXT_TEXT_Y))

        conditioning_prompting1 = PROMPTING_FONT.render(f"in this experiment you will be rating the similarity", 1, WHITE)
        conditioning_prompting2 = PROMPTING_FONT.render(f"of songs on a scale of 1-9. First, listen to a few of", 1, WHITE)
        conditioning_prompting3 = PROMPTING_FONT.render(f"the songs to a sense of the range of songs you ", 1, WHITE)
        conditioning_prompting4 = PROMPTING_FONT.render(f"will be rating", 1, WHITE)
        self.window.blit(conditioning_prompting1, (PROMPTING_X, PROMPTING_Y1))
        self.window.blit(conditioning_prompting2, (PROMPTING_X, PROMPTING_Y2))
        self.window.blit(conditioning_prompting3, (PROMPTING_X, PROMPTING_Y3))
        self.window.blit(conditioning_prompting4, (PROMPTING_X, PROMPTING_Y4))

        counter = NEXT_FONT.render(f"{self.gameInfo.conditioning_number}", 1, WHITE)
        self.window.blit(counter, (20, 10))

    def loop(self, mouse_pressed, mouse_pos):
        if mouse_pressed:
            self.gameInfo.similarityScore = max(min((self.height//2 - mouse_pos)*(SENTIMENT_OPTIONS-1)/SCALE_HEIGHT + 5, 9), 1)

        if not pygame.mixer.music.get_busy():
            self.gameInfo.playing_A = False
            self.gameInfo.playing_B = False
            self.gameInfo.playing_C = False

        if not self.gameInfo.conditioning_completed:
            self.draw_conditioning()
        else:
            self.draw()

        return self.gameInfo
    
    def next_pair(self):
        pygame.mixer.music.stop()

        song_pair = self.gameInfo.songOrder[self.gameInfo.pair_number]
        self.gameInfo.similarityArray[song_pair[0], song_pair[1]] = self.gameInfo.similarityScore
        self.gameInfo.similarityArray[song_pair[1], song_pair[0]] = self.gameInfo.similarityScore

        self.gameInfo.similarityScore = SENTIMENT_INITIAL
        self.gameInfo.pair_number += 1

        # check game end
        if self.gameInfo.pair_number >= len(self.gameInfo.songOrder):
            self.gameInfo.testing_completed = True

    def next_conditioning(self):
        pygame.mixer.music.stop()

        self.gameInfo.conditioning_number += 1

        if self.gameInfo.conditioning_number >= len(self.gameInfo.conditioning_order):
            self.gameInfo.conditioning_completed = True

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

    def play_C(self):
        pygame.mixer.music.load(self.gameInfo.conditioning_order[self.gameInfo.conditioning_number])
        pygame.mixer.music.set_volume(0.7)
        pygame.mixer.music.play()

        if self.gameInfo.playing_C:
            pygame.mixer.music.stop()

        self.gameInfo.playing_C = True