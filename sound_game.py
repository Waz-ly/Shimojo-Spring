import pygame
from GLOBAL import *
import numpy as np
import scipy.spatial
import librosa
import os

class Game:
    def __init__(self, window, width, height, points, labels):
        self.width = width
        self.height = height
        self.window = window

        self.labels = labels
        self.points = points
        self.delauny_triangles = scipy.spatial.Delaunay(self.points)

        self.selection_point = np.array([0.5, 0.5])
        self.bounding_triangle = self.get_bounding_triangle()

        self.playing = False
        self.channel = pygame.mixer.Channel(0)
        self.channel.set_volume(0.7)

        pygame.mixer.init()

    def draw(self):
        self.window.fill(BLACK)

        pygame.draw.rect(
            self.window,
            WHITE,
            (
                10,
                10,
                HEIGHT - 20,
                HEIGHT - 20
            ),
            3
        )

        for index, point in enumerate(self.points):
            if not self.bounding_triangle is None and point in self.bounding_triangle:
                color = BLUE
                label = self.labels[index]
                coords = 15 + (HEIGHT - 30) * point
                coords[0] += 5

                SMALL_FONT.render_to(self.window, coords, label, BLUE)
            else:
                color = WHITE

            pygame.draw.circle(
                self.window,
                color,
                15 + (HEIGHT - 30) * point,
                radius=3
            )

        if not self.bounding_triangle is None:
            pygame.draw.line(self.window, BLUE, 15 + (HEIGHT - 30) * self.bounding_triangle[0], 15 + (HEIGHT - 30) * self.bounding_triangle[1])
            pygame.draw.line(self.window, BLUE, 15 + (HEIGHT - 30) * self.bounding_triangle[1], 15 + (HEIGHT - 30) * self.bounding_triangle[2])
            pygame.draw.line(self.window, BLUE, 15 + (HEIGHT - 30) * self.bounding_triangle[2], 15 + (HEIGHT - 30) * self.bounding_triangle[0])

        pygame.draw.circle(
            self.window,
            RED,
            15 + (HEIGHT - 30) * self.selection_point,
            radius=3
        )

        if self.playing:
            button = pygame.image.load("assets/pause.webp")
        else:
            button = pygame.image.load("assets/play.webp")

        button = pygame.transform.scale(button, (BUTTON_SIZE, BUTTON_SIZE))
        self.window.blit(button, (HEIGHT, 10))

    def point_in_triangle(self, p, a, b, c):
        
        d1, d2, d3 = np.cross(a - p, b - p), np.cross(b - p, c - p), np.cross(c - p, a - p)

        return (d1 < 0) == (d2 < 0) == (d3 < 0)
    
    def triangle_signed_area(self, a, b, c):
        return -0.5*np.cross(b - a, c - a)
    
    def distance(self, a, b):
        return np.sqrt(np.square(a[0] - b[0]) + np.square(a[1] - b[1]))
    
    def get_weights(self, p, a, b, c):
        weight_a = 2 * self.triangle_signed_area(p, b, c) / self.distance(b, c)
        weight_b = 2 * self.triangle_signed_area(a, p, c) / self.distance(c, a)
        weight_c = 2 * self.triangle_signed_area(a, b, p) / self.distance(a, b)
        total_weight = weight_a + weight_b + weight_c

        return weight_a / total_weight, weight_b / total_weight, weight_c / total_weight
    
    def get_bounding_triangle(self):
        for triangle in self.points[self.delauny_triangles.simplices]:

            if self.point_in_triangle(self.selection_point, triangle[0], triangle[1], triangle[2]):
                return triangle
            
        return None

    def new_selection_point(self, mouse_pos):
        self.selection_point = (np.array(mouse_pos) - 15) / (HEIGHT - 30)
        self.bounding_triangle = self.get_bounding_triangle()

    def toggle_play(self):
        if self.playing:
            self.channel.stop()
        else:

            if self.bounding_triangle is None:
                return None
            
            audio = np.zeros(SAMPLE_RATE*20)
            for index, point in enumerate(self.points):
                if point in self.bounding_triangle:
                    bounding_index = 0 if np.array_equal(self.bounding_triangle[0], point) else (1 if np.array_equal(self.bounding_triangle[1], point) else 2)
                    weights = self.get_weights(self.selection_point, self.bounding_triangle[0], self.bounding_triangle[1], self.bounding_triangle[2])
                    bounding_weight = weights[bounding_index]

                    if os.path.exists("stimuli/" + self.labels[index] + ".wav"):
                        file = "stimuli/" + self.labels[index] + ".wav"
                    elif os.path.exists("stimuli/" + self.labels[index] + ".mp3"):
                        file = "stimuli/" + self.labels[index] + ".mp3"
                    elif os.path.exists("stimuli_additional1/" + self.labels[index] + ".wav"):
                        file = "stimuli_additional1/" + self.labels[index] + ".wav"
                    elif os.path.exists("stimuli_additional1/" + self.labels[index] + ".mp3"):
                        file = "stimuli_additional1/" + self.labels[index] + ".mp3"

                    audio_chunk, _ = librosa.load(file, sr=SAMPLE_RATE)
                    audio_chunk /= np.max(np.abs(audio_chunk))
                    audio[:len(audio_chunk)] += bounding_weight * audio_chunk

            sound = pygame.sndarray.make_sound(np.ascontiguousarray((audio * 32767).astype(np.int16)))
            self.channel.play(sound)

    def loop(self):
        if self.channel.get_busy():
            self.playing = True
        else:
            self.playing = False

        self.draw()