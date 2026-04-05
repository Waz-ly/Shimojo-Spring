import pygame
from GLOBAL import *
import numpy as np
import scipy.spatial

class Game:
    def __init__(self, window, width, height, points):
        self.width = width
        self.height = height
        self.window = window

        self.points = points
        self.delauny_triangles = scipy.spatial.Delaunay(self.points)

        self.selection_point = np.array([0.5, 0.5])
        self.bounding_triangle = self.get_bounding_triangle()

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

        for point in self.points:
            pygame.draw.circle(
                self.window,
                WHITE,
                15 + (HEIGHT - 30) * point,
                radius=3
            )

        pygame.draw.circle(
            self.window,
            RED,
            15 + (HEIGHT - 30) * self.selection_point,
            radius=3
        )

        if not self.bounding_triangle is None:
            pygame.draw.line(self.window, RED, 15 + (HEIGHT - 30) * self.bounding_triangle[0], 15 + (HEIGHT - 30) * self.bounding_triangle[1])
            pygame.draw.line(self.window, RED, 15 + (HEIGHT - 30) * self.bounding_triangle[1], 15 + (HEIGHT - 30) * self.bounding_triangle[2])
            pygame.draw.line(self.window, RED, 15 + (HEIGHT - 30) * self.bounding_triangle[2], 15 + (HEIGHT - 30) * self.bounding_triangle[0])

    def point_in_triangle(self, p, a, b, c):
        
        d1, d2, d3 = np.cross(a - p, b - p), np.cross(b - p, c - p), np.cross(c - p, a - p)

        return (d1 < 0) == (d2 < 0) == (d3 < 0)
    
    def get_bounding_triangle(self):
        for triangle in self.points[self.delauny_triangles.simplices]:

            if self.point_in_triangle(self.selection_point, triangle[0], triangle[1], triangle[2]):
                return triangle
            
        return None

    def new_selection_point(self, mouse_pos):
        self.selection_point = (np.array(mouse_pos) - 15) / (HEIGHT - 30)
        self.bounding_triangle = self.get_bounding_triangle()

    def loop(self):

        self.draw()