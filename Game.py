import numpy as np
import pygame
import os
from GLOBAL import *
import random

pygame.init()

class GameInformation:
    def __init__(self):
        self.preference = False

        self.stimuli = ['stimuli/Bach_AI_Stimuli (original).wav']
        for f in os.listdir("stimuli"):
            if not f[0] == '.' and not f[0] == 'Bach_AI_Stimuli (original).wav':
                self.stimuli.append("stimuli/" + f)
        num_stimuli = len(self.stimuli)

        self.familiarity_started = False
        self.familiarity_completed = False
        self.familiarity_ended = False
        self.familiarity_number = 0

        self.conditioning_started = False
        self.conditioning_completed = False
        self.conditioning_ended = False
        self.conditioning_number = 0

        self.conditioning_order = self.stimuli[1:].copy()
        random.shuffle(self.conditioning_order)

        self.songOrder = []

        # for i in range(num_stimuli):
        #     for j in range(i):
        #         self.songOrder.append([i, j])
        #         random.shuffle(self.songOrder[-1])

        # random.shuffle(self.songOrder)

        for i in range(1, num_stimuli):
            self.songOrder.append([0, i])
            random.shuffle(self.songOrder[-1])

        random.shuffle(self.songOrder)

        self.simple_song_Order = []

        for i in range(1, num_stimuli):
            self.simple_song_Order.append([0, i])

        random.shuffle(self.simple_song_Order)

        self.testing_completed = False
        self.pair_number = 0
        self.similarityArray = np.zeros((num_stimuli, num_stimuli))
        self.similarityScore = SENTIMENT_INITIAL

        self.started_listening = False
        self.listened = False
        self.rated = False

        self.since_last_repeat = 0
        self.playing_original = False

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
        next_text = LARGE_FONT.render(f"next", 1, WHITE)
        self.window.blit(next_text, (NEXT_TEXT_X, NEXT_TEXT_Y))

        conditioning_prompting1 = SMALL_FONT.render(f"Click the play buttons to listen to the stimuli.", 1, WHITE)
        conditioning_prompting2 = SMALL_FONT.render(f"Move the slider on the right based on the stimuli's similarity.", 1, WHITE)
        conditioning_prompting3 = SMALL_FONT.render(f"Click next when complete. Try to use the full range of the scale.", 1, WHITE)
        self.window.blit(conditioning_prompting1, (EXPERIMENT_TEXT_X, EXPERIMENT_TEXT_Y1))
        self.window.blit(conditioning_prompting2, (EXPERIMENT_TEXT_X, EXPERIMENT_TEXT_Y2))
        self.window.blit(conditioning_prompting3, (EXPERIMENT_TEXT_X, EXPERIMENT_TEXT_Y3))

        # scale
        pygame.draw.rect(self.window, WHITE, (SCALE_X, SCALE_Y, SCALE_WIDTH, SCALE_HEIGHT))

        for i in range(SENTIMENT_OPTIONS):
            tab_center = self.height//2 - (i-SENTIMENT_OPTIONS//2)*SCALE_HEIGHT//(SENTIMENT_OPTIONS-1)

            tab_y = tab_center - TAB_HEIGHT//2
            text_y = tab_center - SMALL_FONT_SIZE//2

            pygame.draw.rect(self.window, WHITE, (TAB_X, tab_y, TAB_WIDTH, TAB_HEIGHT))

            scale_level = SMALL_FONT.render(f'{i+1}', 1, WHITE)
            self.window.blit(scale_level, (SCALE_NUMBER_X, text_y))

        pygame.draw.circle(self.window, WHITE,
                           (SCALE_CENTER, self.height//2 - (self.gameInfo.similarityScore-5)*SCALE_HEIGHT//(SENTIMENT_OPTIONS-1)),
                           SIMILARITY_INDICATOR_SIZE)

        scale_max = SMALL_FONT.render(f"most similar", 1, WHITE)
        self.window.blit(scale_max, (SCALE_LABEL_X, SCALE_LABEL_Y_1))

        scale_min = SMALL_FONT.render(f"least similar", 1, WHITE)
        self.window.blit(scale_min, (SCALE_LABEL_X, SCALE_LABEL_Y_2))

        counter = LARGE_FONT.render(f"{self.gameInfo.pair_number}", 1, WHITE)
        self.window.blit(counter, (20, 10))

    def draw_preference(self):
        self.window.fill(BLACK)

        if self.gameInfo.playing_A:
            button_A_file = 'pause.webp'
        else:
            button_A_file = 'play.webp'

        button_A_image = pygame.image.load(os.path.join('assets', button_A_file))
        button_A_image = pygame.transform.scale(button_A_image, (BUTTON_SIZE, BUTTON_SIZE))
        self.window.blit(button_A_image, (BUTTON_A2_X, BUTTON_A2_Y))

        stimuli_A_label = LARGE_FONT.render(f"Stimuli A", 1, WHITE)
        self.window.blit(stimuli_A_label, (BUTTON_A2_X + 10, BUTTON_A2_Y - 30))
        
        if self.gameInfo.playing_B:
            button_B_file = 'pause.webp'
        else:
            button_B_file = 'play.webp'

        button_B_image = pygame.image.load(os.path.join('assets', button_B_file))
        button_B_image = pygame.transform.scale(button_B_image, (BUTTON_SIZE, BUTTON_SIZE))
        self.window.blit(button_B_image, (BUTTON_B2_X, BUTTON_A2_Y))

        stimuli_B_label = LARGE_FONT.render(f"Stimuli B", 1, WHITE)
        self.window.blit(stimuli_B_label, (BUTTON_B2_X + 10, BUTTON_B2_Y - 30))

        if (self.gameInfo.listened and self.gameInfo.playing_original) or self.gameInfo.rated:
            pygame.draw.rect(self.window, WHITE, (NEXT_BOX2_X, NEXT_BOX2_Y, NEXT_WIDTH, NEXT_HEIGHT))
            pygame.draw.rect(self.window, BLACK, (NEXT_BOX2_X + 5, NEXT_BOX2_Y + 5, NEXT_WIDTH - 10, NEXT_HEIGHT - 10))
            next_text = LARGE_FONT.render(f"next", 1, WHITE)
            self.window.blit(next_text, (NEXT_TEXT2_X, NEXT_TEXT2_Y))

        conditioning_prompting1 = SMALL_FONT.render(f"Click the play buttons to listen to the stimuli.", 1, WHITE)
        conditioning_prompting2 = SMALL_FONT.render(f"Move the slider at the bottom based on preference.", 1, WHITE)
        conditioning_prompting3 = SMALL_FONT.render(f"Click next when complete. Try to use the full range of the scale.", 1, WHITE)
        self.window.blit(conditioning_prompting1, (EXPERIMENT_TEXT_X, EXPERIMENT_TEXT_Y1))
        self.window.blit(conditioning_prompting2, (EXPERIMENT_TEXT_X, EXPERIMENT_TEXT_Y2))
        self.window.blit(conditioning_prompting3, (EXPERIMENT_TEXT_X, EXPERIMENT_TEXT_Y3))

        # scale
        pygame.draw.rect(self.window, WHITE, (SCALE_X2, SCALE_Y2, SCALE_WIDTH2, SCALE_HEIGHT2))

        for i in range(SENTIMENT_OPTIONS):
            tab_center = self.width//2 - (i-SENTIMENT_OPTIONS//2)*SCALE_WIDTH2//(SENTIMENT_OPTIONS-1)

            tab_x2 = tab_center - TAB_HEIGHT//2
            text_x2 = tab_center - SMALL_FONT_SIZE//2

            pygame.draw.rect(self.window, WHITE, (tab_x2, TAB_Y2, TAB_HEIGHT, TAB_WIDTH))

            # negative numbers = prefer A
            scale_level = SMALL_FONT.render(f'{i-4}', 1, WHITE)
            self.window.blit(scale_level, (text_x2, SCALE_NUMBER_Y2))

        pygame.draw.circle(self.window, WHITE,
                           (self.width//2 - (self.gameInfo.similarityScore-5)*SCALE_WIDTH2//(SENTIMENT_OPTIONS-1), SCALE_CENTER2),
                           SIMILARITY_INDICATOR_SIZE)

        scale_max = SMALL_FONT.render(f"Prefer A", 1, WHITE)
        self.window.blit(scale_max, (SCALE_LABEL_X2_1, SCALE_LABEL_Y2))

        scale_min = SMALL_FONT.render(f"Prefer B", 1, WHITE)
        self.window.blit(scale_min, (SCALE_LABEL_X2_2, SCALE_LABEL_Y2))

        counter = LARGE_FONT.render(f"{self.gameInfo.pair_number}", 1, WHITE)
        self.window.blit(counter, (20, 10))

    def draw_simple_preference(self):
        self.window.fill(BLACK)

        if self.gameInfo.playing_C:
            button_A_file = 'pause.webp'
        else:
            button_A_file = 'play.webp'

        button_A_image = pygame.image.load(os.path.join('assets', button_A_file))
        button_A_image = pygame.transform.scale(button_A_image, (BUTTON_SIZE, BUTTON_SIZE))
        self.window.blit(button_A_image, (BUTTON_A_X, BUTTON_A_Y))

        if (self.gameInfo.listened and self.gameInfo.playing_original) or self.gameInfo.rated:
            pygame.draw.rect(self.window, WHITE, (NEXT_BOX_X, NEXT_BOX_Y, NEXT_WIDTH, NEXT_HEIGHT))
            pygame.draw.rect(self.window, BLACK, (NEXT_BOX_X + 5, NEXT_BOX_Y + 5, NEXT_WIDTH - 10, NEXT_HEIGHT - 10))
            next_text = LARGE_FONT.render(f"next", 1, WHITE)
            self.window.blit(next_text, (NEXT_TEXT_X, NEXT_TEXT_Y))

        counter = LARGE_FONT.render(f"{self.gameInfo.pair_number}", 1, WHITE)
        self.window.blit(counter, (20, 10))

        if self.gameInfo.playing_original:
            conditioning_prompting1 = SMALL_FONT.render(f"Throughout this experiment the original stimuli", 1, BLUE)
            conditioning_prompting2 = SMALL_FONT.render(f"will be played periodically to remind you of how it sounds.", 1, BLUE)
            self.window.blit(conditioning_prompting1, (EXPERIMENT_TEXT_X, EXPERIMENT_TEXT_Y1))
            self.window.blit(conditioning_prompting2, (EXPERIMENT_TEXT_X, EXPERIMENT_TEXT_Y2))
            return None
        
        if self.gameInfo.preference:
            keyword = "preference versus the original"
        else:
            keyword = "similarity to the original"
        conditioning_prompting1 = SMALL_FONT.render(f"Click the play buttons to listen to the stimuli.", 1, WHITE)
        conditioning_prompting2 = SMALL_FONT.render(f"Move the slider on the right based on {keyword}.", 1, WHITE)
        conditioning_prompting3 = SMALL_FONT.render(f"Click next when complete. Try to use the full range of the scale.", 1, WHITE)
        self.window.blit(conditioning_prompting1, (EXPERIMENT_TEXT_X, EXPERIMENT_TEXT_Y1))
        self.window.blit(conditioning_prompting2, (EXPERIMENT_TEXT_X, EXPERIMENT_TEXT_Y2))
        self.window.blit(conditioning_prompting3, (EXPERIMENT_TEXT_X, EXPERIMENT_TEXT_Y3))

        # scale
        pygame.draw.rect(self.window, WHITE, (SCALE_X, SCALE_Y, SCALE_WIDTH, SCALE_HEIGHT))

        for i in range(SENTIMENT_OPTIONS):
            tab_center = self.height//2 - (i-SENTIMENT_OPTIONS//2)*SCALE_HEIGHT//(SENTIMENT_OPTIONS-1)

            tab_y = tab_center - TAB_HEIGHT//2
            text_y = tab_center - SMALL_FONT_SIZE//2

            pygame.draw.rect(self.window, WHITE, (TAB_X, tab_y, TAB_WIDTH, TAB_HEIGHT))

            if self.gameInfo.preference:
                scale_level = SMALL_FONT.render(f'{i-4}', 1, WHITE)
            else:
                scale_level = SMALL_FONT.render(f'{i+1}', 1, WHITE)
            self.window.blit(scale_level, (SCALE_NUMBER_X, text_y))

        pygame.draw.circle(self.window, WHITE,
                           (SCALE_CENTER, self.height//2 - (self.gameInfo.similarityScore-5)*SCALE_HEIGHT//(SENTIMENT_OPTIONS-1)),
                           SIMILARITY_INDICATOR_SIZE)

        if self.gameInfo.preference:
            scale_max = SMALL_FONT.render(f"most preferred", 1, WHITE)
            scale_mid = SMALL_FONT.render(f"equal to orignial", 1, WHITE)
            scale_min = SMALL_FONT.render(f"least preferred", 1, WHITE)
        else:
            scale_max = SMALL_FONT.render(f"most similar", 1, WHITE)
            scale_mid = SMALL_FONT.render(f" ", 1, WHITE)
            scale_min = SMALL_FONT.render(f"least similar", 1, WHITE)

        self.window.blit(scale_max, (SCALE_LABEL_X, SCALE_LABEL_Y_1))
        self.window.blit(scale_mid, (SCALE_LABEL_X, (SCALE_LABEL_Y_2 + SCALE_LABEL_Y_1)//2))
        self.window.blit(scale_min, (SCALE_LABEL_X, SCALE_LABEL_Y_2))

    def draw_familiarity(self):
        self.window.fill(BLACK)

        if self.gameInfo.familiarity_started and not self.gameInfo.familiarity_completed:
            button_C_file = 'pause.webp'
        else:
            button_C_file = 'play.webp'

        button_C_image = pygame.image.load(os.path.join('assets', button_C_file))
        button_C_image = pygame.transform.scale(button_C_image, (BUTTON_SIZE, BUTTON_SIZE))
        self.window.blit(button_C_image, (BUTTON_C_X, BUTTON_C_Y))

        if self.gameInfo.preference:
            conditioning_prompting1 = SMALL_FONT.render(f"In this experiment, you will be rating relative preference", 1, WHITE)
            conditioning_prompting2 = SMALL_FONT.render(f"of variations on a song to the original song on a scale", 1, WHITE)
            conditioning_prompting3 = SMALL_FONT.render(f"of -4 to 4. First, listen to the original a few times to", 1, WHITE)
            conditioning_prompting4 = SMALL_FONT.render(f"become familiar with it. Click play to begin.", 1, WHITE)
        else:
            conditioning_prompting1 = SMALL_FONT.render(f"In this experiment, you will be rating the similarity", 1, WHITE)
            conditioning_prompting2 = SMALL_FONT.render(f"of variations on a song to the original song on a scale", 1, WHITE)
            conditioning_prompting3 = SMALL_FONT.render(f"of 1-9. First, listen to the original a few times to", 1, WHITE)
            conditioning_prompting4 = SMALL_FONT.render(f"become familiar with it. Click play to begin.", 1, WHITE)
        self.window.blit(conditioning_prompting1, (PROMPTING_X, PROMPTING_Y1))
        self.window.blit(conditioning_prompting2, (PROMPTING_X, PROMPTING_Y2))
        self.window.blit(conditioning_prompting3, (PROMPTING_X, PROMPTING_Y3))
        self.window.blit(conditioning_prompting4, (PROMPTING_X, PROMPTING_Y4))

        counter = LARGE_FONT.render(f"{self.gameInfo.familiarity_number}", 1, WHITE)
        self.window.blit(counter, (20, 10))

        if self.gameInfo.familiarity_completed:
            pygame.draw.rect(self.window, WHITE, (NEXT_BOX_X, NEXT_BOX_Y, NEXT_WIDTH, NEXT_HEIGHT))
            pygame.draw.rect(self.window, BLACK, (NEXT_BOX_X + 5, NEXT_BOX_Y + 5, NEXT_WIDTH - 10, NEXT_HEIGHT - 10))
            next_text = LARGE_FONT.render(f"next", 1, WHITE)
            self.window.blit(next_text, (NEXT_TEXT_X, NEXT_TEXT_Y))

    def draw_conditioning(self):
        self.window.fill(BLACK)

        if self.gameInfo.conditioning_started and not self.gameInfo.conditioning_completed:
            button_C_file = 'pause.webp'
        else:
            button_C_file = 'play.webp'

        button_C_image = pygame.image.load(os.path.join('assets', button_C_file))
        button_C_image = pygame.transform.scale(button_C_image, (BUTTON_SIZE, BUTTON_SIZE))
        self.window.blit(button_C_image, (BUTTON_C_X, BUTTON_C_Y))

        conditioning_prompting1 = SMALL_FONT.render(f"Now listen to a few of the songs you will be comparing", 1, WHITE)
        conditioning_prompting2 = SMALL_FONT.render(f"to the original so that you have a sense of the range", 1, WHITE)
        conditioning_prompting3 = SMALL_FONT.render(f"of songs you will be rating. Click play to begin.", 1, WHITE)
        self.window.blit(conditioning_prompting1, (PROMPTING_X, PROMPTING_Y1))
        self.window.blit(conditioning_prompting2, (PROMPTING_X, PROMPTING_Y2))
        self.window.blit(conditioning_prompting3, (PROMPTING_X, PROMPTING_Y3))

        counter = LARGE_FONT.render(f"{self.gameInfo.conditioning_number}", 1, WHITE)
        self.window.blit(counter, (20, 10))

        if self.gameInfo.conditioning_completed:
            pygame.draw.rect(self.window, WHITE, (NEXT_BOX_X, NEXT_BOX_Y, NEXT_WIDTH, NEXT_HEIGHT))
            pygame.draw.rect(self.window, BLACK, (NEXT_BOX_X + 5, NEXT_BOX_Y + 5, NEXT_WIDTH - 10, NEXT_HEIGHT - 10))
            next_text = LARGE_FONT.render(f"next", 1, WHITE)
            self.window.blit(next_text, (NEXT_TEXT_X, NEXT_TEXT_Y))

    def loop(self, mouse_pressed, mouse_pos):
        if mouse_pressed:
            self.gameInfo.similarityScore = max(min((self.height//2 - mouse_pos)*(SENTIMENT_OPTIONS-1)/SCALE_HEIGHT + 5, 9), 1)

        if not pygame.mixer.music.get_busy():
            self.gameInfo.playing_A = False
            self.gameInfo.playing_B = False

        if not self.gameInfo.familiarity_ended:
            if self.gameInfo.familiarity_started:
                self.start_familiarity()
            self.draw_familiarity()
        elif not self.gameInfo.conditioning_ended:
            if self.gameInfo.conditioning_started:
                self.start_conditioning()
            self.draw_conditioning()
        else:
            self.draw()

        return self.gameInfo
    
    def loop2(self, mouse_pressed, mouse_pos):
        if mouse_pressed:
            self.gameInfo.similarityScore = max(min((self.width//2 - mouse_pos)*(SENTIMENT_OPTIONS-1)/SCALE_WIDTH2 + 5, 9), 1)

        if not pygame.mixer.music.get_busy():
            self.gameInfo.playing_A = False
            self.gameInfo.playing_B = False

        if not self.gameInfo.familiarity_ended:
            if self.gameInfo.familiarity_started:
                self.start_familiarity()
            self.draw_familiarity()
        else:
            self.draw_preference()

        return self.gameInfo
    
    def loop3(self, mouse_pressed, mouse_pos):
        if mouse_pressed:
            self.gameInfo.similarityScore = max(min((self.height//2 - mouse_pos)*(SENTIMENT_OPTIONS-1)/SCALE_HEIGHT + 5, 9), 1)
            self.gameInfo.rated = True

        if not pygame.mixer.music.get_busy():
            if self.gameInfo.playing_C:
                self.gameInfo.listened = True

            self.gameInfo.playing_C = False

        self.draw_simple_preference()

        return self.gameInfo
    
    def next_pair_simple(self):
        pygame.mixer.music.stop()

        self.gameInfo.listened = False
        self.gameInfo.rated = False

        if self.gameInfo.playing_original:

            self.gameInfo.playing_original = False
            self.gameInfo.since_last_repeat = 0

        else:

            song_pair = self.gameInfo.simple_song_Order[self.gameInfo.pair_number]

            self.gameInfo.similarityArray[song_pair[0], song_pair[1]] = (self.gameInfo.similarityScore - 5)
            self.gameInfo.similarityArray[song_pair[1], song_pair[0]] = (self.gameInfo.similarityScore - 5)

            self.gameInfo.similarityScore = SENTIMENT_INITIAL
            self.gameInfo.pair_number += 1
            self.gameInfo.since_last_repeat += 1

        if self.gameInfo.since_last_repeat > 4:
            self.gameInfo.playing_original = True

        # check game end
        if self.gameInfo.pair_number >= len(self.gameInfo.simple_song_Order):
            self.gameInfo.testing_completed = True
    
    def next_pair(self):
        pygame.mixer.music.stop()

        song_pair = self.gameInfo.songOrder[self.gameInfo.pair_number]
        self.gameInfo.similarityArray[song_pair[0], song_pair[1]] = self.gameInfo.similarityScore
        self.gameInfo.similarityArray[song_pair[1], song_pair[0]] = self.gameInfo.similarityScore

        if self.gameInfo.preference:
            if song_pair[0] == 0:
                self.gameInfo.similarityArray[song_pair[0], song_pair[1]] = -(self.gameInfo.similarityScore - 5)
                self.gameInfo.similarityArray[song_pair[1], song_pair[0]] = -(self.gameInfo.similarityScore - 5)
            else:
                self.gameInfo.similarityArray[song_pair[0], song_pair[1]] = self.gameInfo.similarityScore - 5
                self.gameInfo.similarityArray[song_pair[1], song_pair[0]] = self.gameInfo.similarityScore - 5

        self.gameInfo.similarityScore = SENTIMENT_INITIAL
        self.gameInfo.pair_number += 1

        # check game end
        if self.gameInfo.pair_number >= len(self.gameInfo.songOrder):
            self.gameInfo.testing_completed = True

    def start_familiarity(self):
        self.gameInfo.familiarity_started = True

        if self.gameInfo.preference:
            familiarity_max = 2
        else:
            familiarity_max = 5

        if self.gameInfo.familiarity_number < familiarity_max and not pygame.mixer.music.get_busy():

            self.gameInfo.familiarity_number += 1

            pygame.mixer.music.load(self.gameInfo.stimuli[0])
            pygame.mixer.music.set_volume(0.7)
            pygame.mixer.music.play()
        
        elif self.gameInfo.familiarity_number >= familiarity_max and not pygame.mixer.music.get_busy():

            self.gameInfo.familiarity_completed = True

    def start_conditioning(self):
        self.gameInfo.conditioning_started = True

        if self.gameInfo.conditioning_number == 2 and not pygame.mixer.music.get_busy():

            pygame.mixer.music.load("stimuli/Bach_AI_Stimuli (super jazz).wav")
            pygame.mixer.music.set_volume(0.7)
            pygame.mixer.music.play()

            self.gameInfo.conditioning_number += 1

        elif self.gameInfo.conditioning_number < 5 and not pygame.mixer.music.get_busy():

            pygame.mixer.music.load(self.gameInfo.conditioning_order[self.gameInfo.conditioning_number])
            pygame.mixer.music.set_volume(0.7)
            pygame.mixer.music.play()

            self.gameInfo.conditioning_number += 1

        elif self.gameInfo.conditioning_number >= 5 and not pygame.mixer.music.get_busy():

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
        if self.gameInfo.playing_original:

            pygame.mixer.music.load(self.gameInfo.stimuli[self.gameInfo.simple_song_Order[0][0]])

        else:

            pygame.mixer.music.load(self.gameInfo.stimuli[self.gameInfo.simple_song_Order[self.gameInfo.pair_number][1]])

        pygame.mixer.music.set_volume(0.7)
        pygame.mixer.music.play()

        if self.gameInfo.playing_C:
            pygame.mixer.music.stop()

        self.gameInfo.playing_C = True