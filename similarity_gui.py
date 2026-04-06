import pygame
from similarity_game import Game
import numpy as np
from GLOBAL import *
import os
import sklearn
import sklearn.metrics

class SimilarityTest:
    def __init__(self, window, width, height):
        self.game = Game(window, width, height)
        self.lastMoves = []
        self.lastLastMoves = []

    def furthest_point_anchors(self, embedding, n_anchors):
        chosen = [0]
        for _ in range(n_anchors - 1):
            dists = np.min(
                sklearn.metrics.pairwise_distances(embedding, embedding[chosen]), axis=1
            )
            chosen.append(np.argmax(dists))
        return np.array(chosen)

    def additional_mode(self):
        result = np.loadtxt('result.csv', delimiter=',', dtype=str)

        labels = result[1:,0]
        data = np.array(result[1:,1:], dtype=float)

        data = np.where(data>0.5, 1/data, np.zeros_like(data))

        mds = sklearn.manifold.MDS(
            n_components=2,
            max_iter=3000,
            eps=1e-9,
            n_init=1,
            random_state=1,
            metric="precomputed",
            n_jobs=1,
            init="classical_mds",
        )
        X_mds = mds.fit(data).embedding_

        X_mds[:, 0] -= np.min(X_mds[:, 0])
        X_mds[:, 1] -= np.min(X_mds[:, 1])
        X_mds /= np.maximum(np.max(X_mds[:, 0]), np.max(X_mds[:, 1]))

        chosen = labels[self.furthest_point_anchors(X_mds, 10)]
        chosen_files = []

        for label in chosen:
            if os.path.exists("stimuli/" + label + ".wav"):
                chosen_files.append("stimuli/" + label + ".wav")
            else:
                chosen_files.append("stimuli/" + label + ".mp3")

        self.game.additional_mode(chosen_files)

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

    def save(self):
        stimuli_modification = []
        stimuli_files = self.game.gameInfo.stimuli
        for file in stimuli_files:
            file_name = os.path.basename(file)
            file_name = os.path.splitext(file_name)[0]

            stimuli_modification.append(file_name)
        
        similarity_array_size = self.game.gameInfo.similarityArray.shape[0]

        output = np.empty((similarity_array_size + 1, similarity_array_size + 1), dtype=object)
        output[0, 0] = ""
        output[0, 1:] = stimuli_modification
        output[1:, 0] = stimuli_modification
        output[1:, 1:] = np.round(self.game.gameInfo.similarityArray, 2)

        np.savetxt('test.csv', output, fmt="%s", delimiter=',')

        pygame.quit()