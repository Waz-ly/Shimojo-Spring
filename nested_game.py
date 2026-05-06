import numpy as np
import pygame
import os
from GLOBAL import *
import random
from sound_main import calculate_MDS

pygame.init()

class GameInformation:
    def __init__(self, mode):
        mds, labels = calculate_MDS(plot=False)

        test_point = "harp"
        test_point_coords = mds[labels.tolist().index(test_point)]

        furthest_label = test_point
        furthest_coord = test_point_coords

        max_distance = 0
        if mode == "far":
            max_distance = 0.3
        elif mode == "near":
            max_distance = 0.25

        if mode == "far":
            for coord, label in zip(mds, labels):
                if np.linalg.norm(test_point_coords - coord) > np.linalg.norm(test_point_coords - furthest_coord):
                    furthest_coord = coord
                    furthest_label = label
        
        furthest_labels = []
        for coord, label in zip(mds, labels):
            if mode == "near" and furthest_label == label:
                continue

            if np.linalg.norm(furthest_coord - coord) < max_distance:
                furthest_labels.append(label)

        furthest_labels.append(test_point)

        self.stimuli = []
        for label in furthest_labels:
            print(label)
            if os.path.isfile("stimuli/" + label + ".wav"):
                self.stimuli.append("stimuli/" + label + ".wav")
            elif os.path.isfile("stimuli/" + label + ".mp3"):
                self.stimuli.append("stimuli/" + label + ".mp3")
            elif os.path.isfile("stimuli_additional1/" + label + ".wav"):
                self.stimuli.append("stimuli_additional1/" + label + ".wav")
            elif os.path.isfile("stimuli_additional1/" + label + ".mp3"):
                self.stimuli.append("stimuli_additional1/" + label + ".mp3")
            else:
                raise Exception("stimuli not found")
            
        num_stimuli = len(self.stimuli)

        self.songOrder = []
        for i in range(len(self.stimuli) - 1):
            self.songOrder.append(i)
        random.shuffle(self.songOrder)
        self.songOrder.append(len(self.stimuli) - 1)

        self.testing_completed = False
        self.song_number = 0
        self.similarityArray = np.zeros(num_stimuli)
        self.similarityScore = SENTIMENT_INITIAL

        self.started_listening = False
        self.listened = False
        self.rated = False

        self.playing_A = False
        self.playing_B = False

class Game:
    def __init__(self, window, width, height, mode):
        self.width = width
        self.height = height
        self.window = window

        self.gameInfo = GameInformation(mode)

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

        if self.gameInfo.rated:
            pygame.draw.rect(self.window, WHITE, (NEXT_BOX_X, NEXT_BOX_Y, NEXT_WIDTH, NEXT_HEIGHT))
            pygame.draw.rect(self.window, BLACK, (NEXT_BOX_X + 5, NEXT_BOX_Y + 5, NEXT_WIDTH - 10, NEXT_HEIGHT - 10))
            LARGE_FONT.render_to(self.window, (NEXT_TEXT_X, NEXT_TEXT_Y), f"next", WHITE)

        SMALL_FONT.render_to(self.window, (EXPERIMENT_TEXT_X, EXPERIMENT_TEXT_Y1), f"Click the play buttons to listen to the stimuli.", WHITE)
        SMALL_FONT.render_to(self.window, (EXPERIMENT_TEXT_X, EXPERIMENT_TEXT_Y2), f"Move the slider on the right based on the stimuli's *score*.", WHITE)
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

        SMALL_FONT.render_to(self.window, (SCALE_LABEL_X, SCALE_LABEL_Y_1), f"most ''", WHITE)
        SMALL_FONT.render_to(self.window, (SCALE_LABEL_X, SCALE_LABEL_Y_2), f"least ''", WHITE)

        LARGE_FONT.render_to(self.window, (20, 10), f"{self.gameInfo.song_number}", WHITE)

    def loop(self, mouse_pressed, mouse_pos):
        if mouse_pressed:
            self.gameInfo.similarityScore = max(min((self.height//2 - mouse_pos)*(SENTIMENT_OPTIONS-1)/SCALE_HEIGHT + 5, 9), 1)
            self.gameInfo.rated = True

        if not pygame.mixer.music.get_busy():
            self.gameInfo.playing_A = False

        self.draw()

        return self.gameInfo
 
    def next_pair(self):
        if not self.gameInfo.rated:
            return None

        self.gameInfo.rated = False
        pygame.mixer.music.stop()

        song_number = self.gameInfo.songOrder[self.gameInfo.song_number]
        self.gameInfo.similarityArray[song_number] = self.gameInfo.similarityScore

        self.gameInfo.similarityScore = SENTIMENT_INITIAL
        self.gameInfo.song_number += 1

        # check game end
        if self.gameInfo.song_number >= len(self.gameInfo.songOrder):
            self.gameInfo.testing_completed = True

    def play_A(self):
        pygame.mixer.music.load(self.gameInfo.stimuli[self.gameInfo.songOrder[self.gameInfo.song_number]])
        pygame.mixer.music.set_volume(0.7)
        pygame.mixer.music.play()

        if self.gameInfo.playing_A:
            pygame.mixer.music.stop()

        self.gameInfo.playing_A = True
        self.gameInfo.playing_B = False